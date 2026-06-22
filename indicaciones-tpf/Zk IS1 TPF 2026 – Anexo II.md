---
Title: Zk IS1 TPF 2026 – Anexo II
TipoNota: permanente
Área:
  - definir
SubÁrea:
  - definir
tags:
  - definir
dg-publish: true
publish: true
aliases:
  - Anexo II – Lineamientos del Microestudio
---
## IS1 TPF 2026 - Anexo II – Lineamientos del Microestudio

### Propósito

El microestudio tiene como propósito introducir a los estudiantes en una práctica inicial de investigación formativa vinculada a un problema auténtico del dominio analizado. Su foco será la claridad percibida del proceso TFG por parte de estudiantes que actualmente transitan dicho proceso.

### Diseño del Microestudio

El microestudio se estructura como un ejercicio de investigación formativa de tipo descriptivo, orientado a explorar la claridad percibida del proceso institucional del TFG en su etapa inicial (desde la reunión de lanzamiento hasta la entrega del anteproyecto), por parte de estudiantes que actualmente se encuentran cursando dicho proceso.

La **pregunta de investigación** que guía el microestudio es:

> **¿Qué nivel de claridad perciben los estudiantes de TFG respecto a etapas, roles y plazos del proceso institucional del TFG, en su fase inicial, luego de la reunión de lanzamiento del semestre?**

Para abordarla, se utilizará un cuestionario breve con ítems en escala tipo [[Zk Tipo Likert|Likert]] (por ejemplo, de 1 a 5), centrados en tres dimensiones principales:

- claridad de las etapas del proceso (qué hacer y en qué orden);
- claridad de los roles (qué corresponde a la Comisión, al Tutor y al Estudiante);
- claridad de los plazos y fechas clave (inscripción de grupo, publicación de tutores, entrega del anteproyecto).

La población de interés está constituida por estudiantes que se encuentran actualmente en proceso de TFG en la carrera. La recolección de datos será realizada por la cátedra mediante un único formulario en línea y consolidada en una base maestra anonimizada. A partir de esa base, la cátedra asignará a cada grupo de IS1 un subconjunto aleatorio de respuestas para su análisis descriptivo.

### Instrumento del Microestudio (Formulario)

El instrumento será elaborado y administrado por la cátedra. El formulario será distribuido directamente a los estudiantes de TFG por los canales institucionales que el docente considere pertinentes. Los estudiantes de IS1 no participarán en la aplicación del cuestionario ni en el acceso a datos personales de los encuestados; trabajarán exclusivamente con subconjuntos de datos ya recopilados y anonimizados que les serán provistos por la cátedra.

**Datos de contexto**

- Código de grupo de TFG (por ejemplo, G0720, G0750, etc.).  
- Semestre/cohorte de inicio del TFG (por ejemplo, 2026 S1).

**Ítems de claridad percibida**  
Escala: 1 a 5, donde 1 = “Nada claro” y 5 = “Totalmente claro”.

- P1. “Luego de la reunión inicial y de las indicaciones recibidas, ¿qué tan claras le resultan las **etapas** del proceso de TFG hasta la entrega del anteproyecto?”  
- P2. “¿Qué tan claros le resultan los **roles** de cada actor (Comisión de TFG, Tutor, Estudiante) en esta primera etapa del TFG?”  
- P3. “¿Qué tan claros le resultan los **plazos y fechas clave** (inscripción de grupo, publicación de tutor, entrega del anteproyecto)?”  
- P4. “En general, ¿qué tan claro le resulta el **flujo completo** del proceso de TFG hasta la entrega del anteproyecto?”

**Pregunta abierta (opcional)**

- P5. “Mencione brevemente algún aspecto del proceso de TFG (etapas, roles o fechas) que le haya resultado especialmente confuso o que considere que podría comunicarse mejor.”

### Trabajo Esperado por Parte del Grupo

Cada grupo de Ingeniería del Software 1 recibirá, por parte de la cátedra, un subconjunto aleatorio de respuestas del formulario (en formato hoja de cálculo o archivo equivalente). A partir de ese subconjunto, deberá realizar como mínimo las siguientes tareas:

1. **Preparación de datos**  
   - Verificar el número de casos incluidos en el subconjunto asignado.  
   - Revisar que todas las respuestas de P1 a P4 estén en el rango 1–5 y registrar si existen valores faltantes.

2. **Análisis descriptivo básico**  
   Para cada ítem P1, P2, P3 y P4:

   - Calcular el **promedio** (media aritmética) de las respuestas en el subconjunto asignado.  
   - Identificar el **valor mínimo y máximo** observado en cada ítem.  
   - (Opcional) Presentar una tabla de frecuencias simples (cuántas respuestas 1, 2, 3, 4 y 5) si el tamaño del subconjunto lo justifica.

   El informe debe incluir al menos una tabla que sintetice estos resultados, por ejemplo:

| Ítem | Media | Mínimo | Máximo |
| ---- | ----- | ------ | ------ |
| P1   | ...   | ...    | ...    |
| P2   | ...   | ...    | ...    |
| P3   | ...   | ...    | ...    |
| P4   | ...   | ...    | ...    |

3. **Análisis cualitativo mínimo**  
   - Leer todas las respuestas de la pregunta abierta P5 del subconjunto asignado.  
   - Identificar al menos **uno o dos temas recurrentes** (por ejemplo, confusión sobre plazos, sobre rol del tutor, sobre inscripción de grupos) y describirlos brevemente.

4. **Respuesta a la pregunta de investigación**  
   Con base en los resultados descriptivos cuantitativos (medias, mínimos y máximos) y en las observaciones cualitativas (P5), cada grupo deberá formular una **respuesta breve y explícita** a la pregunta de investigación:

   > “A partir de los datos analizados en nuestro subconjunto, ¿qué nivel de claridad perciben los estudiantes de TFG respecto a etapas, roles y plazos del proceso institucional del TFG en su fase inicial?”

   Esta respuesta debe:
   - mencionar explícitamente cuáles dimensiones aparecen más claras (medias más altas) y cuáles muestran mayores dudas (medias más bajas o comentarios críticos);  
   - citar al menos uno o dos ejemplos de comentarios abiertos que ilustren las áreas de mayor confusión.

5. **Vinculación con el análisis del sistema**  
   Cada grupo deberá vincular **al menos dos observaciones** derivadas del microestudio con decisiones de análisis o modelado del sistema (por ejemplo, definición de un caso de uso, inclusión de una vista específica de cronograma, adición de un atributo o mensaje en un diagrama de interacción). Esta vinculación debe explicitar:

   - la observación empírica (por ejemplo, “la claridad sobre plazos tiene la media más baja y aparecen comentarios sobre fechas confusas”);  
   - la decisión de diseño adoptada (por ejemplo, “se agrega un caso de uso ‘Consultar cronograma detallado’ y una interfaz donde las fechas se muestran en línea de tiempo”);  
   - la relación entre ambas (cómo la evidencia motiva la decisión de diseño).

### Advertencia Metodológica

En la sección correspondiente del informe, cada grupo deberá incluir una aclaración expresa indicando que el microestudio realizado es de carácter formativo y exploratorio, y que los datos analizados corresponden únicamente a un subconjunto de casos asignado por la cátedra. Esta aclaración es obligatoria y forma parte del encuadre metodológico del trabajo.

En particular, deberá señalarse que:

- el microestudio tiene carácter formativo;
- la muestra utilizada por cada grupo es limitada y no necesariamente representativa de toda la población de estudiantes de TFG;
- los resultados se presentan con fines descriptivos y pedagógicos;
- cualquier generalización robusta requeriría un diseño muestral más riguroso, mayor tamaño de muestra y procedimientos analíticos adicionales.

La intención central no es obtener conclusiones estadísticas definitivas, sino ejercitar el uso responsable de datos empíricos como insumo para el análisis y diseño de sistemas.


