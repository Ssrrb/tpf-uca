# Mapa PlantUML → UML 2.5.1 (conversión a XMI)

## Flujo

```
modelar rápido en .puml  →  tools/ (parser)  →  build/model.json  →  build/model.xmi (UML 2.5.1)  →  Visual Paradigm
```

- Los `.puml` son el borrador de modelado: **no tienen que cumplir UML 2.5.1**
  y no se reescriben para eso. Siguen las reglas de la cátedra que ya controla
  `tools/check_uml.py`.
- Lo que tiene que ser UML 2.5.1 es el **XMI**. Este documento dice cómo cada
  construcción PlantUML se traduce a una metaclase UML 2.5.1, qué se descarta
  y qué hace fallar la conversión.
- **Alcance:** CU-01 a CU-16. CU-00 (casos de uso de alto nivel, generalización
  de actores, clases generales y paquetes) no entra al XMI ni al proyecto de VP.

Referencia: OMG UML 2.5.1, `formal/17-12-05` (<https://www.omg.org/spec/UML/2.5.1/>).
Los § indican capítulo. No verificado contra el PDF todavía: este entorno no
llega a omg.org; lo confirma el paso 6 en GitHub Actions.

## Qué hace fallar el CI

1. Una construcción que el conversor no sabe traducir (no está en estas tablas).
2. Una referencia que no se puede resolver en un modelo único (un mensaje a una
   operación que no existe, una lifeline sin clase, una relación hacia una
   clase no definida, la misma asociación con multiplicidades incompatibles).
3. Un XMI que no valida contra los archivos normativos de OMG o el validador de
   Eclipse UML2.

Lo que se descarta en la conversión **no** falla: es presentación.

## Clases (§7, §9, §10, §11, §12)

| PlantUML | En el XMI (UML 2.5.1) |
|---|---|
| `class X`, `class "Etiqueta" as X` | Class `name = X` (el alias). La etiqueta se descarta (R1) |
| `abstract class X` | Class `isAbstract = true` |
| `interface X` | Interface |
| `enum X { a b }` | Enumeration + EnumerationLiteral |
| `package "P" { }` | Package (la misma clase en varios CU se une en una sola) |
| atributo `nombre: tipo [m..n]` | Property con type y multiplicidad (R2, R3) |
| `+ op(p, q: T): R [m..n]` | Operation + Parameter (in) + Parameter return |
| `+ - # ~` | visibility public, private, protected, package; sin símbolo, sin visibilidad |
| `{inmutable}` | `isReadOnly = true` |
| `{estable}` | Comment sobre la Property (no hay modificador UML equivalente) |
| `A <\|-- B` | Generalization |
| `I <\|.. C` | InterfaceRealization |
| `A "1" *-- "0..*" B` | Association, extremo de A con `aggregation = composite` |
| `A "1" o-- "0..*" B` | Association, `aggregation = shared` |
| `A "m" --> "n" B` | Association; el extremo de B es atributo de A (navegable) y el de A es ownedEnd |
| `A "m" -- "n" B` | Association con ambos extremos como ownedEnd |
| `A ..> B`, `: <<use>>` | Dependency, Usage |
| `note ... of X` | Comment con annotatedElement = X |
| `legend`, `title`, `skinparam`, `hide`, colores | se descartan |

## Secuencia (§17)

| PlantUML | En el XMI |
|---|---|
| cada diagrama | Interaction, dueña: una Collaboration por CU |
| `participant "rol:\nClase" as A` | Lifeline `name = rol`; `represents` = Property `rol` tipada por `Clase` |
| `actor "X" as A` | Lifeline que representa una Property tipada por el Actor X |
| `A -> B : op(...)` | Message `synchCall`, `signature` = Operation `op` de la clase de B |
| `B --> A : valor` | Message `reply` |
| `create B` + `A -> B : «create»(...)` | Message `createMessage` |
| `alt opt loop par break critical` | CombinedFragment con ese operador; la guarda va a InteractionConstraint |
| `ref over A, B ... end ref` | InteractionUse; si el texto nombra otra secuencia, `refersTo` apunta a ella; si no, queda el texto como Comment |
| `box "ERP"` | se descarta |
| `note` | Comment |

Las ocurrencias de envío y recepción se generan como
MessageOccurrenceSpecification en el orden del archivo.

## Estados (§14)

| PlantUML | En el XMI |
|---|---|
| diagrama | StateMachine con una Region |
| `state X`, `state "Etiqueta" as X` | State `name = X` |
| `[*] -->` / `--> [*]` | Pseudostate initial / FinalState |
| `state C <<choice>>` | Pseudostate choice |
| `X --> Y : evento [guarda] / acción` | Transition con Trigger (evento), guard y effect (OpaqueBehavior) |
| `X : entry/do/exit / a` | entry, doActivity, exit |
| `X : texto libre` | Comment sobre el State (R4) |

## Actividades (§15, §16)

| PlantUML | En el XMI |
|---|---|
| diagrama | Activity |
| `start` / `stop`, `end` / `kill` | InitialNode / ActivityFinalNode / FlowFinalNode |
| `:acción;` | OpaqueAction |
| `if/elseif/else/endif`, `repeat ... repeat while`, `while` | DecisionNode + MergeNode; las guardas van en los ControlFlow |
| `fork / fork again / end fork` | ForkNode + JoinNode |
| `\|Carril\|` | ActivityPartition |
| flechas implícitas | ControlFlow |

## Reglas de conversión

- **R1. Nombres.** El nombre UML de una clase es el alias (`CambioEstado`), no
  la etiqueta (`"Cambio de estado"`). Así cada entidad tiene un único nombre en
  todo el modelo y VP no la ve duplicada.
- **R2. Tipos.** Los tipos en castellano se traducen a PrimitiveTypes de UML:
  `texto` → String, `entero` → Integer, `decimal` → Real, `lógico` → Boolean.
  `fecha`, `fecha y hora`, `guaraníes`, `archivo` y `lista de texto` pasan a
  DataType del paquete `Tipos`. Una clase o enumeración del modelo se usa tal cual.
- **R3. Uniones.** `porcentaje | importe` no existe en UML: se genera una
  Enumeration `<Clase><Atributo>` (por ejemplo `AnticipoModalidad`) con esos
  literales, en el paquete `Tipos`.
- **R4. Texto libre.** Lo que no tiene metaclase pero aporta información (texto
  en el compartimento de un estado, `{estable}`, `ref` sin destino) se conserva
  como Comment en vez de perderse.

## Lo que esta tabla no cubre

- Casos de uso, paquetes, componentes y despliegue: no hay diagramas de esos
  tipos en CU-01 a CU-16.
- Restricciones OCL de la especificación: su cobertura sale del paso 6.
