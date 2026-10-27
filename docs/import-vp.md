# Llevar el modelo a Visual Paradigm

Pasos para pasar de los `.puml` a un proyecto de Visual Paradigm 18.1 con los diagramas
de actividades, clases y secuencia de cada CU. Por qué VP: [herramienta-case.md](herramienta-case.md).

## 1. Generar el XMI y los datos del plugin

```bash
python3 tools/modelo.py diagramas --xmi   # build/model.xmi (XMI 2.5.1 / UML 2.5.1)
python3 tools/uml/vp_datos.py             # build/vp-diagramas.json
```

La CI también publica `model.xmi` como artefacto del job `xmi`.

## 2. Compilar el plugin

Necesita un JDK 11 o posterior y el `openapi.jar` que trae VP
(en macOS: `Visual Paradigm.app/Contents/Resources/app/lib/openapi.jar`).

```bash
bash tools/uml/vp/construir.sh /ruta/a/openapi.jar   # build/tpfuca-vp-plugin.zip
```

El zip lleva el plugin compilado y una copia de `vp-diagramas.json`. Si cambian los
`.puml`, hay que repetir los pasos 1 y 2 y reinstalar.

## 3. Instalar el plugin en VP

`Help > Install Plugin`, elegir el zip y reiniciar VP. Las acciones aparecen en
**Project > Import**: *Dibujar CU...* e *Inspeccionar diagrama abierto*.

## 4. Importar el modelo y dibujar

1. Trabajar sobre una **copia** del `.vpp`, nunca sobre el original.
2. Importar `build/model.xmi` desde **Project > Import > XMI** (en el menú clásico, File > Import > XMI). VP crea el modelo
   (paquetes, clases, interacciones y actividades) pero no los diagramas.
3. **Project > Import > Dibujar CU...** y escribir un CU (`CU-01`) o `todos`.
   El plugin crea, por cada CU, el diagrama de clases, los de secuencia y los de
   actividades, y deja un informe en `tpfuca-ultimo-dibujo.txt` junto al proyecto.

Los diagramas de paquetes y de estados no se dibujan en VP: siguen en `.puml`.

## Qué hace el plugin

| Diagrama | Cómo lo dibuja |
|---|---|
| Clases | Reutiliza las clases del XMI, ajusta su tamaño al contenido y usa el layout automático de VP. |
| Secuencia | Lifelines en columnas, activaciones por intervalos, numeración anidada (la respuesta es el último hijo de su llamada), fragmentos con un operando por guarda y notas sobre su lifeline. |
| Actividades | Carriles por partición, nodos por rango (camino más largo), ramas de cada decisión por los costados, espacio libre bajo el rombo para la pregunta y guardas `[sí]` / `[no]` junto al rombo. |

## Problemas conocidos

- **Marca de agua:** sale de la licencia de evaluación de VP; el plugin no la puede quitar.
- **Actividades:** el acomodo es propio del plugin y puede necesitar retoques a mano en
  diagramas con muchas decisiones anidadas.
- *Inspeccionar diagrama abierto* vuelca la estructura del diagrama a
  `tpfuca-inspeccion.txt` para diagnosticar diferencias con lo esperado.
