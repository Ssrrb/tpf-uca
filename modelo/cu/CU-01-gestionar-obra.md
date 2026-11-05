# CU-01 · Gestionar obra

> Borrador v1 para revisar. Solo alcance del MVP. Los campos son los de la
> tabla de la plantilla del profesor, en el mismo orden.

| Campo | Contenido |
|---|---|
| **Nombre de Caso de Uso** | Gestionar obra |
| **Versión** | 1.00 |
| **Creado por** | Grupo 7 · 05/11/2026 |
| **Modificado por** | — |
| **Descripción** | El Administrador crea una obra con sus datos y su configuración, y le asigna los Ingenieros de obra que trabajarán en ella. Mientras la obra existe, el Administrador avanza su estado: En ejecución, Recepción provisoria, Recepción definitiva y Cerrada, sin volver atrás. |
| **Actores** | Administrador |
| **Pre Condiciones** | El usuario tiene el rol de Administrador en la organización. |
| **Post Condiciones** | La obra queda registrada en estado En ejecución, con su código, nombre, cliente, fechas, tasa de IVA, fondo de reparo y, si se configuró, su anticipo. Los Ingenieros de obra elegidos quedan asignados a ella. Se registran el actor y la fecha. Si la operación se cancela o falla, la obra no se crea. |

**Flujo Normal**

| Actor | Acción |
|---|---|
| Administrador | 1. Solicita crear una obra. |
| Administrador | 2. Ingresa el código, el nombre, el cliente, las fechas de inicio y de fin, la tasa de IVA y el porcentaje de fondo de reparo. |
| Administrador | 3. Si la obra tiene anticipo, ingresa su porcentaje o su importe. |
| Administrador | 4. Elige los Ingenieros de obra que asigna a la obra. |
| Administrador | 5. Confirma. |
| Sistema | 6. Valida que el código no esté en uso y que los datos estén completos y sean válidos. |
| Sistema | 7. Registra la obra en estado En ejecución, con sus asignaciones, el actor y la fecha. |

**Flujo Alternativo**

| Actor | Acción |
|---|---|
| Administrador | 2a. El cliente no está en el catálogo: lo registra (CU-02 Mantener catálogos) y continúa en el paso 2. |
| Administrador | 5a. Cancela: la obra no se crea y termina el caso de uso. |
| Administrador | \*a1. Elige una obra que no está Cerrada y solicita avanzar su estado. |
| Sistema | \*a2. Muestra el estado actual y el siguiente. |
| Administrador | \*a3. Confirma. |
| Sistema | \*a4. Pasa la obra al estado siguiente y registra el actor y la fecha. Termina el caso de uso. |
| Administrador | \*b1. Elige una obra que no está Cerrada y modifica sus asignaciones: asigna o quita Ingenieros de obra. |
| Sistema | \*b2. Registra las asignaciones nuevas y las que se quitan, con el actor y la fecha. Una asignación quitada no se borra. Termina el caso de uso. |

| **Excepciones** | |
|---|---|
| 6a | El código ya está en uso en la organización: el sistema lo informa y vuelve al paso 2. |
| 6b | Falta un dato obligatorio, la fecha de fin es anterior a la de inicio o un porcentaje no está entre 0 y 100: el sistema marca cada campo y vuelve al paso 2. |
| 6c | El cliente elegido está inactivo en el catálogo: el sistema lo informa y vuelve al paso 2. |
| 7a | Falla el registro: no se guarda nada de la obra ni de sus asignaciones (NF-02) y se puede reintentar. |

| **Requerimientos** | RF-01, RF-22, RF-23, NF-01, NF-02, NF-03 |
|---|---|

## Puntos para que decidas

1. **Estados de la obra.** Uso los cuatro de RF-23 (En ejecución, Recepción
   provisoria, Recepción definitiva, Cerrada). La v12 los mostraba además como
   tres en pantalla (Activa, En recepción, Cerrada); eso es de la interfaz y lo
   saqué del análisis.
2. **Modificar asignaciones (\*b).** Lo agregué porque «gestionar» lo implica y
   un ingeniero puede entrar a la obra después. RF-01 solo habla de asignar al
   crear; si preferís no agregarlo, se quita.
3. **Modificar los datos de la obra** (nombre, fechas, IVA): no lo incluí,
   porque ningún requerimiento lo pide y cambiar el IVA o el anticipo después de
   certificar traería problemas. Decime si lo querés.
4. **Saqué de la v12:** límite de adendas, tope de caja chica, permisos por obra
   («liquidar subcontratistas»), empresas invitadas y agentes de IA, porque son
   de fase 2. La asignación es solo para Ingenieros de obra: el Administrador ve
   todas las obras por su rol.

## Glosario que fija este CU

Organización, Obra, Anticipo, Asignación, Cliente; estados de la Obra. Ver
`modelo/glosario.md`.
