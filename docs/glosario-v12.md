# Glosario común v12 (Manual de Análisis y Modelo de Diseño de Ctrl+)

Todos los diagramas y textos usan estos términos. Si un diagrama necesita otro, se agrega aquí antes.

## Fuente de verdad
- Texto de los CU: `/mnt/project-files/entregas/v12-armado/ctrl-documentacion-v12.md` (§5 dominio, §6 reglas, §7 estados, §8 CU numerados 1 al 16, §10 decisiones). Ya está renumerado.
- Plantilla del profesor: `TPF 04 - Modelo de Análisis-plantilla-base.docx`. No se agregan secciones.
- Notación y reglas: `docs/catedra/reglas-uml.md` y `docs/uml-subset.md` del repo.

## Subsistemas (solo tres)
**ERP**, **ECMS** y **Motor de finanzas**. Son módulos de una misma aplicación web.
- «Documentación técnica», «estructura de trabajo», «presupuestos» y «documentación de obra» son **áreas** de un subsistema, no subsistemas.
- Un actor **nunca** es un subsistema ni un paquete, y un subsistema nunca es un actor.
- Speckle e IfcOpenShell no son actores ni subsistemas: son servicios externos de apoyo. En secuencia se dibujan como participantes con el nombre del rol (por ejemplo `Visor de modelos`, `Lector IFC`).

## Actores (solo dos, más el abstracto)
**Administrador** e **Ingeniero de obra**; ambos especializan al actor abstracto **Usuario**.
- Finanzas y tesorería **sale del sistema**: no aparece en ningún diagrama ni texto.
- Cliente (comitente) y Subcontratista no son actores: son datos del catálogo (`Cliente`, `Proveedor` de tipo subcontratista).

## Numeración de los CU (nueva, en orden de dependencia)
CU-01 Gestionar obra · CU-02 Mantener catálogos · CU-03 Cargar el presupuesto del cliente · CU-04 Validar y finalizar el presupuesto del cliente · CU-05 Armar y versionar el presupuesto de costos · CU-06 Registrar contrato de subcontratista · CU-07 Medir el avance del certificado · CU-08 Calcular el certificado · CU-09 Liquidar subcontratista · CU-10 Gestionar la documentación de la obra · CU-11 Importar la carpeta existente de la obra · CU-12 Publicar y revisar una versión de modelo · CU-13 Calcular el cómputo del modelo · CU-14 Vincular la estructura de trabajo con el modelo y los documentos · CU-15 Abrir, asignar y cerrar una incidencia · CU-16 Consultar el tablero y la actividad de la obra.

Equivalencia con la v11 y con el md anterior (antes → ahora): 01→01, 05→02, 02→03, 16→04, 03→05, 09→06, 04→07, 06→08, 12→09, 19→10, 20→11, 21→12, 22→13, 24→14, 23→15, 13→16.

## Subsistema de cada CU
| CU | Principal | Participa |
|---|---|---|
| 01, 02, 06 | ERP | — |
| 03, 04, 05, 07 | ECMS | ERP (la obra) |
| 08 | Motor de finanzas | ECMS, ERP |
| 09 | ECMS (orquesta) | ERP (datos del contrato), Motor de finanzas (calcula y registra) |
| 10, 11 | ERP | ECMS (documentación técnica) |
| 12, 15 | ECMS (documentación técnica) | ERP |
| 13 | ECMS (presupuestos) | ECMS (documentación técnica) |
| 14 | ECMS (estructura de trabajo) | ECMS (documentación técnica), ERP (documentación de obra) |
| 16 | ECMS | ERP (la obra) |

## Términos fijos
- **Estructura de trabajo** = en el MVP, la versión vigente del presupuesto de costos (rubros e ítems de código estable, sin costo).
- **Presupuesto del cliente**, **Versión del presupuesto de costos**, **Rubro**, **Ítem**, **Medición**, **Medición de ajuste**, **Certificado**, **Versión del certificado**, **Línea del certificado**, **Liquidación**, **Contrato**, **Ítem del contrato**, **Obra**, **Asignación**, **Organización**, **Usuario**, **Cliente**, **Proveedor** (tipo subcontratista), **Documento**, **Carpeta**, **Modelo**, **Versión de modelo**, **Vínculo**, **Incidencia**: nombres de clase tal como en §5 del md.
- Estados con el nombre del md §7 (por ejemplo *En ejecución*, *Recepción provisoria*, *Vigente*, *Histórica*, *Bloqueado*, *En trabajo*, *Compartido*, *Publicado*, *Archivado*, *Abierta*, *En curso*, *Resuelta*, *Cerrada*, *Descartada*).
- Se escribe «versión del certificado» y «presupuesto de costos», nunca «cert.» ni «PC».
- Montos en guaraníes enteros (PYG).

## Reglas de los diagramas
- Un `.puml` por diagrama: `CU-XX-<tipo>[-n-<detalle>].puml`, con la numeración nueva. Tipos: `clases`, `secuencia`, `estados`, `actividades`.
- Estilo celeste de `CU-01-clases.puml` (`!theme plain`, fondo `#F5F8FA`, borde `#17324D`, encabezado `#EAF2F6`), `title CU-XX · <nombre>`.
- Cada CU tiene un diagrama de clases y uno de secuencia como mínimo; estados o actividades solo si agregan algo.
- Los mensajes de la secuencia son métodos de las clases del diagrama de clases del mismo CU (lo verifica `tools/check_consistencia.py`).
- Controles antes de entregar: `plantuml -checkonly diagramas/CU-XX-*.puml`, `python3 tools/check_consistencia.py`, `bash tools/check_calidad.sh`, `python3 tools/check_uml.py`.
- Nada de Finanzas y tesorería, adendas, ACU, gastos, facturas, cobros ni pagos: son fase 2.
