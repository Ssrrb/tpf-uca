# Templates UML del TPF

## Modelo integral con Overarch

Los diagramas comparten una fuente canónica en `overarch/models/`. Overarch
separa los datos del sistema de sus vistas y valida la integridad referencial
al cargarlos. Esto evita mantener actores, casos de uso, clases, operaciones y
estados como copias independientes en varios archivos PlantUML.

| Archivo | Responsabilidad canónica |
|---|---|
| `00-requerimientos.edn` | IDs de RF-01..RF-12 y RNF-01..RNF-06 |
| `10-casos-de-uso.edn` | cuatro actores, diez CU, asociaciones y trazabilidad RF/RNF |
| `20-analisis-bce.edn` | clases BCE, atributos, operaciones y relaciones de CU-01..CU-10 |
| `30-estados-grupo.edn` | cinco estados, choice y transiciones de `GrupoTFG` |
| `90-views.edn` | vistas de casos de uso, clases, estados y diagnóstico integral |

Se usa Overarch `0.41.0`, indicado en `overarch/VERSION`. Descargar
`overarch.jar` desde la [release oficial](https://github.com/soulspace-org/overarch/releases/tag/v0.41.0)
y elegir una de estas ubicaciones:

```bash
export OVERARCH_JAR=/ruta/a/overarch.jar
# o copiarlo localmente (directorio ignorado):
cp /ruta/a/overarch.jar tpf/diagramas/overarch/tools/overarch.jar
```

Para validar el modelo, generar las vistas PlantUML y renderizar SVG:

```bash
tpf/diagramas/overarch/render.sh
```

Los artefactos se generan en `overarch/generated/` y no se versionan. Los
`.puml` ubicados directamente en `tpf/diagramas/` son vistas de publicación:
pueden conservar leyendas o ajustes docentes que Overarch no representa, pero
no pueden contradecir el modelo EDN.

### Procedimiento de modificación

1. Confirmar el cambio en la minuta, RF/RNF o especificación textual del CU.
2. Modificar primero el elemento canónico en `overarch/models/`, conservando
   el ID cuando solo cambia la presentación.
3. Si cambia un ID, actualizar todas sus referencias en el mismo cambio.
4. Ejecutar `overarch/render.sh` y resolver errores, referencias rotas e IDs
   duplicados. El comando también valida que cada referencia `' op:` de los
   diagramas de secuencia exista y conserve el mismo nombre de operación.
5. Comparar semánticamente las vistas generadas con los `.puml` de publicación.
6. Ajustar las vistas de publicación y regenerar sus SVG.

Overarch soporta vistas UML de casos de uso, clases y máquinas de estado, pero
no diagramas UML de secuencia. Por eso la secuencia se mantiene en PlantUML y
cada llamada relevante incluye un comentario `' op: :namespace/id` que apunta
al método receptor definido en el modelo BCE. Un cambio de operación exige
actualizar el modelo y todos esos usos; no se permite renombrar solo el mensaje.

## Archivos

- `generate_artifacts.py`: reconstruye el modelo BCE consolidado, las vistas
  Overarch y los 24 diagramas de publicación en PlantUML.
- `01-casos-de-uso-general.puml` y `.svg`: diagrama general de casos de uso.
- `01-*` a `10-*`: diagramas de clases de análisis y secuencia por CU.
- `22-estados-grupo-tfg.puml` y `.svg`: máquina de estados del grupo TFG.
- `23-clases-persistentes.puml` y `.svg`: clases persistentes.
- `24-entidad-relacion.puml` y `.svg`: modelo entidad-relación.

## Template de diagrama de clases de análisis

La plantilla usa CU-02, **Inscribir grupo**, y mantiene la misma traza que el
diagrama de secuencia correspondiente: RF-02, RF-03, RNF-02, RNF-04 y Minuta
02. Separa las clases `boundary`, `control` y `entity`, explicita atributos,
operaciones, multiplicidades y la restricción de pertenencia única por
semestre. Es un modelo de análisis: no introduce tablas, repositorios,
frameworks ni decisiones de implementación.

Para crear el diagrama de otro CU:

1. Duplicar el `.puml` y actualizar CU, RF/RNF y minuta del título.
2. Recorrer el flujo normal, alternativas y excepciones de la especificación.
3. Identificar fronteras para la interacción, un control para coordinar el CU
   y únicamente las entidades del dominio que el flujo consulta o modifica.
4. Asignar a cada clase lo que sabe (atributos), hace (operaciones) y con quién
   colabora (relaciones), buscando alta cohesión y bajo acoplamiento.
5. Mantener las conexiones de robustez: actor–frontera, frontera–control y
   control–entidad. El actor no se incluye como clase del sistema.
6. Especificar visibilidad, tipos, multiplicidades y roles cuando aporten
   semántica; usar `{query}` en operaciones sin efectos secundarios.
7. Usar asociación simple como opción normal. Elegir agregación o composición
   solo si existe una semántica todo–parte verificable en el dominio.
8. Confirmar que las operaciones receptoras coincidan con los mensajes del
   diagrama de secuencia del mismo CU.

### Lista de cotejo de clases de análisis

- El diagrama corresponde a un solo CU y declara su trazabilidad.
- Cada clase tiene nombre singular y una responsabilidad coherente.
- Existe al menos un control del CU y las fronteras no contienen lógica de
  negocio ni estado persistente.
- Las entidades representan conceptos presentes en requisitos o minutas.
- Atributos y operaciones usan sintaxis UML y visibilidad explícita.
- Las operaciones se nombran con verbos y las consultas usan `{query}`.
- Asociaciones, roles y multiplicidades reflejan reglas verificables.
- No se usa composición como sinónimo genérico de “contiene”.
- No aparecen detalles de base de datos, UI concreta o tecnología.
- Nombres y operaciones coinciden con la especificación y la secuencia.

Las indicaciones docentes descargadas se encuentran en
`indicaciones-diagramas-clases/`. El punto de entrada es
`Zk !MOC Diagrama de Clases (Fundamentos, Elementos, Relaciones, etc.).md`.

Para actualizarlas sin modificar `download_obsidian.py`:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run download_obsidian.py \
  --url 'https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingenier%C3%ADa+del+Software+1/Clase+13+Diagrama+de+Clases+(Fundamentos%2C+Elementos%2C+Relaciones%2C+etc.)/Zk+!MOC+Diagrama+de+Clases+(Fundamentos%2C+Elementos%2C+Relaciones%2C+etc.)' \
  --out indicaciones-diagramas-clases \
  --scope-root '050 Base de Conocimientos/200  Mi Zettelkasten/100 Docencia/Ingeniería del Software 1/Clase 13 Diagrama de Clases (Fundamentos, Elementos, Relaciones, etc.)'
```

## Template de diagrama de secuencia

La plantilla usa CU-02, **Inscribir grupo**, porque reúne los principales
elementos exigidos por las indicaciones docentes: actor, participantes BCE,
líneas de vida, activaciones, mensajes, retornos y marcos de interacción
`loop` y `alt`. Su traza es RF-02, RF-03, RNF-02, RNF-04 y Minuta 02.

Para crear el diagrama de otro CU:

1. Duplicar el `.puml` y cambiar el identificador, nombre y RF/RNF del título.
2. Tomar los participantes del diagrama de clases BCE del mismo CU.
3. Convertir cada paso del flujo normal en mensajes ordenados.
4. Representar alternativas y excepciones con `alt`, comportamiento opcional
   con `opt` y repeticiones con `loop`.
5. Confirmar que cada mensaje recibido por un objeto corresponde a una
   operación de su clase de análisis.
6. Mantener solo datos, reglas y actores presentes en las minutas oficiales.

La plantilla concreta el flujo de CU-02, no reemplaza su especificación
textual. Al reutilizarla deben sustituirse todos los participantes y mensajes
que no correspondan al CU de destino.

### Convenciones del diagrama de secuencia

- Los participantes aparecen de izquierda a derecha como actor, `boundary`,
  `control` y entidades.
- Las llamadas usan flecha continua (`->`) y los resultados flecha discontinua
  (`-->`).
- Las barras de activación delimitan cuándo un participante ejecuta una
  operación.
- El eje vertical expresa el orden temporal; no debe alterarse para acomodar
  visualmente mensajes fuera de secuencia.
- Los mensajes se nombran como operaciones y deben coincidir con el diagrama
  de clases BCE asociado.
- Las validaciones del sistema permanecen en el controlador o en una entidad;
  el actor no ejecuta reglas del dominio.

### Lista de cotejo de interacción

- El diagrama corresponde a un solo CU y a sus escenarios documentados.
- El actor y el primer mensaje coinciden con el iniciador del CU.
- El flujo normal y todas las excepciones relevantes están representados.
- Cada mensaje tiene emisor, receptor y nombre de operación inequívocos.
- Cada operación existe en la clase receptora del diagrama BCE.
- Se muestran retornos cuando aclaran decisiones o resultados.
- `alt`, `opt` y `loop` incluyen condiciones comprensibles.
- Los nombres de actores, entidades, estados y operaciones son consistentes
  con los demás modelos.
- El título y la leyenda identifican CU, RF/RNF y minuta de origen.

Las indicaciones docentes de interacción descargadas se encuentran en
`indicaciones-diagramas-interaccion/`. El punto de entrada es
`Zk Diagramas de Interacción (Introducción).md`.

Para actualizarlas sin modificar `download_obsidian.py`:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run download_obsidian.py \
  --url 'https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingenier%C3%ADa+del+Software+1/Clase+14+Diagramas+de+Interacci%C3%B3n/Zk+Diagramas+de+Interacci%C3%B3n+(Introducci%C3%B3n)' \
  --out indicaciones-diagramas-interaccion \
  --scope-root '050 Base de Conocimientos/200  Mi Zettelkasten/100 Docencia/Ingeniería del Software 1/Clase 14 Diagramas de Interacción'
```

## Template de diagrama de máquina de estados

### Alcance del modelo

La entidad modelada es el **Grupo de TFG** durante la primera etapa del proceso. El diagrama comienza con la inscripción y termina con la entrega formal del anteproyecto. No incorpora dictamen, defensa ni cierre porque están fuera del alcance definido por el caso.

Los únicos estados sustantivos son los cinco establecidos por RF-10:

1. Pendiente de inscripción.
2. Inscripto.
3. Tutor asignado.
4. En elaboración de anteproyecto.
5. Anteproyecto entregado.

`¿Entrega habilitada?` es un pseudoelemento `choice`, no un estado del dominio. Se utiliza para separar las guardas de entrega válida y entrega bloqueada sin inventar un estado adicional.

### Convenciones aplicadas

Cada transición sigue la forma:

```text
evento [guarda] / efecto
```

- El **evento** expresa qué ocurrió: `inscribirGrupo`, `asignarTutor`, `entregarAnteproyecto`.
- La **guarda** es una condición booleana evaluable: `[sinPertenenciaDuplicadaEnSemestre]`.
- El **efecto** nombra una acción del sistema: `registrarEntrega(fecha, usuario)`.
- El pseudoelemento inicial marca la entrada por defecto; el final expresa que concluyó el comportamiento incluido en el alcance.
- `publicarAsignacion / notificarGrupo` es una transición interna: satisface RF-06 sin crear un estado que RF-10 no define.

### Trazabilidad

| Elemento | Requerimientos y fuente |
|---|---|
| Secuencia de cinco estados | RF-10, Minuta 06 |
| Inscripción válida y rechazo | RF-02, RF-03, Minuta 02 |
| Asignación restringida a Comisión y fecha | RF-05, RNF-03, Minuta 03 |
| Publicación y notificación | RF-06, Minuta 03 |
| Inicio de elaboración con versión preliminar | RF-07, Minuta 04 |
| Entrega formal | RF-09, Minuta 06 |
| Bloqueo fuera de plazo y excepción autorizada | RNF-05, Minuta 06 |
| Registro de fecha y responsable | RNF-04 |

### Lista de cotejo antes de entregar

- Todos los estados son alcanzables desde el inicio.
- Los nombres de estados representan situaciones, no acciones.
- Los eventos, guardas y efectos están diferenciados.
- Las guardas alternativas de entrega son claras y cubren ambos resultados.
- No se mezclan pasos de interfaz ni detalles de implementación.
- El estado final coincide con el límite de alcance del TPF.
- Los nombres coinciden con RF-10 y con los demás modelos UML.

## Regeneración

Para las vistas de publicación, desde la raíz del proyecto:

```bash
env JAVA_TOOL_OPTIONS=-Djava.awt.headless=true \
  plantuml -tsvg tpf/diagramas/*.puml
```

Para las vistas canónicas y su control de consistencia, ejecutar además:

```bash
tpf/diagramas/overarch/render.sh
```

Las indicaciones docentes descargadas se encuentran en `indicaciones-diagramas-estados/`, cuyo punto de entrada es `Zk !MOC Diagramas de Estados.md`.

Para actualizarlas sin modificar `download_obsidian.py`:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run download_obsidian.py \
  --url 'https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingenier%C3%ADa+del+Software+1/Clase+16+Diagrama+de+Estados/Zk+!MOC+Diagramas+de+Estados' \
  --out indicaciones-diagramas-estados \
  --scope-root '050 Base de Conocimientos/200  Mi Zettelkasten/100 Docencia/Ingeniería del Software 1/Clase 16 Diagrama de Estados'
```
