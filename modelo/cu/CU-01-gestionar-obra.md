# CU-01 · Gestionar obra

> Borrador v2 para revisar. Solo alcance del MVP. Los campos son los de la
> tabla de la plantilla del profesor, en el mismo orden.
>
> Cambios desde la v1: el CU se presenta como el inicio del proyecto, con dos
> formas de empezar (desde cero o con un proyecto ya aprobado), y explica qué
> deja listo para los certificados.

| Campo | Contenido |
|---|---|
| **Nombre de Caso de Uso** | Gestionar obra |
| **Versión** | 1.01 |
| **Creado por** | Grupo 7 · 05/11/2026 |
| **Modificado por** | Grupo 7 · 06/11/2026 |
| **Descripción** | Es el inicio de cada proyecto en Ctrl+. El Administrador crea la obra con sus datos, su cliente y los parámetros con que se calculará cada versión del certificado (tasa de IVA, fondo de reparo y anticipo), y le asigna los Ingenieros de obra. La obra puede empezar **desde cero**, sin documentos, o a partir de un **proyecto ya aprobado**: en ese caso el Administrador trae la carpeta con los planos y la documentación que ya existen (CU-11 Importar la carpeta existente de la obra). En los dos casos, la obra queda lista para que el Ingeniero de obra cargue el presupuesto del cliente (CU-03), que es la base de los certificados. Mientras la obra existe, el Administrador avanza su estado: En ejecución, Recepción provisoria, Recepción definitiva y Cerrada, sin volver atrás. |
| **Actores** | Administrador |
| **Pre Condiciones** | El usuario inició sesión (PR-09) y tiene el rol de Administrador en la organización. |
| **Post Condiciones** | La obra queda registrada en estado En ejecución, con su código, nombre, cliente, fechas, tasa de IVA, fondo de reparo y, si se configuró, su anticipo. Los Ingenieros de obra elegidos quedan asignados a ella. Si se inició con un proyecto aprobado, su carpeta queda importada en la documentación de la obra. Se registran el actor y la fecha. Si la operación se cancela o falla, la obra no se crea. |

**Flujo Normal**

| Actor | Acción |
|---|---|
| Administrador | 1. Solicita crear una obra. |
| Administrador | 2. Ingresa el código, el nombre, el cliente y las fechas de inicio y de fin. |
| Administrador | 3. Ingresa los parámetros del certificado: la tasa de IVA, el porcentaje de fondo de reparo y, si la obra tiene anticipo, su porcentaje o su importe. |
| Administrador | 4. Elige los Ingenieros de obra que asigna a la obra. |
| Administrador | 5. Indica cómo inicia la obra: desde cero o con un proyecto ya aprobado. |
| Administrador | 6. Confirma. |
| Sistema | 7. Valida que el código no esté en uso y que los datos estén completos y sean válidos. |
| Sistema | 8. Registra la obra en estado En ejecución, con sus asignaciones, el actor y la fecha, y crea su carpeta con las carpetas principales de la plantilla de la empresa. |

**Flujo Alternativo**

| Actor | Acción |
|---|---|
| Administrador | 2a. El cliente no está en el catálogo: lo registra (CU-02 Mantener catálogos) y continúa en el paso 2. |
| Administrador | 6a. Cancela: la obra no se crea y termina el caso de uso. |
| Administrador | 8a. La obra inicia con un proyecto ya aprobado: importa su carpeta con los planos y la documentación (CU-11 Importar la carpeta existente de la obra). Termina el caso de uso. |
| Administrador | \*a1. Elige una obra que no está Cerrada y solicita avanzar su estado. |
| Sistema | \*a2. Muestra el estado actual y el siguiente. |
| Administrador | \*a3. Confirma. |
| Sistema | \*a4. Pasa la obra al estado siguiente y registra el actor y la fecha. Termina el caso de uso. |
| Administrador | \*b1. Elige una obra que no está Cerrada y modifica sus asignaciones: asigna o quita Ingenieros de obra. |
| Sistema | \*b2. Registra las asignaciones nuevas y las que se quitan, con el actor y la fecha. Una asignación quitada no se borra. Termina el caso de uso. |

| **Excepciones** | |
|---|---|
| 7a | El código ya está en uso en la organización: el sistema lo informa y vuelve al paso 2. |
| 7b | Falta un dato obligatorio, la fecha de fin es anterior a la de inicio o un porcentaje no está entre 0 y 100: el sistema marca cada campo y vuelve al paso 2. |
| 7c | El cliente elegido está inactivo en el catálogo: el sistema lo informa y vuelve al paso 2. |
| 8b | Falla el registro: no se guarda nada de la obra, de sus asignaciones ni de su carpeta (NF-02) y se puede reintentar. |

| **Requerimientos** | RF-01, RF-22, RF-23, NF-01, NF-02, NF-03, PR-02, PR-09 |
|---|---|

## Relaciones con otros CU (para el diagrama de casos de uso)

- CU-02 Mantener catálogos `<<extend>>` CU-01 (punto 2a: falta el cliente).
- CU-11 Importar la carpeta existente de la obra `<<extend>>` CU-01 (punto 8a:
  proyecto ya aprobado).
- CU-03 Cargar el presupuesto del cliente **no** es parte de CU-01: lo hace
  otro actor (Ingeniero de obra) y otro día. CU-01 es su precondición.

## Cómo se conecta con los certificados

CU-01 no calcula nada, pero fija los tres parámetros que usa cada versión del
certificado (CU-08): la tasa de IVA, el porcentaje de fondo de reparo y el
anticipo, que se amortiza hasta cancelarse. La cadena completa es:

CU-01 crea la obra → CU-03 y CU-04 cargan y finalizan el presupuesto del
cliente → CU-05 deja la estructura de trabajo vigente → CU-07 mide → CU-08
calcula cada versión del certificado con los parámetros de CU-01.

## Puntos para que decidas

1. **Obra aprobada que ya tiene certificados emitidos fuera de Ctrl+.** Si la
   obra ya avanzó, ¿la primera versión del certificado en Ctrl+ arranca de cero
   o hay que cargar el avance acumulado anterior (y lo amortizado del
   anticipo)? Hoy ningún CU lo cubre. Si lo querés, propongo que sea un flujo
   alternativo de CU-07 («cargar el avance anterior a Ctrl+»), no de CU-01.
2. **Estados de la obra.** Uso los cuatro de RF-23. La v12 los mostraba además
   como tres en pantalla (Activa, En recepción, Cerrada); eso es de la
   interfaz y lo saqué del análisis.
3. **Modificar asignaciones (\*b).** Lo agregué porque un ingeniero puede
   entrar a la obra después. Si preferís no tenerlo, se quita.
4. **Saqué de la v12:** límite de adendas, tope de caja chica, permisos por obra,
   empresas invitadas y agentes de IA, porque son de fase 2.

## Glosario que fija este CU

Organización, Obra, Anticipo, Asignación, Cliente, Carpeta de la obra; estados
de la Obra. Ver `modelo/glosario.md`.
