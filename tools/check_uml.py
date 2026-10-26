#!/usr/bin/env python3
"""Notación UML 2 que evalúa la cátedra (Ingeniería del Software 1, clases 07 y 09).

Revisa cada .puml según su tipo, tomado del nombre del archivo. Las reglas y
sus fuentes están en docs/catedra/reglas-uml.md.

General (todos)
  G1  skinparam style strictuml (dibuja las flechas como en UML 2, igual que
      los ejemplos de la cátedra).

Casos de uso (casos-de-uso*, generalizacion-actores)
  UC1 Un solo sujeto (rectangle con nombre) contiene todos los casos de uso.
  UC2 Los actores quedan fuera del sujeto.
  UC3 Actor - caso de uso: asociación, línea continua sin flecha (--).
  UC4 Caso de uso - caso de uso: <<include>> o <<extend>> con línea
      discontinua y flecha abierta (..>), o generalización (<|--).
  UC5 Actor - actor: solo generalización (<|--), sin ciclos.
  UC6 Todo actor y todo caso de uso participa en alguna relación.
  UC7 (aviso) El nombre del caso de uso empieza con un verbo en infinitivo.
  UC8 (aviso) Jerarquía de actores de más de 3 niveles.

Clases (clases*, modelo-estructural)
  CL1 Solo relaciones UML 2: asociación (--, -->), agregación (o--),
      composición (*--), generalización (<|--), realización (<|..) y
      dependencia (..>).
  CL2 Asociación, agregación y composición llevan multiplicidad en ambos extremos.
  CL3 Composición: del lado del todo la multiplicidad es 1 o 0..1.
  CL4 Generalización entre elementos del mismo tipo; la realización apunta a
      una interfaz. Sin ciclos de herencia.

Secuencia (secuencia*)
  SQ1 Solo fragmentos combinados de UML 2 (alt, opt, loop, par, break,
      critical, ref). "group" es de PlantUML, no de UML.
  SQ2 alt, else, opt, loop y break llevan su guarda.
  SQ3 Sin mensajes bidireccionales (<->): cada mensaje tiene un emisor y un receptor.

Actividades (actividades*)
  AC1 Exactamente un nodo inicial (start) y al menos un nodo final (stop/end).
  AC2 Cada rama de una decisión lleva guarda: then (..), else (..).

Estados (estados*)
  ST1 Un solo estado inicial ([*] -->) por región; su transición no lleva
      guarda (para elegir el estado de entrada se usa un <<choice>>).
  ST2 Todos los estados son alcanzables desde el inicial.
  ST3 Transiciones con la forma  evento [guarda] / acción  (cada parte opcional).

Paquetes (paquetes*)
  PK1 Dependencia entre paquetes: línea discontinua con flecha abierta (..>).
  PK2 Sin dependencias circulares entre paquetes.

Uso: check_uml.py [--gh] [--strict] [directorio]   (por defecto: diagramas)
Sale con 1 si hay errores (o avisos con --strict).
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

TOKEN = r'(?:"[^"]*"|\([^)]*\)|:[^:\s][^:]*:|\[\*\]|[\w.]+)'
REL = re.compile(
    rf'^\s*(?P<a>{TOKEN})\s*(?P<ma>"[^"]*")?\s*'
    r'(?P<arrow>[<|*o#x+}^]*(?:-|\.)[-.\w\[\]#,]*?[|>*o#x+{^]*)\s*'
    rf'(?P<mb>"[^"]*")?\s*(?P<b>{TOKEN})\s*(?::\s*(?P<label>.*))?$'
)
DIRECCION = re.compile(r'(?<=[-.])(?:up|down|left|right|u|d|l|r)(?=[-.])')
CLASS_DECL = re.compile(
    r'^\s*(abstract\s+class|abstract|class|interface|enum|entity)\s+'
    r'(?:"[^"]*"\s+as\s+)?([A-Za-z_]\w*)(?:\s+as\s+([A-Za-z_]\w*))?.*?(\{)?\s*$'
)
ELEM_DECL = re.compile(
    r'^\s*(actor|usecase|package|rectangle|state|node|folder|frame)\s+'
    r'(?:"(?P<label>[^"]*)"|(?P<name>[\w.]+))(?:\s+as\s+(?P<alias>[\w.]+))?'
    r'[^{]*?(?P<open>\{)?\s*$'
)
VERBO = re.compile(r'^[a-záéíóúñ]+(ar|er|ir)(se)?$', re.I)


class Reporte:
    def __init__(self, gh):
        self.gh, self.errores, self.avisos = gh, [], []

    def _msg(self, nivel, f, n, codigo, texto):
        if self.gh:
            loc = f"file={f}" + (f",line={n}" if n else "")
            return f"::{nivel} {loc}::{codigo} {texto}"
        return f"{codigo} {f}{':' + str(n) if n else ''}: {texto}"

    def error(self, f, n, codigo, texto):
        self.errores.append(self._msg("error", f, n, codigo, texto))

    def aviso(self, f, n, codigo, texto):
        self.avisos.append(self._msg("warning", f, n, codigo, texto))


def lineas(path):
    """[(n, línea)] sin comentarios, notas ni leyendas, conservando el número."""
    texto = path.read_text(encoding="utf-8")
    texto = re.sub(r"/'.*?'/", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)
    out, bloque = [], None
    for n, l in enumerate(texto.splitlines(), 1):
        s = l.strip()
        if bloque:
            if re.match(bloque, s):
                bloque = None
            continue
        if s.startswith("'") or not s:
            continue
        if re.match(r'^(note|legend|header|footer)\b(?!.*:)', s) and not re.match(r'^note\b.*\bas\b', s):
            bloque = r'^end\s*' + {"note": "note", "legend": "legend",
                                   "header": "header", "footer": "footer"}[s.split()[0]]
            continue
        if re.match(r'^(note|legend)\b', s):  # nota de una línea
            continue
        out.append((n, l))
    return out


def flecha(arrow):
    """'<|--' -> ('<|', '-', ''); None si no es una flecha válida."""
    hidden = "hidden" in arrow
    a = re.sub(r'\[[^\]]*\]', '', arrow)
    a = DIRECCION.sub('', a)
    m = re.match(r'^([<|*o#x+}^]*)(-+|\.+)([|>*o#x+{^]*)$', a)
    if not m:
        return None
    return m.group(1), m.group(2)[0], m.group(3), hidden


def relaciones(lns):
    for n, l in lns:
        if re.match(r'^\s*(skinparam|title|!|hide|show|left|top|scale|@)', l):
            continue
        m = REL.match(l)
        if not m:
            continue
        f = flecha(m.group("arrow"))
        if f is None:
            continue
        izq, linea, der, hidden = f
        yield dict(n=n, a=m.group("a"), b=m.group("b"), izq=izq, linea=linea, der=der,
                   hidden=hidden, ma=m.group("ma"), mb=m.group("mb"),
                   label=(m.group("label") or "").strip(), arrow=m.group("arrow"))


def ciclos(grafo):
    """Devuelve un ciclo (lista de nodos) si existe."""
    color, pila = {}, []

    def dfs(u):
        color[u] = 1
        pila.append(u)
        for v in sorted(grafo.get(u, ())):
            if color.get(v) == 1:
                return pila[pila.index(v):] + [v]
            if not color.get(v):
                c = dfs(v)
                if c:
                    return c
        pila.pop()
        color[u] = 2
        return None

    for u in sorted(grafo):
        if not color.get(u):
            c = dfs(u)
            if c:
                return c
    return None


# ---------------------------------------------------------------- casos de uso
def check_casos_de_uso(f, lns, r, solo_generalizacion):
    elems, contenedores, pila = {}, [], []
    for n, l in lns:
        s = l.strip()
        if s == "}":
            if pila:
                pila.pop()
            continue
        m = ELEM_DECL.match(l)
        if m:
            kind = m.group(1)
            key = m.group("alias") or m.group("name") or m.group("label")
            texto = m.group("label") or m.group("name")
            if kind in ("actor", "usecase"):
                elems[key] = dict(kind=kind, n=n, texto=texto, dentro=[k for k, _ in pila])
            elif kind == "rectangle":
                contenedores.append((n, texto))
            if m.group("open"):
                pila.append((kind, key))
    sujetos = [c for c in contenedores]
    cus = {k: e for k, e in elems.items() if e["kind"] == "usecase"}
    actores = {k: e for k, e in elems.items() if e["kind"] == "actor"}

    if cus:
        if len(sujetos) != 1 or not sujetos[0][1]:
            r.error(f, sujetos[1][0] if len(sujetos) > 1 else None, "UC1",
                    "debe haber un solo sujeto (rectangle \"Sistema\" { ... }) con nombre")
        for k, e in cus.items():
            if "rectangle" not in e["dentro"]:
                r.error(f, e["n"], "UC1", f"el caso de uso {k} está fuera del sujeto")
            nombre = re.sub(r'^CU-\d+\s+', '', e["texto"].replace("\\n", " ")).split()
            if nombre and not VERBO.match(nombre[0]):
                r.aviso(f, e["n"], "UC7", f"'{nombre[0]}': el caso de uso debería empezar "
                                          "con un verbo en infinitivo")
    for k, e in actores.items():
        if "rectangle" in e["dentro"]:
            r.error(f, e["n"], "UC2", f"el actor {k} está dentro del sujeto; los actores son externos")

    usados, padres = set(), defaultdict(set)
    for rel in relaciones(lns):
        a, b = rel["a"], rel["b"]
        if rel["hidden"]:
            continue
        ka, kb = elems.get(a, {}).get("kind"), elems.get(b, {}).get("kind")
        if not ka or not kb:
            r.error(f, rel["n"], "UC6", f"relación con un elemento no declarado: {a} / {b}")
            continue
        usados |= {a, b}
        izq, linea, der = rel["izq"], rel["linea"], rel["der"]
        gen = linea == "-" and {izq, der} in ({"<|", ""}, {"|>", ""}) and izq != der
        if gen:
            hijo, padre = (b, a) if izq == "<|" else (a, b)
        if ka != kb:
            if not (linea == "-" and izq == "" and der == ""):
                r.error(f, rel["n"], "UC3", f"'{a} {rel['arrow']} {b}': la asociación actor - caso de "
                                            "uso es una línea continua sin flecha (--)")
            elif "<<" in rel["label"]:
                r.error(f, rel["n"], "UC3", f"'{a} -- {b}': una asociación no lleva "
                                            "estereotipo (include/extend son solo entre casos de uso)")
        elif ka == "usecase":
            dep = linea == "." and {izq, der} in ({"<", ""}, {">", ""}) and izq != der
            estereo = re.findall(r'<<\s*(\w+)\s*>>', rel["label"])
            if dep and estereo in (["include"], ["extend"]):
                pass
            elif gen and not rel["label"]:
                padres[hijo].add(padre)
            else:
                r.error(f, rel["n"], "UC4", f"'{a} {rel['arrow']} {b} : {rel['label']}': entre casos de "
                                            "uso solo <<include>> o <<extend>> (..>) o generalización (<|--)")
        else:
            if gen:
                padres[hijo].add(padre)
            else:
                r.error(f, rel["n"], "UC5", f"'{a} {rel['arrow']} {b}': entre actores solo se admite "
                                            "la generalización (<|--)")

    if not solo_generalizacion:
        for k, e in elems.items():
            if k not in usados:
                r.error(f, e["n"], "UC6", f"{'el actor' if e['kind'] == 'actor' else 'el caso de uso'} "
                                          f"{k} no participa en ninguna relación")
    c = ciclos(padres)
    if c:
        r.error(f, None, "UC5", "generalización circular: " + " -> ".join(c))
    else:
        def nivel(x):
            return 1 + max((nivel(p) for p in padres.get(x, ())), default=0)
        for k in actores:
            if nivel(k) > 3:
                r.aviso(f, actores[k]["n"], "UC8", f"el actor {k} está a {nivel(k)} niveles; "
                                                   "conviene no pasar de 3")


# ---------------------------------------------------------------------- clases
def check_clases(f, lns, r):
    tipos, cuerpo = {}, 0
    rels, herencias = [], []
    for n, l in lns:
        if cuerpo:
            cuerpo += l.count("{") - l.count("}")
            continue
        m = CLASS_DECL.match(l)
        if m:
            nombre = m.group(3) or m.group(2)
            tipos[nombre] = m.group(1).split()[-1]
            for clave, clase in (("extends", "generalización"), ("implements", "realización")):
                e = re.search(rf'\b{clave}\s+([\w, ]+?)\s*(?:<<|\{{|$)', l)
                for padre in (e.group(1).split(",") if e else ()):
                    herencias.append((n, f"'{nombre} {clave} {padre.strip()}'", nombre, padre.strip(), clase))
            if m.group(4):
                cuerpo = 1
            continue
        rels.append((n, l))

    padres = defaultdict(set)
    for rel in relaciones(rels):
        if rel["hidden"]:
            continue
        a, b, izq, linea, der = rel["a"], rel["b"], rel["izq"], rel["linea"], rel["der"]
        desc = f"'{a} {rel['arrow']} {b}'"
        if linea == "-" and {izq, der} <= {"", "<", ">"}:
            clase = "asociación"
        elif linea == "-" and ((izq in ("o", "*") and der in ("", ">")) or
                               (der in ("o", "*") and izq in ("", "<"))):
            clase = "composición" if "*" in (izq, der) else "agregación"
        elif {izq, der} in ({"<|", ""}, {"|>", ""}) and izq != der:
            clase = "generalización" if linea == "-" else "realización"
        elif linea == "." and {izq, der} in ({"<", ""}, {">", ""}) and izq != der:
            clase = "dependencia"
        else:
            r.error(f, rel["n"], "CL1", f"{desc} no es una relación UML 2 entre clases")
            continue
        if clase in ("asociación", "agregación", "composición"):
            if not (rel["ma"] and rel["mb"]):
                r.error(f, rel["n"], "CL2", f"{desc}: la {clase} lleva multiplicidad en ambos extremos")
            if clase == "composición" and rel["ma"] and rel["mb"]:
                todo = rel["ma"] if "*" in izq else rel["mb"]
                if todo.strip('"').strip() not in ("1", "0..1"):
                    r.error(f, rel["n"], "CL3", f"{desc}: en la composición el todo tiene "
                                                f"multiplicidad 1 o 0..1, no {todo}")
        elif clase in ("generalización", "realización"):
            hijo, padre = (b, a) if izq == "<|" else (a, b)
            herencias.append((rel["n"], desc, hijo, padre, clase))
    for n, desc, hijo, padre, clase in herencias:
        th, tp = tipos.get(hijo, "class"), tipos.get(padre, "class")
        if clase == "realización" and tp != "interface":
            r.error(f, n, "CL4", f"{desc}: la realización apunta a una interfaz")
        if clase == "generalización" and (th == "interface") != (tp == "interface"):
            r.error(f, n, "CL4", f"{desc}: una clase realiza (<|..) una interfaz, no la generaliza")
        if clase == "generalización":
            padres[hijo].add(padre)
    c = ciclos(padres)
    if c:
        r.error(f, None, "CL4", "herencia circular: " + " -> ".join(c))


# ------------------------------------------------------------------- secuencia
FRAG = re.compile(r'^\s*(alt|else|opt|loop|par|break|critical|group|ref|neg|assert)\b(.*)$')


def check_secuencia(f, lns, r):
    for n, l in lns:
        m = FRAG.match(l)
        if m:
            op, resto = m.group(1), m.group(2).strip()
            if op in ("group", "neg", "assert"):
                r.error(f, n, "SQ1", f"'{op}' no es un fragmento combinado de PlantUML/UML 2 "
                                     "válido; usar alt, opt, loop, par, break, critical o ref")
            elif op in ("alt", "else", "opt", "loop", "break") and not resto:
                r.error(f, n, "SQ2", f"el fragmento '{op}' necesita su guarda")
            continue
        if re.match(r'^\s*[\w"]+\s*<-+>', l):
            r.error(f, n, "SQ3", "mensaje bidireccional: separar en mensaje y respuesta")


# ------------------------------------------------------------------ actividades
def check_actividades(f, lns, r):
    inicios = [n for n, l in lns if re.match(r'^\s*start\s*$', l)]
    finales = [n for n, l in lns if re.match(r'^\s*(stop|end|kill)\s*$', l)]
    if len(inicios) != 1:
        r.error(f, inicios[1] if len(inicios) > 1 else None, "AC1",
                f"debe haber un solo nodo inicial (start); hay {len(inicios)}")
    if not finales:
        r.error(f, None, "AC1", "falta el nodo final (stop)")
    for n, l in lns:
        s = l.strip()
        if re.match(r'^(else\s*)?if\s*\(|^elseif\s*\(', s) and not re.search(r'\bthen\s*\(.+\)', s):
            r.error(f, n, "AC2", "la rama 'then' de la decisión necesita su guarda: then ([condición])")
        elif re.match(r'^else\b(?!\s*if)', s) and not re.match(r'^else\s*\(.+\)', s):
            r.error(f, n, "AC2", "la rama 'else' de la decisión necesita su guarda: else ([condición])")


# ---------------------------------------------------------------------- estados
TRANSICION = re.compile(r'^\s*(?P<a>\[\*\]|[\w.]+)\s*(?P<arrow><-[-\w\[\]#,]*|-[-\w\[\]#,]*>)\s*'
                        r'(?P<b>\[\*\]|[\w.]+)\s*(?::\s*(?P<label>.*))?$')
ETIQUETA = re.compile(r'^[^\[\]/]*(\[[^\[\]]+\])?\s*(/[^\[\]]*)?$')


def check_estados(f, lns, r):
    pila, iniciales, grafo, estados = [], defaultdict(list), defaultdict(set), {}
    for n, l in lns:
        s = l.strip()
        if s == "}":
            if pila:
                pila.pop()
            continue
        m = ELEM_DECL.match(l)
        if m and m.group(1) == "state":
            key = m.group("alias") or m.group("name")
            estados.setdefault(key, n)
            if pila:
                grafo[pila[-1]]  # el compuesto existe aunque no tenga salidas
            if m.group("open"):
                pila.append(key)
            continue
        t = TRANSICION.match(l)
        if not t:
            continue
        a, b, label = t.group("a"), t.group("b"), (t.group("label") or "").replace("\\n", " ").strip()
        if t.group("arrow").startswith("<"):  # destino <-- origen
            a, b = b, a
        region = pila[-1] if pila else None
        if a == "[*]":
            iniciales[region].append(n)
            if "[" in label:
                r.error(f, n, "ST1", "la transición del estado inicial no lleva guarda; "
                                     "usar un pseudoestado <<choice>>")
            grafo[region or "[inicio]"].add(b)
        elif b != "[*]":
            grafo[a].add(b)
        for x in (a, b):
            if x != "[*]":
                estados.setdefault(x, n)
        if label and not ETIQUETA.match(label):
            r.error(f, n, "ST3", f"'{label}': la transición se escribe evento [guarda] / acción")
    for region, ns in iniciales.items():
        if len(ns) > 1:
            r.error(f, ns[1], "ST1", f"más de un estado inicial en {region or 'el diagrama'}")
    if None not in iniciales:
        r.error(f, None, "ST1", "falta el estado inicial ([*] --> estado)")
        return
    vistos, cola = set(), ["[inicio]"]
    while cola:
        u = cola.pop()
        for v in grafo.get(u, ()):
            if v not in vistos:
                vistos.add(v)
                cola.append(v)
    for e, n in sorted(estados.items(), key=lambda x: x[1]):
        if e not in vistos:
            r.error(f, n, "ST2", f"el estado {e} no es alcanzable desde el estado inicial")


# --------------------------------------------------------------------- paquetes
def check_paquetes(f, lns, r):
    paquetes = set()
    for n, l in lns:
        m = ELEM_DECL.match(l)
        if m and m.group(1) in ("package", "rectangle", "folder", "frame", "node"):
            paquetes.add(m.group("alias") or m.group("name") or m.group("label"))
    grafo = defaultdict(set)
    for rel in relaciones(lns):
        if rel["hidden"] or rel["a"] not in paquetes or rel["b"] not in paquetes:
            continue
        izq, linea, der = rel["izq"], rel["linea"], rel["der"]
        if not (linea == "." and {izq, der} in ({"<", ""}, {">", ""}) and izq != der):
            r.error(f, rel["n"], "PK1", f"'{rel['a']} {rel['arrow']} {rel['b']}': la dependencia "
                                        "entre paquetes es discontinua con flecha abierta (..>)")
            continue
        origen, destino = (rel["b"], rel["a"]) if izq == "<" else (rel["a"], rel["b"])
        grafo[origen].add(destino)
    c = ciclos(grafo)
    if c:
        r.error(f, None, "PK2", "dependencia circular entre paquetes: " + " -> ".join(c))


# ------------------------------------------------------------------------- main
def tipo(nombre):
    m = re.match(r'^CU-\d{2}-([a-z-]+?)(?:-\d+-.*)?\.puml$', nombre)
    return m.group(1) if m else None


def main(argv):
    gh, strict = "--gh" in argv, "--strict" in argv
    args = [a for a in argv if not a.startswith("--")]
    base = Path(args[0] if args else "diagramas")
    r = Reporte(gh)
    archivos = sorted(base.glob("*.puml"))
    for path in archivos:
        f, t, lns = str(path), tipo(path.name), lineas(path)
        if not any(re.match(r'^\s*skinparam\s+style\s+strictuml\s*$', l) for _, l in lns):
            r.error(f, None, "G1", "falta 'skinparam style strictuml' (notación UML 2 estricta)")
        if t in ("casos-de-uso-alto-nivel", "generalizacion-actores"):
            check_casos_de_uso(f, lns, r, t == "generalizacion-actores")
        elif t in ("clases", "modelo-estructural"):
            check_clases(f, lns, r)
        elif t == "secuencia":
            check_secuencia(f, lns, r)
        elif t == "actividades":
            check_actividades(f, lns, r)
        elif t == "estados":
            check_estados(f, lns, r)
        elif t == "paquetes":
            check_paquetes(f, lns, r)
    for e in r.errores:
        print(e)
    for w in r.avisos:
        print(w)
    print(f"\nNotación UML: {len(r.errores)} errores, {len(r.avisos)} avisos "
          f"en {len(archivos)} diagramas.")
    return 1 if r.errores or (strict and r.avisos) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
