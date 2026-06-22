---
Title: Zk Estado Compuesto en UML
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
  - Estado Compuesto
  - Estado Jerárquico
  - Subestados en UML
---
## Estado Compuesto en UML

Un estado compuesto es un estado que contiene una o más regiones internas con subestados. Su propósito es organizar comportamientos complejos sin convertir el diagrama en una red plana de transiciones difíciles de leer ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

La utilidad principal del estado compuesto es jerárquica: permite agrupar situaciones que comparten una lógica común y expresar transiciones de entrada o salida a nivel del grupo completo. Esta idea se vincula con la tradición de los statecharts, que introdujo jerarquía y composición para representar sistemas reactivos complejos de manera más manejable ([[Zk Ref harelStatechartsVisualFormalism1987|Harel, 1987]]).

<!-- Para uso docente: el ejemplo de pedido es deliberadamente simple; puede ampliarse con subestados de pago, preparación o entrega si se busca trabajar refinamiento progresivo. -->

**Figura**
*Estado Compuesto para un Pedido*
![](https://www.plantuml.com/plantuml/svg/JP0_JmCn3CNtV0gp8bMbAqDLkA6gr071M36Od9j6pP-JuniEn7V7wUL4byZs-xsdf-oA8CiOWtaO65r423ZbKQ144aneojMd0HaZ59a2wSlUtWp_YWrOoekeyZKA7MnE7_wRuEaEUKLxTPp7r7SvP8QZTnVPCqwcMDJOZJazVi9gjOKtwdsVZVOIQWly6815VoVdjGGg0tVBx4LNnsSOqEKkfxFdM0zhu0Qo8jNOo9k9gNQSVVFChSIlQGKgrn4tYf9e7hBcsdfSy8MejDOrEqgz_jGV)
*Nota*: La figura muestra un estado compuesto `Pedido` que agrupa subestados internos antes de pasar al estado `Cerrado`.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Estado compuesto con subestados internos.
[*] --> Pedido
state Pedido {
  [*] --> Registrado
  Registrado --> Pagado : pagoConfirmado / registrarPago
  Pagado --> Preparado : prepararPedido
}
Pedido --> Cerrado : entregar / cerrarPedido
Cerrado --> [*]
@enduml
```

### Enlaces Sugeridos

- [[Zk Estado en UML|Estado en UML]]
- [[Zk Región Ortogonal en Máquina de Estados UML|Región Ortogonal]]
- [[Zk Pseudoelementos de Máquina de Estados UML|Pseudoelementos]]
