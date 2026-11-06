# Sistema para construir los casos de uso de Ctrl+

El Modelo de Análisis se construye **un caso de uso por vez**. Ningún CU pasa a
diagramas hasta que su descripción está aprobada, y el documento Word se arma
recién al final, a partir de estos archivos, sin escribir nada a mano en él.

## 1. Por qué fallaba la v12

1. **Las descripciones mezclaban dos alcances.** Cada CU traía el flujo
   completo (fase 2) y encima una nota «En el MVP» que lo contradecía. Ejemplo:
   el flujo de CU-02 pide unidad, categoría y precio, y la nota dice que en el
   MVP no hay nada de eso. Los diagramas se hicieron sobre el flujo, no sobre
   la nota.
2. **Había tres numeraciones a la vez.** El documento v12 usa la numeración
   nueva, pero los `.puml` del repo siguen con la de la v11 (por ejemplo,
   `CU-16-secuencia-1-validacion.puml` es el CU-04 de hoy).
3. **Los términos variaban.** «Responsables», «miembros», «membresía» y
   «asignación» se usaban para lo mismo; la secuencia de CU-01 cita un RF-32
   que no existe en la lista.

## 2. Reglas fijas

- **Fuente de verdad:** `modelo/glosario.md` para los nombres y
  `modelo/cu/CU-XX-*.md` para cada descripción. Si algo no está ahí, no existe.
- **Numeración congelada** (tabla de abajo). Un CU nunca cambia de número.
- **Solo el alcance del MVP.** Lo de fase 2 no aparece en ningún CU, ni como
  nota. Si hace falta recordarlo, va a `modelo/fuera-de-alcance.md`.
- **Plantilla del profesor sin agregados.** Los campos de la descripción son
  exactamente los de la tabla de la plantilla: Nombre, Versión, Creado por,
  Modificado por, Descripción, Actores, Pre condiciones, Post condiciones,
  Flujo normal, Flujo alternativo, Excepciones, Requerimientos. El subsistema
  no es un campo: se ve como paquete en el diagrama de clases.
- **Actores:** solo Administrador e Ingeniero de obra (y Usuario, abstracto).
  Un actor nunca es un subsistema ni una clase de diseño.
- **Ids de requerimientos** tal como están en la lista: `RF-01`, `NF-01`, `PR-01`.
- **Alcance:** el sistema está hecho para una sola empresa (organización)
  (PR-02). Requerimiento agregado PR-09: «La autenticación de los usuarios se
  delega en un servicio externo». Por eso no hay CU de inicio de sesión.

## 3. Orden de trabajo

Los CU se trabajan por bloques. Dentro de un bloque, un CU usa lo que dejaron
los anteriores, así que el glosario del bloque queda cerrado al terminarlo.

| Bloque | CU | Nombre | Depende de |
|---|---|---|---|
| A. Obra y catálogos | CU-01 | Gestionar obra | CU-02 (cliente) |
| | CU-02 | Mantener catálogos | — |
| B. Presupuesto y estructura de trabajo | CU-03 | Cargar el presupuesto del cliente | CU-01 |
| | CU-04 | Validar y finalizar el presupuesto del cliente | CU-03 |
| | CU-05 | Armar y versionar el presupuesto de costos | CU-04 |
| C. Avance, certificado y subcontratos | CU-06 | Registrar contrato de subcontratista | CU-02, CU-05 |
| | CU-07 | Medir el avance del certificado | CU-05, CU-06 |
| | CU-08 | Calcular el certificado | CU-07 |
| | CU-09 | Liquidar subcontratista | CU-06, CU-08 |
| D. Documentos y modelos | CU-10 | Gestionar la documentación de la obra | CU-01 |
| | CU-11 | Importar la carpeta existente de la obra | CU-10 |
| | CU-12 | Publicar y revisar una versión de modelo | CU-10 |
| | CU-13 | Calcular el cómputo del modelo | CU-12 |
| | CU-14 | Vincular la estructura de trabajo con el modelo y los documentos | CU-05, CU-10, CU-12 |
| E. Incidencias y seguimiento | CU-15 | Abrir, asignar y cerrar una incidencia | CU-01 |
| | CU-16 | Consultar el tablero y la actividad de la obra | todos |

## 4. El ciclo de cada CU

| Paso | Qué se hace | Artefacto | Quién aprueba |
|---|---|---|---|
| 1. Descripción | Se escribe la tabla de la plantilla, solo MVP | `modelo/cu/CU-XX-*.md` | Agustín |
| 2. Glosario | Cada clase, estado y término nuevo entra al glosario | `modelo/glosario.md` | junto con 1 |
| 3. Clases | Solo las clases que nombra la descripción | `diagramas/CU-XX-clases.puml` | — |
| 4. Secuencia | Un mensaje por cada paso «Sistema»; solo métodos del diagrama de clases | `diagramas/CU-XX-secuencia.puml` | — |
| 5. Otros | Estados o actividades, solo si agregan algo | `diagramas/CU-XX-estados.puml` | — |
| 6. Controles | `plantuml -checkonly`, `check_consistencia.py`, `check_uml.py` | PNG | Agustín revisa 3 a 5 juntos |
| 7. Cierre | El CU queda «cerrado»; cambiarlo después obliga a reabrirlo | estado en la tabla del §6 | — |

## 5. Checklist de cada CU

**Descripción**

- [ ] Cada sustantivo que será clase está en el glosario con ese nombre exacto.
- [ ] No hay nada de fase 2 ni notas «En el MVP».
- [ ] El flujo normal tiene como mucho 10 pasos, uno por acción, y el actor de
      cada paso es un actor del CU o «Sistema».
- [ ] Cada paso «Sistema» dice una sola responsabilidad (será un método).
- [ ] Los flujos alternativos y las excepciones se numeran por el paso donde
      ocurren (`3a`, `3a1`, `3a2`; `*a` en cualquier momento), sin repetir letra
      entre alternativos y excepciones del mismo paso, y cada uno dice cómo
      termina o a qué paso vuelve.
- [ ] Otro CU se cita con número y nombre, como en la tabla del §3.
- [ ] Requerimientos: solo los que el CU cumple de verdad.

**Diagramas**

- [ ] Clases: paquetes = subsistemas (ERP, ECMS, Motor de finanzas);
      multiplicidad en cada asociación; nombres del glosario.
- [ ] Secuencia: el actor manda el primer mensaje; cada mensaje es un método de
      una clase del diagrama de clases del mismo CU; fragmentos `alt`, `opt`,
      `loop`, `break` con guarda.
- [ ] Estados: los del glosario, con `[*]` inicial y transiciones
      `evento [guarda] / acción`.
- [ ] Estilo celeste de CU-01/02, `skinparam style strictuml`, `title CU-XX · Nombre`.

## 6. Estado de avance

| CU | Descripción | Diagramas | Estado |
|---|---|---|---|
| CU-01 | borrador v2 | — | en revisión |
| CU-02 a CU-16 | — | — | pendiente |

Los `.puml` que hoy están en `diagramas/` son de la v11 (numeración vieja). Se
reemplazan uno a uno a medida que cada CU se cierra; los que todavía no se
rehicieron no se usan.
