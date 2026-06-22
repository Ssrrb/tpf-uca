---
Title: Zk Diagramas de Interacción (Introducción)
TipoNota: permanente
Fecha: 2025-05-19 08:20
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
dg-publish: true
publish: true
---
## Diagramas de Interacción (Introducción)

Los **diagramas de interacción** en UML son una familia de diagramas de **comportamiento** destinados a modelar cómo los **objetos** de un sistema **colaboran** a través del **intercambio de mensajes** para lograr un objetivo común. Estos diagramas permiten visualizar la dinámica de las interacciones, mostrando tanto la secuencia como la estructura de los intercambios entre los participantes del sistema ([[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

### Usos de los Diagramas de Interacción

Los diagramas de interacción se utilizan fundamentalmente para [[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|(Booch et al., 2006)]]:

- Analizar y documentar el [[Zk Diagramas UML 2.5.1 (Dinámicos)|comportamiento dinámico]] de un sistema.
- Comprender y comunicar cómo los [[Zk Modelo Conceptual del UML (Diagrama de Objetos)|objetos]] cooperan para ejecutar [[Zk Diagrama de Casos de Uso - Elementos (Caso de Uso)|procesos o casos de uso]].
- Identificar posibles problemas de comunicación, cuellos de botella y optimizar la arquitectura de software.
- Facilitar el diseño, la validación y la mejora de sistemas complejos, especialmente en etapas de análisis y diseño orientado a objetos.

### Tipos de diagramas de interacción en UML

Según la [[Zk Ref omgUnifiedModelingLanguage2017|Especificación del UML del OMG (2017)]] los diagramas más utilizados para modelar interacción de objetos son:

| Diagrama                                                                             | Descripción breve                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [[Zk Diagramas de Interacción (Diagrama de Secuencia)\|Diagrama de Secuencia]]       | Se centra en la **dimensión** **temporal** de las interacciones.<br><br>Muestra cómo los objetos se comunican a través de mensajes en un **orden cronológico**, permitiendo analizar el flujo de eventos y la secuencia exacta en que ocurren ([[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006\|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017\|OMG, 2027]]).                                                                                                               |
| [[Zk Diagramas de Interacción (Diagrama de Comunicación)\|Diagrama de Comunicación]] | Enfatiza la **estructura y las relaciones** entre los objetos participantes.<br><br>Representa cómo los objetos están **conectados** y cómo se envían mensajes entre ellos, priorizando la organización espacial y las conexiones sobre el orden temporal ([[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006\|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017\|OMG, 2017]]).<br><br> En versiones anteriores del UML este diagrama era conocido como Diagrama de Colaboración. |

>En versiones anteriores del UML, este diagrama era conocido como **Diagrama de Colaboración**. El nombre cambió a **Diagrama de Comunicación** en UML 2.0 para enfatizar su enfoque en la estructura de las interacciones entre los participantes.

^3d4f56

### Diagramas de Interacción y el SDLC

Ver [[Zk Diagramas de Interacción (Diagramas de Interacción y el SDLS)|Diagramas de Interacción y el SDLS]].
