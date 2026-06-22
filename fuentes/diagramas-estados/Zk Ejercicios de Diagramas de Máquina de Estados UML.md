---
Title: Zk Ejercicios de Diagramas de Máquina de Estados UML
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
  - ejercicios
dg-publish: true
publish: true
aliases:
  - Ejercicios de Diagramas de Estados
  - Prácticas de Máquinas de Estado
  - Problemas de Modelado de Estados
---
## Ejercicios de Diagramas de Máquina de Estados UML

Los ejercicios de máquinas de estado deben ayudar a distinguir estados, eventos, guardas y efectos. Por ello es preferible formularlos como problemas de modelado, no sólo como pedidos de dibujo. Esta orientación favorece que el estudiante explicite decisiones de análisis y no se limite a producir una notación visual ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Ejercicio 1: Factura en CRM

Modele el ciclo de vida de una factura considerando al menos los estados `Borrador`, `Emitida`, `Anulada`, `Entregada` y `Cobrada`. Incluya eventos de emisión, anulación, entrega y pago. Explique qué guardas son necesarias para evitar transiciones inválidas.

Conexión: [[Zk Ejemplo de Factura CRM como Máquina de Estados|Factura CRM]]

### Ejercicio 2: Pedido en Comercio Electrónico

Modele el ciclo de vida de un pedido desde su recepción hasta su entrega o cancelación. Incluya verificación de inventario, confirmación de pago, preparación, envío y entrega.

Conexión: [[Zk Ejemplo de Pedido CRM como Máquina de Estados|Pedido CRM]]

### Ejercicio 3: Ascensor

Modele un ascensor simple con estados de espera, movimiento y puertas. Luego proponga una segunda versión con estados compuestos o regiones ortogonales.

Conexión: [[Zk Ejemplo de Ascensor como Máquina de Estados|Ascensor]]

### Ejercicio 4: Revisión Crítica

Revise un diagrama elaborado por otro estudiante e identifique:

- estados que podrían ser acciones;
- eventos confundidos con guardas;
- transiciones faltantes;
- estados no alcanzables;
- ausencia de caminos de error o cancelación.

Conexión: [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]

<!-- Para uso docente: estos ejercicios pueden organizarse como práctica progresiva: primero identificación de estados, luego transiciones, después guardas y finalmente criterios de cobertura para pruebas. -->
