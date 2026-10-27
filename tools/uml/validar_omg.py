#!/usr/bin/env python3
"""Paso 6.2: valida build/model.xmi contra los archivos normativos de OMG.

Descarga de www.omg.org (y solo de ahí) los archivos legibles por máquina de
UML 2.5.1 (formal/17-12-05) y XMI 2.5.1:

  UML.xmi             metamodelo UML 2.5.1      https://www.omg.org/spec/UML/20161101/UML.xmi
  PrimitiveTypes.xmi  tipos primitivos          https://www.omg.org/spec/UML/20161101/PrimitiveTypes.xmi
  XMI.xsd             esquema XMI 2.5.1         https://www.omg.org/spec/XMI/20131001/XMI.xsd

y hace dos validaciones:

  1. Esquema: el documento contra XMI.xsd (lxml). XMI.xsd define solo el
     espacio de nombres xmi:, así que cubre la envoltura XMI, no el contenido UML.
  2. Metamodelo: cada elemento contra UML.xmi. Comprueba que xmi:type sea una
     metaclase concreta de UML 2.5.1, que cada atributo y cada hijo sea una
     propiedad de esa metaclase (o de sus superclases), que las referencias
     apunten a xmi:id existentes del tipo correcto, que los valores de
     enumeraciones y primitivos sean válidos y que se respeten las
     multiplicidades.

No evalúa las restricciones OCL del metamodelo (eso lo hace en parte Eclipse
UML2, ver tools/uml/eclipse/ValidarUML.java).

Uso: validar_omg.py build/model.xmi [--cache DIR] [--out build/validacion-omg.md]
Sale con 1 si hay errores o si no se pudieron obtener los archivos de OMG.
"""
import hashlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

XMI_NS = 'http://www.omg.org/spec/XMI/20131001'
XT = f'{{{XMI_NS}}}type'
XID = f'{{{XMI_NS}}}id'
XIDREF = f'{{{XMI_NS}}}idref'


def parse_xmi(path):
    """Parsea un XMI y normaliza el namespace xmi: (OMG publicó archivos con
    distintas versiones de XMI) al de XMI 2.5.1."""
    raiz = ET.parse(path).getroot()
    for e in raiz.iter():
        for k in [k for k in e.attrib if k.startswith('{') and '/XMI' in k.split('}')[0]]:
            v = e.attrib.pop(k)
            e.set(f'{{{XMI_NS}}}{k.split("}")[1]}', v)
    return raiz
UML_URI = 'http://www.omg.org/spec/UML/20161101'
ARCHIVOS = {
    'UML.xmi': f'https://www.omg.org/spec/UML/20161101/UML.xmi',
    'PrimitiveTypes.xmi': f'https://www.omg.org/spec/UML/20161101/PrimitiveTypes.xmi',
    'XMI.xsd': 'https://www.omg.org/spec/XMI/20131001/XMI.xsd',
}


# ------------------------------------------------------------------ descarga

def descargar(cache):
    cache.mkdir(parents=True, exist_ok=True)
    info = {}
    for nombre, url in ARCHIVOS.items():
        destino = cache / nombre
        if not destino.exists():
            req = urllib.request.Request(url, headers={'User-Agent': 'tpf-uca-ci'})
            with urllib.request.urlopen(req, timeout=60) as r:
                final = urlparse(r.geturl())
                if final.scheme != 'https' or final.hostname not in ('www.omg.org', 'omg.org'):
                    raise RuntimeError(f'{url} redirigió fuera de omg.org: {r.geturl()}')
                destino.write_bytes(r.read())
        datos = destino.read_bytes()
        info[nombre] = {'url': url, 'sha256': hashlib.sha256(datos).hexdigest(), 'bytes': len(datos)}
    texto = (cache / 'UML.xmi').read_text(encoding='utf-8', errors='replace')
    if UML_URI not in texto:
        raise RuntimeError(f'UML.xmi no declara {UML_URI}: no es el metamodelo de UML 2.5.1')
    return info


# ---------------------------------------------------------------- metamodelo

def local(tag):
    return tag.rsplit('}', 1)[-1]


def ref_de(e, attr):
    """Valor de una referencia escrita como atributo, hijo con xmi:idref o hijo con href."""
    if e.get(attr):
        return e.get(attr)
    for h in e:
        if local(h.tag) == attr:
            if h.get(XIDREF):
                return h.get(XIDREF)
            if h.get('href'):
                return h.get('href').rsplit('#', 1)[-1]
    return None


def valor_literal(e, hijo, defecto):
    for h in e:
        if local(h.tag) == hijo:
            v = h.get('value')
            if v is None:
                return 0 if hijo == 'lowerValue' else defecto
            return '*' if v == '*' else int(v)
    return defecto


class Metamodelo:
    def __init__(self, path):
        raiz = parse_xmi(path)
        self.clases, self.enums, self.primitivos = {}, {}, {'Boolean', 'Integer', 'Real',
                                                            'String', 'UnlimitedNatural'}
        self.props, self.asociaciones, self.nombre = {}, {}, {}
        for e in raiz.iter():
            t = e.get(XT)
            if t == 'uml:Class':
                cid = e.get(XID)
                self.nombre[cid] = e.get('name')
                gens = [ref_de(g, 'general') for g in e if local(g.tag) == 'generalization']
                gens += (e.get('superClass') or '').split()
                props = {}
                for p in e:
                    if local(p.tag) == 'ownedAttribute':
                        info = self.prop(p)
                        props[info['name']] = info
                        self.props[p.get(XID)] = info
                self.clases[e.get('name')] = {'id': cid, 'abstract': e.get('isAbstract') == 'true',
                                              'supers': [g for g in gens if g], 'props': props}
            elif t == 'uml:Enumeration':
                self.nombre[e.get(XID)] = e.get('name')
                self.enums[e.get('name')] = {l.get('name') for l in e if local(l.tag) == 'ownedLiteral'}
            elif t == 'uml:PrimitiveType':
                self.nombre[e.get(XID)] = e.get('name')
                self.primitivos.add(e.get('name'))
            elif t == 'uml:Association':
                ends = self.asociaciones.setdefault(e.get(XID), set())
                ends.update((e.get('memberEnd') or '').split())
                for p in e:
                    if local(p.tag) == 'memberEnd' and p.get(XIDREF):
                        ends.add(p.get(XIDREF))
                    elif local(p.tag) == 'ownedEnd':
                        info = self.prop(p)
                        info['asociacion'] = info['asociacion'] or e.get(XID)
                        self.props[p.get(XID)] = info
        # memberEnd puede faltar o venir como hijos: cada extremo también declara
        # su asociación, así que el mapa se completa desde las propiedades.
        for pid, info in self.props.items():
            if info['asociacion']:
                self.asociaciones.setdefault(info['asociacion'], set()).add(pid)
        for c in self.clases.values():
            c['supers'] = [self.nombre.get(s, s) for s in c['supers']]
        self._todas = {}

    def prop(self, p):
        tipo = ref_de(p, 'type')
        return {'id': p.get(XID), 'name': p.get('name'), 'tipo': tipo,
                'compuesta': p.get('aggregation') == 'composite',
                'derivada': p.get('isDerived') == 'true' or p.get('isDerivedUnion') == 'true',
                'lower': valor_literal(p, 'lowerValue', 1), 'upper': valor_literal(p, 'upperValue', 1),
                'asociacion': ref_de(p, 'association'),
                'defecto': any(local(h.tag) == 'defaultValue' for h in p)}

    def tipo_nombre(self, prop):
        return self.nombre.get(prop['tipo'], prop['tipo'])

    def todas(self, clase):
        if clase not in self._todas:
            out = {}
            for s in self.clases[clase]['supers']:
                if s in self.clases:
                    out.update(self.todas(s))
            out.update(self.clases[clase]['props'])
            self._todas[clase] = out
        return self._todas[clase]

    def conforma(self, clase, tipo):
        if clase == tipo:
            return True
        return any(self.conforma(s, tipo) for s in self.clases.get(clase, {}).get('supers', []))

    def opuesta(self, prop):
        ends = self.asociaciones.get(prop['asociacion'], [])
        otras = [self.props.get(x) for x in ends if x != prop['id']]
        return otras[0] if otras and otras[0] else None


# ---------------------------------------------------------------- validación

def validar_metamodelo(mm, doc_path):
    raiz = parse_xmi(doc_path)
    tipos_por_id = {}
    for e in raiz.iter():
        if e.get(XID) and e.get(XT, '').startswith('uml:'):
            tipos_por_id[e.get(XID)] = e.get(XT)[4:]
    errores, avisos = [], []
    primitivos_omg = set()
    vistos = defaultdict(int)

    def err(e, msg):
        errores.append(f'[{e.get(XID) or local(e.tag)}] {msg}')

    def valor_ok(tipo, v):
        if tipo == 'Boolean':
            return v in ('true', 'false')
        if tipo == 'Integer':
            return v.lstrip('-').isdigit()
        if tipo == 'UnlimitedNatural':
            return v == '*' or v.isdigit()
        if tipo == 'Real':
            try:
                float(v)
                return True
            except ValueError:
                return False
        return True

    def revisar(e):
        meta = e.get(XT, '')[4:]
        vistos[meta] += 1
        if meta not in mm.clases:
            err(e, f'xmi:type uml:{meta} no es una metaclase de UML 2.5.1')
            return
        if mm.clases[meta]['abstract']:
            err(e, f'uml:{meta} es abstracta en UML 2.5.1')
        props = mm.todas(meta)
        cuenta = defaultdict(int)
        for k, v in e.attrib.items():
            if k.startswith('{') or k == 'href':
                continue
            p = props.get(k)
            if p is None:
                err(e, f'{meta} no tiene la propiedad "{k}"')
                continue
            if p['derivada']:
                avisos.append(f'[{e.get(XID)}] {meta}.{k} es derivada: no debería escribirse')
            tipo = mm.tipo_nombre(p)
            if tipo in mm.enums:
                if v not in mm.enums[tipo]:
                    err(e, f'{meta}.{k} = "{v}" no es un literal de {tipo}')
                cuenta[k] += 1
            elif tipo in mm.primitivos:
                if not valor_ok(tipo, v):
                    err(e, f'{meta}.{k} = "{v}" no es un {tipo} válido')
                cuenta[k] += 1
            else:
                if p['compuesta']:
                    avisos.append(f'[{e.get(XID)}] {meta}.{k} es compuesta pero se escribió como referencia')
                for idref in v.split():
                    cuenta[k] += 1
                    destino = tipos_por_id.get(idref)
                    if destino is None:
                        err(e, f'{meta}.{k} apunta a "{idref}", que no existe')
                    elif tipo in mm.clases and not mm.conforma(destino, tipo):
                        err(e, f'{meta}.{k} apunta a un {destino}; se esperaba {tipo}')
        for h in e:
            k = local(h.tag)
            p = props.get(k)
            if p is None:
                err(e, f'{meta} no tiene la propiedad "{k}"')
                continue
            cuenta[k] += 1
            tipo = mm.tipo_nombre(p)
            if h.get('href'):
                if 'PrimitiveTypes.xmi#' in h.get('href'):
                    primitivos_omg.add(h.get('href').rsplit('#', 1)[-1])
                continue
            if h.get(XIDREF):
                destino = tipos_por_id.get(h.get(XIDREF))
                if destino is None or (tipo in mm.clases and not mm.conforma(destino, tipo)):
                    err(e, f'{meta}.{k} apunta a "{h.get(XIDREF)}" inválido')
                continue
            if h.get(XT):
                if not p['compuesta']:
                    err(h, f'{meta}.{k} no es compuesta: no puede contener elementos')
                sub = h.get(XT)[4:]
                if tipo in mm.clases and sub in mm.clases and not mm.conforma(sub, tipo):
                    err(h, f'{meta}.{k} espera {tipo} y contiene un {sub}')
                revisar(h)
            elif tipo not in mm.primitivos and tipo not in mm.enums:
                err(h, f'{meta}.{k} espera un {tipo} y tiene un valor sin xmi:type')
        for k, p in props.items():
            n = cuenta.get(k, 0)
            if p['upper'] != '*' and n > p['upper']:
                err(e, f'{meta}.{k} admite {p["upper"]} valores y tiene {n}')
            if n == 0 and p['lower'] and p['lower'] >= 1 and not p['derivada'] and not p['defecto']:
                op = mm.opuesta(p)
                if op and op['compuesta']:
                    continue  # el contenedor la define (p. ej. Lifeline.interaction)
                err(e, f'{meta}.{k} es obligatoria ({p["lower"]}..{p["upper"]}) y falta')

    for e in raiz.iter():
        padre_uml = e.get(XT, '').startswith('uml:')
        if padre_uml and local(e.tag) in ('Model', 'Package'):
            revisar(e)
            break
    return errores, avisos, primitivos_omg, vistos


def validar_esquema(xsd, doc):
    """Devuelve (ok, errores, no_cubierto).

    XMI.xsd declara solo el espacio de nombres xmi: y deja el contenido en un
    comodín estricto. OMG no publica un XSD de UML 2.5.1, así que el error
    "No matching global element declaration" sobre un elemento uml: no es una
    falla del documento: ese contenido lo valida la sección 2 contra UML.xmi.
    """
    try:
        from lxml import etree
    except ImportError:
        return None, ['lxml no está instalado: no se validó contra XMI.xsd'], []
    try:
        schema = etree.XMLSchema(etree.parse(str(xsd)))
    except etree.XMLSchemaParseError as e:
        return None, [f'XMI.xsd no se pudo cargar como esquema: {e}'], []
    try:
        schema.validate(etree.parse(str(doc)))
    except etree.XMLSyntaxError as e:
        return False, [f'XML mal formado: {e}'], []
    errores, no_cubierto = [], []
    for x in schema.error_log:
        msg = f'línea {x.line}: {x.message}'
        if 'demanded by the strict wildcard' in x.message and f'{{{UML_URI}}}' in x.message:
            no_cubierto.append(msg)
        else:
            errores.append(msg)
    return not errores, errores, no_cubierto


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    doc = Path(args[0] if args else 'build/model.xmi')
    cache = Path(argv[argv.index('--cache') + 1]) if '--cache' in argv else Path.home() / '.cache/tpf-uca/omg'
    out = Path(argv[argv.index('--out') + 1]) if '--out' in argv else doc.parent / 'validacion-omg.md'
    md = ['# Validación contra los archivos normativos de OMG', '']
    try:
        info = descargar(cache)
    except Exception as e:  # noqa: BLE001
        md += [f'**No se pudieron obtener los archivos de OMG:** {e}', '',
               'Nada de esta sección quedó validado.']
        out.write_text('\n'.join(md) + '\n', encoding='utf-8')
        print(f'ERROR: no se pudieron obtener los archivos de OMG: {e}')
        return 1
    md += ['| Archivo | URL | SHA-256 | Bytes |', '|---|---|---|---|']
    md += [f'| {n} | {i["url"]} | `{i["sha256"]}` | {i["bytes"]} |' for n, i in info.items()]
    md.append('')

    ok_xsd, log_xsd, no_cubierto = validar_esquema(cache / 'XMI.xsd', doc)
    md += ['## 1. Esquema XMI 2.5.1 (XMI.xsd)', '']
    md.append('Envoltura XMI válida.' if ok_xsd else ('No válido.' if ok_xsd is False else 'No validado.'))
    md += [f'- {x}' for x in log_xsd[:50]] + ['']
    if no_cubierto:
        md += ['XMI.xsd no declara elementos de UML (OMG no publica un XSD de UML 2.5.1), '
               'así que el esquema no cubre el contenido del modelo; lo cubre la sección 2:', '']
        md += [f'- {x}' for x in no_cubierto[:5]] + ['']

    mm = Metamodelo(cache / 'UML.xmi')
    errores, avisos, prims, vistos = validar_metamodelo(mm, doc)
    prims_omg = Metamodelo(cache / 'PrimitiveTypes.xmi').primitivos
    for p in prims - prims_omg:
        errores.append(f'PrimitiveTypes.xmi#{p} no existe en PrimitiveTypes.xmi de OMG')
    md += ['## 2. Metamodelo UML 2.5.1 (UML.xmi)', '',
           f'{len(mm.clases)} metaclases leídas de UML.xmi. Elementos revisados: '
           f'{sum(vistos.values())} de {len(vistos)} metaclases. '
           f'**{len(errores)} errores, {len(avisos)} avisos.**', '']
    md += ['| Metaclase | Elementos |', '|---|---|']
    md += [f'| {k} | {v} |' for k, v in sorted(vistos.items())] + ['']
    if errores:
        md += ['### Errores', ''] + [f'- {x}' for x in errores[:300]] + ['']
    if avisos:
        md += ['### Avisos', ''] + [f'- {x}' for x in avisos[:300]] + ['']
    md += ['## No validado', '',
           '- Restricciones OCL de UML.xmi (las cubre en parte Eclipse UML2).',
           '- Semántica de los textos (guardas, cuerpos de OpaqueExpression y OpaqueBehavior).', '']
    out.write_text('\n'.join(md) + '\n', encoding='utf-8')
    fallo = errores or ok_xsd is False or ok_xsd is None
    print(f'OMG: esquema {"ok" if ok_xsd else "FALLA" if ok_xsd is False else "sin validar"}; '
          f'metamodelo: {len(errores)} errores, {len(avisos)} avisos → {out}')
    for x in log_xsd[:20]:
        print(f'  XSD {x}')
    tipos = Counter(re.sub(r'^\[[^]]*\] |"[^"]*"', '', x) for x in errores)
    for msg, n in tipos.most_common(30):
        print(f'  ERROR x{n}: {msg}')
    return 1 if fallo else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
