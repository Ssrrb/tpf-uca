# Subconjunto PlantUML permitido (mapa a UML 2.5.1)

**Estado: BORRADOR para revisión.** Hasta que se apruebe esta tabla no se
implementan los checks (pasos 4 a 8) ni se toca ningún `.puml`.

Referencia normativa: OMG Unified Modeling Language 2.5.1, documento
`formal/17-12-05` (<https://www.omg.org/spec/UML/2.5.1/>). Los § indican el
capítulo de la especificación (7 Common Structure, 9 Classification, 10 Simple
Classifiers, 11 Structured Classifiers, 12 Packages, 14 State Machines,
15 Activities, 16 Actions, 17 Interactions, 18 Use Cases, 19 Deployments,
22 Standard Profile, Anexo C Keywords). **No verificado contra el PDF**: el
entorno donde se escribió este borrador no llega a omg.org; se confirma en el
paso 6, que descarga los archivos normativos. Base de diagramas: los 56 `.puml` de la
v9 (ver `build/inventory.md`).

## Regla

1. Cada construcción PlantUML que aparece en un `.puml` cae en una de tres categorías:
   - **Modelo**: se traduce a una metaclase UML 2.5.1 y se exporta al XMI.
   - **Presentación**: solo cambia cómo se dibuja; no crea ningún elemento del
     modelo y no se exporta (ver decisión D1).
   - **Prohibida**: no tiene metaclase UML 2.5.1. El CI falla.
2. Lo que no está en esta tabla está prohibido (lista blanca, no lista negra).
3. Los estereotipos solo valen si están declarados en un Profile del repo
   (`shared/profile.puml`), salvo las palabras clave que UML 2.5.1 define
   (Anexo C) y los estereotipos del StandardProfile (§22) listados abajo (D2).

La columna **Uso** dice si la construcción aparece en la v9 (**sí**) o no (**0**,
permitida pero sin uso hoy).

## Clases (§9, §10, §11)

| PlantUML | Metaclase UML 2.5.1 | Notas | Uso |
|---|---|---|---|
| `class X` | Class (§11) | | sí |
| `abstract class X` / `abstract X` | Class con `isAbstract = true` | | sí |
| `interface X` | Interface (§10) | | 0 |
| `enum X { A B }` | Enumeration + EnumerationLiteral (§10) | | sí |
| `package "P" { }` | Package (§12) | | sí |
| `class "Etiqueta" as Alias` | Class `name = Alias` | La etiqueta es solo presentación (D5) | sí |
| atributo `nombre: Tipo [m..n] = valor` | Property (§9) con type, multiplicidad y defaultValue | Tipo debe resolverse a un Type del modelo (D3) | sí |
| operación `+ op(p: T): R [m..n]` | Operation + Parameter (§9) | Parámetros sin tipo: permitido (type es opcional) | sí |
| visibilidad `+ - # ~` | VisibilityKind public, private, protected, package (§7) | Hoy solo las operaciones la llevan (D4) | sí |
| `{readOnly}` `{unique}` `{ordered}` `{id}` `{redefines x}` `{subsets x}` | Modificadores de Property (§9) | `{estable}` e `{inmutable}` no son UML (D10) | sí |
| `{static}` / subrayado, `{abstract}` en operación | isStatic, isAbstract | | 0 |
| `A <\|-- B` / `B --\|> A` | Generalization (§9) | Entre clasificadores del mismo tipo, sin ciclos | sí |
| `I <\|.. C` / `C ..\|> I` | InterfaceRealization (§10) | El destino debe ser `interface` | 0 |
| `A "1" *-- "0..*" B` | Association con `aggregation = composite` (§11) | Lado del todo: 1 o 0..1 | sí |
| `A "1" o-- "0..*" B` | Association con `aggregation = shared` | | sí |
| `A "m" --> "n" B` | Association; el extremo B navegable (`ownedEnd` navegable) | | sí |
| `A "m" -- "n" B` | Association no dirigida | | sí |
| `A ..> B` | Dependency (§7) | `: <<use>>` → Usage (§7) | sí |
| multiplicidad `"1"`, `"0..1"`, `"0..*"`, `"1..*"`, `"*"`, `"n..m"` | MultiplicityElement lower/upper (§7) | **Obligatoria en ambos extremos** de toda asociación | sí |
| etiqueta de asociación `: nombre` | Association.name | | sí |
| `note ... of X` / `note "..." as N` + `N .. X` | Comment con annotatedElement (§7) | | sí |

Prohibidas en clases: `entity`, `struct`, `protocol`, `annotation`,
`metaclass`, `circle`, `exception`, `stereotype`, `dataclass`, `record`,
`object`, `map`, `json`, `diamond`, `<>` (nodo n-ario de PlantUML), `+--`
(contención anidada de PlantUML), `#--`, `x--`, `}--` (pata de gallo) y
cualquier tipo de dato con semántica de otro lenguaje (`String[]`,
`List<T>`, `Map<K,V>`, `int`, `void`). Uso hoy: 0.

## Secuencia (§17)

| PlantUML | Metaclase UML 2.5.1 | Notas | Uso |
|---|---|---|---|
| diagrama completo | Interaction (§17) | | sí |
| `participant "rol:\nClase" as A` | Lifeline; `represents` = Property tipada por `Clase` | `Clase` debe existir en algún diagrama de clases | sí |
| `actor "X" as A` | Lifeline que representa una Property tipada por el Actor X | | sí |
| `A -> B : op(args)` | Message `messageSort = synchCall`, `signature` = Operation de B | La operación debe existir en la clase de B | sí |
| `A ->> B : señal` | Message `asynchCall` / `asynchSignal` | | 0 |
| `B --> A : valor` | Message `messageSort = reply` | | sí |
| `create B` + `A -> B : «create»(...)` | Message `messageSort = createMessage` (§17) | `«create»` es la palabra clave de la notación, no un estereotipo | sí |
| `destroy B` / `A -> B !! ` | DestructionOccurrenceSpecification + `deleteMessage` | | 0 |
| `alt [g] ... else [g] ... end` | CombinedFragment `interactionOperator = alt` + InteractionOperand con guard | Guarda obligatoria | sí |
| `opt`, `loop`, `par`, `break`, `critical` | CombinedFragment con ese InteractionOperatorKind (§17) | `opt`, `loop`, `break` con guarda | sí |
| `ref over A, B : Nombre` / `ref over ... end ref` | **InteractionUse** (§17), no CombinedFragment | Debe nombrar otra Interaction del repo (D7) | sí |
| `activate` / `deactivate` | ExecutionSpecification (§17) | | 0 |
| `note over/left of/right of` | Comment | | sí |

Prohibidas en secuencia: `group` (no es operador UML; ya la prohíbe SQ1),
`boundary`, `control`, `entity`, `database`, `collections`, `queue` (son
estereotipos de robustez o íconos sin Profile), `<->` (mensaje bidireccional),
`->x` (mensaje perdido sin semántica definida en PlantUML), `return`
(abreviatura de PlantUML que infiere el receptor), `autonumber`, `newpage`,
`...` y `|||` (separadores gráficos), `== sección ==` (divisor sin
metaclase). Uso hoy: 0.

`box "ERP" ... end box` no tiene metaclase (UML 2.5.1 no agrupa lifelines
fuera de un fragmento). Se usa en las 18 secuencias: ver D1.

## Casos de uso (§18)

| PlantUML | Metaclase UML 2.5.1 | Notas | Uso |
|---|---|---|---|
| `actor "X" as A` | Actor (§18) | Fuera del sujeto | sí |
| `usecase "Nombre" as U` | UseCase (§18) | | sí |
| `rectangle "Sistema" { ... }` | Classifier sujeto (`UseCase.subject`, §18) | Un sujeto | sí |
| `A -- U` | Association binaria actor–caso de uso | Sin flecha | sí |
| `B ..> I : <<include>>` | Include (§18) | Del base al incluido | 0 |
| `E ..> B : <<extend>>` | Extend (+ ExtensionPoint) | Del que extiende al base | 0 |
| `P <\|-- H` | Generalization (actor–actor o CU–CU) | | sí |
| `package` dentro del `rectangle` | **No válido**: un Classifier sujeto no puede contener Packages (D6) | | sí |

## Estados (§14)

| PlantUML | Metaclase UML 2.5.1 | Uso |
|---|---|---|
| diagrama | StateMachine con una Region | sí |
| `state X` / `state "Etiqueta" as X` | State (§14) | sí |
| `state X { ... }` | State compuesto con Region; `--` o `\|\|` separa regiones ortogonales | 0 |
| `[*] --> X` | Pseudostate `kind = initial` | sí |
| `X --> [*]` | FinalState | sí |
| `state C <<choice>>` | Pseudostate `kind = choice` | sí |
| `<<fork>>`, `<<join>>`, `<<junction>>`, `<<entryPoint>>`, `<<exitPoint>>`, `[H]`, `[H*]`, `<<end>>` | Pseudostate fork, join, junction, entryPoint, exitPoint, shallowHistory, deepHistory, terminate | 0 |
| `X --> Y : evento [guarda] / acción` | Transition con Trigger, guard (Constraint) y effect (OpaqueBehavior) | sí |
| `X : entry / a`, `X : do / a`, `X : exit / a` | State.entry, doActivity, exit | 0 |
| `X : evento [g] / a` | Transition interna (`kind = internal`) | 0 |

Prohibido: texto libre en el compartimento del estado que no sea `entry`, `do`,
`exit` ni una transición interna. Hoy `CU-01-estados` tiene 7 líneas así
(`en_ejecucion : mediciones y certificados: sí`), ver D8. También prohibidos
`<<sdlreceive>>`, `<<inputPin>>`, `<<outputPin>>`, `<<expansionInput>>`,
`<<expansionOutput>>` (son de PlantUML/SDL) y la notación vieja `(*)`.

## Actividades (§15, §16)

| PlantUML (sintaxis nueva) | Metaclase UML 2.5.1 | Uso |
|---|---|---|
| diagrama | Activity | sí |
| `start` | InitialNode | sí |
| `stop` / `end` | ActivityFinalNode | sí |
| `kill` | FlowFinalNode | 0 |
| `:acción;` | OpaqueAction | sí |
| `if (c) then ([g]) ... else ([g]) endif`, `elseif`, `switch/case` | DecisionNode + MergeNode; guardas en los ControlFlow | sí |
| `repeat ... repeat while (c) is ([g]) not ([g])` | MergeNode + DecisionNode con flujo de retorno | sí |
| `while (c) is ([g]) ... endwhile ([g])` | DecisionNode + MergeNode | 0 |
| `fork / fork again / end fork` | ForkNode + JoinNode | sí |
| `\|Carril\|` | ActivityPartition | sí |
| flechas implícitas entre nodos | ControlFlow | sí |
| `note` | Comment | sí |

Prohibido en actividades: `split` (sin JoinNode no hay semántica UML),
`detach`, `backward` (flecha de retorno sin nodo), `partition` y `group`
(agrupación gráfica; el equivalente es el carril), SDL (`:x<`, `:x>`, `:x/`,
`:x]`, `:x}`), `-[#color]->` con texto que no sea guarda, y la sintaxis vieja
`(*) --> `. Uso hoy: 0.

## Paquetes, componentes y despliegue (§12, §11, §19)

| PlantUML | Metaclase UML 2.5.1 | Uso |
|---|---|---|
| `package` | Package | sí |
| `P1 ..> P2 : <<use>>` | Usage | sí |
| `P1 ..> P2 : <<import>>` / `<<access>>` | PackageImport (visibility public / private) | 0 |
| `P1 ..> P2 : <<merge>>` | PackageMerge | 0 |
| `component C`, `[C]` | Component (§11) | 0 |
| `() "I"` / `interface I` + `C - I` (provista), `C ..> I` (requerida) | Interface + InterfaceRealization / Usage | 0 |
| `port` | Port | 0 |
| `node N` | Node (§19) | 0 |
| `artifact A` | Artifact (§19) | 0 |
| `A ..> N : <<deploy>>` | Deployment | 0 |
| `N1 -- N2` | CommunicationPath | 0 |

Prohibido: `folder`, `frame`, `cloud`, `database`, `storage`, `card`, `file`,
`hexagon`, `stack`, `queue`, `agent`, `boundary`, `control`, `label`,
`person` (íconos sin metaclase). Uso hoy: 0.

## Palabras clave y estereotipos sin Profile (D2)

| Texto | Qué es en UML 2.5.1 |
|---|---|
| `<<include>>`, `<<extend>>` | Palabras clave de Include y Extend (Anexo C) |
| `<<use>>`, `<<import>>`, `<<access>>`, `<<merge>>`, `<<deploy>>` | Palabras clave de Usage, PackageImport, PackageMerge, Deployment |
| `«create»` en un mensaje | Notación del createMessage |
| `<<choice>>`, `<<fork>>`, `<<join>>`, `<<junction>>`, `<<entryPoint>>`, `<<exitPoint>>`, `<<end>>` | Clase de Pseudostate (PlantUML los escribe como estereotipo) |

Cualquier otro `<<...>>` necesita estar en `shared/profile.puml` como
Stereotype que extiende una metaclase.

## Presentación (no se exporta)

`@startuml/@enduml`, `!theme plain`, `skinparam ...` (incluida
`skinparam style strictuml`, que exige G1), `hide`/`show`/`remove`,
`left to right direction`, `top to bottom direction`, `title`, `legend ...
endlegend`, `hide footbox`, `header`/`footer`/`caption`, `!include`,
`!define`/`!procedure` (macros del preprocesador), colores `#RRGGBB`,
`together { }`, direcciones en flechas (`-up->`, `-l->`), enlaces ocultos
`-[hidden]-`, y `box ... end box` en secuencia (D1).

## Decisiones que necesito de vos

Cada una tiene mi recomendación. Las que cambian `.puml` se aplican recién
después de que veas el reporte de violaciones.

- **D1. Presentación sin metaclase (`box`, `legend`, `title`, `skinparam`).**
  Leída al pie de la letra, la regla prohíbe todo lo que no tenga metaclase,
  y eso incluye `box` (18 secuencias) y `legend` (20 diagramas).
  *Recomiendo* la categoría "presentación": se permite, no crea elementos y
  no va al XMI. La alternativa estricta obliga a sacar las cajas ERP/ECMS de
  todas las secuencias y las leyendas.
- **D2. Palabras clave sin Profile.** *Recomiendo* aceptar las de la tabla de
  arriba (son de UML 2.5.1) y exigir Profile para cualquier otra.
- **D3. Tipos de los atributos.** Hoy son texto libre en castellano: `texto`
  (57), `guaraníes` (45), `decimal` (36), `fecha` (16), `fecha y hora` (11),
  `lógico` (10), `entero` (8), `archivo` (6), y uniones como
  `porcentaje | importe` (unas 25). Las uniones no existen en UML.
  *Recomiendo* declarar en el glosario PrimitiveType/DataType con esos nombres
  (`texto`→String, `entero`→Integer, `decimal`→Real, `lógico`→Boolean, y
  DataType `fecha`, `fechaHora`, `guaraníes`, `archivo`) y convertir cada
  unión en una Enumeration. Esto cambia unos 25 atributos.
- **D4. Visibilidad.** Ningún atributo la lleva; todas las operaciones llevan `+`.
  En UML es opcional. *Recomiendo* no exigirla, pero si aparece debe ser
  `+ - # ~`.
- **D5. Nombre canónico de las clases.** Unas 45 clases tienen etiqueta con
  espacios o tildes (`"Cambio de estado" as CambioEstado`). *Recomiendo* que el
  nombre UML sea el alias (PascalCase, sin espacios) y la etiqueta quede como
  presentación para el documento de la cátedra. Hay además nombres en plural
  (`Liquidaciones`, `Consumos de la obra`) que violan "singular".
- **D6. Paquetes dentro del sujeto en CU-00.** UML no permite Packages dentro
  de un Classifier sujeto. *Recomiendo* sacar los tres `package` del
  `rectangle` y marcar el subsistema en el nombre o con una nota. La otra
  opción es tres sujetos (ERP, ECMS, Motor de finanzas), pero choca con UC1 de
  la cátedra (un solo sujeto).
- **D7. `ref`.** Es InteractionUse, no CombinedFragment. Dos de los cuatro
  `ref` dicen "Continúa en 2/2: ...", que no nombra una Interaction.
  *Recomiendo* exigir que el texto sea el título de otra secuencia del repo.
- **D8. Texto libre en estados.** Las 7 líneas de `CU-01-estados` no son
  `entry/do/exit`. *Recomiendo* pasarlas a una nota (Comment).
- **D9. Literales de enumeración.** Hoy en snake_case (`en_ejecucion`). La
  convención del paso 3 no los menciona. *Recomiendo* dejarlos así.
- **D10. `{estable}` (6) e `{inmutable}` (3).** No son modificadores UML.
  *Recomiendo* `{inmutable}` → `{readOnly}` y `{estable}` → nota, o
  declararlos como Constraint con nombre.

## Lo que esta tabla no decide

- El mapeo exacto de PlantUML a XMI (qué `xmi:type` y qué propiedades) se fija
  en el paso 6; si algún renglón no se puede exportar fielmente, se marca acá.
- Las restricciones OCL de la especificación no se verifican con esta tabla;
  su cobertura sale del paso 6 (validador de Eclipse UML2).
