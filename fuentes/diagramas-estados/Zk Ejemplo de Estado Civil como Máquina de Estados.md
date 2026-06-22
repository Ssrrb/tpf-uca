---
Title: Zk Ejemplo de Estado Civil como Máquina de Estados
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
  - Estado Civil como Máquina de Estados
  - Ejemplo de Estado Civil
  - Modelo Didáctico de Estado Civil
---
## Ejemplo de Estado Civil como Máquina de Estados

El estado civil puede usarse como ejemplo introductorio de máquina de estados porque permite reconocer estados relativamente familiares y transiciones provocadas por eventos significativos. Debe tratarse, sin embargo, como una simplificación conceptual del dominio y no como un modelo jurídico completo.

La utilidad del ejemplo reside en mostrar que una persona puede encontrarse en situaciones mutuamente diferenciables, como `Soltero`, `Casado`, `Divorciado` o `Viudo`, y que ciertos eventos producen cambios válidos entre esas situaciones. Desde el punto de vista UML, el ejemplo ilustra cómo un objeto o entidad puede tener un ciclo de vida modelable mediante estados y transiciones ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Límites del Ejemplo

- **Hecho consolidado**: el estado civil es una categoría social y jurídica usada en registros personales.
- **Interpretación didáctica**: puede modelarse como ciclo de vida simplificado para introducir estados y transiciones.
- **Límite conceptual**: el modelo no pretende describir toda la normativa paraguaya ni sus casos excepcionales.

<!-- Para uso docente: este ejemplo es útil para introducir la idea de transición, pero conviene advertir que la validez jurídica real depende del marco normativo y administrativo. -->

**Figura**
*Estado Civil como Máquina de Estados Simplificada*
![](https://www.plantuml.com/plantuml/svg/dP5FImCn4CNl-HJZLIZgjGUfhY22lLZm8XwcsN4TcsJA92biFxtPFzXTAGXU4ZBlzsOUarLCg2bxPoxsYer7SDXAJX0z9Gneuex37XKznDGwAgUoxGqdnJgCyIuLPPiJFLa96puIN4-GUxIxHYM7kX8d2i_SVAP7nTP4YwNjZNcxV8V5uXOsuXAfcF7kQnL6h0MMuB4CyH9Ou0gK6YvnKDS_LJEIdUc13wAM1sCzF6Qs4PYPNZdt_0SwHvOzKqXIIMXpGrDlnz7HJ6RCSePC1rd_5NOOzW_Z972tjYLiyGjV1d2-kJFohyndY5EkC-AAGbs-_ni0)
*Nota*: El diagrama muestra una versión simplificada del cambio de estado civil; su finalidad es didáctica y no normativa.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Modelo didáctico simplificado, no jurídico.
[*] --> Soltero
Soltero --> Casado : matrimonio / registrarMatrimonio
Casado --> Divorciado : divorcio / registrarDivorcio
Casado --> Viudo : fallecimientoConyuge / registrarViudez
Divorciado --> Casado : nuevoMatrimonio / registrarMatrimonio
Viudo --> Casado : nuevoMatrimonio / registrarMatrimonio
Casado --> [*] : bajaRegistro
Soltero --> [*] : bajaRegistro
Divorciado --> [*] : bajaRegistro
Viudo --> [*] : bajaRegistro
@enduml
```

### Enlaces Sugeridos

- [[Zk Diagrama de Máquina de Estados UML|Diagrama de Máquina de Estados UML]]
- [[Zk Estado en UML|Estado]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
