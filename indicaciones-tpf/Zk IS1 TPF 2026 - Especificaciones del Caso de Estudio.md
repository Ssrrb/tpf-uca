---
Title: Zk IS1 TPF 2026 - Especificaciones del Caso de Estudio
TipoNota: permanente
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - definir
tags:
  - definir
dg-publish: false
publish: true
aliases:
  - Especificaciones del Caso de Estudio
---
## Especificaciones del Caso de Estudio

### Introducción

El trabajo se centra en el análisis y modelado de un sistema de gestión del Trabajo Final de Grado (TFG) para la carrera de Licenciatura en Análisis de Sistemas Informáticos. El caso se construye a partir de la operativa institucional de tesis publicada por el Departamento de Análisis de Sistemas, donde se indica que el proceso incluye una reunión inicial del semestre, la inscripción a la asignatura, la inscripción de grupos y un período inicial de aproximadamente cuarenta días destinado a la elaboración del anteproyecto.

Para mantener un alcance adecuado a la asignatura IS1, este caso de estudio se limita a la **primera parte** del proceso: desde la apertura del semestre hasta la entrega del anteproyecto. No se abordarán en esta instancia las etapas posteriores de dictamen, defensa o cierre del TFG. Esta delimitación busca, además, mostrar pedagógicamente que un sistema puede construirse por partes, incrementos o iteraciones, y no necesariamente en una única especificación exhaustiva.

El problema actual radica en que el proceso inicial del TFG involucra múltiples actores, plazos y actividades que suelen gestionarse mediante comunicaciones dispersas, formularios separados y seguimiento informal. Esto puede generar dudas sobre requisitos de inscripción, composición de grupos, asignación de tutor, cumplimiento de fechas y estado de elaboración del anteproyecto.

El sistema propuesto busca centralizar y dar trazabilidad a esa primera etapa, permitiendo que estudiantes, Comisión de TFG y tutores dispongan de una visión clara del proceso. El caso fue deliberadamente diseñado con complejidad moderada, de modo que los estudiantes puedan ejercitar la mecánica del análisis: derivar requerimientos desde minutas de reuniones, identificar actores, redactar casos de uso, construir modelos de clases, secuencia, actividades y, cuando corresponda, estados.

### Aplicación del Ciclo de Vida del Desarrollo del Software (SDLC)

La especificación de las fases (Identificación del Problema, Planificación del Proyecto y Captura de Requerimientos) del [[Zk Ciclo de Vida del Desarrollo del Software (SDLC)|SDLC]] será provista como insumo del trabajo. El estudiante deberá concentrarse en la fase de análisis, construyendo los modelos UML a partir de requerimientos, reglas del dominio y minutas de reunión. La intención es que el alumno practique el pasaje ordenado desde necesidades expresadas informalmente por stakeholders hacia requerimientos funcionales y no funcionales, y desde éstos hacia modelos de análisis coherentes.

#### Fase 1: Identificación del Problema

##### Contexto

Cada semestre, la carrera inicia el proceso de TFG con una reunión de lanzamiento y con un conjunto de actividades administrativas y académicas que los estudiantes deben completar dentro de fechas preestablecidas. Entre esas actividades se encuentran la inscripción académica, la inscripción del grupo, la asignación de tutor y la elaboración del anteproyecto durante el período inicial del semestre.

Actualmente, estas actividades se encuentran fragmentadas en distintos canales y dependen en gran medida de recordatorios manuales, consultas informales y seguimiento personal de la comisión. Como consecuencia, algunos estudiantes no tienen claridad sobre el orden de las actividades, las fechas clave, la información requerida para registrar su grupo o el estado de la asignación de tutor. Además, la comisión necesita un mecanismo más ordenado para registrar grupos, asignar tutores y monitorear entregas.

Se requiere, por tanto, un sistema que permita gestionar de forma centralizada la primera etapa del TFG, con foco en inscripción, conformación de grupos, asignación de tutor, seguimiento del anteproyecto y consulta del estado general del proceso.

##### Actores Identificados

- **Estudiante:** realiza la inscripción del grupo, consulta fechas, registra datos del anteproyecto y revisa el estado de su proceso.
- **Comisión de TFG:** configura el semestre, administra grupos, asigna tutores, controla plazos y verifica entregas.
- **Tutor:** realiza seguimiento del grupo asignado y registra observaciones sobre el avance del anteproyecto.
- **Secretaría Académica:** interviene en la inscripción académica a la asignatura, según el flujo operativo de tesis.

#### Fase 2: Planificación del Proyecto

##### Alcance

El proyecto cubre desde la apertura del semestre de TFG hasta la entrega del anteproyecto. En esta iteración no se incluyen dictámenes, presentaciones formales, defensa ni cierre del TFG. El entregable de las fases 1 a 3 será la base para que los estudiantes elaboren el análisis detallado del sistema por medio del modelado fundamentalmente utilizando UML.

##### Cronograma

| Semana | Actividad                                                | Entregable                                     |
|:------:| -------------------------------------------------------- | ---------------------------------------------- |
|   1    | Revisión del caso, actores y contexto institucional      | Lista inicial de actores y eventos del proceso |
|  1–2   | Revisión de minutas y derivación de requerimientos       | Lista preliminar de RF y RNF                   |
|  1–3   | Refinamiento de requerimientos y validación interna      | Especificación consolidada de RF y RNF         |
|  1–2   | Aplicación del microestudio y lectura descriptiva mínima | Síntesis del microestudio                      |
|  1–3   | Modelado UML y consolidación del TPF                     | Documento final del TPF                        |

##### Riesgos y Mitigaciones

| Riesgo                                                                    | Mitigación                                                                 |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Los estudiantes perciben el caso como demasiado amplio                    | Delimitar explícitamente el alcance solo hasta la entrega del anteproyecto |
| Las minutas no contienen suficiente detalle para especificar casos de uso | Redactar minutas con actores, datos, reglas y restricciones observables    |
| Dificultad para relacionar requerimientos con modelos UML                 | Exigir trazabilidad entre minuta, RF/RNF, caso de uso y modelo asociado    |
| Confusión entre ejercicio formativo e investigación concluyente           | Mantener advertencias metodológicas explícitas sobre el microestudio       |
*Nota:* Este apartado tiene un objetivo solo pedagógico, para indicar que en proyectos reales deben considerarse los riesgos.

#### Fase 3: Captura de Requerimientos

##### Requerimientos Funcionales (RF)

| ID    | Requerimiento funcional                                                                                                                                                                                                    | Minuta de reunión asociada                                          |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| RF-01 | El sistema debe permitir a la Comisión de TFG registrar el semestre de TFG con sus fechas claves: reunión inicial, fecha tope de inscripción de grupos, publicación de tutores y fecha límite de entrega del anteproyecto. | [[#Minuta 01 - Reunión Inicial del Proceso\|Minuta 01]]             |
| RF-02 | El estudiante debe poder registrar la inscripción de su grupo indicando nombre tentativo del tema, integrantes y datos de contacto.                                                                                        | [[#Minuta 02 - Inscripción de Grupos\|Minuta 02]]                   |
| RF-03 | El sistema debe validar que un estudiante no pueda pertenecer a más de un grupo de TFG en el mismo semestre.                                                                                                               | [[#Minuta 02 - Inscripción de Grupos\|Minuta 02]]                   |
| RF-04 | La Comisión de TFG debe poder consultar la lista de grupos inscriptos con estado de completitud y cantidad de integrantes.                                                                                                 | [[#Minuta 03 - Gestión de Grupos y Asignación de Tutor\|Minuta 03]] |
| RF-05 | La Comisión de TFG debe poder asignar un tutor a cada grupo inscripto antes de la fecha de publicación definida.                                                                                                           | [[#Minuta 03 - Gestión de Grupos y Asignación de Tutor\|Minuta 03]] |
| RF-06 | El sistema debe permitir publicar la asignación de tutor y notificar al grupo correspondiente.                                                                                                                             | [[#Minuta 03 - Gestión de Grupos y Asignación de Tutor\|Minuta 03]] |
| RF-07 | El grupo debe poder cargar una versión preliminar del anteproyecto con título, problema, objetivo general y alcance.                                                                                                       | [[#Minuta 04 - Carga Inicial del Anteproyecto\|Minuta 04]]          |
| RF-08 | El tutor debe poder registrar observaciones sobre el avance del anteproyecto durante el período de elaboración.                                                                                                            | [[#Minuta 05 - Seguimiento Tutorial\|Minuta 05]]                    |
| RF-09 | El grupo debe poder entregar formalmente el anteproyecto antes de la fecha límite establecida por la Comisión.                                                                                                             | [[#Minuta 06 - Entrega Formal del Anteproyecto\|Minuta 06]]         |
| RF-10 | El sistema debe cambiar el estado del grupo según el avance de la primera etapa: pendiente de inscripción, inscripto, tutor asignado, en elaboración de anteproyecto, anteproyecto entregado.                              | [[#Minuta 06 - Entrega Formal del Anteproyecto\|Minuta 06]]         |
| RF-11 | El estudiante debe poder consultar en cualquier momento el estado de su grupo, tutor asignado, fechas clave y observaciones registradas.                                                                                   | [[#Minuta 05 - Seguimiento Tutorial\|Minuta 05]]                    |
| RF-12 | La Comisión de TFG debe poder generar un listado de grupos que aún no entregaron su anteproyecto al acercarse la fecha límite.                                                                                             | [[#Minuta 06 - Entrega Formal del Anteproyecto\|Minuta 06]]         |

##### Requerimientos No Funcionales (RNF)

| ID     | Requerimiento no funcional                                                                                                                            | Minuta de reunión asociada                                                                                            |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| RNF-01 | La interfaz debe presentar de forma clara las etapas y fechas clave del proceso inicial del TFG.                                                      | [[#Minuta 01 - Reunión Inicial del Proceso\|Minuta 01]]                                                               |
| RNF-02 | El sistema debe ser accesible vía web desde dispositivos de escritorio y móviles.                                                                     | [[#Minuta 02 - Inscripción de Grupos\|Minuta 02]]                                                                     |
| RNF-03 | Solo la Comisión de TFG puede modificar fechas del semestre y asignaciones de tutores.                                                                | [[#Minuta 03 - Gestión de Grupos y Asignación de Tutor\|Minuta 03]]                                                   |
| RNF-04 | El sistema debe registrar fecha y usuario responsable en las acciones de inscripción, asignación, observación y entrega.                              | [[#Minuta 05 - Seguimiento Tutorial\|Minuta 05]]                                                                      |
| RNF-05 | La entrega del anteproyecto debe quedar bloqueada automáticamente una vez vencida la fecha límite, salvo habilitación expresa de la Comisión.         | [[#Minuta 06 - Entrega Formal del Anteproyecto\|Minuta 06]]                                                           |
| RNF-06 | Los estudiantes solo deben poder consultar la información de su propio grupo, mientras que la Comisión puede consultar todos los grupos del semestre. | [[#Minuta 03 - Gestión de Grupos y Asignación de Tutor\|Minuta 03]], [[#Minuta 05 - Seguimiento Tutorial\|Minuta 05]] |

### Anexo I – Minutas de Reunión

Las minutas de reunión que integran este anexo constituyen el insumo de partida para el análisis del caso, especialmente para la identificación de actores, la derivación de requerimientos y la especificación de casos de uso. Aunque han sido formuladas de manera breve y deliberadamente simple por tratarse de un ejercicio didáctico, contienen la información suficiente para elaborar el trabajo requerido.

#### Minuta 01 - Reunión Inicial del Proceso

**Participantes:** Comisión de TFG, Analista, Desarrollador  
**Temas tratados:**

- Cada semestre inicia con una reunión de lanzamiento del TFG.
- La Comisión necesita cargar y publicar las fechas importantes del semestre para evitar confusiones.
- Las fechas mínimas a publicar son: reunión inicial, cierre de inscripción de grupos, publicación de tutores y fecha límite de entrega del anteproyecto.
- Los estudiantes deben poder consultar fácilmente estas fechas desde el sistema.
- La pantalla inicial del proceso debe mostrar con claridad las etapas de esta primera parte del TFG.

**Requerimientos derivados:**

- Registrar semestre y fechas clave.
- Publicar cronograma del proceso inicial.
- Presentar etapas y plazos con claridad.

#### Minuta 02 - Inscripción de Grupos

**Participantes:** Estudiantes, Comisión de TFG, Analista  
**Temas tratados:**

- La inscripción se realiza por grupo, no por estudiante individual aislado.
- Cada grupo puede tener entre 1 y 3 integrantes.
- Al momento de inscribirse, deben registrar un tema tentativo y un medio de contacto.
- Un estudiante no puede figurar en dos grupos distintos del mismo semestre.
- Muchos estudiantes realizan estas gestiones desde el teléfono; por ello, el sistema debe funcionar correctamente también en dispositivos móviles.

**Requerimientos derivados:**

- Registrar grupo con integrantes, tema tentativo y contacto.
- Validar unicidad de pertenencia por semestre.
- Garantizar acceso web móvil.

#### Minuta 03 - Gestión de Grupos y Asignación de Tutor

**Participantes:** Comisión de TFG, Analista, Desarrollador  
**Temas tratados:**

- La Comisión necesita una lista de grupos inscriptos donde pueda ver cantidad de integrantes, tema tentativo y estado de inscripción.
- Solo la Comisión puede asignar tutores.
- La asignación debe publicarse en una fecha definida del cronograma del semestre.
- Una vez asignado el tutor, el grupo debe quedar notificado.
- Los estudiantes solo deben ver la información de su propio grupo; la Comisión necesita ver todos.

**Requerimientos derivados:**

- Consultar grupos inscriptos.
- Asignar tutor.
- Publicar y notificar asignación.
- Restringir accesos según rol.

#### Minuta 04 - Carga Inicial del Anteproyecto

**Participantes:** Estudiantes, Tutor, Analista  
**Temas tratados:**

- Al iniciar el trabajo con el tutor, el grupo debe cargar una versión preliminar del anteproyecto.
- En esta primera versión bastará con registrar título, problema, objetivo general y alcance.
- No se busca aún una versión final, sino un insumo inicial para la orientación del tutor.
- Esta información debe quedar disponible para posteriores revisiones.

**Requerimientos derivados:**

- Registrar versión preliminar del anteproyecto.
- Almacenar datos básicos del anteproyecto.
- Permitir acceso del tutor a dicha información.

#### Minuta 05 - Seguimiento Tutorial

**Participantes:** Tutor, Comisión de TFG, Analista  
**Temas tratados:**

- Durante el período de elaboración, el tutor debe poder dejar observaciones breves sobre el avance del grupo.
- Los estudiantes deben poder consultar esas observaciones para corregir o mejorar su trabajo.
- Toda observación debe quedar registrada con fecha y responsable.
- La Comisión quiere poder revisar si un grupo ya tiene tutor asignado, si cargó su anteproyecto preliminar y si recibió observaciones.

**Requerimientos derivados:**

- Registrar observaciones tutoriales.
- Consultar observaciones y estado del grupo.
- Registrar fecha y responsable de las acciones.

#### Minuta 06 - Entrega Formal del Anteproyecto

**Participantes:** Comisión de TFG, Tutor, Estudiantes, Analista  
**Temas tratados:**

- El grupo debe poder realizar una entrega formal del anteproyecto antes de la fecha límite del semestre.
- Al concretarse la entrega, el estado del grupo debe cambiar a “Anteproyecto entregado”.
- Si la fecha límite ya venció, el sistema no debe aceptar entregas, salvo autorización expresa de la Comisión.
- La Comisión desea consultar un listado de grupos pendientes de entrega para realizar recordatorios antes del vencimiento.
- El flujo de esta primera etapa termina con la entrega del anteproyecto; las etapas posteriores quedarán fuera del presente trabajo práctico.

**Requerimientos derivados:**

- Entregar formalmente anteproyecto.
- Cambiar estado del grupo.
- Bloquear entregas fuera de plazo.
- Consultar grupos pendientes de entrega.
- Delimitar el alcance del caso a esta primera etapa.