# Ctrl+ · Modelo de Análisis (TPF 04, Grupo 7)

Diagramas UML 2 del sistema Ctrl+ para gestión de obras, escritos como texto en
PlantUML. La CLI de PlantUML más esta CI cumplen el papel de herramienta CASE
(ver [docs/herramienta-case.md](docs/herramienta-case.md)).

## Estructura

| Carpeta | Contenido |
|---|---|
| `diagramas/` | Un `.puml` por diagrama. **Solo `.puml`**: PNG, SVG, XMI o `.kuml.kts` hacen fallar la CI. |
| `tools/` | Scripts de control que corre la CI y que se pueden correr a mano. |
| `.github/` | Workflow `CASE PlantUML` y la acción que instala PlantUML (versión y checksum fijos). |

## Funciones CASE cubiertas

| Función de una CASE | Control en la CI | Herramienta | Job |
|---|---|---|---|
| Validar el modelo | Sintaxis de cada `.puml` | `plantuml -checkonly` (`tools/check_sintaxis.sh`) | `sintaxis` |
| Reglas de modelado | Nombres `CU-XX-<tipo>[-n-<detalle>].puml` | Regex en bash (`tools/check_calidad.sh`) | `calidad` |
| Estándar visual | `!theme plain` y la paleta del grupo | `grep` (`tools/check_calidad.sh`) | `calidad` |
| Consistencia entre diagramas | Clases vs secuencia (E1, E2, W1, W2) | `tools/check_consistencia.py` | `consistencia` |
| Completitud | Cada CU tiene diagrama de clases y de secuencia | `tools/check_calidad.sh` | `calidad` |
| Generación de documentación | SVG y PNG desde el texto, como artefacto | `plantuml -tsvg` / `-tpng` | `render` |
| Control de versiones y revisión | PR obligatorio con la CI en verde | Protección de rama | — |
| Intercambio de modelos | XMI estándar, ArgoUML y StarUML (opcional) | `plantuml -txmi[:argo\|:star]` | `xmi (opcional)` |

Los SVG/PNG quedan en el artefacto `diagramas-svg-png` de cada corrida, y los XMI
en `diagramas-xmi` (corre en cada push a `main` o a mano desde *Actions → Run workflow*).
PlantUML exporta a XMI solo los diagramas de clases.

## Reglas

### Nombres

```
^CU-[0-9]{2}-(clases|secuencia|actividades|estados|paquetes|modelo-estructural|casos-de-uso-alto-nivel|generalizacion-actores)(-[0-9]+-<detalle>)?\.puml$
```

`<detalle>` va en minúsculas, sin tildes y separado por guiones. El `-n-` se usa cuando
un diagrama se parte en varios: `CU-02-secuencia-1-carga.puml`, `CU-02-secuencia-2-validacion.puml`.

### Estilo

Cada archivo tiene `!theme plain`, el fondo `#F5F8FA` y el borde `#17324D`. Los
diagramas de clases (`-clases`, `-modelo-estructural`) además llevan
`HeaderBackgroundColor #EAF2F6`. Un solo `@startuml` por archivo.

### Completitud

Cada `CU-XX` (salvo `CU-00`, que es el diagrama general) necesita al menos un
diagrama de clases (`CU-XX-clases*.puml` o `CU-XX-modelo-estructural.puml`) y uno
de secuencia (`CU-XX-secuencia*.puml`).

### Consistencia clases vs secuencia

Se compara, dentro de cada CU, el diagrama de clases con todas sus secuencias.

| Regla | Nivel | Qué detecta |
|---|---|---|
| **E1** | error | Un participante de la secuencia (`"obra:\nObra"`) es de un tipo que no existe como clase en el diagrama de clases del CU. |
| **E2** | error | Un mensaje (`A -> B: metodo(...)`) llama a un método que la clase de `B` no declara ni hereda. |
| **W1** | aviso | Una clase del diagrama no participa en ninguna secuencia del CU (no cuentan `enum`, `interface` ni `<<datatype>>`). |
| **W2** | aviso | Un método declarado en una clase que sí participa nunca se invoca en las secuencias. |

Los errores rompen la CI; los avisos se muestran como anotaciones en el PR sin
bloquear. Las respuestas (`-->`), los mensajes a actores y los textos sin paréntesis no se
analizan. Con `--strict` los avisos también fallan.

## Uso local

Requisitos: Java 17+, Graphviz (para clases; sin él se puede usar `-Playout=smetana`) y
`plantuml` en el `PATH` (`brew install plantuml`, `apt install plantuml` o el `.jar`).

```bash
bash tools/check_sintaxis.sh            # sintaxis
python3 tools/check_consistencia.py     # E1, E2, W1, W2
bash tools/check_calidad.sh             # solo .puml, nombres, estilo, completitud
plantuml -tsvg -o "$PWD/salida" diagramas/*.puml
```

## Flujo de trabajo

1. Rama nueva desde `main`, cambios en `diagramas/`.
2. Pull request: corren `sintaxis`, `consistencia`, `calidad` y `render`.
3. Con los cuatro en verde se puede hacer merge. `main` está protegida.
