---
Title: Zk Análisis de Robustez en el Proceso de Análisis y Diseño Orientado a Objetos
TipoNota: permanente
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - definir
tags:
  - definir
dg-publish: true
publish: true
aliases:
  - Robustez en el Proceso de Análisis y Diseño Orientado a Objetos
  - Análisis de Robustez en el Proceso de Análisis y Diseño Orientado a Objetos
---
## Análisis de Robustez en el Proceso de Análisis y Diseño Orientado a Objetos

El análisis de robustez es una técnica intermedia entre el análisis basado en casos de uso y el diseño orientado a objetos que permite validar la lógica de los casos de uso e identificar los objetos necesarios para su realización ([[Zk Ref jacobsonObjectOrientedSoftwareEngineering1992|Jacobson, 1992]]; [[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]). Consiste en descomponer el texto narrativo de cada caso de uso, oración por oración, para descubrir actores, objetos de frontera, objetos de entidad y objetos de control, y representar sus interacciones mediante un diagrama de robustez.

Históricamente, la técnica se relaciona con el método Objectory de Ivar Jacobson y con enfoques dirigidos por casos de uso, aunque no forma parte de la especificación oficial de UML ([[Zk Ref jacobsonObjectOrientedSoftwareEngineering1992|Jacobson, 1992]]; [[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]). En la práctica, se apoya en estereotipos y convenciones gráficas inspiradas en UML para mostrar objetos y relaciones, operando como un método semi‑formal que complementa los diagramas estándar ([[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

El análisis de robustez responde a la pregunta “qué objetos intervienen y cómo colaboran para cumplir un caso de uso”, actuando como puente entre el modelo de casos de uso (orientado a requisitos) y el modelo de clases de dominio y de diseño (orientado a estructura). Esta posición intermedia reduce la brecha entre la narrativa del usuario y la arquitectura de software, facilitando el paso ordenado desde el texto del caso de uso hacia diagramas de secuencia y, finalmente, hacia clases y métodos ([[Zk Ref jacobsonProcesoUnificadoDesarrollo2006|Jacobson et al., 2006]]; [[Zk Ref rumbaughModeladoDisenoOrientado2001|Rumbaugh et al., 2001]]).

En la mayoría de sus variantes, la técnica emplea tres tipos de objetos:  
- Objetos de **entidad**: representan información y conceptos del dominio que el sistema debe almacenar y manipular de forma persistente. 
  
- Objetos de **frontera** (o límite): encapsulan la interacción con actores externos (interfaces de usuario, APIs, gateways hacia otros sistemas).  
  
- Objetos de **control**: coordinan la lógica de cada caso de uso, orquestando las colaboraciones entre frontera y entidad.  

Esta clasificación es isomorfa al patrón arquitectónico Modelo–Vista–Controlador, donde las entidades se corresponden con el modelo de dominio, las fronteras con la vista y los controles con el controlador, lo que permite articular análisis de robustez y decisiones de arquitectura de alto nivel ([[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]). Así, la técnica ofrece un marco concreto para distribuir responsabilidades entre interfaz, lógica de aplicación y datos.

Los diagramas de robustez materializan esta técnica como un artefacto gráfico que combina rasgos de diagramas de clases (objetos, estereotipos) y de diagramas de actividades o colaboraciones (flujo de mensajes y responsabilidad en cada paso). La construcción sistemática consiste en tomar el flujo principal y los flujos alternativos del caso de uso, recorrerlos frase a frase, e ir “colocando” los objetos adecuados y sus conexiones, garantizando que todo paso de la narrativa tiene un emisor, un receptor y datos bien definidos (lo que facilita la posterior derivación de diagramas de secuencia).

Una práctica habitual establece reglas de conexión para preservar buenas propiedades de diseño: los actores solo se comunican con objetos de frontera; las fronteras solo con actores y controles; las entidades solo con controles; y los controles se comunican con fronteras, entidades y eventualmente otros controles, pero no directamente con actores. Estas restricciones concretan principios como la Ley de Demeter y ayudan a mantener bajo acoplamiento, alta cohesión y separación clara de responsabilidades ([[Zk Ref boochAnalisisDisenoOrientado2005|Booch et al., 2005]]; [[Zk Ref rumbaughModeladoDisenoOrientado2001|Rumbaugh et al., 2001]]).

Dentro de un proceso de análisis y diseño orientado a objetos conducido por casos de uso, el análisis de robustez se sitúa después de la especificación de casos de uso y la identificación preliminar de clases del dominio, y antes del diseño detallado de interacciones y clases. A nivel de flujo de trabajo, los diagramas de robustez sirven de base para derivar diagramas de secuencia (a menudo siguiendo un estilo [[Zk MVC|MVC]]) y, a partir de ellos, refinar el modelo de clases, asignar métodos y distribuir responsabilidades de manera más justificada ([[Zk Ref jacobsonProcesoUnificadoDesarrollo2006|Jacobson et al., 2006]]; [[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]).

Desde una perspectiva didáctica y metodológica, el análisis de robustez aporta al menos tres beneficios: obliga a depurar y completar el texto de los casos de uso, porque cualquier ambigüedad se evidencia al intentar mapearla a objetos; fuerza a separar explícitamente interfaz, lógica de aplicación y datos, reforzando patrones arquitectónicos como MVC; y ofrece un punto de apoyo visual para discutir responsabilidades y colaboraciones antes de entrar en detalles de implementación. Por ello se ha consolidado como una práctica recomendada en cursos y procesos de ingeniería de software orientada a objetos, pese a no ser un elemento oficial del repertorio UML ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

### Enlaces Sugeridos

[[Zk Diagrama de Clases (Elementos, Estereotipos de Clase)|Estereotipos en Diagramas de Clase]]
[[Zk Análisis de Robustez (Microejemplo)|Microejemplo de Análisis De Robustez]]
