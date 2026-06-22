---
Title: Zk Diagrama de Clases (Modelado de Responsabilidades de la Clase)
TipoNota: permanente
Fecha: 2025-05-12 12:05
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
dg-publish: true
publish: true
aliases:
  - Modelado de Responsabilidades de la Clase
---
## Modelado de Responsabilidades de la Clase

El modelado de responsabilidades de la clase es una actividad central del análisis y diseño orientado a objetos, porque determina qué debe saber una clase, qué debe hacer y con quién debe colaborar para cumplir su papel dentro del sistema. No se trata simplemente de repartir operaciones entre rectángulos del diagrama, sino de establecer una arquitectura conceptual en la que cada clase asuma obligaciones coherentes, inteligibles y sostenibles en el tiempo ([[Zk Ref boochAnalisisDisenoOrientado2000|Booch et al., 2000]]; [[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]).

En este sentido, modelar responsabilidades equivale a decidir cómo se distribuye la inteligencia del sistema. Una clase bien diseñada no es un contenedor pasivo de datos, sino una unidad autónoma que conoce una porción pertinente del dominio, protege su estado mediante encapsulamiento y ofrece servicios alineados con aquello que verdaderamente le compete ([[Zk Ref meyerObjectOrientedSoftwareConstruction1997|Meyer, 1997]]; [[Zk Ref weitzenfeldIngenieriaSoftwareOrientada2005|Weitzenfeld, 2005]]).

### Definición

Las responsabilidades de una clase son los compromisos que esta asume dentro del modelo: aquello que sabe, aquello que hace y aquello que coordina con otras clases para contribuir al comportamiento global del sistema. Desde esta perspectiva, una responsabilidad no es solo una operación aislada, sino una obligación conceptual que vincula información, comportamiento y colaboración bajo una misma unidad de diseño ([[Zk Ref boochAnalisisDisenoOrientado2000|Booch et al., 2000]]).

En UML, esas responsabilidades se expresan de manera indirecta pero precisa a través de tres dimensiones complementarias:

- **Atributos**: lo que la clase sabe.
- **Operaciones**: lo que la clase hace.
- **Relaciones**: con quién colabora para cumplir sus tareas ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

Así entendido, el diagrama de clases deja de ser una simple fotografía estructural y se convierte en una hipótesis explícita sobre la distribución del trabajo conceptual del sistema.

### Fundamento Conceptual

En orientación a objetos, los objetos no son registros inertes, sino entidades activas que mantienen su propio estado, exponen comportamiento y se relacionan con otros objetos mediante mensajes. De ahí que asignar responsabilidades no sea una tarea secundaria del diseño, sino el núcleo mismo de la construcción de un sistema orientado a objetos coherente ([[Zk Ref meyerObjectOrientedSoftwareConstruction1997|Meyer, 1997]]; [[Zk Ref weitzenfeldIngenieriaSoftwareOrientada2005|Weitzenfeld, 2005]]).

El encapsulamiento introduce aquí una exigencia decisiva: cada clase debe gestionar su propio estado sin delegar indebidamente esa responsabilidad en otras. Cuando una clase conoce demasiado sobre los detalles internos de sus colaboradoras, el diseño pierde cohesión y aumenta el acoplamiento, deteriorando la mantenibilidad del sistema ([[Zk Ref boochAnalisisDisenoOrientado2000|Booch et al., 2000]]; [[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]).

Por eso, la asignación de responsabilidades constituye también una estrategia de gobierno de la complejidad. Un diseño con clases bien delimitadas reduce dependencias innecesarias, hace el sistema más legible y favorece su evolución sin propagaciones imprevisibles del cambio ([[Zk Ref pressmanIngenieriaSoftwareEnfoque2013|Pressman, 2013]]; [[Zk Ref sommervilleIngenieriaSoftware2011|Sommerville, 2011]]).

### Qué Debe Saber, Hacer y Coordinar una Clase

Una clase bien modelada reúne en forma equilibrada tres dimensiones.

- **Saber**: almacenar o conocer la información que le pertenece legítimamente, ya sea por sus atributos o por sus asociaciones relevantes.
- **Hacer**: ofrecer operaciones que transformen, validen, consulten o mantengan coherente ese conocimiento.
- **Coordinar**: colaborar con otras clases solo en la medida necesaria para cumplir su función, sin invadir sus responsabilidades internas ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]).

Esta triple distinción resulta pedagógicamente fecunda porque obliga a preguntar, para cada clase del modelo: ¿qué información tiene sentido que resida aquí?, ¿qué acciones derivan naturalmente de esa información?, ¿y qué tareas deberían estar, en cambio, en otra clase? Tales preguntas desplazan el foco desde la sintaxis del diagrama hacia su semántica disciplinar.

### Principio Rector: Cohesión y Bajo Acoplamiento

El criterio rector del modelado de responsabilidades es el equilibrio entre **alta cohesión** y **bajo acoplamiento**. Una clase cohesiva concentra responsabilidades estrechamente relacionadas entre sí; una clase débilmente acoplada depende lo menos posible de los detalles internos de otras clases. Estas dos cualidades no son ornamentos de buen estilo, sino condiciones de calidad estructural del diseño ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref pressmanIngenieriaSoftwareEnfoque2013|Pressman, 2013]]).

Cuando una clase acumula tareas heterogéneas, se convierte en una clase sobredimensionada, difícil de comprender y más difícil aún de mantener. Cuando, por el contrario, una responsabilidad queda fragmentada entre demasiadas clases mínimas, el sistema pierde continuidad semántica y aumenta artificialmente sus interdependencias. El arte del diseño consiste en encontrar un punto de equilibrio donde cada clase sea conceptualmente nítida y operativamente suficiente ([[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]).

### Técnicas de Asignación de Responsabilidades

Entre las técnicas más útiles para modelar responsabilidades se encuentra la práctica de identificar primero las abstracciones relevantes del dominio y luego formular para cada una sus responsabilidades, atributos y operaciones. Esta lógica está en la base de enfoques como las tarjetas CRC, donde cada clase se examina en términos de responsabilidades y colaboradores antes de formalizar el diagrama completo ([[Zk Ref jacobsonProcesoUnificadoDesarrollo2006|Jacobson et al., 2006]]; [[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]).

Un criterio práctico y didáctico consiste en revisar si cada clase posee un conjunto manejable de responsabilidades principales, si sus operaciones están alineadas con sus atributos y si sus colaboraciones son realmente necesarias. Este tipo de inspección no reemplaza el juicio conceptual del analista, pero ayuda a detectar sobrediseño, clases anémicas o distribuciones artificiales de tareas ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]).

### Ejemplo Conceptual

En un sistema académico, la clase `Estudiante` debería asumir responsabilidades relacionadas con su propio estado y trayectoria, por ejemplo conservar su matrícula, su historial y su situación académica, así como ofrecer operaciones como `inscribirse()`, `cancelarInscripcion()` u `obtenerHistorial()`. En cambio, no sería deseable que esa misma clase calcule la disponibilidad global de cupos de una `Materia` o emita reportes financieros institucionales, porque esas tareas pertenecen a otros centros de responsabilidad del modelo ([[Zk Ref weitzenfeldIngenieriaSoftwareOrientada2005|Weitzenfeld, 2005]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

De manera análoga, una clase `Materia` debe ser responsable de su código, prerrequisitos, cupos y reglas de disponibilidad; un objeto coordinador, como `SistemaDeInscripciones`, puede articular la colaboración entre ambas clases sin apropiarse del estado interno que no le pertenece. Este tipo de distribución expresa una idea crucial: coordinar no equivale a poseer, y colaborar no equivale a invadir.

**Figura**
**
![](https://www.plantuml.com/plantuml/png/VP5FRnGn3CNl-HJcL12g1DSUKFyKGQLosa_WJTnTgnbxi9rAIyLt9nEnxAo4UecYzvwVVvEvza2BDbL85-zcmzs4KF6WBS0d2XHC_imoe-447eTA_JJEoyZAoHNTRw8xsnRqa5Ks_8lWqofoY_bvPzgat6bLWqVUxUERuI5TL7eA20LR92Xib8DLKkYyo5kDq6cbNvnQAml5OIPGYxqcpzW9FwSqWE2hHokC4WIl2U0I9bpWMqMuWas_ocx8U_PGOwnTVkpt8Jf7mymgDnaBJPpFXoxxyH5OF1jlsPpUV-Z-Yt8PHaR9LD4UHc1UUiu3kWqIik_7rSCTotyVyNzWKBV-icSjlDDpyDd8Z7usTWxrDNrki_ez-wp2sqgBnn8dy1SoVkACTinmvO9bKDogLa9POzujTSDaMH5ks8CclAVLPvB3wsdFR9h9ttY7h6g51Uqaz_h_5_VIB-kVUlLl-es1upEEj7YhWIbTavGsrJy0)
*Nota*: `Estudiante` gestiona su propio estado y trayectoria; `Materia` administra su disponibilidad y cupos; `SistemaDeInscripciones` coordina la colaboración entre ambas sin apropiarse del estado que no le pertenece.

### Errores Frecuentes

Uno de los errores más comunes consiste en diseñar clases centradas solo en datos, dejando la mayor parte del comportamiento en clases externas de control o utilitarias. Ese patrón debilita el encapsulamiento y conduce a modelos donde las clases “saben” algo, pero no “hacen” casi nada, lo que empobrece la lógica orientada a objetos y aproxima el diseño a un estilo meramente procedimental disfrazado de UML ([[Zk Ref meyerObjectOrientedSoftwareConstruction1997|Meyer, 1997]]; [[Zk Ref boochAnalisisDisenoOrientado2000|Booch et al., 2000]]).

Otro error frecuente es asignar responsabilidades por conveniencia de implementación y no por coherencia conceptual. El resultado suele ser un diagrama fácil de dibujar pero difícil de sostener: clases con nombres correctos, pero con obligaciones impropias, dependencias excesivas y fronteras semánticas borrosas.

### Valor Metodológico

El modelado de responsabilidades cumple una función metodológica decisiva porque conecta el análisis del dominio con las decisiones de diseño. Permite pasar de la mera identificación de clases a la formulación de una estructura operativa del sistema, donde cada elemento no solo existe, sino que cumple un papel inteligible en la totalidad del modelo ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

Por esa razón, el diagrama de clases no solo documenta entidades y relaciones; también propone una distribución de trabajo intelectual entre los componentes del sistema. Cuando esa distribución es clara, el modelo se vuelve más comprensible, más enseñable y más resistente al cambio.

### Idea Final

Modelar responsabilidades no consiste en decidir dónde “poner métodos”, sino en establecer qué parte de la inteligencia del sistema corresponde legítimamente a cada clase. Una clase bien diseñada sabe lo que debe saber, hace lo que debe hacer y colabora sin perder su frontera conceptual; allí comienza, en rigor, el verdadero diseño orientado a objetos ([[Zk Ref boochAnalisisDisenoOrientado2000|Booch et al., 2000]]; [[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]).

### Enlaces Sugeridos

- [[Zk Clases y Objetos|Clases y Objetos]]
- [[Zk Atributos, Operaciones y Mensajes|Atributos, Operaciones y Mensajes]]
- [[Zk Encapsulamiento|Encapsulamiento]]
- [[Zk Diagrama de Clases (Elemento, Clase - Atributos)|Atributos en el Diagrama de Clases]]
- [[Zk Diagrama de Clases (Elemento, Clase -  Operaciones, Métodos)|Operaciones y Métodos en el Diagrama de Clases]]
- [[Zk Tarjetas CRC|Tarjetas CRC]]
- [[Zk Diagrama de Clases (Técnicas Comunes de Modelado)|Técnicas Comunes de Modelado]]
- [[Zk Orientación a Objetos como Paradigma de Análisis y Diseño|Orientación a Objetos]]

