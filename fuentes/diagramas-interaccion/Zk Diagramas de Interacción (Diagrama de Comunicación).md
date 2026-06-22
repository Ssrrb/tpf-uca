---
Title: Zk Diagramas de Interacción (Diagrama de Comunicación)
TipoNota: permanente
Fecha: 2025-05-19 09:02
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
dg-publish: true
publish: true
---
## Diagramas de Interacción (Diagrama de Comunicación)

Un **diagrama de comunicación UML** (anteriormente llamado diagrama de colaboración) es un tipo de diagrama de interacción que modela cómo los **objetos** y **actores** colaboran, mostrando explícitamente las **relaciones estructurales** (**enlaces**) entre ellos y el flujo de mensajes que intercambian para cumplir una función o caso de uso. A diferencia del diagrama de secuencia, el énfasis está en la organización espacial y las conexiones entre objetos, no en el orden temporal de los mensajes, aunque este se indica mediante numeración secuencial ([[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]; [[Zk Ref pressmanIngenieriaSoftwareEnfoque2013|Pressman, 2013]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]).

### Casos de Uso de Aplicación

Los diagramas de  comunicación se emplean para ([[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref pressmanIngenieriaSoftwareEnfoque2013|Pressman, 2013]]; [[Zk Ref rumbaughLenguajeUnificadoModelado2007|Rumbaugh et al., 2007]]):

- Visualizar la estructura de colaboración entre objetos en la ejecución de un escenario o caso de uso.
- Analizar y documentar cómo los objetos están conectados y cómo fluyen los mensajes a través de dichos enlaces.
- Identificar dependencias y relaciones entre componentes, facilitando el diseño de arquitecturas desacopladas.
- Complementar diagramas de secuencia, proporcionando una visión estructural de las interacciones, útil para detectar redundancias o acoplamientos excesivos.

### Elementos Principales

| Elemento            | Descripción                                                                             |
| ------------------- | --------------------------------------------------------------------------------------- |
| Actor               | Usuario o sistema externo que interactúa con el sistema.                                |
| Objeto/Participante | Instancia que participa en la colaboración (rectángulo con nombre subrayado o tipo).    |
| Enlace/Conector     | Línea que representa una relación estructural (asociación, enlace) entre objetos.       |
| Mensaje             | Flecha sobre el enlace, etiquetada con número secuencial y nombre del mensaje.          |
| Número de secuencia | Indica el orden de los mensajes (1, 2, etc.), esencial para comprender el flujo lógico. |
| Notas               | Comentarios o aclaraciones sobre elementos o interacciones.                             |

### Ejemplos

### Ejemplo 1

**Figura**
_Ejemplo Genérico de Diagrama de Comunicación_
![](https://www.plantuml.com/plantuml/png/RP1HYzKm48NVyojcYrXzADXsLw7eibSVHD0dmITXcRQnczqqKoTJfVlhJNflQoxSKa9wpjSpXxdpWYppQ47bLnFZC29ON6WMyACMTAZyat4JCexWPR4wd6ow-4lYT1QzFqXmsbdqbuxST_EiuKs2VCJkQM2QNV-9B35yDSE3V6PSL6xrBm4Xu2X1RrXtOiWfeIdABOdGcEZv_rHhd9Pbqa0i3wHyXw5XgLJ-0zbWQxLNLo-yXG_PJvU5QwyvtD-_H6RwMwm3RpC8Xdd-dHYnqMtaaLC-50eqHBt5H3ysNAtmgaCdnB2Uzw5Bh8rk2CMoXjf7BNHVPe0UZX_b9Q1AWEeIK2T0VGbm2U2KEhM1ek1Y6mmDb0ryqyxZeovVlOPrFN5TRtVvEifnEL5-jyit9rfjKKNHRxbLoArsieeajfYGQO6wWSCiT8BFsGeAtk4wmDTxQdq-lqhdkq3UDE1c_OUsmFZSQTVFe_q7)

```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
'left to right direction
'top to bottom direction
skinparam linestyle ortho
scale 1

'Variables
!$sl ="\n"
!$der ="<&arrow-right>" 
!$izq ="<&arrow-left>"
!$arr ="<&arrow-top>"  
!$aba ="<&arrow-bottom>"  
  

Actor Actor_1

rectangle ":objeto_1" as objeto1
rectangle ":objeto_2" as objeto2
rectangle ":objeto_3" as objeto3
rectangle ":objeto_n" as objeton

Actor_1 --r- objeto1 : 1: Mensaje1() $der $sl 6: Mensaje4() $izq $sl 7: Mensaje5() $der
objeto1 --d- objeto2 : 2: Mensaje2() $aba
objeto1 --- objeto1 : 3: AutoMensaje() $aba
objeto2 -r-- objeto3 : 4: Mensaje3() $der
objeto2 --d- objeton : 5: nuevo() $aba

@enduml
```
Nota:
- Elaboración Propia, usando la herramienta [[Zk (Plantuml) Herramienta para crear Diagramas a Partir de Texto|Plantuml]].
- Este diagrama es la versión equivalente a:

![[Zk Diagramas de Interacción (Diagrama de Secuencia)#Ejemplo 1]]


#### Ejemplo 2

**Figura**
_Ejemplo Básico Diagrama de Comunicación de un Esquema de Autenticación de Usuario_
![](https://www.plantuml.com/plantuml/png/TL9DRzD04BtlhvX6Y8249GgSBAWQUe1AlGLwuZ9PJvnLrZjXPgpY_dfsNQTrMbMAulNxUFjcv4ir5Ekx26vvTX1iEuI80_S6sf5XGgVxa0ues87Q42d_I_35CcDyHDMLPMRJ6rrxJkjmJ_1n9lcEVjyAzwcvuiW2Dw7TsG_1mIqZRGsCGGe4JH3o5ZYvfV6Xu1isusvEFCN6aCY60m6BxTYfnqXmxjpo5YNW9fAwipSQuTlYJrhaOqEIpr_VeWZVLUED5ml8HBZ_EoDAfOkYHvdhSw6iXe9lS8O_D1of_5jvOu7VsgC4TgwqnjH6WaLzdLeXPOphe4OTBW0LdeCdZZNvNe8De_BuyaoX6ZXDWd8yeM-ulU94_p9EEefE45SQkwaiL5Azg0CrdDSG6aeMji6Zpxv9_wv_U7w00whUiJJleMoxhDcv5q5LKpsEa5F79NwguPPa39RNKvrxz5NLDEKnuNCDAmsfHJaQitoILB4w7JURljGGkGtfbw3VFzsr9R_3domuZP0_27T9gUcx-1y0)


```plantuml-code
@startuml
!pragma layout smetana
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam BackgroundColor LightGray
'left to right direction
'top to bottom direction
skinparam linestyle ortho
scale 1

'Variables
!$sl ="\n"
!$der ="<&arrow-right>" 
!$izq ="<&arrow-left>"
!$arr ="<&arrow-top>"  
!$aba ="<&arrow-bottom>"  
  
Actor Usuario

rectangle ":IngresoalSistema" as IngresoalSistema
rectangle ":Security" as Security
rectangle ":Session" as Sesion
rectangle ":LogConexiones" as LogConexiones

  

Usuario -r- IngresoalSistema : 1: identificacionUsuario(usuario, password) $sl $der

IngresoalSistema -d- Security : $aba 2: VerificarUsuario(usuario, password)

Security -- Sesion : $aba 3: Asingar(usuario)

Sesion -l- LogConexiones : 4: loginTrack(usuario, fechaHora) $sl $izq
@enduml
```
Nota:
- Elaboración Propia, usando la herramienta [[Zk (Plantuml) Herramienta para crear Diagramas a Partir de Texto|Plantuml]]. 
- Este diagrama es la versión equivalente a:

![[Zk Diagramas de Interacción (Diagrama de Secuencia)#Ejemplo 2]]
