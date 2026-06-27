# Repository Guidelines

## Project Structure

- `indicaciones-tpf/`: official assignment, case study, annexes, and rubric. Treat these files as the requirements source of truth.
- `fuentes/`: course references for class, interaction, and state diagrams.
- `G11.tsv`: the only dataset permitted for the formative microstudy.
- `tpf/Sebas Rojas - Is1 TPF Documentación.docx`: required final-document template.
- `tpf/diagramas/overarch/models/`: canonical EDN model for requirements and UML elements.
- `tpf/diagramas/*.puml` and `*.svg`: publication views and rendered assets.
- `TODO.md`: delivery checklist for the 24 required diagrams.

Do not modify `download_obsidian.py`, generated Overarch output, or downloaded course material.

## Required Workflow

Work in this order: official minutes and requirements → use-case specifications → canonical Overarch model → UML views → microstudy → consistency review → final document.

Maintain traceability through `Minuta → RF/RNF → CU → BCE classes → sequence → state/design model`. Do not add actors, requirements, states, or findings absent from official sources.

Edit shared elements in `tpf/diagramas/overarch/models/` first. Keep namespaced IDs stable; update every reference when an ID changes. Overarch does not generate sequence diagrams, so maintain those in PlantUML and annotate calls with `' op: :namespace/id` matching the receiving BCE operation.

## Validation and Rendering

Use the Overarch version in `tpf/diagramas/overarch/VERSION`. Configure `OVERARCH_JAR`, place the JAR under ignored `overarch/tools/`, or install `overarch`.

```bash
python3 tpf/diagramas/overarch/validate_sequence_refs.py
tpf/diagramas/overarch/render.sh
```

The first command checks sequence-operation references. The second validates EDN, writes ignored `overarch/generated/` views, and renders SVG when PlantUML is installed. Compare generated and publication `.puml` views before updating SVGs.

## Modeling and Data Conventions

Use Spanish domain names consistently. Name use cases with verb + noun and operations with verbs. Analysis classes follow BCE (`boundary`, `control`, `entity`) without implementation details. Sequence messages must match BCE operations; use `alt`, `opt`, or `loop` for alternatives.

For the microstudy, analyze only `G11.tsv`, report missing or invalid P1–P4 values, preserve anonymous quotations, and include the required limited-sample methodological warning. Never invent or supplement results with external data.

## Change Review

Keep commits focused and use imperative subjects, for example `model: add CU-03 BCE classes`. A pull request should identify affected RF/RNF and CU IDs, summarize model and document changes, report validation commands, and include updated SVGs when publication views change. Before delivery, verify all 18 requirements, 10 use cases, 24 diagrams, template order, index, author data, and APA references.

## Fuentes (documentación oficial)

| Documento | Ruta |
|-----------|------|
| Mapa de Contenido (índice) | `obsidian-export/Zk !MOC Ingeniería del Software 1 – TPF 2026.md` |
| Especificación del TPF | `obsidian-export/Zk Ingeniería del Software 1 – TPF 2026 – Especificaciones.md` |
| Caso de Estudio (RF, RNF, Minutas) | `obsidian-export/Zk IS1 TPF 2026 - Especificaciones del Caso de Estudio.md` |
| Anexo II — Microestudio | `obsidian-export/Zk IS1 TPF 2026 – Anexo II.md` |
| Anexo III — Rúbrica | `obsidian-export/Zk IS1 TPF 2026 – Anexo III.md` |
| Plantilla de formato | `tpf/Sebas Rojas - Is1 TPF Documentación.docx` |
| Dataset asignado | `G11.tsv` |