---
Title: Zk Ciclo de Vida de un Objeto
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
  - modelado
dg-publish: true
publish: true
aliases:
  - Ciclo de Vida del Objeto
  - Vida de una Instancia
  - Evolución de un Objeto
---
## Ciclo de Vida de un Objeto

El ciclo de vida de un objeto describe las situaciones relevantes por las que una instancia puede pasar desde su creación hasta su terminación, cierre lógico o desaparición del dominio. En modelado orientado a objetos, este ciclo adquiere importancia cuando las operaciones válidas sobre una instancia dependen de su estado actual y de los eventos que recibe ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

Una factura, por ejemplo, puede pasar de `Borrador` a `Emitida`, luego a `Entregada` y finalmente a `Cobrada`. Cada estado habilita operaciones distintas, restringe otras y permite interpretar el sentido de los eventos que recibe.

### Relación con Máquinas de Estado

Una máquina de estados formaliza el ciclo de vida mediante estados, transiciones, eventos, guardas y efectos. Esta formalización ayuda a convertir reglas de negocio dispersas en un modelo explícito, revisable y comunicable entre analistas, diseñadores, programadores y usuarios expertos ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Enlaces Sugeridos

- [[Zk Diagrama de Máquina de Estados UML|Diagrama de Máquina de Estados UML]]
- [[Zk Estado en UML|Estado]]
- [[Zk Ejemplo de Factura CRM como Máquina de Estados|Factura CRM]]
