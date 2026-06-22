---
Title: Zk Pseudoelementos de Máquina de Estados UML
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
  - Pseudoelementos UML
  - Pseudostates de Máquina de Estados
  - Nodos Especiales en Máquinas de Estado
---
## Pseudoelementos de Máquina de Estados UML

Los pseudoelementos de una máquina de estados UML no representan estados sustantivos del dominio, sino nodos especiales que organizan la entrada, salida, selección, unión, sincronización o memoria del comportamiento. Su uso permite modelar estructuras que serían ambiguas si se expresaran sólo mediante estados y transiciones ordinarias ([[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Pseudoelementos Frecuentes

- **Inicial**: punto de entrada por defecto de una región.
- **Final**: culminación de una región o máquina.
- **Choice**: decisión dinámica evaluada en tiempo de ejecución.
- **Junction**: unión o encadenamiento de transiciones.
- **Fork**: división de flujo hacia regiones concurrentes.
- **Join**: sincronización de flujos concurrentes.
- **History**: recuperación de un subestado previamente activo.
- **Terminate**: terminación abrupta de la ejecución de la máquina.

Estos elementos amplían la expresividad del diagrama y permiten representar decisiones, sincronizaciones o memoria de subestados sin convertir cada elemento gráfico en un estado de dominio. La distinción es importante para evitar modelos visualmente cargados pero conceptualmente confusos.

<!-- Para uso docente: en cursos introductorios conviene presentar primero inicial, final y choice; luego incorporar fork, join e historia cuando ya se comprendan estados compuestos y regiones ortogonales. -->

### Enlaces Sugeridos

- [[Zk Estado Inicial y Estado Final en UML|Estado Inicial y Estado Final]]
- [[Zk Estado Compuesto en UML|Estado Compuesto]]
- [[Zk Región Ortogonal en Máquina de Estados UML|Región Ortogonal]]
