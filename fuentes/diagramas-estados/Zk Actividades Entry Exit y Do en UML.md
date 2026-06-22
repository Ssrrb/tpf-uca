---
Title: Zk Actividades Entry Exit y Do en UML
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
  - Actividades de Estado en UML
  - Entry Exit y Do
  - Comportamientos de Entrada Salida y Permanencia
---
## Actividades Entry Exit y Do en UML

En una máquina de estados UML, un estado puede tener comportamientos asociados a su entrada, permanencia y salida. Estos comportamientos se expresan habitualmente mediante `entry/`, `do/` y `exit/`, y permiten separar lo que ocurre al entrar en un estado, lo que se ejecuta mientras el estado permanece activo y lo que se realiza al abandonarlo ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Tipos

- **`entry/`**: comportamiento ejecutado al entrar en el estado.
- **`exit/`**: comportamiento ejecutado al salir del estado.
- **`do/`**: actividad ejecutada mientras el estado permanece activo.

### Criterio de Uso

Una acción como `registrarEmision` suele pertenecer a la transición que conduce a `Emitida` si representa la consecuencia directa de un evento. En cambio, una acción como `iniciarTemporizador` puede ser una actividad de entrada si debe ejecutarse siempre que se entra a un estado, sin importar desde qué transición se llegó ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Advertencia Conceptual

Las actividades `do` son más delicadas que `entry` y `exit`, porque pueden implicar ejecución prolongada, interrupción y concurrencia. Esta dificultad ha sido discutida en estudios recientes sobre la semántica de máquinas de estado UML/PSSM, donde las actividades ejecutadas durante la permanencia en un estado pueden introducir problemas de sincronización y no determinismo ([[Zk Ref elekesSemanticsPatternsDoActivities2024|Elekes et al., 2024]]).

### Enlaces Sugeridos

- [[Zk Estado en UML|Estado en UML]]
- [[Zk Efecto de Transición en UML|Efecto de Transición]]
- [[Zk Región Ortogonal en Máquina de Estados UML|Región Ortogonal]]
