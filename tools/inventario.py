#!/usr/bin/env python3
"""Paso 1 del pipeline UML 2.5.1: inventario de los .puml.

Clasifica cada diagrama por tipo (por el contenido, y lo compara con el sufijo
del nombre) y cuenta sus elementos con expresiones regulares simples. Es un
conteo orientativo: el modelo exacto lo arma tools/uml/parser.py (paso 4).

Uso: inventario.py [directorio] [--out build/inventory.md]
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

TIPOS_NOMBRE = {
    'casos-de-uso': 'casos de uso', 'generalizacion-actores': 'casos de uso',
    'clases': 'clase', 'secuencia': 'secuencia', 'estados': 'estados',
    'actividades': 'actividad', 'paquetes': 'paquetes',
    'componentes': 'componentes', 'despliegue': 'despliegue',
}

ID = r'(?:"[^"]*"|[\w.]+)'
PATRONES = {
    'clase': {
        'clases': r'^\s*(?:abstract\s+)?class\s',
        'clases abstractas': r'^\s*abstract\s+(?:class\s)?',
        'interfaces': r'^\s*interface\s',
        'enumeraciones': r'^\s*enum\s',
        'paquetes': r'^\s*package\s',
        'relaciones': rf'^\s*{ID}\s*("[^"]*")?\s*[<|*o]*[-.]{{1,2}}[|>*o]*\s*("[^"]*")?\s*{ID}',
        'notas': r'^\s*note\s',
    },
    'secuencia': {
        'actores': r'^\s*actor\s',
        'lifelines': r'^\s*(participant|actor|boundary|control|entity|database|collections|queue)\s',
        'mensajes': rf'^\s*{ID}\s*[-<]?-{{1,2}}>{{1,2}}\s*{ID}\s*:',
        'creaciones': r'^\s*create\s',
        'fragmentos': r'^\s*(alt|opt|loop|par|break|critical|group)\b',
        'ref (InteractionUse)': r'^\s*ref\s+over\b',
        'box': r'^\s*box\b',
        'notas': r'^\s*note\s',
    },
    'casos de uso': {
        'actores': r'^\s*actor\s',
        'casos de uso': r'^\s*usecase\s',
        'sujetos': r'^\s*rectangle\s',
        'paquetes': r'^\s*package\s',
        'asociaciones': rf'^\s*{ID}\s*--\s*{ID}\s*$',
        'include/extend': r'<<(include|extend)>>',
        'generalizaciones': r'<\|--|--\|>',
        'notas': r'^\s*note\s',
    },
    'estados': {
        'estados': r'^\s*state\s',
        'pseudoestados choice': r'<<choice>>',
        'transiciones': r'-->',
        'notas': r'^\s*note\s',
    },
    'actividad': {
        'acciones': r'^\s*:',
        'particiones': r'^\s*\|[^|]+\|\s*$',
        'decisiones': r'^\s*(if|elseif|repeat while|while)\b',
        'fork': r'^\s*fork\b(?!\s+again)',
        'nodos finales': r'^\s*(stop|end)\s*$',
        'notas': r'^\s*note\s',
    },
    'paquetes': {
        'paquetes': r'^\s*(package|folder|frame)\s',
        'dependencias': r'\.\.>',
        'notas': r'^\s*note\s',
    },
}


def tipo_por_contenido(texto):
    lineas = texto.splitlines()
    if any(re.match(r'^\s*(start|stop|:.*;)\s*$', l) for l in lineas) or any(
            re.match(r'^\s*\|[^|]+\|', l) for l in lineas):
        return 'actividad'
    if any(re.match(r'^\s*usecase\s', l) for l in lineas) or (
            any(re.match(r'^\s*actor\s', l) for l in lineas)
            and not any(re.match(r'^\s*participant\s', l) for l in lineas)):
        return 'casos de uso'
    if any(re.match(r'^\s*(participant|box)\b', l) for l in lineas):
        return 'secuencia'
    if any(re.match(r'^\s*state\s|^\s*\[\*\]', l) for l in lineas):
        return 'estados'
    if any(re.match(r'^\s*(abstract\s+)?(class|interface|enum)\s', l) for l in lineas):
        return 'clase'
    if any(re.match(r'^\s*package\s', l) for l in lineas):
        return 'paquetes'
    if any(re.match(r'^\s*component\s', l) for l in lineas):
        return 'componentes'
    if any(re.match(r'^\s*node\s', l) for l in lineas):
        return 'despliegue'
    return 'desconocido'


def tipo_por_nombre(nombre):
    for clave, tipo in TIPOS_NOMBRE.items():
        if f'-{clave}' in nombre:
            return tipo
    return 'desconocido'


def contar(texto, tipo):
    sin_skin = re.sub(r'skinparam\s+\w+\s*\{[^}]*\}', '', texto)
    lineas = [l for l in sin_skin.splitlines()
              if not l.strip().startswith(("'", 'skinparam', '!', 'hide', 'title'))]
    return {k: sum(1 for l in lineas if re.search(p, l))
            for k, p in PATRONES.get(tipo, {}).items()}


def version_plantuml():
    try:
        out = subprocess.run(['plantuml', '-version'], capture_output=True, text=True,
                             timeout=60).stdout
        return out.splitlines()[0] if out else 'no disponible'
    except (OSError, subprocess.TimeoutExpired):
        return 'no disponible'


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    out = Path(argv[argv.index('--out') + 1]) if '--out' in argv else Path('build/inventory.md')
    if '--out' in argv:
        args.remove(str(out))
    raiz = Path(args[0] if args else 'diagramas')
    archivos = sorted(raiz.rglob('*.puml'))
    filas, por_tipo, discrepancias = [], Counter(), []
    for f in archivos:
        texto = f.read_text(encoding='utf-8')
        tc, tn = tipo_por_contenido(texto), tipo_por_nombre(f.name)
        if tc != tn:
            discrepancias.append(f'{f}: por nombre «{tn}», por contenido «{tc}»')
        por_tipo[tc] += 1
        conteo = contar(texto, tc)
        detalle = ', '.join(f'{k}: {v}' for k, v in conteo.items() if v)
        filas.append(f'| `{f}` | {tc} | {len(texto.splitlines())} | {detalle} |')

    ci = sorted(str(p) for p in Path('.github/workflows').glob('*.y*ml')) if Path('.github/workflows').is_dir() else []
    gitlab = Path('.gitlab-ci.yml').exists()
    fijada = re.search(r'PLANTUML_VERSION:\s*"([^"]+)"',
                       ''.join(Path(p).read_text() for p in ci)) if ci else None

    md = ['# Inventario de diagramas PlantUML', '',
          f'Generado por `tools/inventario.py` sobre `{raiz}/`. {len(archivos)} archivos `.puml`.', '',
          '## CI existente', '',
          f'- GitHub Actions: {", ".join(f"`{c}`" for c in ci) or "no hay"}',
          f'- GitLab CI: {"sí" if gitlab else "no hay"}',
          f'- PlantUML fijado en la CI: `{fijada.group(1) if fijada else "sin fijar"}` '
          '(descargado de GitHub Releases y verificado por SHA-256 en `.github/actions/plantuml`)',
          f'- PlantUML en esta ejecución: `{version_plantuml()}`', '',
          '## Totales por tipo', '', '| Tipo | Archivos |', '|---|---|']
    md += [f'| {t} | {n} |' for t, n in sorted(por_tipo.items())]
    for t in ('componentes', 'despliegue'):
        if t not in por_tipo:
            md.append(f'| {t} | 0 |')
    md += ['', '## Discrepancias nombre / contenido', '']
    md += [f'- {d}' for d in discrepancias] or ['Ninguna: el sufijo del nombre coincide con el contenido.']
    md += ['', '## Detalle', '',
           'Los conteos son por línea y orientativos (expresiones regulares); '
           'el conteo exacto sale de `build/model.json`.', '',
           '| Archivo | Tipo | Líneas | Elementos |', '|---|---|---|---|'] + filas
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(f'Inventario: {len(archivos)} archivos → {out}')


if __name__ == '__main__':
    main(sys.argv[1:])
