---
Title: Zk Diagrama de Máquina de Estados y Otros Diagramas UML
TipoNota: permanente
Fecha: 2026-05-26
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
  - uml
  - diagramaDeEstados
dg-publish: true
publish: true
aliases:
  - Relación entre Diagramas de Estados y Otros Diagramas UML
  - Estados y Otras Vistas UML
  - Máquinas de Estado en el Conjunto UML
---
## Diagrama de Máquina de Estados y Otros Diagramas UML

El diagrama de máquina de estados se articula con otros diagramas UML porque cada vista enfatiza un aspecto distinto del sistema. Su aporte específico es mostrar comportamiento dependiente del estado; por ello debe complementarse, no confundirse, con diagramas que representan estructura, interacción o flujo de trabajo ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

| Diagrama | Relación Principal | Precaución Conceptual |
| --- | --- | --- |
| Casos de uso | Aportan escenarios, eventos candidatos y reglas funcionales. | No todo escenario se transforma directamente en estado. |
| Clases | Las máquinas de estado pueden asociarse a instancias de clases o clasificadores. | Un estado no debe confundirse con una clase. |
| Actividades | Ayudan a comprender flujos de trabajo y procesos. | Un flujo de actividades no equivale a comportamiento dependiente de estado. |
| Secuencia | Muestran mensajes entre objetos en una interacción temporal. | Una secuencia no muestra todo el ciclo de vida de un objeto. |
| Comunicación | Expresan vínculos e intercambio de mensajes entre objetos. | Los mensajes pueden disparar eventos, pero no sustituyen la máquina de estados. |

### Tesis

La máquina de estados responde principalmente a la pregunta: “¿cómo cambia el comportamiento de esta entidad a lo largo de su vida?”. Otros diagramas responden preguntas distintas: “¿qué estructura tiene el sistema?”, “¿qué actores interactúan con él?”, “¿qué mensajes se intercambian?” o “¿qué flujo de trabajo se sigue?”. La complementariedad entre diagramas es una de las razones por las que UML se organiza como un lenguaje de múltiples vistas y no como una única representación universal ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Enlaces Sugeridos

- [[Zk Diagrama de Máquina de Estados UML|Diagrama de Máquina de Estados UML]]
- [[Zk Estado en UML|Estado]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
