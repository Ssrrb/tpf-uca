---
Title: Zk Comportamiento Dependiente del Estado
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
  - comportamiento
dg-publish: true
publish: true
aliases:
  - Comportamiento Dependiente del Estado
  - Conducta Dependiente del Estado
  - Respuesta Según Estado
---
## Comportamiento Dependiente del Estado

El comportamiento dependiente del estado aparece cuando una entidad puede responder de manera distinta ante un mismo evento según la situación interna en la que se encuentra. Esta idea es el núcleo que justifica el uso de una máquina de estados: no se modela sólo una secuencia de pasos, sino una red de situaciones posibles y cambios válidos entre ellas ([[Zk Ref harelStatechartsVisualFormalism1987|Harel, 1987]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

En términos de diseño, el estado funciona como una memoria abstracta del historial relevante del objeto. No registra todo lo que ocurrió, sino aquello que modifica las respuestas futuras del sistema. Por ejemplo, una factura `Emitida` no admite las mismas operaciones que una factura `Borrador`, aunque ambas pertenezcan a la misma clase de dominio.

### Valor para el Modelado

- **Análisis**: ayuda a descubrir reglas de negocio implícitas, restricciones y excepciones.
- **Diseño**: permite organizar responsabilidades alrededor de cambios válidos de situación.
- **Implementación**: puede guiar tablas de transición, condicionales controlados, patrón State o librerías de máquinas de estado.
- **Pruebas**: facilita derivar casos de prueba a partir de estados, transiciones y caminos relevantes ([[Zk Ref aggarwalTestCaseGeneration2012|Aggarwal y Sabharwal, 2012]]).

### Riesgo

No todo cambio observable debe convertirse en estado. Un estado debe representar una situación relativamente estable y relevante para el comportamiento futuro, no una acción instantánea ni un simple dato accidental ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]).

### Enlaces Sugeridos

- [[Zk Diagrama de Máquina de Estados UML|Diagrama de Máquina de Estados UML]]
- [[Zk Estado en UML|Estado en UML]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Errores Frecuentes en Diagramas de Máquina de Estados UML|Errores Frecuentes]]
