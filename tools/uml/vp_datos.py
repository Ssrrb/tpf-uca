#!/usr/bin/env python3
"""Datos para el plugin de VP que dibuja los diagramas de cada CU.

El XMI lleva el modelo, pero no el dibujo. El plugin (tools/uml/vp) lee este
JSON, busca en el proyecto de VP las clases importadas del XMI y arma los
diagramas de cada CU con la API de VP.

Uso: vp_datos.py [build/model.json] [--out build/vp-diagramas.json]
"""
import json
import re
import sys
from pathlib import Path


def de_archivo(srcs, archivo):
    return any(s.rsplit(':', 1)[0].endswith(archivo) for s in srcs)


def items(lista):
    out = []
    for it in lista:
        t = it['tipo']
        if t == 'message':
            out.append({'tipo': 'mensaje', 'de': it['from'], 'a': it['to'], 'clase': it['sort'],
                        'texto': it['texto'], 'operacion': it.get('operacion')})
        elif t == 'fragment':
            out.append({'tipo': 'fragmento', 'operador': it['operador'],
                        'operandos': [{'guarda': op.get('guarda'), 'items': items(op.get('items', []))}
                                      for op in it.get('operandos', [])]})
        elif t == 'ref':
            out.append({'tipo': 'ref', 'lifelines': it['lifelines'], 'texto': it['texto']})
        elif t == 'comment':
            out.append({'tipo': 'nota', 'texto': it['texto'], 'anota': it.get('anota', []),
                        'divisor': bool(it.get('divisor'))})
    return out


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    out = Path(argv[argv.index('--out') + 1]) if '--out' in argv else Path('build/vp-diagramas.json')
    if '--out' in argv:
        args.remove(str(out))
    d = json.loads(Path(args[0] if args else 'build/model.json').read_text(encoding='utf-8'))
    cus = sorted({i['cu'] for i in d['interacciones']} | {a['cu'] for a in d['actividades']} |
                 {m['cu'] for m in d['maquinas_de_estados']} |
                 {re.search(r'CU-\d+', s).group(0) for c in d['clasificadores'] for s in c['srcs']
                  if re.search(r'CU-\d+-clases', s)})
    datos = {'formato': 2, 'cus': []}
    for cu in cus:
        archivo = f'{cu}-clases.puml'
        clases = [{'nombre': c['name'], 'tipo': c['kind'], 'paquete': c['package']}
                  for c in d['clasificadores'] if de_archivo(c['srcs'], archivo)]
        rels = [{'tipo': r['kind'], 'a': r['a'], 'b': r['b'], 'nombre': r.get('label')}
                for r in d['relaciones'] if de_archivo(r['srcs'], archivo)]
        secs = [{'nombre': i['name'], 'titulo': i.get('titulo'),
                 'lifelines': [{'alias': l['alias'], 'nombre': l['label'].split(':')[0].strip()
                                if not l.get('es_actor') else l['label'],
                                'tipo': l.get('tipo_ref'), 'actor': bool(l.get('es_actor'))}
                               for l in i['lifelines']],
                 'items': items(i['items'])}
                for i in d['interacciones'] if i['cu'] == cu]
        acts = [{'nombre': a['name'], 'titulo': a.get('titulo'), 'particiones': a['particiones'],
                 'nodos': [{'id': n['id'], 'tipo': n['kind'], 'nombre': n.get('name'), 'particion': n.get('particion')}
                           for n in a['nodos']],
                 'flujos': [{'de': f['from'], 'a': f['to'], 'guarda': f.get('guarda')} for f in a['flujos']]}
                for a in d['actividades'] if a['cu'] == cu]
        datos['cus'].append({'cu': cu, 'clases': clases, 'relaciones': rels, 'secuencias': secs,
                             'actividades': acts})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'VP: {len(datos["cus"])} CUs → {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
