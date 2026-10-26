#!/usr/bin/env python3
"""Consistencia entre diagramas: clases vs secuencia, por caso de uso.

Para cada CU-XX compara su diagrama de clases (CU-XX-clases*.puml o
CU-XX-modelo-estructural.puml) con sus diagramas de secuencia
(CU-XX-secuencia*.puml).

Reglas
  E1 (error)  Un participante de una secuencia es de un tipo que no existe
              como clase en el diagrama de clases del mismo CU.
              Ej.: participant "x:\\nFactura" sin class Factura.
  E2 (error)  Una secuencia envía un mensaje a un método que la clase
              destino no declara (ni hereda de una superclase del diagrama).
              Ej.: Pres -> Version: publicar() sin + publicar() en la clase.
  W1 (aviso)  Una clase del diagrama de clases no participa en ninguna
              secuencia del CU. Los enum, interfaces y clases con
              estereotipo <<datatype>> no cuentan.
  W2 (aviso)  Un método declarado en una clase que sí participa en las
              secuencias nunca se invoca en ellas.

Solo se analizan mensajes síncronos o asíncronos (->, ->>) con forma de
llamada: nombre(...). Las respuestas (-->), los mensajes a actores y los
textos libres sin paréntesis se ignoran. Un CU sin diagrama de clases o sin
secuencia se omite aquí: eso lo controla check_completitud.

Uso: check_consistencia.py [--strict] [directorio]   (por defecto: diagramas)
Sale con 1 si hay errores (o avisos con --strict).
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

CU_RE = re.compile(r"^(CU-\d{2})-")
CLASS_DECL = re.compile(
    r'^\s*(abstract\s+class|abstract|class|interface|enum|entity|protocol)\s+'
    r'(?:"[^"]*"\s+as\s+)?([A-Za-z_][\w]*)(?:\s+as\s+([A-Za-z_]\w*))?'
    r'(?:\s*<[^>]*>)?\s*(<<[^>]*>>)?.*?(\{)?\s*$'
)
METHOD = re.compile(r"^\s*[+\-#~]?\s*(?:\{[^}]*\}\s*)?/?([A-Za-z_]\w*)\s*\(")
INHERIT = re.compile(r"^\s*([A-Za-z_]\w*)\s*(<\|--|<\|\.\.)\s*([A-Za-z_]\w*)|"
                     r"^\s*([A-Za-z_]\w*)\s*(--\|>|\.\.\|>)\s*([A-Za-z_]\w*)")
EXTENDS = re.compile(r"\b(?:extends|implements)\s+([A-Za-z_][\w, ]*)")
PARTICIPANT = re.compile(
    r'^\s*(participant|actor|boundary|control|entity|database|collections|queue)\s+'
    r'(?:"([^"]*)"|([A-Za-z_]\w*))(?:\s+as\s+([A-Za-z_]\w*))?'
)
MESSAGE = re.compile(
    r'^\s*([A-Za-z_]\w*|\[)\s*(-+>>?|->x|-\\\\|-/)\s*([A-Za-z_]\w*|\])'
    r'\s*(?:\+\+|--|\*\*|!!)?\s*:\s*(.*)$'
)
CALL = re.compile(r"^\s*(?:[A-Za-z_]\w*\s*[:=]\s*)?([A-Za-z_]\w*)\s*\(")


def strip_comments(text):
    text = re.sub(r"/'.*?'/", "", text, flags=re.S)
    return [l for l in text.splitlines() if not l.lstrip().startswith("'")]


def parse_clases(path):
    """Devuelve {clase: {'methods': set, 'kind': str, 'stereo': str}}, {hija: {padres}}."""
    clases, padres = {}, defaultdict(set)
    current, depth = None, 0
    for line in strip_comments(path.read_text(encoding="utf-8")):
        if current:
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                current = None
                continue
            m = METHOD.match(line)
            if m:
                clases[current]["methods"].add(m.group(1))
            continue
        m = CLASS_DECL.match(line)
        if m:
            kind = m.group(1).split()[-1]
            name = m.group(3) or m.group(2)
            clases.setdefault(name, {"methods": set(), "kind": kind,
                                     "stereo": (m.group(4) or "").lower()})
            e = EXTENDS.search(line)
            if e:
                padres[name].update(p.strip() for p in e.group(1).split(","))
            if m.group(5):
                current, depth = name, 1
            continue
        m = INHERIT.match(line)
        if m:
            if m.group(1):
                padres[m.group(3)].add(m.group(1))
            else:
                padres[m.group(4)].add(m.group(6))
    return clases, padres


def tipo_participante(label, name):
    """'obra:\\nObra' -> 'Obra'; ':Obra' -> 'Obra'; 'Obra' -> 'Obra'."""
    text = (label if label is not None else name).replace("\\n", "")
    if ":" in text:
        text = text.split(":", 1)[1]
    text = text.strip()
    return re.sub(r"\W", "", text) or None


def parse_secuencia(path):
    """Devuelve {alias: tipo|None(actor)}, [(linea, origen, destino, metodo)]."""
    parts, msgs = {}, []
    for n, line in enumerate(strip_comments(path.read_text(encoding="utf-8")), 1):
        p = PARTICIPANT.match(line)
        if p:
            kind, label, name, alias = p.groups()
            key = alias or name or label
            parts[key] = None if kind == "actor" else tipo_participante(label, name)
            continue
        m = MESSAGE.match(line)
        if not m or m.group(2).startswith("--"):
            continue
        src, _, dst, text = m.groups()
        c = CALL.match(text)
        if c:
            msgs.append((n, src, dst, c.group(1)))
    return parts, msgs


def metodos_con_herencia(clase, clases, padres, seen=None):
    seen = seen or set()
    if clase in seen or clase not in clases:
        return set()
    seen.add(clase)
    out = set(clases[clase]["methods"])
    for p in padres.get(clase, ()):
        out |= metodos_con_herencia(p, clases, padres, seen)
    return out


def main(argv):
    strict = "--strict" in argv
    args = [a for a in argv if not a.startswith("--")]
    base = Path(args[0] if args else "diagramas")
    por_cu = defaultdict(lambda: {"clases": [], "secuencia": []})
    for f in sorted(base.glob("CU-*.puml")):
        m = CU_RE.match(f.name)
        if not m:
            continue
        resto = f.name[len(m.group(0)):]
        if resto.startswith(("clases", "modelo-estructural")):
            por_cu[m.group(1)]["clases"].append(f)
        elif resto.startswith("secuencia"):
            por_cu[m.group(1)]["secuencia"].append(f)

    errores, avisos = [], []
    for cu, files in sorted(por_cu.items()):
        if not files["clases"] or not files["secuencia"]:
            continue
        clases, padres = {}, defaultdict(set)
        for f in files["clases"]:
            c, p = parse_clases(f)
            clases.update(c)
            for k, v in p.items():
                padres[k] |= v
        usadas, invocados = set(), defaultdict(set)
        for f in files["secuencia"]:
            parts, msgs = parse_secuencia(f)
            for alias, tipo in parts.items():
                if tipo is None:
                    continue
                if tipo not in clases:
                    errores.append(f"E1 {f.name}: participante '{alias}' de tipo "
                                   f"'{tipo}' no existe en el diagrama de clases de {cu}")
                else:
                    usadas.add(tipo)
            for n, src, dst, metodo in msgs:
                tipo = parts.get(dst)
                if tipo is None or tipo not in clases:
                    continue
                invocados[tipo].add(metodo)
                if metodo not in metodos_con_herencia(tipo, clases, padres):
                    errores.append(f"E2 {f.name}:{n}: '{src} -> {dst}: {metodo}()' "
                                   f"pero la clase {tipo} no declara {metodo}()")
        for nombre, info in sorted(clases.items()):
            if info["kind"] in ("enum", "interface") or "datatype" in info["stereo"]:
                continue
            if nombre not in usadas:
                avisos.append(f"W1 {cu}: la clase {nombre} no participa en ninguna secuencia")
                continue
            for metodo in sorted(info["methods"] - invocados[nombre]):
                avisos.append(f"W2 {cu}: {nombre}.{metodo}() no se invoca en ninguna secuencia")

    for e in errores:
        print(f"::error::{e}" if "--gh" in argv else e)
    for w in avisos:
        print(f"::warning::{w}" if "--gh" in argv else w)
    print(f"\nConsistencia: {len(errores)} errores, {len(avisos)} avisos "
          f"en {len(por_cu)} casos de uso.")
    return 1 if errores or (strict and avisos) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
