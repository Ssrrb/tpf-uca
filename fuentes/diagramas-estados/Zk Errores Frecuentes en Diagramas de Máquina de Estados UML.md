---
Title: Zk Errores Frecuentes en Diagramas de Máquina de Estados UML
TipoNota: permanente
Fecha: 2026-05-26
Área:
  - ingenieríaDelSoftware
SubÁrea:
  - uml
Status: ok
tags:
  - digitalGarden
  - uml
  - didactica
  - diagramaDeEstados
dg-publish: true
publish: true
aliases:
  - Errores Frecuentes en Diagramas de Estados
  - Antipatrones en Máquinas de Estado
  - Problemas Típicos de Modelado de Estados
---
## Errores Frecuentes en Diagramas de Máquina de Estados UML

Los errores más comunes al construir diagramas de máquina de estados provienen de confundir estados, eventos, condiciones y acciones. Esta confusión produce modelos visualmente aceptables, pero semánticamente débiles: el diagrama parece seguir la notación, pero no representa con claridad el comportamiento del sistema ([[Zk Ref boochLenguajeUnificadoModelado2006|Booch et al., 2006]]; [[Zk Ref omgUnifiedModelingLanguage2017|OMG, 2017]]).

### Errores Típicos

- **Nombrar acciones como estados**: usar `ValidarPago` como estado cuando debería ser una acción o actividad.
- **Nombrar condiciones como eventos**: usar `StockDisponible` como evento cuando debería ser una guarda.
- **Mezclar evento y guarda**: escribir `Inventario suficiente / insuficiente` en una transición, sin separar ocurrencia y condición.
- **Crear estados irrelevantes**: agregar estados que no modifican el comportamiento futuro.
- **Omitir transiciones de error**: modelar sólo el camino feliz y dejar fuera cancelaciones, rechazos o vencimientos.
- **Duplicar niveles de abstracción**: mezclar estados de negocio con pasos técnicos de interfaz sin explicar la frontera del modelo.
- **Usar concurrencia sin independencia real**: crear regiones ortogonales cuando sólo existe una secuencia alternativa.

### Regla

Una pregunta útil para detectar errores es: “si la entidad recibe el mismo evento en dos situaciones distintas, ¿responde de manera diferente?”. Si la respuesta es no, quizá esas situaciones no deban ser estados separados. La pregunta ayuda a vincular el estado con su función conductual y no sólo con una etiqueta nominal.

### Enlaces Sugeridos

- [[Zk Estado en UML|Estado]]
- [[Zk Evento en Máquina de Estados UML|Evento]]
- [[Zk Guardia en Máquina de Estados UML|Guardia]]
- [[Zk Criterios de Calidad de un Diagrama de Máquina de Estados UML|Criterios de Calidad]]
