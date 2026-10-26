# Decisión: herramienta CASE del TPF

- **Fecha:** 25/10/2026
- **Estado:** Aprobada por agustin sebastian
- **Decisión:** se usa **PlantUML con su CLI** como herramienta CASE textual para todos los diagramas del Modelo de Análisis de Ctrl+.

## Por qué

PlantUML es la única herramienta evaluada que cumple a la vez las tres condiciones del grupo: es una CASE basada en texto o CLI, es fácil de instalar y trabaja con `.puml`.

- **Fácil de instalar:** un solo `.jar` con Java, o `brew install plantuml`, `apt install plantuml` o `winget`. Para el editor, la extensión PlantUML de VS Code.
- **Valida la sintaxis:** `plantuml -checkonly *.puml` revisa cada diagrama sin dibujarlo.
- **Exporta como una CASE:** además de PNG, SVG y PDF, exporta a **XMI** (`-txmi`, `-txmi:argo`, `-txmi:star`), el formato estándar de intercambio de modelos UML, que abren ArgoUML, StarUML y otras CASE.
- **Funciona con IA:** es texto plano y la IA lo escribe muy bien, porque es el formato UML con más ejemplos públicos.
- **Cumple lo que evalúa la cátedra:** la notación UML 2 de cada diagrama (flechas, multiplicidades, sintaxis de clases, secuencia, estados y actividades).

## Alternativas descartadas

| Herramienta | Motivo |
|---|---|
| kuml | No lee ni exporta `.puml`: usa su propio lenguaje en Kotlin. |
| Visual Paradigm Online | Es visual y demasiado engorrosa para el flujo del grupo. |
| Umple | Usa una sintaxis propia que no es compatible con PlantUML. |
| PlantUML + puml2code | El generador de código está abandonado desde 2022. |

## Convenciones

- Hay un archivo `.puml` por diagrama, con este nombre: `CU-XX-<tipo>[-n-<detalle>].puml`.
- Estilo: `!theme plain` con la paleta celeste del CU-01 y el CU-02 (`BackgroundColor #F5F8FA`, `BorderColor #17324D`, `HeaderBackgroundColor #EAF2F6`).
- Antes de pegar un diagrama en el documento: `plantuml -checkonly CU-*.puml`, sin errores.
- Los diagramas de clases necesitan Graphviz para dibujarse. Si no está instalado, se puede usar `-Playout=smetana`.
- `CU-04-clases.kuml.kts` queda solo como prueba de kuml y no forma parte de la entrega.
