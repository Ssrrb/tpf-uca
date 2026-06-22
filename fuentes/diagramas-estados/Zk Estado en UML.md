---
Title: Zk Estado en UML
TipoNota: permanente
Fecha: 2026-05-26
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
  - diagramaDeEstados
  - uml
dg-publish: true
publish: true
aliases:
  - Estado UML
  - Estado en una Máquina de Estados
  - Situación Conductual
---
## Estado en UML

Un estado representa una situación durante la vida de una entidad en la que esta satisface alguna condición, espera ciertos eventos o ejecuta alguna actividad. En una máquina de estados UML, el estado no es un simple valor de atributo: es una abstracción conductual que permite explicar cómo la entidad puede responder a eventos futuros ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

Un buen estado debe ser significativo para el comportamiento del modelo. Si dos situaciones no modifican las transiciones posibles, las guardas relevantes o los efectos esperados, probablemente no convenga separarlas como estados distintos. Esta decisión exige interpretar el dominio, no sólo traducir sustantivos a cajas de un diagrama.

### Criterios para Identificar Estados

- **Estabilidad relativa**: el estado describe una situación que puede mantenerse durante cierto tiempo lógico.
- **Diferencia conductual**: la entidad responde de modo diferente a ciertos eventos.
- **Relevancia del dominio**: el nombre del estado tiene sentido para usuarios, analistas o diseñadores.
- **Trazabilidad**: el estado puede justificarse a partir de requisitos, reglas de negocio o restricciones técnicas.

### Ejemplos

- `Borrador`, `Emitida`, `Cobrada` en una factura.
- `Registrado`, `Pagado`, `Preparado`, `Entregado` en un pedido.
- `Activo`, `Suspendido`, `Cerrado` en una cuenta.

### Enlaces Sugeridos

- [[Zk Estado Inicial y Estado Final en UML|Estado Inicial y Estado Final]]
- [[Zk Estado Compuesto en UML|Estado Compuesto]]
- [[Zk Actividades Entry Exit y Do en UML|Actividades Entry, Exit y Do]]
- [[Zk Errores Frecuentes en Diagramas de Máquina de Estados UML|Errores Frecuentes]]
