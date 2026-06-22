---
Title: Zk Guardia en Máquina de Estados UML
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
  - Guarda en UML
  - Condición de Transición
  - Condición de Guarda
---
## Guardia en Máquina de Estados UML

Una guarda es una condición booleana que debe evaluarse como verdadera para que una transición pueda dispararse. La guarda no produce por sí misma el cambio de estado; sólo habilita o bloquea una transición ante un evento o disparador determinado ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

En notación UML se escribe entre corchetes. Esta convención permite separar el evento que ocurre de la condición que autoriza la transición, de modo que una misma ocurrencia pueda conducir a resultados distintos según el estado del sistema y las condiciones del dominio.

### Ejemplo

```text
pagoConfirmado [montoPagado = totalFactura] / cerrarFactura
```

En este caso, `pagoConfirmado` es el evento, `[montoPagado = totalFactura]` es la guarda y `cerrarFactura` es el efecto.

### Criterios de Buena Formulación

- La guarda debe ser evaluable como verdadera o falsa.
- Debe evitarse redactarla como una acción.
- Debe expresar una condición relevante para decidir la transición.
- Si varias transiciones comparten el mismo evento, sus guardas deberían ser mutuamente claras y, cuando sea necesario, exhaustivas.

### Enlaces Sugeridos

- [[Zk Evento en Máquina de Estados UML|Evento]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
