# Glosario de Ctrl+ (fuente de verdad)

Todo texto y todo diagrama usan estos nombres. Un término nuevo entra aquí en
la misma iteración del CU que lo necesita. La columna «No usar» lista los
sinónimos prohibidos.

## Actores

| Término | Definición | No usar |
|---|---|---|
| Usuario | Actor abstracto: persona de la organización que entra a Ctrl+. | — |
| Administrador | Usuario que administra la empresa en Ctrl+: crea obras, asigna ingenieros, mantiene catálogos. Rol de la organización. | administrador técnico |
| Ingeniero de obra | Usuario que trabaja en una obra a la que está asignado. Rol en la obra. | responsable, miembro, integrante |
| Servidor BIM | Sistema externo, actor secundario de CU-12: recibe las publicaciones de los conectores de los programas de modelado y sirve el visor 3D. | Speckle (no se nombra el producto) |

Cliente y Proveedor **no** son actores: son datos del catálogo.

**Alcance:** Ctrl+ está hecho para una sola empresa (organización) (PR-02) y
delega la autenticación de los usuarios en un servicio externo (PR-09). Por eso
no hay casos de uso de inicio de sesión ni de registro: en los CU aparece solo
como precondición, «el usuario inició sesión».

## Subsistemas

Módulos de la misma aplicación web. No son actores. En los diagramas de clases
son paquetes.

| Término | Responsabilidad |
|---|---|
| ERP | Organización, usuarios, obras, catálogos, contratos, documentación de la obra. |
| ECMS | Presupuestos, estructura de trabajo, mediciones, modelos, incidencias. |
| Motor de finanzas | Cálculo de las versiones del certificado y de las liquidaciones. |

## Clases y estados

Se completa a medida que se cierran los CU. «Desde» indica el CU que la introduce.

| Clase | Subsistema | Definición | Desde | Estados |
|---|---|---|---|---|
| Organización | ERP | La constructora. Hay una sola. | CU-01 | — |
| Obra | ERP | Proyecto de construcción con código único, cliente, fechas, tasa de IVA, anticipo y fondo de reparo. | CU-01 | En ejecución, Recepción provisoria, Recepción definitiva, Cerrada |
| Anticipo | ERP | Adelanto opcional de una obra, por porcentaje o por importe, que cada versión del certificado amortiza. | CU-01 | — |
| Asignación | ERP | Vínculo de un Ingeniero de obra con una obra, con actor y fecha. | CU-01 | — |
| Cliente | ERP | Comitente de una obra, en el catálogo, identificado por RUC. | CU-01 (se mantiene en CU-02) | Activo, Inactivo |
| Carpeta de la obra | ERP | Carpeta compartida de una obra; nace con las carpetas principales de la plantilla de la empresa. | CU-01 (se trabaja en CU-10 y CU-11) | — |

## Términos generales

| Término | Definición | No usar |
|---|---|---|
| Asignar | Dar a un Ingeniero de obra acceso a una obra. | dar membresía |
| Avanzar el estado | Pasar la obra a su estado siguiente, sin volver atrás. | cambiar de fase |
| Actor y fecha | Quién hizo una operación y cuándo; se guarda en toda operación (NF-03). | auditoría (en el texto de un CU) |
| Montos | Guaraníes enteros (PYG). | — |
| Parámetros del certificado | Tasa de IVA, porcentaje de fondo de reparo y anticipo de una obra; los fija CU-01 y los usa CU-08. | impuestos de la obra |
| Desde cero / proyecto ya aprobado | Las dos formas de iniciar una obra en CU-01. | — |
