"""Checks de nombres sobre el modelo unido (C1 y C6) y el reporte.

Códigos
  P1  construcción no traducible a UML 2.5.1 (parser)
  C1  nombres duplicados o variantes de escritura de la misma entidad
  C2  la misma clase con tipo o paquete distinto en dos diagramas
  C3  lifeline sin clase o mensaje a una operación inexistente
  C4  referencia a un elemento no definido (tipo, relación, estado, ref)
  C5  multiplicidades o firmas incompatibles entre diagramas
  C6  convención de nombres: clases en PascalCase singular, atributos y
      operaciones en camelCase
  R4  (info) texto libre que se conserva como Comment
"""
import re
from collections import defaultdict

from .model import normalizar

LETRA_MAY = 'A-ZÁÉÍÓÚÑÜ'
LETRA_MIN = 'a-záéíóúñü'
PASCAL = re.compile(rf'^[{LETRA_MAY}][{LETRA_MAY}{LETRA_MIN}0-9]*$')
CAMEL = re.compile(rf'^[{LETRA_MIN}][{LETRA_MAY}{LETRA_MIN}0-9]*$')
# Palabras en singular que terminan en "s" (heurística del plural).
SINGULAR_EN_S = {'mes', 'ies', 'gas', 'análisis', 'analisis', 'tesis', 'crisis', 'pais', 'país',
                 'adendas', 'ajustes'}


def es_plural(nombre):
    ultima = re.findall(rf'[{LETRA_MAY}][{LETRA_MIN}0-9]*', nombre)
    ultima = (ultima[-1] if ultima else nombre).lower()
    primera = re.match(rf'^[{LETRA_MAY}][{LETRA_MIN}0-9]*', nombre)
    primera = primera.group(0).lower() if primera else nombre.lower()
    return any(p.endswith('s') and p not in SINGULAR_EN_S and len(p) > 3 for p in {primera})


def nombres(modelo, problemas):
    # C1: dos nombres distintos que se normalizan igual (tildes, mayúsculas, espacios).
    por_clave = defaultdict(set)
    for c in modelo.clasificadores.values():
        por_clave[normalizar(c['name'])].add((c['name'], c['srcs'][0]))
    for a in modelo.actores.values():
        por_clave[normalizar(a['name'])].add((a['name'], a['srcs'][0]))
    for variantes in por_clave.values():
        if len({v[0] for v in variantes}) > 1:
            v = sorted(variantes)
            problemas.agregar('C1', v[1][1], 'variantes del mismo nombre: ' +
                              ', '.join(f'{n} ({s})' for n, s in v))
    # C1: una etiqueta usada para dos clases distintas.
    for etiqueta, clases in modelo.etiquetas.items():
        if len(clases) > 1:
            src = modelo.clasificadores[sorted(clases)[0]]['srcs'][0]
            problemas.agregar('C1', src, f'la etiqueta "{etiqueta}" se usa para {", ".join(sorted(clases))}')
    # C1: una clase con dos etiquetas.
    for c in modelo.clasificadores.values():
        if len(c['labels']) > 1:
            problemas.agregar('C1', c['srcs'][0], f'{c["name"]} tiene varias etiquetas: '
                              + ', '.join(f'"{x}"' for x in c['labels']), nivel='aviso')
    # C1: atributos u operaciones de una clase que difieren solo en tildes o mayúsculas.
    for c in modelo.clasificadores.values():
        for grupo in ('atributos', 'operaciones'):
            claves = defaultdict(list)
            for m in c[grupo].values():
                claves[normalizar(m['name'])].append(m)
            for ms in claves.values():
                if len(ms) > 1:
                    problemas.agregar('C1', ms[1]['src'], f'{c["name"]}: '
                                      + ' y '.join(m['name'] for m in ms) + ' son variantes del mismo nombre')

    # C6: convenciones.
    for c in modelo.clasificadores.values():
        if not PASCAL.match(c['name']):
            problemas.agregar('C6', c['srcs'][0], f'clase "{c["name"]}" no está en PascalCase')
        elif c['kind'] != 'enum' and es_plural(c['name']):
            problemas.agregar('C6', c['srcs'][0], f'clase "{c["name"]}" parece plural', nivel='aviso')
        for a in c['atributos'].values():
            if not CAMEL.match(a['name']):
                problemas.agregar('C6', a['src'], f'atributo {c["name"]}.{a["name"]} no está en camelCase')
        for o in c['operaciones'].values():
            if not CAMEL.match(o['name']):
                problemas.agregar('C6', o['src'], f'operación {c["name"]}.{o["name"]}() no está en camelCase')


TITULOS = {
    'P1': 'Construcciones no traducibles a UML 2.5.1',
    'C1': 'Nombres duplicados o variantes de escritura',
    'C2': 'Misma clase con tipo o paquete distinto',
    'C3': 'Lifelines y mensajes sin clase u operación',
    'C4': 'Referencias a elementos no definidos',
    'C5': 'Multiplicidades, tipos o firmas incompatibles',
    'C6': 'Convención de nombres',
    'R4': 'Texto libre conservado como Comment',
    'P2': 'Fuera de alcance',
}


def reporte(problemas, resumen):
    errores = [p for p in problemas if p['nivel'] == 'error']
    avisos = [p for p in problemas if p['nivel'] == 'aviso']
    md = ['# Reporte del modelo UML', '',
          f'**{len(errores)} errores, {len(avisos)} avisos.** '
          + ('El build falla.' if errores else 'Sin errores.'), '']
    md += [f'- {k}: {v}' for k, v in resumen.items()]
    md.append('')
    por_codigo = defaultdict(list)
    for p in problemas:
        por_codigo[p['codigo']].append(p)
    for codigo in TITULOS:
        ps = por_codigo.get(codigo)
        if not ps:
            continue
        md += [f'## {codigo} · {TITULOS[codigo]} ({len(ps)})', '',
               '| Nivel | Dónde | Detalle |', '|---|---|---|']
        for p in sorted(ps, key=lambda x: (x['nivel'] != 'error', orden_src(x['src']))):
            md.append(f'| {p["nivel"]} | `{p["src"]}` | {p["msg"].replace("|", "∣")} |')
        md.append('')
    return '\n'.join(md) + '\n', len(errores)


def orden_src(src):
    archivo, _, linea = src.partition(':')
    return archivo, int(linea) if linea.isdigit() else 0
