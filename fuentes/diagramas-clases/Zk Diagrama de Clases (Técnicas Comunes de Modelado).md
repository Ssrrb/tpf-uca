---
Title: Zk Diagrama de Clases (Técnicas Comunes de Modelado)
TipoNota: permanente
Fecha: 2025-05-12 12:14
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
## Diagrama de Clases (Técnicas Comunes de Modelado)

Las técnicas de modelado en diagramas de clases permiten capturar la estructura estática de sistemas mediante cuatro enfoques complementarios: definición del vocabulario del dominio, distribución equilibrada de responsabilidades, modelado de entidades no software y gestión de datos primitivos. Estas técnicas se alinean con los principios fundamentales del UML [[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|(Booch et al., 2006)]].

### Vocabulario del Sistema

#### Objetivo
Identificar y formalizar las abstracciones clave del dominio.

| Componente                 | Acciones                                                                                                                         | Participantes Involucrados |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Abstracciones**          | Modelar conceptos relevantes del entorno analizado                                                                               | Usuarios y desarrolladores |
| **Captura de vocabulario** | - Identificar conceptos clave  <br>- Definir para cada abstracción:  <br>- Responsabilidades  <br>- Atributos  <br>- Operaciones | Equipo interdisciplinario  |

#### Ejemplo  
En un sistema bancario, las abstracciones incluyen `Cuenta`, `Transacción` y `Cliente`, cada una con atributos como `saldo` y operaciones como `realizarDepósito()`.

### Distribución de Responsabilidades

#### Principio Rector
Equilibrio entre cohesión y acoplamiento [[050 Base de Conocimientos/900 Biblioteca/boochLenguajeUnificadoModelado2006/Zk Ref boochLenguajeUnificadoModelado2006|(Booch et al., 2006) ]]

#### Técnicas

1. **Responsabilidad única:** Cada clase modela una entidad discreta.
2. **Colaboración:** Grupos de clases trabajan para objetivos comunes.
3. **Refinamiento iterativo:**
    - Dividir clases sobredimensionadas
    - Consolidar clases mínimas
    - Buscar equilibrio en la carga funcional

#### Checklist de Validación

- ¿Cada clase tiene 3-7 responsabilidades principales?
- ¿Las operaciones están alineadas con los atributos de la clase?
    

### Modelado de Elementos No Software

#### Alcance
Incluir entidades físicas o conceptuales del dominio.

| Tipo                     | Ejemplos                 | Representación UML                    |
| ------------------------ | ------------------------ | ------------------------------------- |
| **Entidades físicas**    | Dispositivos, documentos | Clases con estereotipo `<<Physical>>` |
| **Conceptos abstractos** | Políticas, regulaciones  | Clases con notas adjuntas             |

### Modelado de Datos Primitivos

#### Estrategia

Cuando un tipo de dato primitivo (p. ej., un número de teléfono, una dirección postal, un
rango de fechas) requiere operaciones o validaciones propias, se eleva a clase en lugar de
permanecer como atributo simple [(Booch et al., 2006)](Zk Ref boochLenguajeUnificadoModelado2006).

| Situación | Enfoque recomendado |
|-----------|---------------------|
| Solo almacena valor sin lógica | Atributo de tipo primitivo |
| Necesita validación o conversión | Clase dedicada (p. ej., `Dinero`, `Telefono`) |
| Se reutiliza en múltiples clases | Clase de tipo de valor (*value object*) |

### Buenas Prácticas

- Comenzar el modelado capturando el **vocabulario del dominio** antes de asignar
  responsabilidades; el vocabulario fija el lenguaje compartido entre usuarios y
  desarrolladores [(Booch et al., 2006)](Zk Ref boochLenguajeUnificadoModelado2006).
- Aplicar el principio de **responsabilidad única**: una clase debe tener una sola razón
  para cambiar [(Rumbaugh et al., 2007)](Zk Ref rumbaughLenguajeUnificadoModelado2007).
- Elevar primitivos a clases solo cuando el tipo necesita **comportamiento propio**; hacerlo
  indiscriminadamente infla el modelo sin beneficio.
- Modelar entidades no software con **estereotipos UML** apropiados
  (`«hardware»`, `«document»`, `«policy»`) para que el lector distinga elementos del
  sistema de elementos del entorno.

### Errores Comunes

| Error | Consecuencia | Corrección |
|-------|-------------|------------|
| Clases con demasiadas responsabilidades (*God class*) | Alta fragilidad ante cambios | Dividir por cohesión funcional |
| Omitir entidades no software | Modelo incompleto del dominio | Incluir con estereotipos |
| Elevar todos los primitivos a clases | Modelo sobrecargado | Elevar solo los que tienen comportamiento |

### Enlaces Sugeridos

- [[Zk Diagrama de Clases (Elementos, Clases)|Clases]]
- [[Zk Diagrama de Clases (Clases Abstractas)|Clases Abstractas]]
- [[Zk Diagrama de Clases (Elementos, Interfaces)|Interfaces]]
- [[Zk Diagrama de Clases (Relaciones)|Relaciones]]

