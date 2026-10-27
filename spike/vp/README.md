# Spike de importación en Visual Paradigm

Dos XMI mínimos con el mismo contenido (clases `Obra` y `Cliente`, una
asociación dirigida `Obra "0..*" --> "1" Cliente : contratada por`):

- `minimo-uml251.xmi`: XMI 2.5.1 / UML 2.5.1 (namespaces `20131001` y `20161101`).
- `minimo-xmi21.xmi`: XMI 2.1 / UML 2.1 (namespaces `schema.omg.org`).

Resultado (27-10-2026, VP 18.1, File > Import > XMI): los dos archivos se importaron y aparecieron las dos clases. VP acepta XMI 2.5.1, así que no hace falta generar `model-vp.xmi` en 2.1.
