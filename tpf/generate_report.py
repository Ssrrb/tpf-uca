#!/usr/bin/env python3
"""Genera el informe final del TPF G11 en Markdown."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TPF = ROOT / "tpf"
DIAG = TPF / "diagramas"
G11 = ROOT / "G11.tsv"


def load_cus():
    spec = importlib.util.spec_from_file_location("generate_artifacts", DIAG / "generate_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.CUS


def read_microstudy():
    with G11.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    stats = {}
    issues = {}
    for item in ["P1", "P2", "P3", "P4"]:
        values = []
        missing = []
        invalid = []
        for idx, row in enumerate(rows, 1):
            raw = (row.get(item) or "").strip()
            if not raw:
                missing.append(idx)
                continue
            try:
                value = int(raw)
            except ValueError:
                invalid.append((idx, raw))
                continue
            if value < 1 or value > 5:
                invalid.append((idx, raw))
                continue
            values.append(value)
        stats[item] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "freq": {v: values.count(v) for v in range(1, 6)},
        }
        issues[item] = {"missing": missing, "invalid": invalid}
    comments = [(row.get("Comentario.") or "").strip() for row in rows]
    comments = [comment for comment in comments if comment]
    periods = {}
    for row in rows:
        periods[row["Período"]] = periods.get(row["Período"], 0) + 1
    return rows, stats, issues, comments, periods


def diagram_markdown() -> str:
    diagrams = [
        ("01. Diagrama general de casos de uso", "01-casos-de-uso-general.svg"),
    ]
    for cu in load_cus():
        base = f"{cu['n']}-{cu['id']}"
        diagrams.append((f"{2 + (int(cu['n']) - 1) * 2:02d}. Diagrama de clases de análisis BCE de CU-{cu['n']}", f"{base}-clases-analisis.svg"))
        diagrams.append((f"{3 + (int(cu['n']) - 1) * 2:02d}. Diagrama de secuencia de CU-{cu['n']}", f"{base}-secuencia.svg"))
    diagrams.extend(
        [
            ("22. Diagrama de estados del grupo TFG", "22-estados-grupo-tfg.svg"),
            ("23. Diagrama de clases persistentes", "23-clases-persistentes.svg"),
            ("24. Diagrama entidad-relación", "24-entidad-relacion.svg"),
        ]
    )
    return "\n\n".join(f"### {title}\n\n![](diagramas/{file})" for title, file in diagrams)


def use_case_specs(cus) -> str:
    blocks = []
    for cu in cus:
        blocks.append(
            f"""### CU-{cu['n']} {cu['title']}

**Actor principal:** {cu['actor']}.  
**Trazabilidad:** {cu['rf']}; {cu['rnf']}; {cu['minuta']}.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

{chr(10).join(f'{idx}. {step}' for idx, step in enumerate(cu['normal'], 1))}

**Flujos alternativos**

{chr(10).join(f'- {alt}' for alt in cu['alts'])}
"""
        )
    return "\n".join(blocks)


def traceability(cus) -> str:
    reqs = [f"RF-{i:02d}" for i in range(1, 13)] + [f"RNF-{i:02d}" for i in range(1, 7)]
    rows = ["| Requerimiento | Casos de uso que lo cubren |", "|---|---|"]
    for req in reqs:
        covered = [f"CU-{cu['n']} {cu['title']}" for cu in cus if req in f"{cu['rf']}, {cu['rnf']}"]
        rows.append(f"| {req} | {', '.join(covered) if covered else 'Cobertura transversal documentada'} |")
    return "\n".join(rows)


def microstudy_section() -> str:
    rows, stats, issues, comments, periods = read_microstudy()
    prep = []
    for item, issue in issues.items():
        miss = "ninguno" if not issue["missing"] else ", ".join(map(str, issue["missing"]))
        inv = "ninguno" if not issue["invalid"] else ", ".join(f"{i}={v}" for i, v in issue["invalid"])
        prep.append(f"- {item}: faltantes {miss}; inválidos {inv}.")
    stat_rows = ["| Ítem | Media | Mínimo | Máximo | Frecuencia 1 | Frecuencia 2 | Frecuencia 3 | Frecuencia 4 | Frecuencia 5 |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for item in ["P1", "P2", "P3", "P4"]:
        s = stats[item]
        stat_rows.append(
            f"| {item} | {s['mean']:.2f} | {s['min']} | {s['max']} | {s['freq'][1]} | {s['freq'][2]} | {s['freq'][3]} | {s['freq'][4]} | {s['freq'][5]} |"
        )
    period_text = ", ".join(f"{period}: {count}" for period, count in sorted(periods.items()))
    return f"""## Microestudio formativo

### Preparación de datos

El subconjunto `G11.tsv` contiene {len(rows)} casos anonimizados. Distribución por período: {period_text}. La revisión de P1 a P4 encontró:

{chr(10).join(prep)}

### Resultados descriptivos

{chr(10).join(stat_rows)}

La claridad percibida es alta en el subconjunto analizado. P1, claridad de etapas, y P3, claridad de plazos y fechas clave, tienen las medias más altas ({stats['P1']['mean']:.2f} y {stats['P3']['mean']:.2f}). P4, claridad del flujo completo, presenta la media más baja ({stats['P4']['mean']:.2f}), aunque su mínimo observado es 4. P2, claridad de roles, queda en {stats['P2']['mean']:.2f}; no hay valores menores a 4.

### Lectura cualitativa mínima

Se registraron {len(comments)} comentarios abiertos. Los temas principales son:

- Predomina una percepción de claridad general: "Todo fue muy claro y voy avanzando bien con las reuniones con el tutor!" y "Se entendió bien todo."
- Las dudas se concentran en comunicación y disponibilidad de información de apoyo: un comentario menciona dificultad para encontrar documentaciones actualizadas sobre modelos de anteproyecto, y otro señala que "Sería oportuno mejorar la comunicación entre alumnos y tutores."

### Respuesta a la pregunta de investigación

A partir de los datos del subconjunto G11, los estudiantes perciben un nivel alto de claridad sobre etapas, roles y plazos de la fase inicial del TFG. La evidencia cuantitativa muestra medias entre {min(s['mean'] for s in stats.values()):.2f} y {max(s['mean'] for s in stats.values()):.2f}, con mínimos entre 3 y 4. La dimensión menos sólida es la comprensión del flujo completo, no por valores bajos, sino porque concentra más respuestas 4 que 5. La evidencia cualitativa no contradice esa lectura: aparecen comentarios de claridad general, junto con necesidades puntuales de mejor comunicación con tutores y mejor acceso a documentación actualizada.

### Advertencia metodológica obligatoria

Este microestudio tiene carácter formativo, descriptivo y exploratorio. Los datos analizados corresponden únicamente al subconjunto G11 asignado por la cátedra y no necesariamente representan a toda la población de estudiantes de TFG. Los resultados se presentan con fines pedagógicos y de apoyo al análisis del sistema. Cualquier generalización robusta requeriría un diseño muestral más riguroso, mayor tamaño de muestra y procedimientos analíticos adicionales.

### Decisiones de análisis justificadas por los hallazgos

1. Se conserva como central el CU-09 Consultar estado del grupo, con estado, tutor, fechas clave y observaciones en una sola vista. La decisión se apoya en que P4 es la dimensión con media más baja relativa y en comentarios que piden mejorar la comunicación entre alumnos y tutores.
2. Se explicita la publicación clara de cronograma en CU-01 y la consulta de fechas clave en CU-09. Aunque P3 es alta, el comentario sobre documentación no disponible muestra que la claridad depende de que los insumos estén centralizados y actualizados.
"""


def main() -> None:
    cus = load_cus()
    actors = "\n".join(
        [
            "- Estudiante: inscribe grupo, carga y entrega anteproyecto, consulta estado y observaciones.",
            "- Comisión de TFG: configura semestre, consulta grupos, asigna y publica tutores, controla grupos sin entrega.",
            "- Tutor: registra observaciones sobre grupos asignados.",
            "- Secretaría Académica: actor de contexto para inscripción académica; no tiene RF de interacción directa con el sistema en esta iteración.",
        ]
    )
    rules = "\n".join(
        [
            "- Cada grupo tiene entre 1 y 3 integrantes.",
            "- Un estudiante no puede pertenecer a más de un grupo de TFG en el mismo semestre.",
            "- Solo la Comisión modifica fechas del semestre y asignaciones de tutores.",
            "- Toda inscripción, asignación, observación y entrega registra fecha y usuario responsable.",
            "- La entrega queda bloqueada al vencer la fecha límite, salvo autorización expresa de la Comisión.",
            "- Los estudiantes solo consultan su propio grupo; la Comisión consulta todos los grupos del semestre.",
            "- El alcance termina con la entrega formal del anteproyecto; no incluye dictamen, defensa ni cierre.",
        ]
    )
    md = f"""---
title: "Sistema web de gestión de la primera etapa del TFG"
subtitle: "Trabajo Práctico Final - Ingeniería del Software 1"
author: "Sebas Rojas - Grupo G11"
lang: es-PY
---

# Sistema web de gestión de la primera etapa del TFG

## Alcance

El sistema modelado cubre la primera etapa del Trabajo Final de Grado de la Licenciatura en Análisis de Sistemas Informáticos de la Universidad Católica de Asunción: apertura del semestre, inscripción de grupos, asignación y publicación de tutores, elaboración inicial y entrega formal del anteproyecto. Quedan fuera del alcance el dictamen, la defensa y el cierre del TFG.

## Actores

{actors}

## Reglas de negocio

{rules}

## Casos de uso identificados

| ID | Caso de uso | Actor principal | Requerimientos |
|---|---|---|---|
{chr(10).join(f'| CU-{cu["n"]} | {cu["title"]} | {cu["actor"]} | {cu["rf"]}; {cu["rnf"]} |' for cu in cus)}

## Especificación textual de casos de uso

{use_case_specs(cus)}

## Matriz de trazabilidad requerimientos-casos de uso

{traceability(cus)}

{microstudy_section()}

## Diagramas UML

{diagram_markdown()}

## Consistencia entre modelos

Los diagramas mantienen la cadena de trazabilidad Minuta -> RF/RNF -> CU -> clases BCE -> secuencia -> estados/diseño. Las secuencias referencian operaciones canónicas mediante comentarios `op:` validados por `tpf/diagramas/overarch/validate_sequence_refs.py`. El estado del grupo usado en análisis y diseño respeta los cinco estados de RF-10 y no agrega estados de etapas posteriores.
"""
    (TPF / "informe-final-g11.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
