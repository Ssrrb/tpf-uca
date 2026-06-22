---
Title: Zk Ejemplo de Pedido CRM como Máquina de Estados
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
  - Pedido CRM como Máquina de Estados
  - Ciclo de Vida de un Pedido
  - Ejemplo de Pedido en CRM
---
## Ejemplo de Pedido CRM como Máquina de Estados

Un pedido en un CRM es un buen ejemplo de comportamiento dependiente del estado porque integra reglas de inventario, pago, preparación, despacho, entrega y cancelación. Cada transición modifica las operaciones válidas posteriores y permite distinguir entre camino normal, excepciones y cancelaciones.

La versión revisada separa eventos, guardas y efectos para evitar expresiones ambiguas como “Inventario suficiente / Inventario insuficiente”, que mezclan condición y consecuencia. En UML, esta separación mejora la precisión del modelo porque distingue la ocurrencia que dispara la transición, la condición que la habilita y el comportamiento que se ejecuta como resultado ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

<!-- Para uso docente: este ejemplo permite conectar modelado de dominio, reglas de negocio y pruebas de transición. -->

**Figura**
*Pedido CRM como Máquina de Estados*
![](https://www.plantuml.com/plantuml/svg/bLCxQyCm4DxrAzIr4Dgk7KhQD9H01zD0bv3X8b-S8x9aJd8W-VKzoNOUfGbqCT9ttqEwaySX0iUsjkgkOQXgq1Rsleqwr1Z1WGfRSWqmr3h4lKNvCfaiE5MCXH1UerHMRSIPyMvE1zIFPvGtCDkAVUlAYRUUzITLc_Z1i5V1WDW-gSNzKez6B_eB3QsezFfPSrvoWMNQFyY-8ic77b57Qj9z8zEQ3BZIpzmEdToBaWavCWGyb0rvf_xc9fS2NKa2u3nwiytoeJw896yHKdNcGYj0fY_bUCx7JE1fQ93XHaf74Bo0ojyEUQVGU4ShcoCO0_8EE9zENTeaumauWnPozne1fKCRE43kdgMLiAzAfwvWJCDA7Uhb4-_Mn7MdD_rcwFwbeBFOKPTTOcX0ebbqc50Uh7B_1s8dYZBNJdQCwC6KYdnbuETtDTsQpnz9Ny-1lyRwN_dfZ4afBrMTr0CobWZvBNu0)
*Nota*: El diagrama modela el ciclo de vida simplificado de un pedido, incorporando alternativas por falta de stock, rechazo de pago y cancelación.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Modelo didáctico simplificado de pedido en CRM.
[*] --> Recibido : recibirPedido / registrarPedido
Recibido --> VerificandoInventario : iniciarVerificacion
VerificandoInventario --> PendienteStock : inventarioVerificado [stockInsuficiente] / notificarEspera
VerificandoInventario --> EsperandoPago : inventarioVerificado [stockDisponible] / reservarStock
EsperandoPago --> Cancelado : pagoRechazado / liberarStock
EsperandoPago --> EnPreparacion : pagoConfirmado / confirmarPedido
EnPreparacion --> Enviado : despachar / enviarConfirmacion
Enviado --> Entregado : confirmarEntrega / cerrarPedido
Recibido --> Cancelado : cancelar / registrarCancelacion
PendienteStock --> Cancelado : cancelar / registrarCancelacion
Entregado --> [*]
Cancelado --> [*]
@enduml
```

### Enlaces Sugeridos

- [[Zk Evento en Máquina de Estados UML|Evento]]
- [[Zk Guardia en Máquina de Estados UML|Guardia]]
- [[Zk Efecto de Transición en UML|Efecto]]
- [[Zk Pruebas Basadas en Máquinas de Estado|Pruebas Basadas en Máquinas de Estado]]
