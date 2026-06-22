---
Title: Zk Diagrama de Máquina de Estados UML
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
  - Diagrama de Máquina de Estados UML
  - Diagrama de Estados UML
  - State Machine Diagram
---
## Diagrama de Máquina de Estados UML

Un diagrama de máquina de estados UML representa el comportamiento de una entidad cuyo modo de responder a los eventos depende de su estado actual. Su utilidad aparece con mayor claridad cuando un mismo estímulo puede producir efectos distintos según la situación interna del objeto, componente, subsistema o sistema modelado ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

La idea central no consiste sólo en listar estados, sino en mostrar qué transiciones son válidas, qué eventos las disparan, qué guardas las habilitan y qué efectos se producen cuando la transición ocurre. Esta forma de modelar procede de una tradición más amplia de sistemas reactivos y statecharts, donde la jerarquía, la concurrencia y los cambios dependientes del contexto permiten representar comportamientos más ricos que los autómatas planos simples ([[Zk Ref harelStatechartsVisualFormalism1987|Harel, 1987]]).

### Distinción Conceptual

- **Hecho consolidado**: UML reconoce las máquinas de estado como diagramas de comportamiento orientados a representar estados, transiciones, eventos y comportamiento asociado ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).
- **Aclaración terminológica**: en materiales introductorios puede usarse “diagrama de estados” como nombre abreviado, pero el nombre técnico formal es “diagrama de máquina de estados”.

### Criterio de Uso

Conviene usar una máquina de estados cuando el comportamiento de una entidad no depende sólo del evento recibido, sino también de la condición o situación en la que esa entidad se encuentra. En cambio, si lo central es representar un flujo de trabajo, una secuencia de actividades o una interacción entre varios objetos, pueden ser más adecuados los [[Zk Modelo Conceptual del UML (Diagrama de Actividades)|diagramas de actividades]] o de [[Zk Modelo Conceptual del UML (Diagrama de Secuencia)|secuencia]].

### Enlaces Sugeridos

- [[Zk Comportamiento Dependiente del Estado|Comportamiento Dependiente del Estado]]
- [[Zk Estado en UML|Estado en UML]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Diagrama de Máquina de Estados y Otros Diagramas UML|Relación con Otros Diagramas UML]]
- [[Zk Pruebas Basadas en Máquinas de Estado|Pruebas Basadas en Máquinas de Estado]]
