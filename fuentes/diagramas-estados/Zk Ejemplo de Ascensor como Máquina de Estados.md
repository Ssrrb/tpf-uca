---
Title: Zk Ejemplo de Ascensor como Máquina de Estados
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
  - ejemplo
dg-publish: true
publish: true
aliases:
  - Ascensor como Máquina de Estados
  - Ejemplo UML de Ascensor
  - Modelo de Estados de un Ascensor
---
## Ejemplo de Ascensor como Máquina de Estados

Un ascensor permite introducir comportamiento reactivo, condiciones de movimiento y acciones de entrada o salida. Como ejemplo público y formativo, resulta útil porque muestra que un sistema aparentemente simple cambia su comportamiento según eventos, condiciones de seguridad y situación actual ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

La versión simplificada representa el ciclo básico: espera, movimiento, apertura y cierre de puertas. Una versión avanzada podría separar en regiones ortogonales el movimiento, las puertas, alarmas y sensores, pero esa ampliación debe reservarse para modelos donde esas dimensiones evolucionen de manera relativamente independiente ([[Zk Ref harelStatechartsVisualFormalism1987|Harel, 1987]]).

<!-- Para uso docente: este ejemplo es conveniente después de que el estudiante distingue estado, evento y guarda; si se presenta demasiado temprano, la concurrencia de puertas, motor y sensores puede distraer del núcleo conceptual. -->

**Figura**
*Ascensor como Máquina de Estados Simplificada*
![](https://www.plantuml.com/plantuml/svg/dPB1QW8n48Rl-nJnMf2sLy7YraeH54hjJJpC9iDsC9aiawoWJz_4hdQLbeANP9AP_ykVJ2OXWiJMsMBG2DGEb8MzRwCA3YCm565Bt820Ko7kBQPHI1y5Fnbj8OGofapLHfnhpoiwe7hebJo3tjRYMpPJRxse1TMVyLLWNmGD2VjOhEysQZXyKZEUXGO5YbFGxIxzZXmXHwz6obfmOE0TDLLaGAqR2lu5GoJsQZ1MULaccs0twbuXQsI3ilJHooNthKM94CgAZlD_wF4r6YeXwI35XSdVwJrOQJNm0OnF68CH-MJmMjKZJL4acSiadSFJqGb1J9f0Fj0rNYXppwIpgl--2H685z-tpG1ee0QPio6TnHZ-a5yqWblSGGUvlGkvzwFEm8f2H0V591MdR_O5)
*Nota*: La figura muestra una versión didáctica simple. No incluye sensores de seguridad, sobrecarga, emergencia ni concurrencia entre subsistemas.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Modelo didáctico simplificado de ascensor.
[*] --> EnEspera
EnEspera --> EnMovimiento : llamadaRecibida [pisoDestino != pisoActual] / encenderMotor
EnEspera --> PuertasAbiertas : llamadaRecibida [pisoDestino == pisoActual] / abrirPuertas
EnMovimiento --> PuertasAbiertas : pisoDestinoAlcanzado / detenerMotor
PuertasAbiertas --> PuertasCerradas : cerrarPuertas / iniciarTemporizador
PuertasCerradas --> EnEspera : sinLlamadas / apagarIndicadores
PuertasCerradas --> EnMovimiento : nuevaLlamada [pisoDestino != pisoActual] / encenderMotor
EnEspera --> [*] : apagarSistema
@enduml
```

### Enlaces Sugeridos

- [[Zk Estado Compuesto en UML|Estado Compuesto]]
- [[Zk Región Ortogonal en Máquina de Estados UML|Región Ortogonal]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
