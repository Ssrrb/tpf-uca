---
title: "Sistema web de gestión de la primera etapa del TFG"
subtitle: "Trabajo Práctico Final - Ingeniería del Software 1"
author: "Sebas Rojas - Grupo G11"
lang: es-PY
---

# Sistema web de gestión de la primera etapa del TFG

## Alcance

El sistema modelado cubre la primera etapa del Trabajo Final de Grado de la Licenciatura en Análisis de Sistemas Informáticos de la Universidad Católica de Asunción: apertura del semestre, inscripción de grupos, asignación y publicación de tutores, elaboración inicial y entrega formal del anteproyecto. Quedan fuera del alcance el dictamen, la defensa y el cierre del TFG.

## Actores

- Estudiante: inscribe grupo, carga y entrega anteproyecto, consulta estado y observaciones.
- Comisión de TFG: configura semestre, consulta grupos, asigna y publica tutores, controla grupos sin entrega.
- Tutor: registra observaciones sobre grupos asignados.
- Secretaría Académica: actor de contexto para inscripción académica; no tiene RF de interacción directa con el sistema en esta iteración.

## Reglas de negocio

- Cada grupo tiene entre 1 y 3 integrantes.
- Un estudiante no puede pertenecer a más de un grupo de TFG en el mismo semestre.
- Solo la Comisión modifica fechas del semestre y asignaciones de tutores.
- Toda inscripción, asignación, observación y entrega registra fecha y usuario responsable.
- La entrega queda bloqueada al vencer la fecha límite, salvo autorización expresa de la Comisión.
- Los estudiantes solo consultan su propio grupo; la Comisión consulta todos los grupos del semestre.
- El alcance termina con la entrega formal del anteproyecto; no incluye dictamen, defensa ni cierre.

## Casos de uso identificados

| ID | Caso de uso | Actor principal | Requerimientos |
|---|---|---|---|
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

## Especificación textual de casos de uso

### CU-01 Configurar semestre

**Actor principal:** Comisión de TFG.  
**Trazabilidad:** RF-01; RNF-01, RNF-03; Minuta 01.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. La Comisión solicita configurar el semestre de TFG.
2. El sistema muestra el formulario de fechas clave.
3. La Comisión ingresa reunión inicial, cierre de inscripción, publicación de tutores y entrega del anteproyecto.
4. El sistema valida que las fechas obligatorias estén completas y ordenadas.
5. El sistema registra el semestre y publica el cronograma inicial.

**Flujos alternativos**

- Si faltan fechas o el orden es inválido, el sistema informa errores y no registra el semestre.

### CU-02 Inscribir grupo

**Actor principal:** Estudiante.  
**Trazabilidad:** RF-02, RF-03; RNF-02, RNF-04; Minuta 02.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. El estudiante solicita inscribir su grupo.
2. El sistema muestra el formulario de inscripción.
3. El estudiante ingresa tema tentativo, integrantes y medio de contacto.
4. El sistema valida datos obligatorios, cantidad de integrantes y pertenencia única por semestre.
5. El sistema registra el grupo y cambia su estado a Inscripto.

**Flujos alternativos**

- Si el grupo no tiene entre 1 y 3 integrantes, se informa el error.
- Si un estudiante ya pertenece a otro grupo del semestre, se rechaza la inscripción.

### CU-03 Consultar grupos inscriptos

**Actor principal:** Comisión de TFG.  
**Trazabilidad:** RF-04; RNF-06; Minuta 03.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. La Comisión solicita la lista de grupos del semestre.
2. El sistema verifica el rol de Comisión.
3. El sistema obtiene los grupos inscriptos.
4. El sistema calcula completitud, cantidad de integrantes, tema y estado.
5. El sistema muestra el listado consolidado.

**Flujos alternativos**

- Si el usuario no pertenece a Comisión, se deniega la consulta general.

### CU-04 Asignar tutor

**Actor principal:** Comisión de TFG.  
**Trazabilidad:** RF-05; RNF-03, RNF-04; Minuta 03.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. La Comisión selecciona un grupo inscripto y un tutor.
2. El sistema verifica autorización de Comisión.
3. El sistema valida que la asignación ocurra antes de la fecha de publicación.
4. El sistema registra tutor, fecha y responsable.
5. El sistema actualiza el estado del grupo a Tutor asignado.

**Flujos alternativos**

- Si el usuario no es Comisión, el sistema deniega la operación.
- Si ya pasó la fecha de publicación, el sistema informa que la asignación no corresponde en este flujo.

### CU-05 Publicar asignación de tutor

**Actor principal:** Comisión de TFG.  
**Trazabilidad:** RF-06; RNF-03; Minuta 03.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. La Comisión solicita publicar asignaciones de tutores.
2. El sistema verifica autorización de Comisión.
3. El sistema valida que existan grupos con tutor asignado.
4. El sistema marca las asignaciones como publicadas.
5. El sistema notifica al grupo correspondiente.

**Flujos alternativos**

- Si un grupo inscripto no tiene tutor asignado, queda fuera de la publicación y se informa a Comisión.

### CU-06 Cargar versión preliminar

**Actor principal:** Estudiante.  
**Trazabilidad:** RF-07; RNF-04; Minuta 04.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. El estudiante solicita cargar la versión preliminar.
2. El sistema recupera el grupo del estudiante.
3. El estudiante ingresa título, problema, objetivo general y alcance.
4. El sistema valida que los campos mínimos estén completos.
5. El sistema registra la versión y cambia el estado a En elaboración de anteproyecto.

**Flujos alternativos**

- Si falta alguno de los campos mínimos, el sistema informa errores y conserva el estado anterior.

### CU-07 Registrar observaciones

**Actor principal:** Tutor.  
**Trazabilidad:** RF-08; RNF-04; Minuta 05.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. El tutor selecciona un grupo asignado.
2. El sistema verifica que el tutor esté asignado al grupo.
3. El tutor ingresa la observación breve.
4. El sistema registra observación, fecha y responsable.
5. El sistema deja la observación disponible para estudiantes y Comisión.

**Flujos alternativos**

- Si el tutor no está asignado al grupo, el sistema deniega el registro.

### CU-08 Entregar anteproyecto

**Actor principal:** Estudiante.  
**Trazabilidad:** RF-09, RF-10; RNF-04, RNF-05; Minuta 06.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. El estudiante solicita entregar formalmente el anteproyecto.
2. El sistema obtiene el grupo y la fecha límite del semestre.
3. El sistema valida que la entrega esté en plazo o tenga autorización expresa de Comisión.
4. El sistema registra la entrega formal con fecha y usuario.
5. El sistema cambia el estado del grupo a Anteproyecto entregado.

**Flujos alternativos**

- Si la fecha límite venció y no existe autorización expresa, el sistema bloquea la entrega.

### CU-09 Consultar estado del grupo

**Actor principal:** Estudiante.  
**Trazabilidad:** RF-11; RNF-01, RNF-06; Minuta 05.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. El estudiante solicita consultar el estado de su grupo.
2. El sistema obtiene únicamente el grupo asociado al estudiante.
3. El sistema recupera estado, tutor, fechas clave y observaciones.
4. El sistema muestra la información del grupo propio.

**Flujos alternativos**

- Si el estudiante no tiene grupo en el semestre, el sistema informa que no existe inscripción asociada.

### CU-10 Generar listado de grupos sin entrega

**Actor principal:** Comisión de TFG.  
**Trazabilidad:** RF-12; RNF-06; Minuta 06.  
**Precondición:** el usuario se encuentra autenticado con el rol requerido y existe un semestre de TFG vigente cuando el flujo lo necesita.  
**Postcondición de éxito:** se actualiza o consulta la información correspondiente sin salir del alcance de la primera etapa del TFG.

**Flujo normal**

1. La Comisión solicita el listado de grupos pendientes.
2. El sistema verifica acceso de Comisión.
3. El sistema verifica proximidad a la fecha límite.
4. El sistema selecciona grupos que aún no entregaron anteproyecto.
5. El sistema muestra el listado para recordatorios.

**Flujos alternativos**

- Si no se está cerca del plazo, el sistema puede mostrar el listado con advertencia de oportunidad.


## Matriz de trazabilidad requerimientos-casos de uso

| Requerimiento | Casos de uso que lo cubren |
|---|---|
| RF-01 | CU-01 Configurar semestre |
| RF-02 | CU-02 Inscribir grupo |
| RF-03 | CU-02 Inscribir grupo |
| RF-04 | CU-03 Consultar grupos inscriptos |
| RF-05 | CU-04 Asignar tutor |
| RF-06 | CU-05 Publicar asignación de tutor |
| RF-07 | CU-06 Cargar versión preliminar |
| RF-08 | CU-07 Registrar observaciones |
| RF-09 | CU-08 Entregar anteproyecto |
| RF-10 | CU-08 Entregar anteproyecto |
| RF-11 | CU-09 Consultar estado del grupo |
| RF-12 | CU-10 Generar listado de grupos sin entrega |
| RNF-01 | CU-01 Configurar semestre, CU-09 Consultar estado del grupo |
| RNF-02 | CU-02 Inscribir grupo |
| RNF-03 | CU-01 Configurar semestre, CU-04 Asignar tutor, CU-05 Publicar asignación de tutor |
| RNF-04 | CU-02 Inscribir grupo, CU-04 Asignar tutor, CU-06 Cargar versión preliminar, CU-07 Registrar observaciones, CU-08 Entregar anteproyecto |
| RNF-05 | CU-08 Entregar anteproyecto |
| RNF-06 | CU-03 Consultar grupos inscriptos, CU-09 Consultar estado del grupo, CU-10 Generar listado de grupos sin entrega |

## Microestudio formativo

### Preparación de datos

El subconjunto `G11.tsv` contiene 10 casos anonimizados. Distribución por período: 2024 S2: 1, 2025 S1: 2, 2025 S2: 2, 2026 S1: 3, Otro: 2. La revisión de P1 a P4 encontró:

- P1: faltantes ninguno; inválidos ninguno.
- P2: faltantes ninguno; inválidos ninguno.
- P3: faltantes ninguno; inválidos ninguno.
- P4: faltantes ninguno; inválidos ninguno.

### Resultados descriptivos

| Ítem | Media | Mínimo | Máximo | Frecuencia 1 | Frecuencia 2 | Frecuencia 3 | Frecuencia 4 | Frecuencia 5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 4.70 | 3 | 5 | 0 | 0 | 1 | 1 | 8 |
| P2 | 4.60 | 4 | 5 | 0 | 0 | 0 | 4 | 6 |
| P3 | 4.70 | 4 | 5 | 0 | 0 | 0 | 3 | 7 |
| P4 | 4.50 | 4 | 5 | 0 | 0 | 0 | 5 | 5 |

La claridad percibida es alta en el subconjunto analizado. P1, claridad de etapas, y P3, claridad de plazos y fechas clave, tienen las medias más altas (4.70 y 4.70). P4, claridad del flujo completo, presenta la media más baja (4.50), aunque su mínimo observado es 4. P2, claridad de roles, queda en 4.60; no hay valores menores a 4.

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


## Diagramas UML

### 01. Diagrama general de casos de uso

![](diagramas/01-casos-de-uso-general.svg)

### 02. Diagrama de clases de análisis BCE de CU-01

![](diagramas/01-configurar-semestre-clases-analisis.svg)

### 03. Diagrama de secuencia de CU-01

![](diagramas/01-configurar-semestre-secuencia.svg)

### 04. Diagrama de clases de análisis BCE de CU-02

![](diagramas/02-inscribir-grupo-clases-analisis.svg)

### 05. Diagrama de secuencia de CU-02

![](diagramas/02-inscribir-grupo-secuencia.svg)

### 06. Diagrama de clases de análisis BCE de CU-03

![](diagramas/03-consultar-grupos-inscriptos-clases-analisis.svg)

### 07. Diagrama de secuencia de CU-03

![](diagramas/03-consultar-grupos-inscriptos-secuencia.svg)

### 08. Diagrama de clases de análisis BCE de CU-04

![](diagramas/04-asignar-tutor-clases-analisis.svg)

### 09. Diagrama de secuencia de CU-04

![](diagramas/04-asignar-tutor-secuencia.svg)

### 10. Diagrama de clases de análisis BCE de CU-05

![](diagramas/05-publicar-asignacion-tutor-clases-analisis.svg)

### 11. Diagrama de secuencia de CU-05

![](diagramas/05-publicar-asignacion-tutor-secuencia.svg)

### 12. Diagrama de clases de análisis BCE de CU-06

![](diagramas/06-cargar-version-preliminar-clases-analisis.svg)

### 13. Diagrama de secuencia de CU-06

![](diagramas/06-cargar-version-preliminar-secuencia.svg)

### 14. Diagrama de clases de análisis BCE de CU-07

![](diagramas/07-registrar-observaciones-clases-analisis.svg)

### 15. Diagrama de secuencia de CU-07

![](diagramas/07-registrar-observaciones-secuencia.svg)

### 16. Diagrama de clases de análisis BCE de CU-08

![](diagramas/08-entregar-anteproyecto-clases-analisis.svg)

### 17. Diagrama de secuencia de CU-08

![](diagramas/08-entregar-anteproyecto-secuencia.svg)

### 18. Diagrama de clases de análisis BCE de CU-09

![](diagramas/09-consultar-estado-grupo-clases-analisis.svg)

### 19. Diagrama de secuencia de CU-09

![](diagramas/09-consultar-estado-grupo-secuencia.svg)

### 20. Diagrama de clases de análisis BCE de CU-10

![](diagramas/10-generar-listado-sin-entrega-clases-analisis.svg)

### 21. Diagrama de secuencia de CU-10

![](diagramas/10-generar-listado-sin-entrega-secuencia.svg)

### 22. Diagrama de estados del grupo TFG

![](diagramas/22-estados-grupo-tfg.svg)

### 23. Diagrama de clases persistentes

![](diagramas/23-clases-persistentes.svg)

### 24. Diagrama entidad-relación

![](diagramas/24-entidad-relacion.svg)

### 25. Diagrama de actividades del proceso inicial del TFG

![](diagramas/25-actividades-proceso-inicial-tfg.svg)

## Consistencia entre modelos

Los diagramas mantienen la cadena de trazabilidad Minuta -> RF/RNF -> CU -> clases BCE -> secuencia -> estados/diseño. Las secuencias referencian operaciones canónicas mediante comentarios `op:` validados por `tpf/diagramas/overarch/validate_sequence_refs.py`. El estado del grupo usado en análisis y diseño respeta los cinco estados de RF-10 y no agrega estados de etapas posteriores.
