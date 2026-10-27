"""Parser de los .puml del repo a estructuras por diagrama.

Cubre el subconjunto de PlantUML que usan los diagramas (ver
docs/uml-subset.md). Cada elemento conserva archivo y línea de origen
(`src` = "archivo:línea"). Una línea que no se reconoce queda como
problema "P1 construcción no traducible": la conversión a XMI no la puede
representar y el CI falla.
"""
import re
from pathlib import Path

# ---------------------------------------------------------------- utilidades

# Directivas de presentación: no crean elementos del modelo.
PRESENTACION = re.compile(
    r'^(?:!theme\b|!pragma\b|skinparam\b|hide\b|show\b|remove\b|title\b|'
    r'left to right direction|top to bottom direction|scale\b|caption\b|'
    r'header\b|footer\b|autoactivate\b|@startuml|@enduml)'
)
SKIN_BLOCK = re.compile(r'^skinparam\s+[\w.]+\s*\{\s*$')
INCLUDE = re.compile(r'^!include\s+(\S+)')


class Linea:
    __slots__ = ('n', 'texto', 'archivo')

    def __init__(self, n, texto, archivo):
        self.n, self.texto, self.archivo = n, texto, archivo

    @property
    def src(self):
        return f'{self.archivo}:{self.n}'


def leer(path, raiz, vistos=None):
    """Devuelve las líneas útiles (sin comentarios ni skinparam en bloque),
    con los !include resueltos. Cada línea guarda su archivo de origen."""
    vistos = vistos or set()
    path = Path(path)
    if path.resolve() in vistos:
        return []
    vistos.add(path.resolve())
    rel = _rel(path, raiz)
    texto = path.read_text(encoding='utf-8')
    # comentarios de bloque /' ... '/ conservando los saltos de línea
    texto = re.sub(r"/'.*?'/", lambda m: '\n' * m.group(0).count('\n'), texto, flags=re.S)
    out, en_skin = [], 0
    for n, cruda in enumerate(texto.splitlines(), 1):
        t = cruda.strip()
        if en_skin:
            en_skin += t.count('{') - t.count('}')
            continue
        if not t or t.startswith("'"):
            continue
        if SKIN_BLOCK.match(t):
            en_skin = 1
            continue
        m = INCLUDE.match(t)
        if m:
            destino = (path.parent / m.group(1)).resolve()
            out += [l for l in leer(destino, raiz, vistos)
                    if l.texto not in ('@startuml', '@enduml')]
            continue
        out.append(Linea(n, t, rel))
    return out


def _rel(path, raiz):
    try:
        return str(Path(path).resolve().relative_to(Path(raiz).resolve()))
    except ValueError:
        return str(path)


def titulo(lineas):
    for l in lineas:
        m = re.match(r'^title\s+(.*)$', l.texto)
        if m:
            return m.group(1).strip()
    return None


def sin_comillas(s):
    s = s.strip()
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] == '"' else s


def etiqueta_limpia(s):
    return re.sub(r'\s+', ' ', sin_comillas(s).replace('\\n', ' ')).strip()


class Problemas:
    def __init__(self):
        self.lista = []

    def agregar(self, codigo, src, msg, nivel='error'):
        self.lista.append({'codigo': codigo, 'src': src, 'msg': msg, 'nivel': nivel})


def leer_bloque(lineas, i, fin):
    """Junta las líneas desde i+1 hasta la que cumple fin(texto). Devuelve (texto, j)."""
    partes, j = [], i + 1
    while j < len(lineas) and not fin(lineas[j].texto):
        partes.append(lineas[j].texto)
        j += 1
    return '\n'.join(partes), j


NOTA_INICIO = re.compile(
    r'^(?:r|h)?note\s+(?:(left|right|top|bottom|over)(?:\s+of)?(?:\s+([^:]+?))?|"([^"]*)"\s+as\s+(\w+)|as\s+(\w+))\s*(?::\s*(.*))?$')


def nota(lineas, i, problemas):
    """Lee una nota de una o varias líneas. Devuelve (dict, siguiente índice)."""
    l = lineas[i]
    m = NOTA_INICIO.match(l.texto)
    if not m:
        problemas.agregar('P1', l.src, f'nota no reconocida: {l.texto}')
        return None, i + 1
    _, objetivos, texto_n, alias_n, alias2 = m.groups()[:5]
    en_linea = m.group(6)
    objetivos = [o.strip() for o in objetivos.split(',')] if objetivos else []
    if texto_n is not None:
        return {'texto': texto_n.replace('\\n', '\n'), 'anota': [], 'alias': alias_n,
                'src': l.src}, i + 1
    if en_linea is not None:
        return {'texto': en_linea, 'anota': objetivos, 'alias': alias2, 'src': l.src}, i + 1
    cuerpo, j = leer_bloque(lineas, i, lambda t: t in ('end note', 'endnote', 'end rnote', 'end hnote'))
    return {'texto': cuerpo, 'anota': objetivos, 'alias': alias2, 'src': l.src}, j + 1


def saltar_legend(lineas, i):
    _, j = leer_bloque(lineas, i, lambda t: t in ('endlegend', 'end legend'))
    return j + 1


# ------------------------------------------------------------------- clases

CLASE = re.compile(
    r'^(abstract\s+class|abstract|class|interface|enum|entity|struct|protocol|annotation|'
    r'metaclass|circle|exception|dataclass|record|stereotype|object|map|json)\s+'
    r'(?:"(?P<label>[^"]+)"\s+as\s+(?P<alias>[\w]+)|(?P<name>[\w]+)(?:\s+as\s+"?(?P<label2>[^"{<]+?)"?)?)'
    r'\s*(?P<stereo><<[^>]+>>)?\s*(?:extends\s+(?P<ext>[\w, ]+?))?\s*(?:implements\s+(?P<impl>[\w, ]+?))?'
    r'\s*(?P<open>\{)?\s*(?P<cierre>\})?\s*$'
)
PERMITIDAS = {'class', 'abstract class', 'abstract', 'interface', 'enum'}
PAQUETE = re.compile(r'^(package|namespace|folder|frame|rectangle|node|cloud|database)\s+'
                     r'(?:"([^"]+)"|([\w.]+))(?:\s+as\s+(\w+))?\s*(<<[^>]+>>)?\s*\{\s*$')
MULT = r'"[^"]*"'
FLECHA = (r'(?P<arrow>(?:<\||<|\*|o|\+|#|x|\})?[-.]+(?:\[[^\]]*\])?'
          r'(?:(?:up|down|left|right|u|d|l|r)[-.]+)?(?:\|>|>|\*|o|\+|#|x|\{)?)')
RELACION = re.compile(
    rf'^(?P<a>"[^"]+"|[\w.]+)\s*(?P<ma>{MULT})?\s*{FLECHA}\s*(?P<mb>{MULT})?\s*'
    r'(?P<b>"[^"]+"|[\w.]+)\s*(?::\s*(?P<label>.*))?$'
)
ATRIBUTO = re.compile(
    r'^(?P<vis>[-+#~])?\s*(?P<static>\{static\}\s*)?(?P<derivado>/)?(?P<name>[^\s:(){}]+)\s*'
    r'(?::\s*(?P<tipo>.*?))?\s*$'
)
OPERACION = re.compile(
    r'^(?P<vis>[-+#~])?\s*(?P<mods>(?:\{(?:static|abstract)\}\s*)*)(?P<name>[^\s(]+)\s*'
    r'\((?P<params>[^)]*)\)\s*(?::\s*(?P<ret>.*?))?\s*$'
)
MULT_SUFIJO = re.compile(r'\s*\[(\d+|\*)(?:\.\.(\d+|\*))?\]\s*$')
MODIFICADORES = re.compile(r'\s*\{([^}]*)\}\s*$')
DEFAULT = re.compile(r'^(.*?)\s*=\s*(.+)$')


def mult(texto):
    """'0..*' -> {'lower': 0, 'upper': '*'}; '1' -> 1..1; '*' -> 0..*."""
    if texto is None:
        return None
    t = sin_comillas(texto).strip()
    m = re.fullmatch(r'(\d+|\*|n)(?:\s*\.\.\s*(\d+|\*|n))?', t)
    if not m:
        return {'texto': t, 'invalida': True}
    lo, up = m.group(1), m.group(2)
    if up is None:
        if lo in ('*', 'n'):
            return {'lower': 0, 'upper': '*'}
        return {'lower': int(lo), 'upper': int(lo)}
    return {'lower': 0 if lo in ('*', 'n') else int(lo),
            'upper': '*' if up in ('*', 'n') else int(up)}


def separar_tipo(tipo):
    """'decimal [0..1] {readOnly}' -> ('decimal', mult, ['readOnly'], default)."""
    if tipo is None:
        return None, None, [], None
    mods = []
    while True:
        m = MODIFICADORES.search(tipo)
        if not m:
            break
        mods = [x.strip() for x in m.group(1).split(',')] + mods
        tipo = tipo[:m.start()]
    default = None
    d = DEFAULT.match(tipo)
    if d:
        tipo, default = d.group(1), d.group(2).strip()
    mu = None
    m = MULT_SUFIJO.search(tipo)
    if m:
        mu = mult(m.group(1) + (f'..{m.group(2)}' if m.group(2) else ''))
        tipo = tipo[:m.start()]
    return tipo.strip() or None, mu, mods, default


def parse_params(texto):
    params = []
    for p in [x.strip() for x in texto.split(',') if x.strip()]:
        if ':' in p:
            n, t = p.split(':', 1)
            t, mu, _, default = separar_tipo(t)
            params.append({'name': n.strip(), 'type': t, 'mult': mu, 'default': default})
        else:
            params.append({'name': p, 'type': None, 'mult': None, 'default': None})
    return params


def flecha_a_relacion(arrow):
    """Normaliza la flecha a (tipo, invertida). Tipo en: generalization,
    realization, composition, aggregation, association, dependency, link."""
    a = re.sub(r'\[[^\]]*\]', '', arrow)
    a = re.sub(r'(?<=[-.])(up|down|left|right|u|d|l|r)(?=[-.])', '', a)
    punteada = '.' in a
    izq, der = re.match(r'^([^-.]*)[-.]+([^-.]*)$', a).groups()
    if '<|' in izq or '|>' in der:
        tipo = 'realization' if punteada else 'generalization'
        return tipo, '|>' in der  # invertida: el padre está a la derecha
    if '*' in (izq + der):
        return 'composition', der == '*'
    if 'o' in (izq + der):
        return 'aggregation', der == 'o'
    if izq in ('+', '#', 'x', '}') or der in ('+', '#', 'x', '{'):
        return 'prohibida', False
    if punteada:
        if '>' in der or '<' in izq:
            return 'dependency', izq == '<'
        return 'link', False
    if '>' in der and '<' in izq:
        return 'association-bi', False
    if '>' in der:
        return 'association', False
    if '<' in izq:
        return 'association', True
    return 'association-nd', False


def parse_clases(lineas, problemas):
    d = {'clasificadores': [], 'relaciones': [], 'paquetes': [], 'notas': []}
    pila, actual, alias_nota = [], None, {}
    i = 0
    while i < len(lineas):
        l = lineas[i]
        t = l.texto
        if PRESENTACION.match(t) or t == 'together {':
            if t == 'together {':
                pila.append(None)
            i += 1
            continue
        if actual is not None:
            if t == '}':
                actual = None
            elif re.fullmatch(r'(--|==|\.\.|__)(.*(--|==|\.\.|__))?', t):
                pass
            elif actual['kind'] == 'enum':
                for lit in [x.strip() for x in t.split(',') if x.strip()]:
                    actual['literales'].append({'name': lit, 'src': l.src})
            else:
                miembro(actual, l, problemas)
            i += 1
            continue
        if t.startswith(('note ', 'rnote ', 'hnote ')):
            n, i = nota(lineas, i, problemas)
            if n:
                d['notas'].append(n)
                if n['alias']:
                    alias_nota[n['alias']] = n
            continue
        if t.startswith('legend'):
            i = saltar_legend(lineas, i)
            continue
        m = PAQUETE.match(t)
        if m:
            kind = m.group(1)
            if kind not in ('package', 'namespace'):
                problemas.agregar('P1', l.src, f'"{kind}" no tiene metaclase UML: usar package')
            nombre = m.group(2) or m.group(3)
            pila.append(nombre)
            d['paquetes'].append({'name': nombre, 'padre': _paquete(pila[:-1]), 'src': l.src})
            i += 1
            continue
        if t == '}':
            if pila:
                pila.pop()
            i += 1
            continue
        m = CLASE.match(t)
        if m:
            kind = re.sub(r'\s+', ' ', m.group(1))
            if kind not in PERMITIDAS:
                problemas.agregar('P1', l.src, f'"{kind}" no tiene metaclase UML 2.5.1')
            nombre = m.group('alias') or m.group('name')
            etiqueta = m.group('label') or (m.group('label2') or '').strip() or None
            c = {'name': nombre, 'label': etiqueta,
                 'kind': {'abstract class': 'class', 'abstract': 'class'}.get(kind, kind),
                 'abstract': kind.startswith('abstract'), 'stereotype': m.group('stereo'),
                 'package': _paquete(pila), 'atributos': [], 'operaciones': [],
                 'literales': [], 'src': l.src}
            d['clasificadores'].append(c)
            for grupo, rel in (('ext', 'generalization'), ('impl', 'realization')):
                for padre in (m.group(grupo) or '').split(','):
                    if padre.strip():
                        d['relaciones'].append({'kind': rel, 'a': nombre, 'b': padre.strip(),
                                                'src': l.src})
            if m.group('open') and not m.group('cierre'):
                actual = c
            i += 1
            continue
        m = RELACION.match(t)
        if m:
            tipo, invertida = flecha_a_relacion(m.group('arrow'))
            a, b = sin_comillas(m.group('a')), sin_comillas(m.group('b'))
            ma, mb = m.group('ma'), m.group('mb')
            if a in alias_nota or b in alias_nota:
                n = alias_nota.get(a) or alias_nota.get(b)
                n['anota'].append(b if a in alias_nota else a)
                i += 1
                continue
            if tipo == 'prohibida':
                problemas.agregar('P1', l.src, f'flecha "{m.group("arrow")}" sin metaclase UML')
                i += 1
                continue
            if invertida:
                a, b, ma, mb = b, a, mb, ma
            # Convención: en generalización/realización 'a' es el hijo y 'b' el padre;
            # en composición/agregación 'a' es el todo; en el resto 'a' es el origen.
            if tipo in ('generalization', 'realization'):
                a, b, ma, mb = b, a, mb, ma
            d['relaciones'].append({
                'kind': tipo, 'a': a, 'b': b, 'mult_a': mult(ma), 'mult_b': mult(mb),
                'label': (m.group('label') or '').strip() or None, 'src': l.src})
            i += 1
            continue
        problemas.agregar('P1', l.src, f'construcción no traducible: {t}')
        i += 1
    return d


def _paquete(pila):
    nombres = [p for p in pila if p]
    return '::'.join(nombres) if nombres else None


def miembro(clase, l, problemas):
    t = l.texto
    if '(' in t and ')' in t and not re.match(r'^[-+#~]?\s*[^\s(:]+\s*:', t):
        m = OPERACION.match(t)
        if m:
            ret, mu, _, _ = separar_tipo(m.group('ret'))
            clase['operaciones'].append({
                'name': m.group('name'), 'visibility': m.group('vis'),
                'params': parse_params(m.group('params')), 'return': ret, 'return_mult': mu,
                'static': '{static}' in m.group('mods'),
                'abstract': '{abstract}' in m.group('mods'), 'src': l.src})
            return
    m = ATRIBUTO.match(t)
    if m:
        tipo, mu, mods, default = separar_tipo(m.group('tipo'))
        clase['atributos'].append({
            'name': m.group('name'), 'visibility': m.group('vis'), 'type': tipo,
            'mult': mu, 'modificadores': mods, 'default': default,
            'static': bool(m.group('static')), 'derivado': bool(m.group('derivado')),
            'src': l.src})
        return
    problemas.agregar('P1', l.src, f'miembro no reconocido en {clase["name"]}: {t}')


# ---------------------------------------------------------------- secuencia

PARTICIPANTE = re.compile(
    r'^(participant|actor|boundary|control|entity|database|collections|queue)\s+'
    r'(?:"(?P<label>[^"]+)"|(?P<name>[\w.]+))(?:\s+as\s+(?P<alias>[\w.]+))?'
    r'\s*(?P<stereo><<[^>]+>>)?\s*(?:#\w+)?\s*$'
)
MENSAJE = re.compile(
    r'^(?P<a>[\w.]+|\[|\]|"[^"]+")\s*(?P<arrow>(?:<<?|/|\\\\|x|o)?-{1,2}(?:\[[^\]]*\])?(?:>>?|\\\\|/|x|o)?)\s*'
    r'(?P<b>[\w.]+|\[|\]|"[^"]+")\s*(?P<act>\+\+|--|\*\*|!!)?\s*(?::\s*(?P<texto>.*))?$'
)
FRAGMENTO = re.compile(r'^(alt|opt|loop|par|break|critical|group|neg|strict|seq|ignore|consider|assert)\b\s*(.*)$')
OPERADORES_UML = {'alt', 'opt', 'loop', 'par', 'break', 'critical', 'neg', 'strict', 'seq',
                  'ignore', 'consider', 'assert'}
REF = re.compile(r'^ref\s+over\s+([^:]+?)\s*(?::\s*(.*))?$')
LLAMADA = re.compile(r'^\s*(?:(?P<asig>[\w.]+)\s*[:=]\s*)?(?P<op>[^\s(«»<>]+)\s*\((?P<args>.*)\)\s*(?P<resto>.*)$')
CREATE_MSG = re.compile(r'^\s*(?:«create»|<<create>>|create)\s*(?P<clase>[\w]+)?\s*(?:\((?P<args>.*)\))?\s*$')


def tipo_lifeline(label, name):
    """'obra:\\nObra' -> ('obra', 'Obra'); ':Obra' -> ('', 'Obra'); 'Obra' -> ('Obra', None)."""
    texto = (label if label is not None else name).replace('\\n', '')
    if ':' in texto:
        rol, tipo = texto.split(':', 1)
        return rol.strip(), re.sub(r'\s+', '', tipo.strip()) or None
    return texto.strip(), None


def parse_secuencia(lineas, problemas):
    d = {'lifelines': [], 'items': [], 'notas': []}
    por_alias = {}
    pila = [d['items']]
    crear = set()

    def lifeline(alias, src, implicita=False):
        if alias not in por_alias:
            ll = {'alias': alias, 'rol': alias, 'type': None, 'kind': 'participant',
                  'label': alias, 'src': src, 'implicita': implicita}
            por_alias[alias] = ll
            d['lifelines'].append(ll)
        return por_alias[alias]

    i = 0
    while i < len(lineas):
        l = lineas[i]
        t = l.texto
        if PRESENTACION.match(t):
            i += 1
            continue
        if t.startswith(('note ', 'rnote ', 'hnote ')):
            n, i = nota(lineas, i, problemas)
            if n:
                pila[-1].append({'tipo': 'comment', **n})
            continue
        if t.startswith('legend'):
            i = saltar_legend(lineas, i)
            continue
        if re.match(r'^box\b', t) or t == 'end box':
            i += 1
            continue
        m = PARTICIPANTE.match(t)
        if m:
            kind = m.group(1)
            if kind not in ('participant', 'actor'):
                problemas.agregar('P1', l.src, f'"{kind}" es un ícono de PlantUML sin metaclase: usar participant')
            alias = m.group('alias') or m.group('name') or m.group('label')
            rol, tipo = tipo_lifeline(m.group('label'), m.group('name'))
            ll = lifeline(alias, l.src)
            ll.update({'rol': rol, 'type': tipo, 'kind': kind,
                       'label': etiqueta_limpia(m.group('label') or m.group('name'))})
            i += 1
            continue
        m = re.match(r'^create\s+(?:(participant|actor)\s+)?(?:"[^"]+"\s+as\s+)?([\w.]+)\s*$', t)
        if m:
            lifeline(m.group(2), l.src)
            crear.add(m.group(2))
            i += 1
            continue
        m = re.match(r'^==\s*(.*?)\s*==$', t)
        if m:
            pila[-1].append({'tipo': 'comment', 'texto': m.group(1), 'anota': [], 'src': l.src,
                             'divisor': True})
            i += 1
            continue
        m = re.match(r'^ref\s+over\b', t)
        if m:
            r = REF.match(t)
            participantes = [x.strip() for x in r.group(1).split(',')]
            if r.group(2) is not None:
                texto, j = r.group(2), i + 1
            else:
                texto, j = leer_bloque(lineas, i, lambda x: x in ('end ref', 'endref'))
                j += 1
            pila[-1].append({'tipo': 'ref', 'lifelines': participantes,
                             'texto': texto.strip(), 'src': l.src})
            i = j
            continue
        m = FRAGMENTO.match(t)
        if m:
            op = m.group(1)
            if op not in OPERADORES_UML:
                problemas.agregar('P1', l.src, f'"{op}" no es un operador de fragmento UML')
            frag = {'tipo': 'fragment', 'operador': op,
                    'operandos': [{'guarda': m.group(2).strip() or None, 'items': [], 'src': l.src}],
                    'src': l.src}
            pila[-1].append(frag)
            pila.append(frag['operandos'][0]['items'])
            pila_frag.append(frag)
            i += 1
            continue
        m = re.match(r'^else\b\s*(.*)$', t)
        if m and pila_frag:
            frag = pila_frag[-1]
            op = {'guarda': m.group(1).strip() or None, 'items': [], 'src': l.src}
            frag['operandos'].append(op)
            pila[-1] = op['items']
            i += 1
            continue
        if t == 'end' and pila_frag:
            pila_frag.pop()
            pila.pop()
            i += 1
            continue
        if re.match(r'^(activate|deactivate|destroy)\s+([\w.]+)', t):
            accion, quien = re.match(r'^(activate|deactivate|destroy)\s+([\w.]+)', t).groups()
            pila[-1].append({'tipo': accion, 'lifeline': quien, 'src': l.src})
            i += 1
            continue
        if re.match(r'^(autonumber|newpage|\.\.\.|\|\|\||return\b)', t):
            problemas.agregar('P1', l.src, f'construcción de PlantUML sin metaclase UML: {t}')
            i += 1
            continue
        m = MENSAJE.match(t)
        if m and '-' in m.group('arrow'):
            arrow = m.group('arrow')
            a, b = sin_comillas(m.group('a')), sin_comillas(m.group('b'))
            if a in '[]' or b in '[]':
                problemas.agregar('P1', l.src, 'mensaje encontrado/perdido ([ o ]) no soportado')
                i += 1
                continue
            if arrow.startswith('<') and arrow.endswith('>'):
                problemas.agregar('P1', l.src, 'mensaje bidireccional: no existe en UML')
                i += 1
                continue
            if arrow.startswith('<'):
                a, b = b, a
                arrow = arrow[1:] + '>'
            for x in (a, b):
                lifeline(x, l.src, implicita=True)
            texto = (m.group('texto') or '').strip()
            if 'x' in arrow.replace('xx', ''):
                problemas.agregar('P1', l.src, 'mensaje perdido (->x) no soportado')
            if arrow.startswith('--') or arrow.startswith('-[') and '--' in arrow:
                sort = 'reply'
            elif '>>' in arrow:
                sort = 'asynchCall'
            else:
                sort = 'synchCall'
            msg = {'tipo': 'message', 'from': a, 'to': b, 'sort': sort, 'texto': texto,
                   'operacion': None, 'args': None, 'src': l.src}
            c = CREATE_MSG.match(texto)
            if b in crear and sort != 'reply':
                msg['sort'] = 'createMessage'
                crear.discard(b)
                if c:
                    msg['args'] = c.group('args')
            elif c:
                msg['sort'] = 'createMessage'
                msg['args'] = c.group('args')
            elif sort != 'reply':
                ll = LLAMADA.match(texto)
                if ll:
                    msg['operacion'] = ll.group('op')
                    msg['args'] = ll.group('args')
            if m.group('act') == '!!':
                msg['destruye'] = True
            pila[-1].append(msg)
            i += 1
            continue
        problemas.agregar('P1', l.src, f'construcción no traducible: {t}')
        i += 1
    return d


pila_frag = []  # se reinicia en parse_diagrama


# ------------------------------------------------------------------ estados

ESTADO = re.compile(
    r'^state\s+(?:"(?P<label>[^"]+)"\s+as\s+(?P<alias>[\w]+)|(?P<name>[\w]+)(?:\s+as\s+"(?P<label2>[^"]+)")?)'
    r'\s*(?P<stereo><<\w+>>)?\s*(?:#\w+)?\s*(?P<open>\{)?\s*(?::\s*(?P<desc>.*))?$'
)
TRANSICION = re.compile(
    r'^(?P<a>\[\*\]|\[H\*?\]|[\w.]+)\s*(?P<arrow>-+(?:\[[^\]]*\])?(?:(?:up|down|left|right|u|d|l|r)-+)?>)\s*'
    r'(?P<b>\[\*\]|\[H\*?\]|[\w.]+)\s*(?::\s*(?P<label>.*))?$'
)
DESCRIPCION = re.compile(r'^(?P<s>[\w]+)\s*:\s*(?P<texto>.*)$')
PSEUDO = {'<<choice>>': 'choice', '<<fork>>': 'fork', '<<join>>': 'join',
          '<<junction>>': 'junction', '<<entryPoint>>': 'entryPoint',
          '<<exitPoint>>': 'exitPoint', '<<end>>': 'terminate'}
TRIGGER = re.compile(r'^(?P<ev>[^\[/]*)?(?:\[(?P<g>[^\]]*)\])?\s*(?:/\s*(?P<ef>.*))?$')


def parse_estados(lineas, problemas):
    d = {'estados': [], 'transiciones': [], 'notas': []}
    por_nombre = {}
    pila = [None]

    def estado(nombre, src):
        if nombre not in por_nombre:
            e = {'name': nombre, 'label': None, 'kind': 'state', 'padre': pila[-1],
                 'descripciones': [], 'entry': None, 'do': None, 'exit': None, 'src': src}
            por_nombre[nombre] = e
            d['estados'].append(e)
        return por_nombre[nombre]

    i = 0
    while i < len(lineas):
        l = lineas[i]
        t = l.texto
        if PRESENTACION.match(t):
            i += 1
            continue
        if t.startswith(('note ', 'rnote ', 'hnote ')):
            n, i = nota(lineas, i, problemas)
            if n:
                d['notas'].append(n)
            continue
        if t.startswith('legend'):
            i = saltar_legend(lineas, i)
            continue
        m = ESTADO.match(t)
        if m:
            nombre = m.group('alias') or m.group('name')
            e = estado(nombre, l.src)
            e['label'] = m.group('label') or m.group('label2') or e['label']
            st = m.group('stereo')
            if st:
                if st not in PSEUDO:
                    problemas.agregar('P1', l.src, f'estereotipo de estado sin metaclase UML: {st}')
                else:
                    e['kind'] = PSEUDO[st]
            if m.group('desc'):
                describir(e, m.group('desc'), l.src)
            if m.group('open'):
                pila.append(nombre)
            i += 1
            continue
        if t == '}' and len(pila) > 1:
            pila.pop()
            i += 1
            continue
        if t in ('--', '||'):
            problemas.agregar('P1', l.src, 'regiones ortogonales todavía no soportadas por el conversor')
            i += 1
            continue
        m = TRANSICION.match(t)
        if m:
            a, b = m.group('a'), m.group('b')
            label = (m.group('label') or '').strip()
            tr = TRIGGER.match(label) if label else None
            for x in (a, b):
                if not x.startswith('['):
                    estado(x, l.src)
                elif x.startswith('[H'):
                    problemas.agregar('P1', l.src, 'historia todavía no soportada por el conversor')
            d['transiciones'].append({
                'from': a if a != '[*]' else f'[*]{pila[-1] or ""}',
                'to': b if b != '[*]' else f'[*]fin{pila[-1] or ""}',
                'evento': (tr.group('ev') or '').strip() or None if tr else None,
                'guarda': (tr.group('g') or '').strip() or None if tr else None,
                'efecto': (tr.group('ef') or '').strip() or None if tr else None,
                'texto': label or None, 'region': pila[-1], 'src': l.src})
            i += 1
            continue
        m = DESCRIPCION.match(t)
        if m and m.group('s') in por_nombre:
            describir(por_nombre[m.group('s')], m.group('texto'), l.src)
            i += 1
            continue
        problemas.agregar('P1', l.src, f'construcción no traducible: {t}')
        i += 1
    return d


def describir(e, texto, src):
    m = re.match(r'^(entry|do|exit)\s*/\s*(.*)$', texto)
    if m:
        e[m.group(1)] = m.group(2).strip()
    else:
        e['descripciones'].append({'texto': texto.strip(), 'src': src})


# -------------------------------------------------------------- actividades

ACCION_FIN = re.compile(r'(?<!\\);\s*$')
SDL_FIN = re.compile(r'[<>/\]}|]\s*$')


def parse_actividades(lineas, problemas):
    """Devuelve un árbol de bloques; el grafo se arma en model.py."""
    raiz = {'tipo': 'secuencia', 'items': []}
    pila = [raiz]
    d = {'raiz': raiz, 'particiones': [], 'notas': []}
    carril = None
    i = 0

    def agregar(nodo):
        nodo.setdefault('particion', carril)
        pila[-1]['items'].append(nodo)

    while i < len(lineas):
        l = lineas[i]
        t = l.texto
        if PRESENTACION.match(t):
            i += 1
            continue
        if t.startswith(('note ', 'floating note')):
            n, i = nota(lineas, i, problemas) if t.startswith('note ') else (None, i + 1)
            if n:
                d['notas'].append(n)
            continue
        if t.startswith('legend'):
            i = saltar_legend(lineas, i)
            continue
        m = re.match(r'^\|(?:#\w+\|)?([^|]+)\|$', t)
        if m:
            carril = m.group(1).strip()
            if carril not in d['particiones']:
                d['particiones'].append(carril)
            i += 1
            continue
        if t.startswith(':'):
            partes, j = [t[1:]], i
            while not ACCION_FIN.search(partes[-1]) and j + 1 < len(lineas):
                if SDL_FIN.search(partes[-1]) and len(partes) == 1 and False:
                    break
                j += 1
                partes.append(lineas[j].texto)
            texto = '\n'.join(partes)
            if not ACCION_FIN.search(texto):
                problemas.agregar('P1', l.src, 'acción SDL o sin ";": sin metaclase UML')
            agregar({'tipo': 'accion', 'texto': ACCION_FIN.sub('', texto).strip(), 'src': l.src})
            i = j + 1
            continue
        if t == 'start':
            agregar({'tipo': 'inicio', 'src': l.src})
        elif t in ('stop', 'end'):
            agregar({'tipo': 'fin', 'src': l.src})
        elif t == 'kill':
            agregar({'tipo': 'fin_flujo', 'src': l.src})
        elif t in ('detach', 'split', 'split again', 'end split') or t.startswith('backward'):
            problemas.agregar('P1', l.src, f'"{t}" no tiene metaclase UML')
        elif re.match(r'^if\s*\(', t):
            m = re.match(r'^if\s*\((?P<c>.*)\)\s*then\s*(?:\((?P<g>[^)]*)\))?\s*$', t)
            if not m:
                problemas.agregar('P1', l.src, f'if no reconocido: {t}')
            nodo = {'tipo': 'decision', 'pregunta': m.group('c') if m else t,
                    'ramas': [{'guarda': m.group('g') if m else None, 'items': [], 'src': l.src}],
                    'src': l.src}
            agregar(nodo)
            pila.append({'tipo': 'rama', 'items': nodo['ramas'][0]['items'], 'nodo': nodo})
        elif re.match(r'^elseif\s*\(', t):
            m = re.match(r'^elseif\s*\((?P<c>.*)\)\s*then\s*(?:\((?P<g>[^)]*)\))?\s*$', t)
            nodo = pila[-1]['nodo']
            rama = {'guarda': m.group('g'), 'pregunta': m.group('c'), 'items': [], 'src': l.src}
            nodo['ramas'].append(rama)
            pila[-1] = {'tipo': 'rama', 'items': rama['items'], 'nodo': nodo}
        elif re.match(r'^else\b', t):
            m = re.match(r'^else\s*(?:\((?P<g>[^)]*)\))?\s*$', t)
            nodo = pila[-1]['nodo']
            rama = {'guarda': m.group('g') if m else None, 'items': [], 'src': l.src, 'else': True}
            nodo['ramas'].append(rama)
            pila[-1] = {'tipo': 'rama', 'items': rama['items'], 'nodo': nodo}
        elif t in ('endif', 'end if'):
            pila.pop()
        elif t == 'repeat' or t.startswith('repeat :'):
            nodo = {'tipo': 'repetir', 'items': [], 'src': l.src}
            agregar(nodo)
            pila.append({'tipo': 'rama', 'items': nodo['items'], 'nodo': nodo})
        elif t.startswith('repeat while'):
            m = re.match(r'^repeat while\s*\((?P<c>.*?)\)\s*(?:is\s*\((?P<si>[^)]*)\))?\s*'
                         r'(?:not\s*\((?P<no>[^)]*)\))?\s*$', t)
            nodo = pila.pop()['nodo']
            nodo.update({'pregunta': m.group('c'), 'guarda_si': m.group('si'),
                         'guarda_no': m.group('no'), 'src_fin': l.src})
        elif re.match(r'^while\s*\(', t):
            m = re.match(r'^while\s*\((?P<c>.*?)\)\s*(?:is\s*\((?P<si>[^)]*)\))?\s*$', t)
            nodo = {'tipo': 'mientras', 'pregunta': m.group('c'), 'guarda_si': m.group('si'),
                    'items': [], 'src': l.src}
            agregar(nodo)
            pila.append({'tipo': 'rama', 'items': nodo['items'], 'nodo': nodo})
        elif t.startswith('endwhile'):
            m = re.match(r'^endwhile\s*(?:\((?P<no>[^)]*)\))?\s*$', t)
            nodo = pila.pop()['nodo']
            nodo['guarda_no'] = m.group('no') if m else None
        elif t == 'fork':
            nodo = {'tipo': 'fork', 'ramas': [{'items': []}], 'src': l.src}
            agregar(nodo)
            pila.append({'tipo': 'rama', 'items': nodo['ramas'][0]['items'], 'nodo': nodo})
        elif t == 'fork again':
            nodo = pila[-1]['nodo']
            nodo['ramas'].append({'items': []})
            pila[-1] = {'tipo': 'rama', 'items': nodo['ramas'][-1]['items'], 'nodo': nodo}
        elif t.startswith('end fork') or t.startswith('end merge'):
            pila.pop()
        else:
            problemas.agregar('P1', l.src, f'construcción no traducible: {t}')
        i += 1
    return d


# ------------------------------------------------------------------- entrada

TIPOS = ('clases', 'secuencia', 'estados', 'actividades', 'casos-de-uso',
         'generalizacion-actores', 'paquetes')


def tipo_de(path):
    for t in TIPOS:
        if f'-{t}' in Path(path).name:
            return t
    return None


def parse_diagrama(path, raiz, problemas):
    global pila_frag
    pila_frag = []
    lineas = leer(path, raiz)
    tipo = tipo_de(path)
    base = {'archivo': _rel(path, raiz), 'tipo': tipo, 'titulo': titulo(lineas),
            'cu': (re.match(r'^(CU-\d{2})', Path(path).name) or [None, None])[1]}
    if tipo == 'clases':
        base.update(parse_clases(lineas, problemas))
    elif tipo == 'secuencia':
        base.update(parse_secuencia(lineas, problemas))
        if pila_frag:
            problemas.agregar('P1', base['archivo'], 'fragmento sin "end"')
    elif tipo == 'estados':
        base.update(parse_estados(lineas, problemas))
    elif tipo == 'actividades':
        base.update(parse_actividades(lineas, problemas))
    else:
        problemas.agregar('P2', base['archivo'], f'tipo de diagrama fuera de alcance: {tipo}',
                          nivel='aviso')
    return base
