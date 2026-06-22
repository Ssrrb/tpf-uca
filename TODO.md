# TODO — Diagramas del TPF 2026 · Grupo G11

Total previsto: **24 diagramas**.

Los diagramas deben mantener los mismos nombres de actores, casos de uso, clases,
operaciones y estados. Cada uno debe indicar los RF relacionados para conservar la
trazabilidad `Minuta → RF → CU → Clases → Secuencia → Estados`.

## Modelo de Análisis

- [ ] **01. Diagrama general de casos de uso** — Incluir la frontera del sistema, los cuatro actores, los diez CU y sus relaciones UML.

### CU-01 — Configurar semestre (RF-01)

- [ ] **02. Diagrama de clases de análisis BCE de CU-01** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **03. Diagrama de secuencia de CU-01** — Representar el flujo normal, validaciones de fechas y excepciones.

### CU-02 — Inscribir grupo (RF-02, RF-03)

- [ ] **04. Diagrama de clases de análisis BCE de CU-02** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **05. Diagrama de secuencia de CU-02** — Incluir la validación de que un estudiante no pertenezca a otro grupo del mismo semestre.

### CU-03 — Consultar grupos inscriptos (RF-04)

- [ ] **06. Diagrama de clases de análisis BCE de CU-03** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **07. Diagrama de secuencia de CU-03** — Mostrar la consulta de completitud, cantidad de integrantes, tema y estado.

### CU-04 — Asignar tutor (RF-05)

- [ ] **08. Diagrama de clases de análisis BCE de CU-04** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **09. Diagrama de secuencia de CU-04** — Incluir la validación de autorización y de la fecha de publicación.

### CU-05 — Publicar asignación de tutor (RF-06)

- [ ] **10. Diagrama de clases de análisis BCE de CU-05** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **11. Diagrama de secuencia de CU-05** — Mostrar la publicación, notificación al grupo y actualización correspondiente.

### CU-06 — Cargar versión preliminar del anteproyecto (RF-07)

- [ ] **12. Diagrama de clases de análisis BCE de CU-06** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **13. Diagrama de secuencia de CU-06** — Incluir título, problema, objetivo general, alcance y validaciones.

### CU-07 — Registrar observaciones (RF-08)

- [ ] **14. Diagrama de clases de análisis BCE de CU-07** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **15. Diagrama de secuencia de CU-07** — Mostrar la verificación del tutor asignado y el registro trazable de la observación.

### CU-08 — Entregar anteproyecto (RF-09, RF-10)

- [ ] **16. Diagrama de clases de análisis BCE de CU-08** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **17. Diagrama de secuencia de CU-08** — Incluir control del plazo, posible autorización excepcional, entrega formal y cambio de estado.

### CU-09 — Consultar estado del grupo (RF-11)

- [ ] **18. Diagrama de clases de análisis BCE de CU-09** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **19. Diagrama de secuencia de CU-09** — Mostrar estado, tutor, fechas clave y observaciones, respetando el acceso al grupo propio.

### CU-10 — Generar listado de grupos sin entrega (RF-12)

- [ ] **20. Diagrama de clases de análisis BCE de CU-10** — Incluir boundary, control, entidades y relaciones necesarias.
- [ ] **21. Diagrama de secuencia de CU-10** — Mostrar la verificación de proximidad al plazo y la selección de grupos pendientes.

### Comportamiento del grupo TFG

- [ ] **22. Diagrama de estados del grupo TFG (RF-10)** — Modelar `Pendiente de inscripción → Inscripto → Tutor asignado → En elaboración de anteproyecto → Anteproyecto entregado`, con eventos, guardas y acciones aplicables.

## Modelo de Diseño

- [ ] **23. Diagrama de clases persistentes** — Consolidar las entidades persistentes, atributos, identificadores, asociaciones, multiplicidades y restricciones derivadas del modelo de análisis.
- [ ] **24. Diagrama entidad–relación** — Representar tablas, claves primarias, claves foráneas, cardinalidades y restricciones de integridad de forma coherente con las clases persistentes.

## Verificación final

- [ ] Confirmar que existen exactamente 24 diagramas y que todos son legibles dentro del documento.
- [ ] Verificar que cada CU tenga su especificación textual, diagrama BCE y diagrama de secuencia correspondientes.
- [ ] Comprobar que los mensajes de los diagramas de secuencia correspondan a operaciones de las clases BCE.
- [ ] Comprobar la consistencia de nombres y relaciones entre clases de análisis, clases persistentes y modelo entidad–relación.
- [ ] Verificar la cobertura de RF-01 a RF-12 y RNF-01 a RNF-06 en la matriz RF/RNF vs. CU.
- [ ] Insertar los diagramas en el orden exigido por la plantilla y actualizar el índice del documento.

