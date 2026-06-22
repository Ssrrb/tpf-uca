---
Title: Zk Región Ortogonal en Máquina de Estados UML
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
  - Región Ortogonal
  - Regiones Concurrentes
  - Concurrencia en Máquinas de Estado
---
## Región Ortogonal en Máquina de Estados UML

Una región ortogonal permite que un estado compuesto contenga subcomportamientos activos en paralelo. En lugar de representar una única trayectoria interna, el modelo expresa que varias regiones pueden evolucionar simultáneamente y coordinarse mediante eventos, condiciones o sincronizaciones ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

En materiales introductorios suele hablarse de “regiones concurrentes”. Esa expresión es comprensible, pero el término técnico “región ortogonal” permite distinguir la concurrencia estructural dentro de un estado compuesto de una simple bifurcación visual. Esta posibilidad de representar concurrencia es una de las contribuciones históricas de los statecharts al modelado de sistemas reactivos ([[Zk Ref harelStatechartsVisualFormalism1987|Harel, 1987]]).

<!-- Para uso docente: antes de introducir regiones ortogonales, conviene que el estudiante ya comprenda estado compuesto y transición. -->

**Figura**
*Regiones Ortogonales en un Sistema de Monitoreo*
![](https://www.plantuml.com/plantuml/svg/TL5BIyH03BxFhuXNeQ3NFSYk2YAuNjQRU8ZJK8UTcPHCAdJ5_svQ7srrlGJoFP9l9kkYADgbw4vQmIOXHEovKoY953EwiW-vHS44HVj8LYNuqJ0nFc8f6pNckLEwzPntuK1mDfDSejytmbskhpYom5reNlH6i7V5euqzTu-dJr1L5x3b79I5s5aqfQc7DmVmhRec9My1QzxoQqY1ihBHn-1HlmjvXgn0Go9xfbcMp7-ppP9-cYz1FMoigbcg1qej2MedUC-IC1ht1_kjt4J58T4IMJf7pT4DI-Sd5WvOetjtqzSDrY7a2h351iMjATTsn0y0)
*Nota*: La figura representa dos regiones internas que evolucionan de forma simultánea: una vinculada al movimiento y otra a la temperatura.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Estado compuesto con dos regiones ortogonales.
[*] --> Monitoreo
state Monitoreo {
  [*] --> DetectandoMovimiento
  DetectandoMovimiento --> SinMovimiento : timeout
  SinMovimiento --> DetectandoMovimiento : movimientoDetectado
  --
  [*] --> TemperaturaNormal
  TemperaturaNormal --> TemperaturaAlta : temperaturaAlta
  TemperaturaAlta --> TemperaturaNormal : temperaturaNormalizada
}
Monitoreo --> [*] : apagar
@enduml
```

### Riesgo de Modelado

No debe usarse una región ortogonal sólo para ahorrar espacio gráfico. Su empleo debe responder a la existencia de dimensiones de estado relativamente independientes y simultáneas.

### Enlaces Sugeridos

- [[Zk Estado Compuesto en UML|Estado Compuesto]]
- [[Zk Actividades Entry Exit y Do en UML|Actividades Entry, Exit y Do]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
