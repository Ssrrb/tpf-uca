#!/usr/bin/env python3
"""Pasos 4 y 5 del pipeline: .puml → build/model.json + build/report.md.

Parsea los diagramas de CU-01 en adelante (CU-00 queda fuera del modelo),
los une en un modelo único, corre los checks de consistencia y escribe el
reporte. Sale con 1 si hay errores.

Uso: modelo.py [directorio] [--out build] [--xmi] [--gh] [--incluir-cu00]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from uml import checks  # noqa: E402
from uml.model import Modelo  # noqa: E402
from uml.parser import Problemas, parse_diagrama  # noqa: E402


def construir(directorio, raiz='.', incluir_cu00=False):
    problemas = Problemas()
    archivos = sorted(Path(directorio).rglob('*.puml'))
    archivos = [f for f in archivos if f.name.startswith('CU-') and
                (incluir_cu00 or not f.name.startswith('CU-00'))]
    diagramas = [parse_diagrama(f, raiz, problemas) for f in archivos]
    modelo = Modelo(problemas)
    orden = {'clases': 0, 'secuencia': 1, 'estados': 2, 'actividades': 3}
    for d in sorted(diagramas, key=lambda d: orden.get(d['tipo'], 9)):
        if d['tipo'] == 'clases':
            modelo.agregar_clases(d)
    modelo.resolver_relaciones()
    modelo.tipar()
    for d in diagramas:
        if d['tipo'] == 'secuencia':
            modelo.agregar_secuencia(d)
        elif d['tipo'] == 'estados':
            modelo.agregar_estados(d)
        elif d['tipo'] == 'actividades':
            modelo.agregar_actividades(d)
    modelo.resolver_refs()
    checks.nombres(modelo, problemas)
    return modelo, problemas, archivos


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    out = Path('build')
    if '--out' in argv:
        out = Path(argv[argv.index('--out') + 1])
        args.remove(str(out))
    directorio = args[0] if args else 'diagramas'
    modelo, problemas, archivos = construir(directorio, incluir_cu00='--incluir-cu00' in argv)
    datos = modelo.a_json()
    datos['fuentes'] = [str(f) for f in archivos]
    datos['problemas'] = problemas.lista
    out.mkdir(parents=True, exist_ok=True)
    (out / 'model.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding='utf-8')
    resumen = {
        'Diagramas': len(archivos),
        'Clasificadores': len(datos['clasificadores']),
        'Tipos generados (R2, R3)': len(datos['tipos']),
        'Actores': len(datos['actores']),
        'Relaciones': len(datos['relaciones']),
        'Interacciones': len(datos['interacciones']),
        'Máquinas de estados': len(datos['maquinas_de_estados']),
        'Actividades': len(datos['actividades']),
    }
    if '--xmi' in argv:
        from uml import xmi
        texto, gen = xmi.generar(datos)
        (out / 'model.xmi').write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + texto + '\n',
                                       encoding='utf-8')
        resumen['XMI'] = f'{out}/model.xmi ({len(gen.ids)} elementos con xmi:id)'
    md, errores = checks.reporte(problemas.lista, resumen)
    (out / 'report.md').write_text(md, encoding='utf-8')
    if '--gh' in argv:
        for p in problemas.lista:
            if p['nivel'] in ('error', 'aviso'):
                archivo, _, linea = p['src'].partition(':')
                nivel = 'error' if p['nivel'] == 'error' else 'warning'
                print(f'::{nivel} file={archivo},line={linea or 1}::{p["codigo"]} {p["msg"]}')
    avisos = sum(1 for p in problemas.lista if p['nivel'] == 'aviso')
    print(f'Modelo: {len(archivos)} diagramas → {out}/model.json; {errores} errores, '
          f'{avisos} avisos → {out}/report.md')
    return 1 if errores else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
