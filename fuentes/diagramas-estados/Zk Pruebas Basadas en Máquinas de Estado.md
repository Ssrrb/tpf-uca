---
Title: Zk Pruebas Basadas en Máquinas de Estado
TipoNota: permanente
Fecha: 2026-05-26
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - testing
Status: ok
tags:
  - digitalGarden
  - testing
  - modelBasedTesting
  - diagramaDeEstados
dg-publish: true
publish: true
aliases:
  - Pruebas Basadas en Estados
  - Testing con Máquinas de Estado
  - Model-Based Testing con Estados
---
## Pruebas Basadas en Máquinas de Estado

Las pruebas basadas en máquinas de estado usan el modelo de estados y transiciones como base para derivar casos de prueba. En lugar de seleccionar casos sólo por intuición, el modelo permite definir criterios de cobertura conductual: visitar estados, recorrer transiciones o comprobar combinaciones relevantes de entrada y salida ([[Zk Ref aggarwalTestCaseGeneration2012|Aggarwal y Sabharwal, 2012]]).

### Criterios de Cobertura

- **Cobertura de estados**: los casos de prueba alcanzan cada estado al menos una vez.
- **Cobertura de transiciones**: los casos recorren cada transición al menos una vez.
- **Cobertura de pares de transiciones**: para cada estado, se ejercitan combinaciones relevantes de transición entrante y saliente.

La cobertura de transiciones suele ser más exigente que la cobertura de estados, porque no basta con llegar a cada situación; también hay que verificar que los cambios entre situaciones funcionen correctamente. Este uso refuerza la relación entre modelado UML, verificación y diseño de pruebas durante el ciclo de vida del software ([[Zk Ref pressmanIngenieriaSoftwareEnfoque2013|Pressman, 2013]]; [[Zk Ref aggarwalTestCaseGeneration2012|Aggarwal y Sabharwal, 2012]]).

<!-- Para uso docente: esta técnica permite mostrar que un diagrama UML no es sólo documentación, sino también una base para revisar requisitos y derivar pruebas. -->

### Enlaces Sugeridos

- [[Zk Diagrama de Máquina de Estados y SDLC|Diagrama de Máquina de Estados y SDLC]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
