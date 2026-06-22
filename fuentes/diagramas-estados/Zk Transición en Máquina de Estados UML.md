---
Title: Zk Transición en Máquina de Estados UML
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
  - Transición UML
  - Cambio de Estado
  - Transición de Máquina de Estados
---
## Transición en Máquina de Estados UML

Una transición representa un cambio posible entre estados dentro de una máquina de estados. En su forma didáctica más usual, se expresa como `evento [guarda] / efecto`, aunque una formulación más cercana a UML distingue entre disparador, guarda y efecto ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

La transición no debe leerse como una flecha decorativa, sino como una regla de comportamiento. Indica bajo qué circunstancias una entidad puede abandonar un estado, activar otro y ejecutar un comportamiento asociado. En este sentido, una transición combina una posibilidad de cambio con una restricción y una consecuencia observable.

### Estructura

```text
disparador [guarda] / efecto
```

- **Disparador**: ocurrencia que puede iniciar la transición.
- **Guarda**: condición booleana que debe cumplirse para que la transición se habilite.
- **Efecto**: comportamiento ejecutado cuando la transición se dispara efectivamente.

### Ejemplo

```text
pagoConfirmado [montoPagado = totalFactura] / cerrarFactura
```

Este ejemplo indica que el evento `pagoConfirmado` sólo conduce al cierre de la factura si se cumple la condición de pago completo. El efecto `cerrarFactura` se ejecuta como consecuencia de la transición.

### Enlaces Sugeridos

- [[Zk Evento en Máquina de Estados UML|Evento]]
- [[Zk Guardia en Máquina de Estados UML|Guardia]]
- [[Zk Efecto de Transición en UML|Efecto de Transición]]
- [[Zk Pruebas Basadas en Máquinas de Estado|Pruebas Basadas en Máquinas de Estado]]
