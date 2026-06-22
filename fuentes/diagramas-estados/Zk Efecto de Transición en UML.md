---
Title: Zk Efecto de Transición en UML
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
  - Efecto de Transición
  - Acción de Transición
  - Comportamiento Asociado a una Transición
---
## Efecto de Transición en UML

El efecto de una transición es el comportamiento que se ejecuta cuando la transición se dispara efectivamente. En la notación didáctica habitual se coloca después de la barra inclinada, como en `evento [guarda] / efecto`, aunque UML lo define dentro de una estructura más precisa de transición, disparador, guarda y efecto ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

Conviene distinguir efecto de acción. Una acción es una unidad ejecutable de comportamiento; el efecto es el comportamiento asociado a una transición concreta. En muchos ejemplos introductorios, el efecto se expresa como una acción simple, pero conceptualmente no son sinónimos absolutos ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]).

### Ejemplo

```text
emitir [datosValidos] / registrarEmision
```

La transición se dispara por el evento `emitir`, se habilita si la guarda `[datosValidos]` es verdadera y ejecuta el efecto `registrarEmision`.

### Criterio de Modelado

Un efecto debería nombrarse como una acción de sistema o una operación significativa, no como un estado. Por ejemplo, `registrarPago` es mejor efecto que `Pagado`, porque `Pagado` nombra una situación resultante y no el comportamiento ejecutado durante el cambio.

### Enlaces Sugeridos

- [[Zk Transición en Máquina de Estados UML|Transición]]
- [[Zk Actividades Entry Exit y Do en UML|Actividades Entry, Exit y Do]]
- [[Zk Errores Frecuentes en Diagramas de Máquina de Estados UML|Errores Frecuentes]]
