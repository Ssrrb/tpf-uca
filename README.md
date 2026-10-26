# Ctrl+ · Modelo de Análisis (TPF 04, Grupo 7)

## Para qué existe este repo

El Modelo de Análisis de Ctrl+ es un conjunto de diagramas UML que describen el
mismo sistema desde distintos ángulos. Los riesgos son:

1. que un diagrama esté mal escrito,
2. que dos diagramas se contradigan (una secuencia llama a un método que la clase no tiene),
3. que falte un diagrama o que no siga las convenciones del grupo,
4. que la imagen del documento no corresponda a la última versión.

Una **herramienta CASE** existe para evitar eso: guarda el modelo, lo valida,
mantiene la consistencia y genera la documentación. Acá la CASE se arma con tres
piezas simples:

- **El modelo es texto.** Cada diagrama es un `.puml` en `diagramas/`. Se puede
  versionar, comparar y revisar como código.
- **PlantUML lo interpreta.** Su CLI valida la sintaxis y dibuja SVG, PNG y XMI.
- **La CI lo controla.** En cada pull request, GitHub Actions corre los controles.
  `main` está protegida: sin CI en verde no hay merge.

## Cómo funciona

```
editar .puml → pull request → CI ─┬─ sintaxis     plantuml -checkonly
                                  ├─ consistencia clases vs secuencia
                                  ├─ calidad      nombres, estilo, completitud, solo .puml
                                  ├─ render       SVG y PNG como artefacto
                                  └─ xmi          exportación opcional (en main)
                                 ↓ todo en verde
                               merge a main
```

| Función CASE | Control | Dónde |
|---|---|---|
| Validar el modelo | Sintaxis de cada `.puml` | `tools/check_sintaxis.sh` |
| Consistencia | Clases vs secuencia (E1, E2, W1, W2) | `tools/check_consistencia.py` |
| Reglas de modelado y estándar visual | Nombres, `!theme plain` y paleta, completitud | `tools/check_calidad.sh` |
| Documentación | SVG y PNG desde el texto | job `render` |
| Intercambio de modelos | XMI para ArgoUML y StarUML | job `xmi (opcional)` |
| Revisión | PR obligatorio con CI en verde | protección de `main` |

## Reglas

- **Nombres:** `CU-XX-<tipo>[-n-<detalle>].puml`, por ejemplo `CU-02-secuencia-1-carga.puml`.
- **Estilo:** `!theme plain`, fondo `#F5F8FA`, borde `#17324D`; las clases además usan `#EAF2F6`.
- **Completitud:** cada CU (menos CU-00) tiene al menos un diagrama de clases y uno de secuencia.
- **Solo `.puml`** en `diagramas/`: las imágenes se generan, no se suben.
- **Consistencia**, dentro de cada CU:
  - **E1** (error): un participante de la secuencia es de una clase que no existe.
  - **E2** (error): un mensaje llama a un método que la clase no declara.
  - **W1** (aviso): una clase no participa en ninguna secuencia.
  - **W2** (aviso): un método nunca se invoca.

## Uso local

Requisitos: Java 17+, Graphviz y `plantuml` en el `PATH`.

```bash
bash tools/check_sintaxis.sh
python3 tools/check_consistencia.py
bash tools/check_calidad.sh
plantuml -tsvg -o "$PWD/salida" diagramas/*.puml
```

Por qué PlantUML y no otra herramienta: [docs/herramienta-case.md](docs/herramienta-case.md).
