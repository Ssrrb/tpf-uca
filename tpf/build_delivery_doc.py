#!/usr/bin/env python3
"""Construye el documento de entrega del TPF G11 en formato de la plantilla."""

from __future__ import annotations

import csv
import importlib.util
import shutil
import subprocess
import zipfile
from xml.etree import ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TPF = ROOT / "tpf"
DIAG = TPF / "diagramas"
G11 = ROOT / "G11.tsv"
TEMPLATE = TPF / "Sebas Rojas - Is1 TPF Documentación.docx"
OUT_MD = TPF / "informe-final-g11-entrega.md"
OUT_DOCX = TPF / "Sebas Rojas - Is1 TPF Documentación - G11 completo.docx"
MEDIA = TPF / "_delivery_media"
PAGE_BREAK = """```{=openxml}
<w:p><w:r><w:br w:type="page" /></w:r></w:p>
```"""


FUNCTIONAL_REQUIREMENTS = [
    ("RF-01", "El sistema debe permitir a la Comisión de TFG registrar el semestre de TFG con sus fechas claves: reunión inicial, fecha tope de inscripción de grupos, publicación de tutores y fecha límite de entrega del anteproyecto.", "Minuta 01"),
    ("RF-02", "El estudiante debe poder registrar la inscripción de su grupo indicando nombre tentativo del tema, integrantes y datos de contacto.", "Minuta 02"),
    ("RF-03", "El sistema debe validar que un estudiante no pueda pertenecer a más de un grupo de TFG en el mismo semestre.", "Minuta 02"),
    ("RF-04", "La Comisión de TFG debe poder consultar la lista de grupos inscriptos con estado de completitud y cantidad de integrantes.", "Minuta 03"),
    ("RF-05", "La Comisión de TFG debe poder asignar un tutor a cada grupo inscripto antes de la fecha de publicación definida.", "Minuta 03"),
    ("RF-06", "El sistema debe permitir publicar la asignación de tutor y notificar al grupo correspondiente.", "Minuta 03"),
    ("RF-07", "El grupo debe poder cargar una versión preliminar del anteproyecto con título, problema, objetivo general y alcance.", "Minuta 04"),
    ("RF-08", "El tutor debe poder registrar observaciones sobre el avance del anteproyecto durante el período de elaboración.", "Minuta 05"),
    ("RF-09", "El grupo debe poder entregar formalmente el anteproyecto antes de la fecha límite establecida por la Comisión.", "Minuta 06"),
    ("RF-10", "El sistema debe cambiar el estado del grupo según el avance de la primera etapa: pendiente de inscripción, inscripto, tutor asignado, en elaboración de anteproyecto, anteproyecto entregado.", "Minuta 06"),
    ("RF-11", "El estudiante debe poder consultar en cualquier momento el estado de su grupo, tutor asignado, fechas clave y observaciones registradas.", "Minuta 05"),
    ("RF-12", "La Comisión de TFG debe poder generar un listado de grupos que aún no entregaron su anteproyecto al acercarse la fecha límite.", "Minuta 06"),
]

NON_FUNCTIONAL_REQUIREMENTS = [
    ("RNF-01", "La interfaz debe presentar de forma clara las etapas y fechas clave del proceso inicial del TFG.", "Minuta 01"),
    ("RNF-02", "El sistema debe ser accesible vía web desde dispositivos de escritorio y móviles.", "Minuta 02"),
    ("RNF-03", "Solo la Comisión de TFG puede modificar fechas del semestre y asignaciones de tutores.", "Minuta 03"),
    ("RNF-04", "El sistema debe registrar fecha y usuario responsable en las acciones de inscripción, asignación, observación y entrega.", "Minuta 05"),
    ("RNF-05", "La entrega del anteproyecto debe quedar bloqueada automáticamente una vez vencida la fecha límite, salvo habilitación expresa de la Comisión.", "Minuta 06"),
    ("RNF-06", "Los estudiantes solo deben poder consultar la información de su propio grupo, mientras que la Comisión puede consultar todos los grupos del semestre.", "Minuta 03 / Minuta 05"),
]

ACTORS = [
    ("Estudiante", "Actor principal que inscribe el grupo, carga la versión preliminar, entrega el anteproyecto y consulta estado, tutor, fechas clave y observaciones de su propio grupo."),
    ("Comisión de TFG", "Actor principal responsable de configurar el semestre, consultar grupos, asignar tutores, publicar asignaciones y generar listados de grupos sin entrega."),
    ("Tutor", "Actor principal que registra observaciones sobre los grupos asignados durante la elaboración del anteproyecto."),
    ("Secretaría Académica", "Actor de contexto oficial relacionado con la inscripción académica; no posee requerimientos funcionales de interacción directa con el sistema en esta iteración."),
]


def load_cus() -> list[dict]:
    spec = importlib.util.spec_from_file_location("generate_artifacts", DIAG / "generate_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.CUS


def copy_logo() -> Path:
    MEDIA.mkdir(exist_ok=True)
    logo = MEDIA / "template-logo.png"
    if not logo.exists():
        with zipfile.ZipFile(TEMPLATE) as docx:
            logo.write_bytes(docx.read("word/media/image1.png"))
    return logo


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(cell.replace("\n", "<br>") for cell in row) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def requirement_table(items: list[tuple[str, str, str]]) -> str:
    return md_table(["ID", "Requerimiento", "Minuta asociada"], [list(item) for item in items])


def use_case_index(cus: list[dict]) -> str:
    rows = [[f"CU-{cu['n']}", cu["title"], cu["actor"], f"{cu['rf']}; {cu['rnf']}"] for cu in cus]
    return md_table(["ID", "Caso de uso", "Actor principal", "Requerimiento(s)"], rows)


def use_case_spec(cu: dict) -> str:
    flow_rows = []
    for idx, step in enumerate(cu["normal"], 1):
        if idx in (1, 3):
            actor_action = step
            system_response = ""
        else:
            actor_action = ""
            system_response = step
        flow_rows.append([str(idx), actor_action, system_response])
    return "\n\n".join(
        [
            md_table(
                ["Campo", "Detalle"],
                [
                    ["Nombre Caso de Uso", f"CU-{cu['n']} {cu['title']}"],
                    ["Versión", "1.0"],
                    ["Creado por", "Sebas Rojas - Grupo G11"],
                    ["Fecha", "junio 2026"],
                    ["Modificado por", "Sebas Rojas - Grupo G11"],
                    ["Fecha", "junio 2026"],
                    ["Descripción", f"Permite ejecutar el proceso de {cu['title'].lower()} dentro de la primera etapa del TFG."],
                    ["Requerimiento(s) a que responde", f"{cu['rf']}; {cu['rnf']}"],
                    ["Actores", cu["actor"]],
                    ["Pre Condiciones", "El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita."],
                    ["Pos Condiciones", "Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG."],
                ],
            ),
            "**Flujo Normal**",
            md_table(["Paso", "Actor - Acción", "Respuesta del Sistema"], flow_rows),
            "**Excepciones**",
            "\n".join(f"- {alt}" for alt in cu["alts"]),
        ]
    )


def matrix(cus: list[dict]) -> str:
    reqs = [item[0] for item in FUNCTIONAL_REQUIREMENTS + NON_FUNCTIONAL_REQUIREMENTS]
    headers = ["Requerimiento"] + [f"CU-{cu['n']}" for cu in cus]
    rows = []
    for req in reqs:
        row = [req]
        for cu in cus:
            row.append("●" if req in f"{cu['rf']}; {cu['rnf']}" else "")
        rows.append(row)
    return md_table(headers, rows)


def read_microstudy() -> tuple[str, str]:
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
                missing.append(str(idx))
                continue
            try:
                value = int(raw)
            except ValueError:
                invalid.append(f"{idx}={raw}")
                continue
            if value < 1 or value > 5:
                invalid.append(f"{idx}={raw}")
                continue
            values.append(value)
        stats[item] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "freq": [values.count(v) for v in range(1, 6)],
        }
        issues[item] = {
            "missing": ", ".join(missing) if missing else "ninguno",
            "invalid": ", ".join(invalid) if invalid else "ninguno",
        }
    periods: dict[str, int] = {}
    comments = []
    for row in rows:
        periods[row["Período"]] = periods.get(row["Período"], 0) + 1
        comment = (row.get("Comentario.") or "").strip()
        if comment:
            comments.append(comment)
    data_rows = [[item, issues[item]["missing"], issues[item]["invalid"]] for item in ["P1", "P2", "P3", "P4"]]
    stat_rows = [
        [item, f"{stats[item]['mean']:.2f}", str(stats[item]["min"]), str(stats[item]["max"]), *map(str, stats[item]["freq"])]
        for item in ["P1", "P2", "P3", "P4"]
    ]
    prep = (
        f"El subconjunto `G11.tsv` contiene {len(rows)} casos anonimizados. "
        f"Distribución por período: {', '.join(f'{k}: {v}' for k, v in sorted(periods.items()))}.\n\n"
        + md_table(["Ítem", "Faltantes", "Inválidos"], data_rows)
    )
    results = "\n\n".join(
        [
            md_table(["Ítem", "Media", "Mínimo", "Máximo", "Frec. 1", "Frec. 2", "Frec. 3", "Frec. 4", "Frec. 5"], stat_rows),
            f"La claridad percibida es alta en el subconjunto analizado. Las medias observadas van de {min(s['mean'] for s in stats.values()):.2f} a {max(s['mean'] for s in stats.values()):.2f}. P4, claridad del flujo completo, presenta la media más baja relativa ({stats['P4']['mean']:.2f}), aunque su mínimo observado es 4.",
            "Comentarios preservados: " + " / ".join(f'"{comment}"' for comment in comments),
            "Advertencia metodológica: este microestudio tiene carácter formativo, descriptivo y exploratorio. Los datos analizados corresponden únicamente al subconjunto G11 asignado por la cátedra y no necesariamente representan a toda la población de estudiantes de TFG.",
        ]
    )
    return prep, results


def diagram_section(cu: dict) -> str:
    base = f"{cu['n']}-{cu['id']}"
    return "\n\n".join(
        [
            f"## Caso de Uso CU-{cu['n']} {cu['title']}",
            "### Especificación Caso de Uso",
            use_case_spec(cu),
            "### Diagrama de Clases del Caso de Uso",
            f"![](diagramas/{base}-clases-analisis.svg)",
            "### Diagrama de Interacción del Caso de Uso",
            f"![](diagramas/{base}-secuencia.svg)",
        ]
    )


def build_markdown() -> str:
    cus = load_cus()
    logo = copy_logo()
    micro_prep, micro_results = read_microstudy()
    actor_table = md_table(["Actor", "Descripción"], [list(actor) for actor in ACTORS])
    toc = "\n".join(
        [
            "**Contenido**",
            "",
            "- Modelo de Análisis",
            "  - Requerimientos",
            "  - Identificación de Actores",
            "  - Diagrama de Casos de Uso",
            "  - Casos de Uso",
            "  - Matriz de Requerimientos vs Casos de Uso",
            "  - Microestudio formativo",
            "- Modelo de Diseño",
            "  - Diagrama de Estados",
            "  - Diagrama de Actividades",
            "  - Diagrama de Clases Persistentes",
            "  - Diagrama de Entidad Relación",
            "- Referencias",
        ]
    )
    use_case_sections = "\n\n".join(diagram_section(cu) for cu in cus)
    return f"""---
lang: es-PY
---

![]({logo.relative_to(TPF)}){{width=1.703in height=1.646in}}

Facultad de Ciencias y Tecnología

Carrera de Análisis de Sistemas Informáticos

Ingeniería del Software 1

**Trabajo Práctico Final**

Autor/es

Sebas Rojas - Grupo G11

Profesor

Dr. Emilio Gutiérrez

Asunción - Paraguay

junio 2026

{PAGE_BREAK}

{toc}

{PAGE_BREAK}

# Modelo de Análisis

El sistema modelado cubre la primera etapa del Trabajo Final de Grado de la Licenciatura en Análisis de Sistemas Informáticos de la Universidad Católica de Asunción: apertura del semestre, inscripción de grupos, asignación y publicación de tutores, elaboración inicial y entrega formal del anteproyecto. Quedan fuera del alcance el dictamen, la defensa y el cierre del TFG.

## Requerimientos

### Requerimientos Funcionales

{requirement_table(FUNCTIONAL_REQUIREMENTS)}

### Requerimientos No Funcionales

{requirement_table(NON_FUNCTIONAL_REQUIREMENTS)}

## Identificación de Actores

{actor_table}

## Diagrama de Casos de Uso

### Sistema web de gestión de la primera etapa del TFG

![](diagramas/01-casos-de-uso-general.svg)

## Casos de uso identificados

{use_case_index(cus)}

{use_case_sections}

{PAGE_BREAK}

## Matriz de Requerimientos vs Casos de Uso

{matrix(cus)}

{PAGE_BREAK}

## Microestudio formativo

### Preparación de datos

{micro_prep}

### Resultados y decisiones de análisis

{micro_results}

# Modelo de Diseño

## Diagrama de Estados

![](diagramas/22-estados-grupo-tfg.svg)

## Diagrama de Actividades del Proceso Inicial del TFG

![](diagramas/25-actividades-proceso-inicial-tfg.svg)

## Diagrama de Clases Persistentes

![](diagramas/23-clases-persistentes.svg)

## Diagrama de Entidad Relación

![](diagramas/24-entidad-relacion.svg)

# Referencias

- Cátedra de Ingeniería del Software 1. (2026). *Trabajo Práctico Final 2026: Especificaciones del caso de estudio, anexos y rúbrica*.
- Cátedra de Ingeniería del Software 1. (2026). *Materiales de clase sobre diagramas de clases, interacción y estados UML*.
- Grupo G11. (2026). *Subconjunto de datos anónimo G11.tsv para microestudio formativo*.
"""


def main() -> None:
    OUT_MD.write_text(build_markdown(), encoding="utf-8")
    subprocess.run(
        [
            "pandoc",
            str(OUT_MD.name),
            "--from",
            "markdown",
            "--reference-doc",
            str(TEMPLATE.name),
            "--resource-path",
            ".:..",
            "-o",
            str(OUT_DOCX.name),
        ],
        cwd=TPF,
        check=True,
    )
    center_cover_page()


def center_cover_page() -> None:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    ET.register_namespace("w", ns["w"])
    tmp = OUT_DOCX.with_suffix(".tmp.docx")
    with zipfile.ZipFile(OUT_DOCX, "r") as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                root = ET.fromstring(data)
                body = root.find("w:body", ns)
                assert body is not None
                for paragraph in body.findall("w:p", ns):
                    ppr = paragraph.find("w:pPr", ns)
                    if ppr is None:
                        ppr = ET.Element(f"{{{ns['w']}}}pPr")
                        paragraph.insert(0, ppr)
                    jc = ppr.find("w:jc", ns)
                    if jc is None:
                        jc = ET.SubElement(ppr, f"{{{ns['w']}}}jc")
                    jc.set(f"{{{ns['w']}}}val", "center")
                    if paragraph.find(".//w:br[@w:type='page']", ns) is not None:
                        break
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            dst.writestr(item, data)
    shutil.move(tmp, OUT_DOCX)


if __name__ == "__main__":
    main()
