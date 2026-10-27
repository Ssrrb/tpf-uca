"""Une los diagramas parseados en un único modelo (build/model.json).

- Las clases con el mismo nombre (alias) en distintos CU son una sola: se unen
  atributos, operaciones, etiquetas y orígenes.
- Los tipos en castellano se traducen según docs/uml-subset.md (R2) y las
  uniones `a | b` generan una Enumeration (R3).
- Secuencias, máquinas de estados y actividades quedan como comportamientos
  del modelo, con sus referencias resueltas contra las clases.

Los problemas de consistencia se juntan en `problemas` (ver checks.py).
"""
import re
import unicodedata
from collections import OrderedDict, defaultdict

PRIMITIVOS = {'texto': 'String', 'entero': 'Integer', 'decimal': 'Real', 'lógico': 'Boolean',
              'logico': 'Boolean'}
DATATYPES = {'fecha': 'Fecha', 'fecha y hora': 'FechaHora', 'guaraníes': 'Guaranies',
             'guaranies': 'Guaranies', 'archivo': 'Archivo', 'porcentaje': 'Porcentaje'}
SIN_RETORNO = {'vacío', 'vacio', 'void'}
PAQUETE_TIPOS = 'Tipos'


def normalizar(nombre):
    s = unicodedata.normalize('NFKD', nombre or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[\s_\-.]', '', s).lower()


def pascal(texto):
    s = unicodedata.normalize('NFKD', texto)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ''.join(p[:1].upper() + p[1:] for p in re.split(r'[^\w]+|_', s) if p)


class Modelo:
    def __init__(self, problemas):
        self.p = problemas
        self.clasificadores = OrderedDict()   # nombre -> dict
        self.paquetes = OrderedDict()
        self.relaciones = []
        self.datatypes = OrderedDict()
        self.actores = OrderedDict()
        self.interacciones = []
        self.maquinas = []
        self.actividades = []
        self.comentarios = []
        self.etiquetas = defaultdict(set)     # etiqueta -> {nombres}

    # ---------------------------------------------------------------- clases
    def agregar_clases(self, d):
        for pq in d['paquetes']:
            self._paquete(pq['name'], pq['src'])
        for c in d['clasificadores']:
            self._clasificador(c, d['archivo'])
        for r in d['relaciones']:
            r = dict(r)
            r['cu'] = d['cu']
            self.relaciones.append(r)
        for n in d['notas']:
            self.comentarios.append({'texto': n['texto'], 'anota': n['anota'], 'src': n['src'],
                                     'ambito': 'clases'})

    def _paquete(self, nombre, src):
        partes = nombre.split('::')
        for i in range(len(partes)):
            q = '::'.join(partes[:i + 1])
            self.paquetes.setdefault(q, {'name': partes[i], 'qname': q,
                                         'padre': '::'.join(partes[:i]) or None, 'srcs': []})
            if i == len(partes) - 1 and src not in self.paquetes[q]['srcs']:
                self.paquetes[q]['srcs'].append(src)

    def _clasificador(self, c, archivo):
        nombre = c['name']
        if c['label']:
            self.etiquetas[c['label']].add(nombre)
        if nombre not in self.clasificadores:
            self.clasificadores[nombre] = {
                'name': nombre, 'kind': c['kind'], 'abstract': c['abstract'],
                'package': c['package'], 'labels': [], 'stereotype': c['stereotype'],
                'atributos': OrderedDict(), 'operaciones': OrderedDict(),
                'literales': OrderedDict(), 'srcs': []}
        dst = self.clasificadores[nombre]
        dst['srcs'].append(c['src'])
        if c['label'] and c['label'] not in dst['labels']:
            dst['labels'].append(c['label'])
        if dst['kind'] != c['kind']:
            self.p.agregar('C2', c['src'], f'{nombre} es {c["kind"]} acá y {dst["kind"]} en '
                           f'{dst["srcs"][0]}')
        if c['abstract'] and not dst['abstract']:
            dst['abstract'] = True
        if c['package'] and dst['package'] and c['package'] != dst['package']:
            self.p.agregar('C2', c['src'], f'{nombre} está en el paquete {c["package"]} acá y en '
                           f'{dst["package"]} en {dst["srcs"][0]}')
        dst['package'] = dst['package'] or c['package']
        for a in c['atributos']:
            prev = dst['atributos'].get(a['name'])
            if prev is None:
                dst['atributos'][a['name']] = dict(a, srcs=[a['src']])
                continue
            prev['srcs'].append(a['src'])
            if (a['type'] or '') != (prev['type'] or '') and a['type'] and prev['type']:
                self.p.agregar('C5', a['src'], f'{nombre}.{a["name"]} tiene tipo "{a["type"]}" '
                               f'acá y "{prev["type"]}" en {prev["src"]}')
            if a['mult'] and prev['mult'] and a['mult'] != prev['mult']:
                self.p.agregar('C5', a['src'], f'{nombre}.{a["name"]} tiene multiplicidad '
                               f'{fmt_mult(a["mult"])} acá y {fmt_mult(prev["mult"])} en {prev["src"]}')
            prev['type'] = prev['type'] or a['type']
            prev['mult'] = prev['mult'] or a['mult']
            prev['visibility'] = prev['visibility'] or a['visibility']
            for m in a['modificadores']:
                if m not in prev['modificadores']:
                    prev['modificadores'].append(m)
        for o in c['operaciones']:
            prev = dst['operaciones'].get(o['name'])
            if prev is None:
                dst['operaciones'][o['name']] = dict(o, srcs=[o['src']])
                continue
            prev['srcs'].append(o['src'])
            if len(o['params']) != len(prev['params']):
                self.p.agregar('C5', o['src'], f'{nombre}.{o["name"]}() tiene {len(o["params"])} '
                               f'parámetros acá y {len(prev["params"])} en {prev["src"]}',
                               nivel='aviso')
            elif any(x['type'] and y['type'] and x['type'] != y['type']
                     for x, y in zip(o['params'], prev['params'])):
                self.p.agregar('C5', o['src'], f'{nombre}.{o["name"]}() cambia el tipo de un '
                               f'parámetro respecto de {prev["src"]}', nivel='aviso')
            else:
                for x, y in zip(o['params'], prev['params']):
                    y['type'] = y['type'] or x['type']
            if o['return'] and prev['return'] and o['return'] != prev['return']:
                self.p.agregar('C5', o['src'], f'{nombre}.{o["name"]}() devuelve "{o["return"]}" '
                               f'acá y "{prev["return"]}" en {prev["src"]}')
            prev['return'] = prev['return'] or o['return']
        for lit in c['literales']:
            dst['literales'].setdefault(lit['name'], lit)

    # ------------------------------------------------------------------ tipos
    def resolver_tipo(self, texto, duenio, atributo, src):
        """Devuelve una referencia {'primitivo': X} | {'ref': nombre} | None."""
        if not texto:
            return None
        t = texto.strip()
        m = re.match(r'^lista(?:\s+de\s+(.+))?$', t, re.I)
        if m:
            # "lista de X" -> tipo X con multiplicidad 0..*; "lista" sola, sin tipo.
            interno = self.resolver_tipo(m.group(1), duenio, atributo, src) if m.group(1) else {}
            return dict(interno or {}, coleccion=True) if interno is not None else None
        if t in self.clasificadores:
            return {'ref': t}
        clave_n = normalizar(t)
        variantes = {n for n, c in self.clasificadores.items()
                     if normalizar(n) == clave_n or any(normalizar(x) == clave_n for x in c['labels'])}
        if len(variantes) == 1:
            nombre = variantes.pop()
            self.p.agregar('C1', src, f'tipo "{t}" de {duenio}.{atributo} es una variante de '
                           f'escritura de {nombre}: se usa {nombre}', nivel='aviso')
            return {'ref': nombre}
        clave = t.lower()
        if clave in PRIMITIVOS:
            return {'primitivo': PRIMITIVOS[clave]}
        if clave in DATATYPES:
            nombre = DATATYPES[clave]
            self.datatypes.setdefault(nombre, {'name': nombre, 'kind': 'datatype',
                                               'origen': t, 'srcs': []})
            self.datatypes[nombre]['srcs'].append(src)
            return {'ref': nombre}
        if '|' in t:
            literales = [x.strip() for x in t.split('|') if x.strip()]
            nombre = pascal(duenio) + pascal(atributo)
            prev = self.datatypes.get(nombre)
            if prev and prev['literales'] != literales:
                self.p.agregar('C5', src, f'la unión de {duenio}.{atributo} cambia de literales '
                               f'respecto de {prev["srcs"][0]}')
            self.datatypes.setdefault(nombre, {'name': nombre, 'kind': 'enum', 'origen': t,
                                               'literales': literales, 'srcs': []})
            self.datatypes[nombre]['srcs'].append(src)
            return {'ref': nombre}
        self.p.agregar('C4', src, f'tipo "{t}" de {duenio}.{atributo} no está definido '
                       '(ni clase, ni enumeración, ni tipo de R2)')
        return None

    # ------------------------------------------------------------- relaciones
    def resolver_relaciones(self):
        vistas = {}
        unidas = []
        for r in self.relaciones:
            faltan = [x for x in (r['a'], r['b']) if x not in self.clasificadores]
            if faltan:
                self.p.agregar('C4', r['src'], f'relación hacia elemento no definido: {", ".join(faltan)}')
                continue
            if r['kind'] in ('association', 'association-nd', 'association-bi',
                             'composition', 'aggregation'):
                if not r['mult_a'] or not r['mult_b']:
                    self.p.agregar('C5', r['src'], f'asociación {r["a"]} – {r["b"]} sin multiplicidad '
                                   'en algún extremo')
                for m in (r['mult_a'], r['mult_b']):
                    if m and m.get('invalida'):
                        self.p.agregar('C5', r['src'], f'multiplicidad no válida: "{m["texto"]}"')
            familia = 'herencia' if r['kind'] in ('generalization', 'realization') else (
                'dependencia' if r['kind'] == 'dependency' else 'asociacion')
            clave = (familia, r['a'], r['b']) if familia != 'asociacion' else (
                familia, *sorted((r['a'], r['b'])))
            prev = vistas.get(clave)
            if prev is None:
                r = dict(r, srcs=[r['src']])
                vistas[clave] = r
                unidas.append(r)
                continue
            prev['srcs'].append(r['src'])
            if familia != 'asociacion':
                continue
            if prev['a'] != r['a']:     # misma asociación escrita al revés
                r = dict(r, a=r['b'], b=r['a'], mult_a=r['mult_b'], mult_b=r['mult_a'])
            if prev['kind'] != r['kind']:
                self.p.agregar('C5', r['src'], f'{r["a"]} – {r["b"]} es {r["kind"]} acá y '
                               f'{prev["kind"]} en {prev["src"]}')
            for lado in ('mult_a', 'mult_b'):
                if r[lado] and prev[lado] and r[lado] != prev[lado]:
                    self.p.agregar('C5', r['src'], f'multiplicidades incompatibles en {r["a"]} – '
                                   f'{r["b"]}: {fmt_mult(r["mult_a"])}/{fmt_mult(r["mult_b"])} acá, '
                                   f'{fmt_mult(prev["mult_a"])}/{fmt_mult(prev["mult_b"])} en {prev["src"]}')
            if r.get('label') and prev.get('label') and r['label'] != prev['label']:
                self.p.agregar('C1', r['src'], f'{r["a"]} – {r["b"]} se llama "{r["label"]}" acá y '
                               f'"{prev["label"]}" en {prev["src"]}', nivel='aviso')
        self.relaciones = unidas
        self._ciclos_herencia()

    def _ciclos_herencia(self):
        padres = defaultdict(set)
        for r in self.relaciones:
            if r['kind'] == 'generalization':
                padres[r['a']].add(r['b'])
        for c in padres:
            vistos, pila = set(), [c]
            while pila:
                x = pila.pop()
                for p in padres.get(x, ()):
                    if p == c:
                        self.p.agregar('C4', self.clasificadores[c]['srcs'][0], f'ciclo de herencia en {c}')
                        pila = []
                        break
                    if p not in vistos:
                        vistos.add(p)
                        pila.append(p)

    def ancestros(self, nombre):
        out, pila = [], [nombre]
        while pila:
            x = pila.pop()
            for r in self.relaciones:
                if r['kind'] in ('generalization', 'realization') and r['a'] == x and r['b'] not in out:
                    out.append(r['b'])
                    pila.append(r['b'])
        return out

    def operacion(self, clase, nombre):
        for c in [clase] + self.ancestros(clase):
            op = self.clasificadores.get(c, {}).get('operaciones', {}).get(nombre)
            if op:
                return c, op
        return None, None

    # ------------------------------------------------------------- secuencias
    def agregar_secuencia(self, d):
        inter = {'name': nombre_comportamiento(d), 'archivo': d['archivo'], 'cu': d['cu'],
                 'lifelines': [], 'items': d['items'], 'titulo': d['titulo']}
        for ll in d['lifelines']:
            ll = dict(ll)
            if ll['kind'] == 'actor':
                # "Administrador (o Finanzas y tesorería)" -> Actor "Administrador";
                # la aclaración queda en el nombre de la lifeline.
                nombre = re.sub(r'\s*\(.*\)\s*$', '', ll['label']) or ll['label']
                self.actores.setdefault(nombre, {'name': nombre, 'srcs': []})
                self.actores[nombre]['srcs'].append(ll['src'])
                ll['tipo_ref'] = nombre
                ll['es_actor'] = True
            else:
                tipo = ll['type'] or (ll['alias'] if ll['implicita'] else None)
                if tipo not in self.clasificadores:
                    self.p.agregar('C3', ll['src'], f'la lifeline "{ll["label"]}" es de tipo '
                                   f'"{tipo}", que no es una clase del modelo')
                    ll['tipo_ref'] = None
                else:
                    ll['tipo_ref'] = tipo
            inter['lifelines'].append(ll)
        tipos = {ll['alias']: ll for ll in inter['lifelines']}
        self._mensajes(d['items'], tipos)
        self.interacciones.append(inter)

    def _mensajes(self, items, tipos):
        for it in items:
            if it['tipo'] == 'fragment':
                for op in it['operandos']:
                    self._mensajes(op['items'], tipos)
            elif it['tipo'] == 'message' and it['sort'] in ('synchCall', 'asynchCall'):
                dst = tipos.get(it['to'])
                if not dst or dst.get('es_actor') or not dst.get('tipo_ref'):
                    continue
                if not it['operacion']:
                    self.p.agregar('C3', it['src'], f'mensaje "{it["texto"]}" a {dst["tipo_ref"]} '
                                   'no tiene forma de llamada op(...)')
                    continue
                duenio, op = self.operacion(dst['tipo_ref'], it['operacion'])
                if not op:
                    self.p.agregar('C3', it['src'], f'{it["operacion"]}() no es una operación de '
                                   f'{dst["tipo_ref"]} (ni de sus ancestros)')
                else:
                    it['signature'] = f'{duenio}.{op["name"]}'

    def resolver_refs(self):
        por_titulo = {}
        for inter in self.interacciones:
            for k in (inter['name'], inter['titulo'] or ''):
                por_titulo[normalizar(k)] = inter['name']

        def buscar(texto, cu):
            destino = por_titulo.get(normalizar(texto))
            if destino:
                return destino
            m = re.search(r'contin[uú]a en (\d+)\s*/\s*\d+', texto, re.I)
            if m:
                for inter in self.interacciones:
                    if inter['cu'] == cu and f'-secuencia-{m.group(1)}-' in inter['archivo']:
                        return inter['name']
            m = re.search(r'\b(CU-\d{2})\b', texto)
            if m:
                for inter in self.interacciones:
                    if inter['cu'] == m.group(1):
                        return inter['name']
            return None

        def walk(items, cu):
            for it in items:
                if it['tipo'] == 'fragment':
                    for op in it['operandos']:
                        walk(op['items'], cu)
                elif it['tipo'] == 'ref':
                    destino = buscar(it['texto'], cu)
                    it['refersTo'] = destino
                    if not destino:
                        self.p.agregar('C4', it['src'], f'ref "{it["texto"]}" no nombra otra '
                                       'secuencia del modelo: queda como comentario', nivel='aviso')
        for inter in self.interacciones:
            walk(inter['items'], inter['cu'])

    # ----------------------------------------------------------------- estados
    def agregar_estados(self, d):
        maq = {'name': nombre_comportamiento(d), 'archivo': d['archivo'], 'cu': d['cu'],
               'titulo': d['titulo'], 'estados': d['estados'], 'transiciones': d['transiciones'],
               'notas': d['notas']}
        nombres = {e['name'] for e in d['estados']}
        if not any(t['from'].startswith('[*]') for t in d['transiciones']):
            self.p.agregar('C4', d['archivo'], 'máquina de estados sin estado inicial')
        for e in d['estados']:
            if e['descripciones']:
                self.p.agregar('R4', e['src'], f'texto libre en el estado {e["name"]}: pasa a '
                               'Comment', nivel='info')
        for t in d['transiciones']:
            for x in (t['from'], t['to']):
                if not x.startswith('[*]') and x not in nombres:
                    self.p.agregar('C4', t['src'], f'transición hacia estado no definido: {x}')
        self.maquinas.append(maq)

    # ------------------------------------------------------------- actividades
    def agregar_actividades(self, d):
        act = {'name': nombre_comportamiento(d), 'archivo': d['archivo'], 'cu': d['cu'],
               'titulo': d['titulo'], 'particiones': d['particiones'], 'nodos': [], 'flujos': [],
               'notas': d['notas']}
        grafo = Grafo(act)
        salidas = grafo.secuencia(d['raiz']['items'], [])
        if salidas:
            self.p.agregar('C4', d['archivo'], 'la actividad tiene caminos que no terminan en un nodo final',
                           nivel='aviso')
        if sum(1 for n in act['nodos'] if n['kind'] == 'InitialNode') != 1:
            self.p.agregar('C4', d['archivo'], 'la actividad necesita exactamente un nodo inicial')
        self.actividades.append(act)

    # ------------------------------------------------------------------ salida
    def tipar(self):
        for c in self.clasificadores.values():
            for a in c['atributos'].values():
                a['type_ref'] = self.resolver_tipo(a['type'], c['name'], a['name'], a['src'])
            for o in c['operaciones'].values():
                for p in o['params']:
                    p['type_ref'] = self.resolver_tipo(p['type'], c['name'], f'{o["name"]}.{p["name"]}',
                                                       o['src']) if p['type'] else None
                if (o['return'] or '').strip().lower() in SIN_RETORNO:
                    o['return'] = None
                o['return_ref'] = self.resolver_tipo(o['return'], c['name'], f'{o["name"]}.return',
                                                     o['src']) if o['return'] else None

    def a_json(self):
        def lista(od):
            return list(od.values())
        return {
            'formato': 'tpf-uca/model@1',
            'paquetes': lista(self.paquetes),
            'clasificadores': [dict(c, atributos=lista(c['atributos']),
                                    operaciones=lista(c['operaciones']),
                                    literales=lista(c['literales']))
                               for c in self.clasificadores.values()],
            'tipos': lista(self.datatypes),
            'actores': lista(self.actores),
            'relaciones': self.relaciones,
            'interacciones': self.interacciones,
            'maquinas_de_estados': self.maquinas,
            'actividades': self.actividades,
            'comentarios': self.comentarios,
        }


def fmt_mult(m):
    if not m:
        return '?'
    if m.get('invalida'):
        return m['texto']
    return str(m['lower']) if m['lower'] == m['upper'] else f'{m["lower"]}..{m["upper"]}'


def nombre_comportamiento(d):
    """CU-02-secuencia-1-carga.puml -> 'CU-02 secuencia 1 carga'."""
    base = d['archivo'].rsplit('/', 1)[-1].removesuffix('.puml')
    return base.replace('-', ' ', 2).replace('-', ' ')


class Grafo:
    """Convierte el árbol de bloques de una actividad en nodos y ControlFlow."""

    def __init__(self, act):
        self.act = act

    def nodo(self, kind, it=None, name=None):
        n = {'id': f'n{len(self.act["nodos"]) + 1}', 'kind': kind, 'name': name,
             'particion': (it or {}).get('particion'), 'src': (it or {}).get('src')}
        self.act['nodos'].append(n)
        return n['id']

    def unir(self, preds, destino):
        for origen, guarda in preds:
            self.act['flujos'].append({'from': origen, 'to': destino, 'guarda': guarda})

    def secuencia(self, items, preds):
        for it in items:
            preds = self.bloque(it, preds)
        return preds

    def bloque(self, it, preds):
        t = it['tipo']
        if t == 'inicio':
            return [(self.nodo('InitialNode', it), None)]
        if t == 'fin':
            self.unir(preds, self.nodo('ActivityFinalNode', it))
            return []
        if t == 'fin_flujo':
            self.unir(preds, self.nodo('FlowFinalNode', it))
            return []
        if t == 'accion':
            n = self.nodo('OpaqueAction', it, it['texto'])
            self.unir(preds, n)
            return [(n, None)]
        if t == 'decision':
            salidas, entrada = [], preds
            tiene_else = any(r.get('else') for r in it['ramas'])
            pendiente = None
            for k, rama in enumerate(it['ramas']):
                if rama.get('else'):
                    salidas += self.secuencia(rama['items'], [(pendiente, rama['guarda'])])
                    pendiente = None
                    continue
                pregunta = it['pregunta'] if k == 0 else rama['pregunta']
                d = self.nodo('DecisionNode', rama if k else it, pregunta)
                self.unir(entrada if k == 0 else [(pendiente, 'else')], d)
                salidas += self.secuencia(rama['items'], [(d, rama['guarda'])])
                pendiente = d
            if pendiente and not tiene_else:
                salidas.append((pendiente, 'else'))
            if not salidas:
                return []
            m = self.nodo('MergeNode', it)
            self.unir(salidas, m)
            return [(m, None)]
        if t == 'repetir':
            m = self.nodo('MergeNode', it)
            self.unir(preds, m)
            fin = self.secuencia(it['items'], [(m, None)])
            d = self.nodo('DecisionNode', it, it.get('pregunta'))
            self.unir(fin, d)
            self.act['flujos'].append({'from': d, 'to': m, 'guarda': it.get('guarda_si')})
            return [(d, it.get('guarda_no'))]
        if t == 'mientras':
            m = self.nodo('MergeNode', it)
            self.unir(preds, m)
            d = self.nodo('DecisionNode', it, it['pregunta'])
            self.unir([(m, None)], d)
            fin = self.secuencia(it['items'], [(d, it.get('guarda_si'))])
            self.unir(fin, m)
            return [(d, it.get('guarda_no'))]
        if t == 'fork':
            f = self.nodo('ForkNode', it)
            self.unir(preds, f)
            salidas = []
            for rama in it['ramas']:
                salidas += self.secuencia(rama['items'], [(f, None)])
            j = self.nodo('JoinNode', it)
            self.unir(salidas, j)
            return [(j, None)]
        raise ValueError(t)
