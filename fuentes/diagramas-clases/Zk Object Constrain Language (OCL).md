---
Title: Zk Object Constrain Language (OCL)
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
  - OCL
  - Object Constrain Language
  - Object Constrain Language (OCL)
---
## Object Constrain Language (OCL)

**OCL** es un lenguaje formal de texto, puro y sin efectos secundarios, diseñado por el [[Zk OMG - Object Management Group|OMG]] para añadir precisión a los modelos de software. Se utiliza principalmente para definir restricciones (constraints) que los diagramas de clases UML no pueden expresar gráficamente, como reglas de negocio complejas o invariantes de estado ([[Zk Ref objectmanagementgroupomgObjectConstraintLanguage2014|OMG, 2014]]).

### Estructura de una Expresión
Toda expresión OCL requiere un **Contexto** y un **Cuerpo**.

#### Invariantes (`inv`)
Condiciones que deben cumplirse siempre para todas las instancias de una clase.
```ocl
context Persona
inv: self.edad >= 0
```

#### Pre y Post condiciones (`pre`, `post`)

Definen el contrato de ejecución de una operación.

Object Constraint Language

```ocl
context Cuenta::retirar(monto: Real)
pre: monto > 0 and self.saldo >= monto
post: self.saldo = self.saldo@pre - monto
```

### Colecciones en OCL

OCL es extremadamente potente para manejar grupos de objetos mediante cuatro tipos básicos:

| Tipo           | ¿Permite Duplicados? | ¿Tiene Orden? |
| -------------- |:--------------------:|:-------------:|
| **Set**        | No                   | No            |
| **OrderedSet** | No                   | Sí            |
| **Bag**        | Sí                   | No            |
| **Sequence**   | Sí                   | Sí            |

### Justificación Técnica

1. **Precisión:** Elimina la ambigüedad del lenguaje natural en los requisitos.
    
2. **Side-Effect Free:** Garantiza que la evaluación de una restricción no altere el estado del sistema.
    
3. **Poder de Consulta:** Permite navegar por asociaciones complejas (ejemplo: `self.cliente.pedidos->select(total > 100)`).
    

### Enlaces Sugeridos

[[Zk UML - Unified Modeling Language Antecedentes|Lenguaje Unificado de Modelado]]
