---
lang: es-PY
---

![](_delivery_media/template-logo.png){width=1.703in height=1.646in}

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

```{=openxml}
<w:p><w:r><w:br w:type="page" /></w:r></w:p>
```

```{=openxml}
<w:p><w:r><w:t>Modelo de Análisis</w:t><w:tab/><w:t>3</w:t></w:r></w:p>
<w:p><w:r><w:t>Requerimientos</w:t><w:tab/><w:t>3</w:t></w:r></w:p>
<w:p><w:r><w:t>Requerimientos Funcionales</w:t><w:tab/><w:t>3</w:t></w:r></w:p>
<w:p><w:r><w:t>Requerimientos No Funcionales</w:t><w:tab/><w:t>4</w:t></w:r></w:p>
<w:p><w:r><w:t>Identificación de Actores</w:t><w:tab/><w:t>4</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Casos de Uso</w:t><w:tab/><w:t>6</w:t></w:r></w:p>
<w:p><w:r><w:t>Sistema …</w:t><w:tab/><w:t>6</w:t></w:r></w:p>
<w:p><w:r><w:t>Caso de Uso &lt;nombre&gt;</w:t><w:tab/><w:t>7</w:t></w:r></w:p>
<w:p><w:r><w:t>Especificación Caso de Uso</w:t><w:tab/><w:t>7</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Clases del Caso de Uso</w:t><w:tab/><w:t>8</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Interacción del Caso de Uso</w:t><w:tab/><w:t>8</w:t></w:r></w:p>
<w:p><w:r><w:t>Caso de Uso &lt;nombre&gt;</w:t><w:tab/><w:t>9</w:t></w:r></w:p>
<w:p><w:r><w:t>Especificación Caso de Uso</w:t><w:tab/><w:t>9</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Clases del Caso de Uso</w:t><w:tab/><w:t>10</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Interacción del Caso de Uso</w:t><w:tab/><w:t>11</w:t></w:r></w:p>
<w:p><w:r><w:t>Caso de Uso &lt;nombre&gt;</w:t><w:tab/><w:t>12</w:t></w:r></w:p>
<w:p><w:r><w:t>Especificación Caso de Uso</w:t><w:tab/><w:t>12</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Clases del Caso de Uso</w:t><w:tab/><w:t>12</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Interacción del Caso de Uso</w:t><w:tab/><w:t>12</w:t></w:r></w:p>
<w:p><w:r><w:t>Matriz de Requerimientos vs Casos de Uso</w:t><w:tab/><w:t>13</w:t></w:r></w:p>
<w:p><w:r><w:t>Modelo de Diseño</w:t><w:tab/><w:t>15</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Clases Persistentes</w:t><w:tab/><w:t>15</w:t></w:r></w:p>
<w:p><w:r><w:t>Diagrama de Entidad Relación</w:t><w:tab/><w:t>15</w:t></w:r></w:p>
<w:p><w:r><w:t>Referencias</w:t></w:r></w:p>
```

```{=openxml}
<w:p><w:r><w:br w:type="page" /></w:r></w:p>
```

# Modelo de Análisis

El sistema modelado cubre la primera etapa del Trabajo Final de Grado de la Licenciatura en Análisis de Sistemas Informáticos de la Universidad Católica de Asunción: apertura del semestre, inscripción de grupos, asignación y publicación de tutores, elaboración inicial y entrega formal del anteproyecto. Quedan fuera del alcance el dictamen, la defensa y el cierre del TFG.

## Requerimientos

### Requerimientos Funcionales

| ID | Requerimiento | Minuta asociada |
| --- | --- | --- |
| RF-01 | El sistema debe permitir a la Comisión de TFG registrar el semestre de TFG con sus fechas claves: reunión inicial, fecha tope de inscripción de grupos, publicación de tutores y fecha límite de entrega del anteproyecto. | Minuta 01 |
| RF-02 | El estudiante debe poder registrar la inscripción de su grupo indicando nombre tentativo del tema, integrantes y datos de contacto. | Minuta 02 |
| RF-03 | El sistema debe validar que un estudiante no pueda pertenecer a más de un grupo de TFG en el mismo semestre. | Minuta 02 |
| RF-04 | La Comisión de TFG debe poder consultar la lista de grupos inscriptos con estado de completitud y cantidad de integrantes. | Minuta 03 |
| RF-05 | La Comisión de TFG debe poder asignar un tutor a cada grupo inscripto antes de la fecha de publicación definida. | Minuta 03 |
| RF-06 | El sistema debe permitir publicar la asignación de tutor y notificar al grupo correspondiente. | Minuta 03 |
| RF-07 | El grupo debe poder cargar una versión preliminar del anteproyecto con título, problema, objetivo general y alcance. | Minuta 04 |
| RF-08 | El tutor debe poder registrar observaciones sobre el avance del anteproyecto durante el período de elaboración. | Minuta 05 |
| RF-09 | El grupo debe poder entregar formalmente el anteproyecto antes de la fecha límite establecida por la Comisión. | Minuta 06 |
| RF-10 | El sistema debe cambiar el estado del grupo según el avance de la primera etapa: pendiente de inscripción, inscripto, tutor asignado, en elaboración de anteproyecto, anteproyecto entregado. | Minuta 06 |
| RF-11 | El estudiante debe poder consultar en cualquier momento el estado de su grupo, tutor asignado, fechas clave y observaciones registradas. | Minuta 05 |
| RF-12 | La Comisión de TFG debe poder generar un listado de grupos que aún no entregaron su anteproyecto al acercarse la fecha límite. | Minuta 06 |

### Requerimientos No Funcionales

| ID | Requerimiento | Minuta asociada |
| --- | --- | --- |
| RNF-01 | La interfaz debe presentar de forma clara las etapas y fechas clave del proceso inicial del TFG. | Minuta 01 |
| RNF-02 | El sistema debe ser accesible vía web desde dispositivos de escritorio y móviles. | Minuta 02 |
| RNF-03 | Solo la Comisión de TFG puede modificar fechas del semestre y asignaciones de tutores. | Minuta 03 |
| RNF-04 | El sistema debe registrar fecha y usuario responsable en las acciones de inscripción, asignación, observación y entrega. | Minuta 05 |
| RNF-05 | La entrega del anteproyecto debe quedar bloqueada automáticamente una vez vencida la fecha límite, salvo habilitación expresa de la Comisión. | Minuta 06 |
| RNF-06 | Los estudiantes solo deben poder consultar la información de su propio grupo, mientras que la Comisión puede consultar todos los grupos del semestre. | Minuta 03 / Minuta 05 |

## Identificación de Actores

| Actor | Descripción |
| --- | --- |
| Estudiante | Actor principal que inscribe el grupo, carga la versión preliminar, entrega el anteproyecto y consulta estado, tutor, fechas clave y observaciones de su propio grupo. |
| Comisión de TFG | Actor principal responsable de configurar el semestre, consultar grupos, asignar tutores, publicar asignaciones y generar listados de grupos sin entrega. |
| Tutor | Actor principal que registra observaciones sobre los grupos asignados durante la elaboración del anteproyecto. |
| Secretaría Académica | Actor de contexto oficial relacionado con la inscripción académica; no posee requerimientos funcionales de interacción directa con el sistema en esta iteración. |

## Diagrama de Casos de Uso

### Sistema web de gestión de la primera etapa del TFG

![](diagramas/01-casos-de-uso-general.svg)

## Casos de uso identificados

| ID | Caso de uso | Actor principal | Requerimiento(s) |
| --- | --- | --- | --- |
| CU-01 | Configurar semestre | Comisión de TFG | RF-01; RNF-01, RNF-03 |
| CU-02 | Inscribir grupo | Estudiante | RF-02, RF-03; RNF-02, RNF-04 |
| CU-03 | Consultar grupos inscriptos | Comisión de TFG | RF-04; RNF-06 |
| CU-04 | Asignar tutor | Comisión de TFG | RF-05; RNF-03, RNF-04 |
| CU-05 | Publicar asignación de tutor | Comisión de TFG | RF-06; RNF-03 |
| CU-06 | Cargar versión preliminar | Estudiante | RF-07; RNF-04 |
| CU-07 | Registrar observaciones | Tutor | RF-08; RNF-04 |
| CU-08 | Entregar anteproyecto | Estudiante | RF-09, RF-10; RNF-04, RNF-05 |
| CU-09 | Consultar estado del grupo | Estudiante | RF-11; RNF-01, RNF-06 |
| CU-10 | Generar listado de grupos sin entrega | Comisión de TFG | RF-12; RNF-06 |

## Caso de Uso CU-01 Configurar semestre

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-01 Configurar semestre |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de configurar semestre dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-01; RNF-01, RNF-03 |
| Actores | Comisión de TFG |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | La Comisión solicita configurar el semestre de TFG. |  |
| 2 |  | El sistema muestra el formulario de fechas clave. |
| 3 | La Comisión ingresa reunión inicial, cierre de inscripción, publicación de tutores y entrega del anteproyecto. |  |
| 4 |  | El sistema valida que las fechas obligatorias estén completas y ordenadas. |
| 5 |  | El sistema registra el semestre y publica el cronograma inicial. |

**Excepciones**

- Si faltan fechas o el orden es inválido, el sistema informa errores y no registra el semestre.

### Diagrama de Clases del Caso de Uso

![](diagramas/01-configurar-semestre-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/01-configurar-semestre-secuencia.svg)

## Caso de Uso CU-02 Inscribir grupo

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-02 Inscribir grupo |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de inscribir grupo dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-02, RF-03; RNF-02, RNF-04 |
| Actores | Estudiante |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | El estudiante solicita inscribir su grupo. |  |
| 2 |  | El sistema muestra el formulario de inscripción. |
| 3 | El estudiante ingresa tema tentativo, integrantes y medio de contacto. |  |
| 4 |  | El sistema valida datos obligatorios, cantidad de integrantes y pertenencia única por semestre. |
| 5 |  | El sistema registra el grupo y cambia su estado a Inscripto. |

**Excepciones**

- Si el grupo no tiene entre 1 y 3 integrantes, se informa el error.
- Si un estudiante ya pertenece a otro grupo del semestre, se rechaza la inscripción.

### Diagrama de Clases del Caso de Uso

![](diagramas/02-inscribir-grupo-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/02-inscribir-grupo-secuencia.svg)

## Caso de Uso CU-03 Consultar grupos inscriptos

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-03 Consultar grupos inscriptos |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de consultar grupos inscriptos dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-04; RNF-06 |
| Actores | Comisión de TFG |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | La Comisión solicita la lista de grupos del semestre. |  |
| 2 |  | El sistema verifica el rol de Comisión. |
| 3 | El sistema obtiene los grupos inscriptos. |  |
| 4 |  | El sistema calcula completitud, cantidad de integrantes, tema y estado. |
| 5 |  | El sistema muestra el listado consolidado. |

**Excepciones**

- Si el usuario no pertenece a Comisión, se deniega la consulta general.

### Diagrama de Clases del Caso de Uso

![](diagramas/03-consultar-grupos-inscriptos-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/03-consultar-grupos-inscriptos-secuencia.svg)

## Caso de Uso CU-04 Asignar tutor

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-04 Asignar tutor |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de asignar tutor dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-05; RNF-03, RNF-04 |
| Actores | Comisión de TFG |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | La Comisión selecciona un grupo inscripto y un tutor. |  |
| 2 |  | El sistema verifica autorización de Comisión. |
| 3 | El sistema valida que la asignación ocurra antes de la fecha de publicación. |  |
| 4 |  | El sistema registra tutor, fecha y responsable. |
| 5 |  | El sistema actualiza el estado del grupo a Tutor asignado. |

**Excepciones**

- Si el usuario no es Comisión, el sistema deniega la operación.
- Si ya pasó la fecha de publicación, el sistema informa que la asignación no corresponde en este flujo.

### Diagrama de Clases del Caso de Uso

![](diagramas/04-asignar-tutor-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/04-asignar-tutor-secuencia.svg)

## Caso de Uso CU-05 Publicar asignación de tutor

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-05 Publicar asignación de tutor |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de publicar asignación de tutor dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-06; RNF-03 |
| Actores | Comisión de TFG |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | La Comisión solicita publicar asignaciones de tutores. |  |
| 2 |  | El sistema verifica autorización de Comisión. |
| 3 | El sistema valida que existan grupos con tutor asignado. |  |
| 4 |  | El sistema marca las asignaciones como publicadas. |
| 5 |  | El sistema notifica al grupo correspondiente. |

**Excepciones**

- Si un grupo inscripto no tiene tutor asignado, queda fuera de la publicación y se informa a Comisión.

### Diagrama de Clases del Caso de Uso

![](diagramas/05-publicar-asignacion-tutor-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/05-publicar-asignacion-tutor-secuencia.svg)

## Caso de Uso CU-06 Cargar versión preliminar

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-06 Cargar versión preliminar |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de cargar versión preliminar dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-07; RNF-04 |
| Actores | Estudiante |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | El estudiante solicita cargar la versión preliminar. |  |
| 2 |  | El sistema recupera el grupo del estudiante. |
| 3 | El estudiante ingresa título, problema, objetivo general y alcance. |  |
| 4 |  | El sistema valida que los campos mínimos estén completos. |
| 5 |  | El sistema registra la versión y cambia el estado a En elaboración de anteproyecto. |

**Excepciones**

- Si falta alguno de los campos mínimos, el sistema informa errores y conserva el estado anterior.

### Diagrama de Clases del Caso de Uso

![](diagramas/06-cargar-version-preliminar-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/06-cargar-version-preliminar-secuencia.svg)

## Caso de Uso CU-07 Registrar observaciones

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-07 Registrar observaciones |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de registrar observaciones dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-08; RNF-04 |
| Actores | Tutor |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | El tutor selecciona un grupo asignado. |  |
| 2 |  | El sistema verifica que el tutor esté asignado al grupo. |
| 3 | El tutor ingresa la observación breve. |  |
| 4 |  | El sistema registra observación, fecha y responsable. |
| 5 |  | El sistema deja la observación disponible para estudiantes y Comisión. |

**Excepciones**

- Si el tutor no está asignado al grupo, el sistema deniega el registro.

### Diagrama de Clases del Caso de Uso

![](diagramas/07-registrar-observaciones-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/07-registrar-observaciones-secuencia.svg)

## Caso de Uso CU-08 Entregar anteproyecto

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-08 Entregar anteproyecto |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de entregar anteproyecto dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-09, RF-10; RNF-04, RNF-05 |
| Actores | Estudiante |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | El estudiante solicita entregar formalmente el anteproyecto. |  |
| 2 |  | El sistema obtiene el grupo y la fecha límite del semestre. |
| 3 | El sistema valida que la entrega esté en plazo o tenga autorización expresa de Comisión. |  |
| 4 |  | El sistema registra la entrega formal con fecha y usuario. |
| 5 |  | El sistema cambia el estado del grupo a Anteproyecto entregado. |

**Excepciones**

- Si la fecha límite venció y no existe autorización expresa, el sistema bloquea la entrega.

### Diagrama de Clases del Caso de Uso

![](diagramas/08-entregar-anteproyecto-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/08-entregar-anteproyecto-secuencia.svg)

## Caso de Uso CU-09 Consultar estado del grupo

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-09 Consultar estado del grupo |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de consultar estado del grupo dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-11; RNF-01, RNF-06 |
| Actores | Estudiante |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | El estudiante solicita consultar el estado de su grupo. |  |
| 2 |  | El sistema obtiene únicamente el grupo asociado al estudiante. |
| 3 | El sistema recupera estado, tutor, fechas clave y observaciones. |  |
| 4 |  | El sistema muestra la información del grupo propio. |

**Excepciones**

- Si el estudiante no tiene grupo en el semestre, el sistema informa que no existe inscripción asociada.

### Diagrama de Clases del Caso de Uso

![](diagramas/09-consultar-estado-grupo-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/09-consultar-estado-grupo-secuencia.svg)

## Caso de Uso CU-10 Generar listado de grupos sin entrega

### Especificación Caso de Uso

| Campo | Detalle |
| --- | --- |
| Nombre Caso de Uso | CU-10 Generar listado de grupos sin entrega |
| Versión | 1.0 |
| Creado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Modificado por | Sebas Rojas - Grupo G11 |
| Fecha | junio 2026 |
| Descripción | Permite ejecutar el proceso de generar listado de grupos sin entrega dentro de la primera etapa del TFG. |
| Requerimiento(s) a que responde | RF-12; RNF-06 |
| Actores | Comisión de TFG |
| Pre Condiciones | El usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita. |
| Pos Condiciones | Se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG. |

**Flujo Normal**

| Paso | Actor - Acción | Respuesta del Sistema |
| --- | --- | --- |
| 1 | La Comisión solicita el listado de grupos pendientes. |  |
| 2 |  | El sistema verifica acceso de Comisión. |
| 3 | El sistema verifica proximidad a la fecha límite. |  |
| 4 |  | El sistema selecciona grupos que aún no entregaron anteproyecto. |
| 5 |  | El sistema muestra el listado para recordatorios. |

**Excepciones**

- Si no se está cerca del plazo, el sistema puede mostrar el listado con advertencia de oportunidad.

### Diagrama de Clases del Caso de Uso

![](diagramas/10-generar-listado-sin-entrega-clases-analisis.svg)

### Diagrama de Interacción del Caso de Uso

![](diagramas/10-generar-listado-sin-entrega-secuencia.svg)

```{=openxml}
<w:p><w:r><w:br w:type="page" /></w:r></w:p>
```

## Matriz de Requerimientos vs Casos de Uso

| Requerimiento | CU-01 | CU-02 | CU-03 | CU-04 | CU-05 | CU-06 | CU-07 | CU-08 | CU-09 | CU-10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RF-01 | ● |  |  |  |  |  |  |  |  |  |
| RF-02 |  | ● |  |  |  |  |  |  |  |  |
| RF-03 |  | ● |  |  |  |  |  |  |  |  |
| RF-04 |  |  | ● |  |  |  |  |  |  |  |
| RF-05 |  |  |  | ● |  |  |  |  |  |  |
| RF-06 |  |  |  |  | ● |  |  |  |  |  |
| RF-07 |  |  |  |  |  | ● |  |  |  |  |
| RF-08 |  |  |  |  |  |  | ● |  |  |  |
| RF-09 |  |  |  |  |  |  |  | ● |  |  |
| RF-10 |  |  |  |  |  |  |  | ● |  |  |
| RF-11 |  |  |  |  |  |  |  |  | ● |  |
| RF-12 |  |  |  |  |  |  |  |  |  | ● |
| RNF-01 | ● |  |  |  |  |  |  |  | ● |  |
| RNF-02 |  | ● |  |  |  |  |  |  |  |  |
| RNF-03 | ● |  |  | ● | ● |  |  |  |  |  |
| RNF-04 |  | ● |  | ● |  | ● | ● | ● |  |  |
| RNF-05 |  |  |  |  |  |  |  | ● |  |  |
| RNF-06 |  |  | ● |  |  |  |  |  | ● | ● |

```{=openxml}
<w:p><w:r><w:br w:type="page" /></w:r></w:p>
```

## Microestudio formativo

### Preparación de datos

El subconjunto `G11.tsv` contiene 10 casos anonimizados. Distribución por período: 2024 S2: 1, 2025 S1: 2, 2025 S2: 2, 2026 S1: 3, Otro: 2. La revisión de P1 a P4 encontró:

| Ítem | Faltantes | Inválidos |
| --- | --- | --- |
| P1 | ninguno | ninguno |
| P2 | ninguno | ninguno |
| P3 | ninguno | ninguno |
| P4 | ninguno | ninguno |

### Resultados descriptivos

| Ítem | Media | Mínimo | Máximo | Frec. 1 | Frec. 2 | Frec. 3 | Frec. 4 | Frec. 5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 4.70 | 3 | 5 | 0 | 0 | 1 | 1 | 8 |
| P2 | 4.60 | 4 | 5 | 0 | 0 | 0 | 4 | 6 |
| P3 | 4.70 | 4 | 5 | 0 | 0 | 0 | 3 | 7 |
| P4 | 4.50 | 4 | 5 | 0 | 0 | 0 | 5 | 5 |

La claridad percibida es alta en el subconjunto analizado. P1, claridad de etapas, y P3, claridad de plazos y fechas clave, tienen las medias más altas (4.70 y 4.70). P4, claridad del flujo completo, presenta la media más baja relativa (4.50), aunque su mínimo observado es 4. P2, claridad de roles, queda en 4.60; no hay valores menores a 4.

### Lectura cualitativa mínima

Se registraron 4 comentarios abiertos. Los temas principales son:

- Predomina una percepción de claridad general: "Todo fue muy claro y voy avanzando bien con las reuniones con el tutor!" y "Se entendió bien todo."
- Las dudas se concentran en comunicación y disponibilidad de información de apoyo: un comentario menciona dificultad para encontrar documentaciones actualizadas sobre modelos de anteproyecto, y otro señala que "Sería oportuno mejorar la comunicación entre alumnos y tutores."

### Respuesta a la pregunta de investigación

A partir de los datos del subconjunto G11, los estudiantes perciben un nivel alto de claridad sobre etapas, roles y plazos de la fase inicial del TFG. La evidencia cuantitativa muestra medias entre 4.50 y 4.70, con mínimos entre 3 y 4. La dimensión menos sólida es la comprensión del flujo completo, no por valores bajos, sino porque concentra más respuestas 4 que 5. La evidencia cualitativa no contradice esa lectura: aparecen comentarios de claridad general, junto con necesidades puntuales de mejor comunicación con tutores y mejor acceso a documentación actualizada.

### Advertencia metodológica obligatoria

Este microestudio tiene carácter formativo, descriptivo y exploratorio. Los datos analizados corresponden únicamente al subconjunto G11 asignado por la cátedra y no necesariamente representan a toda la población de estudiantes de TFG. Los resultados se presentan con fines pedagógicos y de apoyo al análisis del sistema. Cualquier generalización robusta requeriría un diseño muestral más riguroso, mayor tamaño de muestra y procedimientos analíticos adicionales.

### Decisiones de análisis justificadas por los hallazgos

1. Se conserva como central el CU-09 Consultar estado del grupo, con estado, tutor, fechas clave y observaciones en una sola vista. La decisión se apoya en que P4 es la dimensión con media más baja relativa y en comentarios que piden mejorar la comunicación entre alumnos y tutores.
2. Se explicita la publicación clara de cronograma en CU-01 y la consulta de fechas clave en CU-09. Aunque P3 es alta, el comentario sobre documentación no disponible muestra que la claridad depende de que los insumos estén centralizados y actualizados.


# Modelo de Diseño

## Diagrama de Estados

![](diagramas/22-estados-grupo-tfg.svg)

## Diagrama de Actividades del Proceso Inicial del TFG

![](diagramas/25-actividades-proceso-inicial-tfg.svg)

## Diagrama de Clases Persistentes

![](diagramas/23-clases-persistentes.svg)

## Diagrama de Entidad Relación

![](diagramas/24-entidad-relacion.svg)

## Consistencia entre modelos

Los diagramas mantienen la cadena de trazabilidad Minuta -> RF/RNF -> CU -> clases BCE -> secuencia -> estados/diseño. Las secuencias referencian operaciones canónicas mediante comentarios `op:` validados por `tpf/diagramas/overarch/validate_sequence_refs.py`. El estado del grupo usado en análisis y diseño respeta los cinco estados de RF-10 y no agrega estados de etapas posteriores.

# Referencias

- Cátedra de Ingeniería del Software 1. (2026). *Trabajo Práctico Final 2026: Especificaciones del caso de estudio, anexos y rúbrica*.
- Cátedra de Ingeniería del Software 1. (2026). *Materiales de clase sobre diagramas de clases, interacción y estados UML*.
- Grupo G11. (2026). *Subconjunto de datos anónimo G11.tsv para microestudio formativo*.
