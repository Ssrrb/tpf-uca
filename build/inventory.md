# Inventario de diagramas PlantUML

Generado por `tools/inventario.py` sobre `diagramas/`. 56 archivos `.puml`.

## CI existente

- GitHub Actions: `.github/workflows/case.yml`
- GitLab CI: no hay
- PlantUML fijado en la CI: `1.2025.4` (descargado de GitHub Releases y verificado por SHA-256 en `.github/actions/plantuml`)
- PlantUML en esta ejecución: `PlantUML version 1.2025.4 (Sat Jun 28 11:09:25 UTC 2025)`

## Totales por tipo

| Tipo | Archivos |
|---|---|
| actividad | 9 |
| casos de uso | 2 |
| clase | 17 |
| estados | 9 |
| paquetes | 1 |
| secuencia | 18 |
| componentes | 0 |
| despliegue | 0 |

## Discrepancias nombre / contenido

Ninguna: el sufijo del nombre coincide con el contenido.

## Detalle

Los conteos son por línea y orientativos (expresiones regulares); el conteo exacto sale de `build/model.json`.

| Archivo | Tipo | Líneas | Elementos |
|---|---|---|---|
| `diagramas/CU-00-casos-de-uso-alto-nivel.puml` | casos de uso | 92 | actores: 3, casos de uso: 16, sujetos: 1, paquetes: 3, asociaciones: 19 |
| `diagramas/CU-00-clases.puml` | clase | 146 | clases: 28, paquetes: 3, relaciones: 38, notas: 1 |
| `diagramas/CU-00-generalizacion-actores.puml` | casos de uso | 55 | actores: 4, generalizaciones: 3, notas: 2 |
| `diagramas/CU-00-paquetes.puml` | paquetes | 115 | paquetes: 20, dependencias: 17, notas: 2 |
| `diagramas/CU-01-actividades.puml` | actividad | 69 | acciones: 10, particiones: 5, decisiones: 5, nodos finales: 1 |
| `diagramas/CU-01-clases.puml` | clase | 128 | clases: 8, enumeraciones: 2, paquetes: 1, relaciones: 8, notas: 1 |
| `diagramas/CU-01-estados.puml` | estados | 59 | estados: 4, transiciones: 5, notas: 1 |
| `diagramas/CU-01-secuencia.puml` | secuencia | 87 | actores: 1, lifelines: 9, mensajes: 26, creaciones: 4, fragmentos: 7, box: 1, notas: 1 |
| `diagramas/CU-02-actividades.puml` | actividad | 63 | acciones: 9, particiones: 5, decisiones: 3, nodos finales: 2 |
| `diagramas/CU-02-clases.puml` | clase | 109 | clases: 7, enumeraciones: 1, paquetes: 1, relaciones: 7, notas: 1 |
| `diagramas/CU-02-secuencia.puml` | secuencia | 79 | actores: 1, lifelines: 6, mensajes: 21, creaciones: 2, fragmentos: 9, ref (InteractionUse): 1, box: 1 |
| `diagramas/CU-03-clases.puml` | clase | 133 | clases: 9, paquetes: 2, relaciones: 9, notas: 2 |
| `diagramas/CU-03-estados.puml` | estados | 54 | estados: 4, transiciones: 8, notas: 1 |
| `diagramas/CU-03-secuencia.puml` | secuencia | 110 | actores: 1, lifelines: 11, mensajes: 36, creaciones: 3, fragmentos: 10, box: 2, notas: 1 |
| `diagramas/CU-04-actividades.puml` | actividad | 72 | acciones: 11, particiones: 8, decisiones: 4, nodos finales: 2, notas: 1 |
| `diagramas/CU-04-clases.puml` | clase | 162 | clases: 12, enumeraciones: 1, paquetes: 2, relaciones: 14, notas: 1 |
| `diagramas/CU-04-estados.puml` | estados | 63 | estados: 7, pseudoestados choice: 1, transiciones: 13, notas: 1 |
| `diagramas/CU-04-secuencia.puml` | secuencia | 109 | actores: 1, lifelines: 11, mensajes: 38, creaciones: 5, fragmentos: 9, box: 2, notas: 1 |
| `diagramas/CU-05-clases.puml` | clase | 117 | clases: 11, clases abstractas: 2, enumeraciones: 1, paquetes: 1, relaciones: 11, notas: 1 |
| `diagramas/CU-05-estados.puml` | estados | 52 | estados: 4, pseudoestados choice: 1, transiciones: 6, notas: 1 |
| `diagramas/CU-05-secuencia.puml` | secuencia | 67 | actores: 1, lifelines: 6, mensajes: 18, creaciones: 3, fragmentos: 3, box: 1, notas: 1 |
| `diagramas/CU-06-actividades.puml` | actividad | 67 | acciones: 9, particiones: 6, decisiones: 2, nodos finales: 3, notas: 1 |
| `diagramas/CU-06-clases.puml` | clase | 149 | clases: 12, paquetes: 3, relaciones: 14, notas: 1 |
| `diagramas/CU-06-secuencia-1-calculo.puml` | secuencia | 76 | actores: 1, lifelines: 8, mensajes: 18, fragmentos: 6, ref (InteractionUse): 1, box: 3, notas: 1 |
| `diagramas/CU-06-secuencia-2-consumo.puml` | secuencia | 63 | actores: 1, lifelines: 7, mensajes: 14, fragmentos: 5, box: 3 |
| `diagramas/CU-07-actividades.puml` | actividad | 71 | acciones: 12, particiones: 6, decisiones: 5, nodos finales: 2 |
| `diagramas/CU-07-clases.puml` | clase | 124 | clases: 10, enumeraciones: 1, paquetes: 3, relaciones: 9, notas: 1 |
| `diagramas/CU-07-secuencia.puml` | secuencia | 87 | actores: 1, lifelines: 9, mensajes: 26, creaciones: 3, fragmentos: 8, box: 3 |
| `diagramas/CU-08-clases.puml` | clase | 116 | clases: 10, clases abstractas: 1, paquetes: 3, relaciones: 9, notas: 1 |
| `diagramas/CU-08-estados.puml` | estados | 59 | estados: 7, pseudoestados choice: 2, transiciones: 10, notas: 1 |
| `diagramas/CU-08-secuencia.puml` | secuencia | 83 | actores: 1, lifelines: 8, mensajes: 22, creaciones: 3, fragmentos: 6, box: 3, notas: 1 |
| `diagramas/CU-09-actividades.puml` | actividad | 64 | acciones: 10, particiones: 6, decisiones: 4, nodos finales: 1 |
| `diagramas/CU-09-clases.puml` | clase | 102 | clases: 7, paquetes: 2, relaciones: 6, notas: 1 |
| `diagramas/CU-09-secuencia.puml` | secuencia | 77 | actores: 1, lifelines: 8, mensajes: 21, creaciones: 3, fragmentos: 6, box: 2, notas: 1 |
| `diagramas/CU-10-actividades.puml` | actividad | 66 | acciones: 9, particiones: 7, decisiones: 2, nodos finales: 2 |
| `diagramas/CU-10-clases.puml` | clase | 125 | clases: 10, paquetes: 3, relaciones: 11, notas: 1 |
| `diagramas/CU-10-secuencia.puml` | secuencia | 95 | actores: 1, lifelines: 11, mensajes: 24, creaciones: 1, fragmentos: 9, box: 3, notas: 2 |
| `diagramas/CU-11-actividades.puml` | actividad | 77 | acciones: 12, particiones: 6, decisiones: 5, nodos finales: 3 |
| `diagramas/CU-11-clases.puml` | clase | 116 | clases: 7, enumeraciones: 1, paquetes: 2, relaciones: 6, notas: 1 |
| `diagramas/CU-11-secuencia.puml` | secuencia | 94 | actores: 1, lifelines: 8, mensajes: 29, creaciones: 2, fragmentos: 6, box: 2, notas: 2 |
| `diagramas/CU-12-clases.puml` | clase | 104 | clases: 6, paquetes: 3, relaciones: 7, notas: 1 |
| `diagramas/CU-12-estados.puml` | estados | 55 | estados: 5, pseudoestados choice: 1, transiciones: 8, notas: 1 |
| `diagramas/CU-12-secuencia.puml` | secuencia | 86 | actores: 1, lifelines: 7, mensajes: 24, creaciones: 1, fragmentos: 9, box: 3, notas: 1 |
| `diagramas/CU-13-actividades.puml` | actividad | 71 | acciones: 11, particiones: 8, decisiones: 3, fork: 1, nodos finales: 1 |
| `diagramas/CU-13-clases.puml` | clase | 98 | clases: 6, paquetes: 3, relaciones: 6, notas: 1 |
| `diagramas/CU-13-secuencia.puml` | secuencia | 69 | actores: 1, lifelines: 7, mensajes: 20, creaciones: 1, fragmentos: 5, box: 3 |
| `diagramas/CU-14-clases.puml` | clase | 100 | clases: 10, clases abstractas: 2, paquetes: 2, relaciones: 9, notas: 1 |
| `diagramas/CU-14-estados.puml` | estados | 53 | estados: 4, pseudoestados choice: 1, transiciones: 6, notas: 1 |
| `diagramas/CU-14-secuencia.puml` | secuencia | 70 | actores: 1, lifelines: 6, mensajes: 19, creaciones: 3, fragmentos: 4, box: 2, notas: 1 |
| `diagramas/CU-15-clases.puml` | clase | 92 | clases: 5, paquetes: 1, relaciones: 6, notas: 1 |
| `diagramas/CU-15-estados.puml` | estados | 52 | estados: 4, transiciones: 7, notas: 1 |
| `diagramas/CU-15-secuencia.puml` | secuencia | 76 | actores: 1, lifelines: 6, mensajes: 24, creaciones: 2, fragmentos: 7, box: 1 |
| `diagramas/CU-16-clases.puml` | clase | 110 | clases: 7, enumeraciones: 1, paquetes: 1, relaciones: 6, notas: 1 |
| `diagramas/CU-16-estados.puml` | estados | 61 | estados: 4, pseudoestados choice: 1, transiciones: 9, notas: 2 |
| `diagramas/CU-16-secuencia-1-validacion.puml` | secuencia | 50 | actores: 1, lifelines: 5, mensajes: 7, creaciones: 1, fragmentos: 4, ref (InteractionUse): 1, box: 1 |
| `diagramas/CU-16-secuencia-2-finalizacion.puml` | secuencia | 60 | actores: 1, lifelines: 6, mensajes: 12, fragmentos: 6, ref (InteractionUse): 1, box: 1 |
