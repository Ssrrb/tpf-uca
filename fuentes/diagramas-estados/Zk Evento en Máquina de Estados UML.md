---
Title: Zk Evento en Máquina de Estados UML
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
  - Evento en UML
  - Disparador de Transición
  - Ocurrencia Significativa
---
## Evento en Máquina de Estados UML

Un evento es una ocurrencia significativa para el modelo. Puede representar la recepción de una señal, la invocación de una operación, el cumplimiento de una condición o el paso del tiempo. En una máquina de estados, el evento puede actuar como disparador de una transición, pero no debe confundirse con la guarda que la condiciona ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

La distinción es importante: el evento responde a la pregunta “¿qué ocurrió?”, mientras que la guarda responde a “¿bajo qué condición puede ocurrir el cambio?”. Si ambas preguntas se mezclan, el diagrama pierde precisión y se vuelve difícil de usar para diseño, implementación o pruebas.

### Tipos Frecuentes

- **Señal**: recepción asincrónica de un mensaje o estímulo.
- **Llamada**: invocación de una operación.
- **Tiempo**: vencimiento de un plazo o llegada de un instante.
- **Cambio**: cumplimiento de una condición observada.

### Ejemplos

- `pagoConfirmado`
- `timeout`
- `cancelarPedido`
- `temperaturaAlta`

### Error Frecuente

Nombrar una transición como `Inventario suficiente / Inventario insuficiente` mezcla evento y condición. Una versión más clara sería:

```text
inventarioVerificado [stockDisponible] / reservarStock
inventarioVerificado [no stockDisponible] / marcarPedidoPendiente
```

### Enlaces Sugeridos

- [[Zk Guardia en Máquina de Estados UML|Guardia]]
- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Errores Frecuentes en Diagramas de Máquina de Estados UML|Errores Frecuentes]]
