# Decisión: herramienta CASE del TPF

> **Actualización del 27/10/2026:** además de PlantUML se usa una CASE real,
> **Visual Paradigm** de escritorio. Ver la [segunda decisión](#decisión-2-visual-paradigm-como-case-real) al final.

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

## Decisión 2: Visual Paradigm como CASE real

- **Fecha:** 27/10/2026
- **Estado:** Aprobada por agustin sebastian
- **Decisión:** el modelo se lleva a **Visual Paradigm 18.1** (escritorio), que pasa a ser
  la CASE donde vive el modelo UML 2.5.1 y desde donde se exportan los diagramas de
  actividades, clases y secuencia. PlantUML sigue siendo el borrador y la fuente de verdad:
  los `.puml` se editan, la CI los valida y de ellos sale el XMI.

### Por qué

- **Repositorio de modelo:** VP guarda un modelo único donde la misma clase, operación o
  lifeline se reutiliza en todos los diagramas. PlantUML solo dibuja; el modelo único lo
  arma `tools/modelo.py` y VP lo conserva y lo deja navegar y editar.
- **Notación UML 2.5.1 de una herramienta reconocida:** carriles de actividad, fragmentos
  combinados con operandos, numeración anidada de mensajes y ocurrencias de ejecución, tal
  como los dibuja una CASE comercial.
- **Intercambio estándar:** VP importa el XMI 2.5.1 que genera la CI (validado contra el
  metamodelo de la OMG y con Eclipse UML2), así que no hay que redibujar nada a mano.

### Por qué hace falta un plugin

VP importa el XMI como **modelo** pero no dibuja los diagramas, porque el XMI no lleva
información gráfica. El plugin `tools/uml/vp` (API Java de VP) lee `build/vp-diagramas.json`
(generado por `tools/uml/vp_datos.py`), busca en el proyecto los elementos importados y arma
los diagramas de cada CU: clases, secuencia y actividades. Se tomó como referencia el plugin
[nbourdi/PlantUML-VP-Plugin](https://github.com/nbourdi/PlantUML-VP-Plugin) y el proyecto de
ejemplo `sample.vpp` de VP para imitar cómo VP guarda cada diagrama.

### Alcance y límites

- **En VP:** diagramas de actividades, clases y secuencia de CU-01 a CU-16.
- **Siguen en `.puml`:** diagramas de paquetes y de estados.
- En VP las guardas de actividad se normalizan a `[sí]` / `[no]`; un `else` pasa a `[no]`, o a
  `[otro]` cuando la decisión no es de sí o no. Los `.puml` no cambian.
- Con la licencia de evaluación VP agrega una marca de agua al exportar; el plugin no puede
  quitarla. Hace falta una licencia (por ejemplo la académica) para exportar sin ella.
- `openapi.jar` es propietario de VP y no se versiona; los `.vpp` tampoco.
- Cómo instalar el plugin y dibujar: [import-vp.md](import-vp.md).

### Alternativas descartadas

| Opción | Motivo |
|---|---|
| Visual Paradigm Online | No admite plugins de la API Java, así que no se pueden dibujar los diagramas en lote. |
| Redibujar a mano en VP | Lento y propenso a errores: el diagrama se separa del `.puml` validado. |
| Solo el XMI, sin plugin | VP muestra el modelo en el árbol pero sin diagramas. |
| PlantUML-VP-Plugin tal cual | Importa cada `.puml` por separado, sin el modelo único validado (C1-C6) ni sus controles; se usó como referencia de la API. |
