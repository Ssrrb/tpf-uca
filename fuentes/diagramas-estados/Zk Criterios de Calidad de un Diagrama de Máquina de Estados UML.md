---
Title: Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML
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
  - calidad
  - diagramaDeEstados
dg-publish: true
publish: true
aliases:
  - Calidad de Diagramas de Estados
  - Rúbrica para Máquinas de Estado
  - Evaluación de Diagramas de Estados
---
## Criterios de Calidad de un Diagrama de Máquina de Estados UML

Un diagrama de máquina de estados de buena calidad no se mide por la cantidad de estados, sino por la claridad con que expresa comportamiento relevante, transiciones válidas y restricciones del dominio. Como artefacto de modelado, debe hacer visibles las condiciones bajo las cuales una entidad cambia de situación y las consecuencias esperadas de esos cambios ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Rúbrica Mínima

- **Estados significativos**: cada estado representa una situación relevante para el comportamiento futuro.
- **Transiciones justificadas**: cada flecha expresa un cambio posible y necesario.
- **Eventos claros**: los disparadores están nombrados como ocurrencias, no como condiciones ni estados.
- **Guardas evaluables**: las condiciones se formulan como expresiones verdaderas o falsas.
- **Efectos adecuados**: los efectos nombran acciones u operaciones, no estados resultantes.
- **Alcanzabilidad**: todo estado sustantivo debería poder alcanzarse desde el inicio.
- **Terminación o continuidad explícita**: el modelo debe mostrar si la vida del objeto termina o si permanece en ciclos válidos.
- **Nivel de abstracción homogéneo**: no deben mezclarse detalles de interfaz, reglas de dominio y acciones técnicas sin criterio.

Esta rúbrica combina criterios de sintaxis UML con criterios semánticos de calidad del modelo: no basta con que el diagrama “se vea correcto”; también debe representar adecuadamente las reglas de comportamiento que pretende comunicar ([[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

<!-- Para uso docente: esta rúbrica puede emplearse para corregir ejercicios, construir listas de cotejo o guiar una revisión por pares entre estudiantes. -->

### Enlaces Sugeridos

- [[Zk Errores Frecuentes en Diagramas de Máquina de Estados UML|Errores Frecuentes]]
- [[Zk Pruebas Basadas en Máquinas de Estado|Pruebas Basadas en Máquinas de Estado]]
- [[Zk Guardia en Máquina de Estados UML|Guardia]]
