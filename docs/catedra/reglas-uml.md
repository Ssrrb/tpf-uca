# Reglas UML de la cátedra y cómo las verifica la CI

Resumen de las notas de Ingeniería del Software 1 (egrpy.org) que usamos para
`tools/check_uml.py`. Las notas citan a Booch et al. (2006), Rumbaugh et al.
(2000) y la especificación UML 2.5.1 de OMG (2017); donde la nota no fija la
notación, la regla sigue esa especificación.

Fuentes:

- [Clase 07 · MOC Modelo Conceptual del UML (Diagramas)](https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingeniería+del+Software+1/Clase+07+Modelo+Conceptual+del+UML+-+Diagramas/Zk+!MOC+Modelo+Conceptual+del+UML+(Diagramas))
  y sus notas de diagramas de casos de uso, clases, secuencia, actividades, estados y paquetes.
- [Clase 09 · MOC Diagrama de Casos de Uso (Fundamentos, Elementos, Relaciones)](https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingeniería+del+Software+1/Clase+09+Diagrama+de+Casos+de+Uso+(Fundamentos%2C+Elementos%2C+Relaciones)/Zk+!MOC+Diagrama+de+Casos+de+Uso+(Fundamentos%2C+Elementos%2C+Relaciones))
  y sus notas: Elementos (Sujeto, Actores, Caso de Uso) y Relaciones (entre
  actores, entre actores y casos de uso, entre casos de uso).

## General

| Regla | Qué dice la cátedra | Código |
|---|---|---|
| Notación UML estricta | Todos los ejemplos usan `skinparam style strictuml` | G1 |

## Diagrama de casos de uso (clase 09)

Elementos: **actor**, **caso de uso** y **sujeto**. Relaciones: asociación,
`<<include>>`, `<<extend>>` y generalización.

| Regla | Qué dice la cátedra | PlantUML | Código |
|---|---|---|---|
| Sujeto | Rectángulo que delimita el alcance y contiene los casos de uso | `rectangle "Sistema" { usecase ... }` | UC1 |
| Actores fuera | El actor es una entidad externa; queda fuera del sujeto | `actor` fuera del `rectangle` | UC2 |
| Asociación actor - CU | Línea simple, sin flecha (la navegabilidad y la multiplicidad son opcionales) | `Actor -- CU` | UC3 |
| `<<include>>` | Obligatorio; del caso base al incluido; dependencia (línea discontinua, flecha abierta) | `Base ..> Incluido : <<include>>` | UC4 |
| `<<extend>>` | Opcional (condicionado); del que extiende al caso base | `Extension ..> Base : <<extend>>` | UC4 |
| Generalización entre CU | El hijo hereda y especializa al padre | `Padre <\|-- Hijo` | UC4 |
| Entre actores | "La única relación admitida entre actores es la generalización" | `Padre <\|-- Hijo` | UC5 |
| Sin elementos sueltos | Todo actor interactúa con el sistema a través de casos de uso | al menos una relación | UC6 |
| Nombre del CU (aviso) | Funcionalidad completa con valor para el actor | verbo en infinitivo | UC7 |
| Jerarquía de actores (aviso) | Evitar jerarquías de más de 3 niveles | | UC8 |

## Diagrama de clases (clase 07)

| Regla | Qué dice la cátedra / UML 2 | Código |
|---|---|---|
| Relaciones válidas | Asociación (`--`, `-->`), agregación (`o--`), composición (`*--`), generalización (`<\|--`), realización (`<\|..`), dependencia (`..>`) | CL1 |
| Multiplicidad | Indica cuántos objetos participan en la asociación ("1", "0..*", "1..*") | CL2 |
| Composición | La parte pertenece a un solo todo: del lado del todo, 1 o 0..1 | CL3 |
| Herencia | Generalización entre elementos del mismo tipo; la realización apunta a una interfaz; sin ciclos | CL4 |

## Diagrama de secuencia (clase 07)

| Regla | Qué dice la cátedra / UML 2 | Código |
|---|---|---|
| Fragmentos combinados | Operadores UML 2 (`alt`, `opt`, `loop`, `par`, `break`, `critical`, `ref`); `group` es de PlantUML | SQ1 |
| Guardas | `alt` con guardas por operando ("libro disponible" / "libro no disponible") | SQ2 |
| Mensajes | Flecha sólida = síncrono, punteada = retorno; sin mensajes bidireccionales | SQ3 |

La consistencia entre clases y secuencias (E1, E2, W1, W2) sigue en
`tools/check_consistencia.py`.

## Diagrama de actividades (clase 07)

| Regla | Qué dice la cátedra / UML 2 | Código |
|---|---|---|
| Nodos inicial y final | `start` / `stop` | AC1 |
| Decisiones con guarda | `if (...) then ([sí]) ... else ([no])` | AC2 |

## Diagrama de estados (clase 07)

| Regla | Qué dice la cátedra / UML 2 | Código |
|---|---|---|
| Estado inicial | Se parte siempre del estado inicial (`[*] -->`); uno por región y su transición sin guarda (para elegir, `<<choice>>`) | ST1 |
| Alcanzabilidad | Ciclo de vida de un objeto: todo estado se alcanza desde el inicial | ST2 |
| Transiciones | `evento [guarda] / acción` | ST3 |

## Diagrama de paquetes (clase 07)

| Regla | Qué dice la cátedra / UML 2 | Código |
|---|---|---|
| Dependencias | Flecha punteada; el origen depende del destino | PK1 |
| Sin ciclos | "Las dependencias circulares entre paquetes son una señal de alerta arquitectónica que debe evitarse" | PK2 |

## Correcciones que salieron de estas reglas

- `CU-03-secuencia`: `group Operación atómica` pasó a `critical` (SQ1).
- `CU-05-estados`: dos transiciones iniciales con guarda pasaron a un `<<choice>>` (ST1).
- `CU-09-estados`: la guarda de la transición inicial pasó a una nota de precondición (ST1).
- Todos los diagramas: `skinparam style strictuml` (G1).
