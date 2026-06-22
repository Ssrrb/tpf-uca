---
Title: Zk Ejemplo de Factura CRM como Máquina de Estados
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
  - Factura CRM como Máquina de Estados
  - Ciclo de Vida de una Factura
  - Ejemplo de Factura en CRM
---
## Ejemplo de Factura CRM como Máquina de Estados

Una factura en un sistema CRM puede modelarse mediante una máquina de estados porque sus operaciones válidas dependen de su situación dentro del ciclo de vida. No se debería cobrar una factura inexistente, ni entregar una factura anulada, ni cerrar una factura sin registrar el pago correspondiente.

El ejemplo ilustra cómo las reglas de negocio pueden representarse como estados, transiciones, guardas y efectos. Esta forma de modelar es coherente con el uso de máquinas de estado UML para describir objetos cuyo comportamiento cambia durante su vida ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

<!-- Para uso docente: la versión anterior confundía una acción de carga o registro con una actividad de salida de estado; aquí se modela como efecto de una transición o como parte del ciclo de creación. -->

**Figura**
*Factura CRM como Máquina de Estados*
![](https://www.plantuml.com/plantuml/svg/RP5FJyCm3CNl-HJXYZG1Lmve_nYQn64I4fTg1o-rIhGahXptK3uzJaktJd29tFZzdlsQPHPWwM8mTor34y46wAaJcoCA933vx5CB3D5cwGFgoTuDmBNZ0kIy4ksSEi6ze_JXlz4-pYHhSEU6gKlrXWAnVVVDbxmnz2OxKDidKzqVxMBnOjV43BLAdgrZ1Dw1ZcCmb_iYUerUV0sgmLAnhMeGofyGV4tvQ1yiO-DrLs2LPa_fbb-bBi30Gwbu3WmzLv1fIY7siMNCXV1Q-UWBqs129GxRdPdwmtP9r6tqnx6-cV3RDrTTeJPquf6v20_GaArQFJSKsu129Pf3JNBvB_Cb_yIgL4gyHK4d6lxuVyvfSh7GPp2JpVIzn5JhY_y0)
*Nota*: El diagrama representa una simplificación del ciclo de vida de una factura en un CRM. Los estados y transiciones pueden variar según reglas contables, fiscales o de negocio.

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
scale 1
' Modelo didáctico simplificado de factura en CRM.
[*] --> Borrador : crearFactura
Borrador --> Emitida : emitir [datosValidos] / registrarEmision
Borrador --> Anulada : anular / registrarAnulacion
Emitida --> Impresa : imprimir / generarPDF
Impresa --> Entregada : entregar / registrarEntrega
Entregada --> Cobrada : registrarPago [pagoCompleto] / cerrarFactura
Emitida --> Anulada : anular [errorDetectado] / registrarAnulacion
Cobrada --> [*]
Anulada --> [*]
@enduml
```

### Enlaces Sugeridos

- [[Zk Ciclo de Vida de un Objeto|Ciclo de Vida de un Objeto]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
