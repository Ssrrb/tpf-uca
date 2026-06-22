---
Title: Zk Diagrama de Clases (Elementos - Clases Persistentes)
TipoNota: permanente
Fecha: 2025-05-05 11:02
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
  - diagramaDeClases
dg-publish: true
publish: true
---
## Diagrama de Clases (Elementos - Clases Persistentes)

Una **clase persistente** es aquella cuyo estado puede conservarse más allá de la ejecución de la aplicación, generalmente mediante su almacenamiento en una base de datos u otro medio permanente. Estas clases modelan entidades del dominio que requieren persistencia y suelen estar asociadas a mecanismos de mapeo objeto-relacional o a capas de persistencia en la arquitectura del software ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

### Clase Persistente

Una **clase persistente** representa una entidad de negocio cuyo ciclo de vida trasciende la ejecución del programa, permitiendo que sus instancias sean almacenadas y recuperadas posteriormente. La persistencia implica que los objetos de estas clases pueden ser guardados, modificados, consultados y eliminados en un almacenamiento permanente, como una base de datos relacional u orientada a objetos.  ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

No todas las clases de un modelo deben ser persistentes; la decisión depende de los requisitos del sistema y de la necesidad de conservar información a largo plazo. Las clases persistentes suelen corresponder a entidades principales del dominio, como Cliente, Producto o Pedido

### Características

| Característica              | Explicación                                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Estado persistente          | Los objetos de la clase pueden mantener su estado entre diferentes ejecuciones del sistema                                                             |
| Mapeo a almacenamiento      | Generalmente, cada clase persistente se mapea a una tabla (en bases de datos relacionales) o a una colección (en bases de datos orientadas a objetos). |
| Atributos persistentes      | Los atributos de la clase corresponden a columnas o campos en el almacenamiento.                                                                       |
| Operaciones de persistencia | Suelen incluir métodos para crear, leer, actualizar y eliminar (CRUD) instancias.                                                                      |
| Restricciones y Reglas      | Pueden tener restricciones de integridad y reglas de negocio asociadas, que deben cumplirse durante las operaciones de persistencia.                   |

#### Sintaxis
En UML, una clase persistente puede representarse como una clase estándar, pero es común utilizar el estereotipo `<<persistent>>` o `<<entity>>` para distinguirlas de las clases transitorias o de control[](https://www.scielo.org.mx/pdf/cys/v7n4/v7n4a2.pdf). En los diagramas de clases, se recomienda detallar los atributos, tipos de datos y restricciones relevantes para la persistencia.

**Figura**
_Ejemplo de una Clase Persistente_
![](https://www.plantuml.com/plantuml/png/JOwnJiD038RtUmep1SG2QrLLXGu8YQrFu5nCQjLdHpxV413lJfEbMIpx-sphFzP0ZrO4KlSmEOu5GN2s5b0B1IgcUcMTqB50ZLdeLftpSh8nMR3MjxYPlWLzPjCp_n2yR5RUCLz7jwR3oSGSldYyn8VZd3gXxu0my0N1m4uvs3I5JGlkBSBAXdVthy9ACKy4vd6nL3CAmMjAQo0u2PC6mNvF6XppuG2_2U2PXnsmnjAgbTvf1-Tmrd4XL91b2yQ6Fg0_FgrMkB2kqrywaWwjo3y0)

```plantuml-code
@startuml 
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
left to right direction
'top to bottom direction
skinparam linetype ortho
scale 1

class Cliente <<entity>> {
  +id: int
  +nombre: String
  +email: String
  +guardar()
  +eliminar()
}
@enduml
```
*Nota*: Ver [[Zk Diagrama de Clases (Elementos, Estereotipos de Clase)#^c4b52a|Estereotipos de Clases]]

### Reglas y Recomendaciones para Identificar Clases Persistentes

- Las clases que representan entidades fundamentales del dominio suelen ser persistentes
- Si una clase compuesta es persistente, sus componentes también lo serán.
- Si una subclase es persistente, sus superclases también deben serlo.
- Las clases de control o utilitarias generalmente **no** son persistentes.
- Es recomendable separar la lógica de persistencia de la lógica de negocio, utilizando capas o patrones de acceso a datos.

### Relación con el Modelo de Datos

La transformación de clases persistentes en UML a tablas de una base de datos es una práctica común en el desarrollo de sistemas de información. Cada clase persistente se convierte, típicamente, en una tabla, y sus atributos en columnas. Las relaciones entre clases (asociaciones, agregaciones, composiciones) se transforman en claves foráneas o tablas intermedias según la cardinalidad.