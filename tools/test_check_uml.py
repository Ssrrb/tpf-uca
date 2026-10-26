#!/usr/bin/env python3
"""Pruebas de check_uml.py: cada regla detecta su error y deja pasar lo correcto.

Uso: python3 tools/test_check_uml.py
"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_uml  # noqa: E402

CABECERA = "@startuml\n!theme plain\nskinparam style strictuml\n"


def codigos(nombre, cuerpo):
    """Corre check_uml sobre un solo diagrama y devuelve los códigos reportados."""
    with tempfile.TemporaryDirectory() as d:
        Path(d, nombre).write_text(CABECERA + cuerpo + "\n@enduml\n", encoding="utf-8")
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            check_uml.main([d])
    return {l.split()[0] for l in salida.getvalue().splitlines() if l[:2].isalpha() and l[2:3].isdigit()}


CU = "CU-00-casos-de-uso-alto-nivel.puml"
CU_OK = """
actor Cliente as C
actor "Sistema ERP" as ERP <<sistema>>
rectangle "Tienda" {
  usecase "Comprar producto" as U1
  usecase "Pagar compra" as U2
  usecase "Aplicar cupón" as U3
}
C -- U1
U2 -- ERP
U1 ..> U2 : <<include>>
U3 ..> U1 : <<extend>>
"""


class CasosDeUso(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(CU, CU_OK), set())

    def test_falta_strictuml(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, CU).write_text("@startuml\n" + CU_OK + "@enduml\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check_uml.main([d]), 1)

    def test_asociacion_con_flecha(self):
        self.assertIn("UC3", codigos(CU, CU_OK.replace("C -- U1", "C --> U1")))

    def test_asociacion_discontinua(self):
        self.assertIn("UC3", codigos(CU, CU_OK.replace("C -- U1", "C .. U1")))

    def test_include_con_linea_continua(self):
        self.assertIn("UC4", codigos(CU, CU_OK.replace("U1 ..> U2", "U1 --> U2")))

    def test_estereotipo_no_uml2(self):
        self.assertIn("UC4", codigos(CU, CU_OK.replace("<<include>>", "<<uses>>")))

    def test_asociacion_entre_casos_de_uso(self):
        self.assertIn("UC4", codigos(CU, CU_OK.replace("U1 ..> U2 : <<include>>", "U1 -- U2")))

    def test_asociacion_entre_actores(self):
        self.assertIn("UC5", codigos(CU, CU_OK + "C -- ERP\n"))

    def test_generalizacion_entre_actores(self):
        self.assertEqual(codigos(CU, CU_OK + "actor Persona as P\nP <|-- C\n"), set())

    def test_actor_dentro_del_sujeto(self):
        self.assertIn("UC2", codigos(CU, CU_OK.replace('rectangle "Tienda" {', 'rectangle "Tienda" {\n  actor Cajero as K')
                                     + "K -- U1\n"))

    def test_caso_de_uso_fuera_del_sujeto(self):
        self.assertIn("UC1", codigos(CU, CU_OK + 'usecase "Ver catálogo" as U4\nC -- U4\n'))

    def test_sin_sujeto(self):
        cuerpo = CU_OK.replace('rectangle "Tienda" {', "").replace("}\n", "")
        self.assertIn("UC1", codigos(CU, cuerpo))

    def test_elemento_aislado(self):
        self.assertIn("UC6", codigos(CU, CU_OK + "actor Auditor as A\n"))

    def test_nombre_sin_verbo(self):
        self.assertIn("UC7", codigos(CU, CU_OK.replace("Comprar producto", "Compra de producto")))


CL = "CU-01-clases.puml"
CL_OK = """
class Pedido {
  + total: decimal
  --
  + confirmar(): vacío
}
class Linea
class Producto
interface Pagable
class Control <<control>>
Pedido "1" *-- "1..*" Linea : contiene
Linea "0..*" --> "1" Producto : refiere
Pagable <|.. Pedido
Control ..> Pedido : usa
"""


class Clases(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(CL, CL_OK), set())

    def test_flecha_no_uml(self):
        self.assertIn("CL1", codigos(CL, CL_OK + "Linea #-- Producto\n"))

    def test_sin_multiplicidad(self):
        self.assertIn("CL2", codigos(CL, CL_OK.replace('Linea "0..*" --> "1" Producto', "Linea --> Producto")))

    def test_composicion_todo_muchos(self):
        self.assertIn("CL3", codigos(CL, CL_OK.replace('Pedido "1" *--', 'Pedido "0..*" *--')))

    def test_realizacion_a_clase(self):
        self.assertIn("CL4", codigos(CL, CL_OK + "Producto <|.. Linea\n"))

    def test_generalizacion_a_interfaz(self):
        self.assertIn("CL4", codigos(CL, CL_OK + "Pagable <|-- Linea\n"))

    def test_herencia_circular_con_extends(self):
        self.assertIn("CL4", codigos(CL, CL_OK + "class A extends B\nclass B extends A\n"))

    def test_implements_a_clase(self):
        self.assertIn("CL4", codigos(CL, CL_OK + "class A implements Producto\n"))

    def test_herencia_circular(self):
        self.assertIn("CL4", codigos(CL, CL_OK + "Linea <|-- Producto\nProducto <|-- Linea\n"))


SQ = "CU-01-secuencia.puml"
SQ_OK = """
actor Usuario
participant "s:\\nSistema" as S
Usuario -> S: pedir()
alt Hay stock
  S --> Usuario: ok
else Sin stock
  S --> Usuario: error
end
loop Por cada ítem
  S -> S: sumar()
end
"""


class Secuencia(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(SQ, SQ_OK), set())

    def test_group(self):
        self.assertIn("SQ1", codigos(SQ, SQ_OK.replace("loop Por cada ítem", "group Por cada ítem")))

    def test_sin_guarda(self):
        self.assertIn("SQ2", codigos(SQ, SQ_OK.replace("alt Hay stock", "alt")))

    def test_bidireccional(self):
        self.assertIn("SQ3", codigos(SQ, SQ_OK + "Usuario <-> S: hablar\n"))


AC = "CU-01-actividades.puml"
AC_OK = """
start
:Pedir;
if (¿Hay stock?) then ([sí])
  :Vender;
else ([no])
  :Avisar;
  stop
endif
stop
"""


class Actividades(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(AC, AC_OK), set())

    def test_dos_inicios(self):
        self.assertIn("AC1", codigos(AC, "start\n" + AC_OK))

    def test_sin_final(self):
        self.assertIn("AC1", codigos(AC, AC_OK.replace("stop", ":Fin;")))

    def test_then_sin_guarda(self):
        self.assertIn("AC2", codigos(AC, AC_OK.replace("then ([sí])", "then")))

    def test_else_sin_guarda(self):
        self.assertIn("AC2", codigos(AC, AC_OK.replace("else ([no])", "else")))


ST = "CU-01-estados.puml"
ST_OK = """
state c <<choice>>
[*] --> c : crear()
c --> borrador : [sin datos]
c --> activo : [con datos]
borrador --> activo : completar() [datos válidos] / guardar()
activo --> [*]
"""


class Estados(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(ST, ST_OK), set())

    def test_flecha_invertida(self):
        cuerpo = ST_OK.replace("borrador --> activo : completar()", "activo <-- borrador : completar()")
        self.assertEqual(codigos(ST, cuerpo), set())

    def test_dos_iniciales(self):
        self.assertIn("ST1", codigos(ST, ST_OK + "[*] --> borrador\n"))

    def test_inicial_con_guarda(self):
        self.assertIn("ST1", codigos(ST, ST_OK.replace("[*] --> c : crear()", "[*] --> c : crear() [ok]")))

    def test_sin_inicial(self):
        self.assertIn("ST1", codigos(ST, ST_OK.replace("[*] --> c : crear()\n", "")))

    def test_inalcanzable(self):
        self.assertIn("ST2", codigos(ST, ST_OK + "archivado --> activo : restaurar()\n"))

    def test_etiqueta_mal_formada(self):
        self.assertIn("ST3", codigos(ST, ST_OK.replace("completar() [datos válidos] / guardar()",
                                                        "completar() / guardar() [datos válidos]")))


PK = "CU-01-paquetes.puml"
PK_OK = """
package "Dominio" as dom {
}
package "Interfaz" as ui {
}
package "Datos" as dat {
}
ui ..> dom : <<use>>
dat ..> dom : <<use>>
"""


class Paquetes(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(codigos(PK, PK_OK), set())

    def test_dependencia_continua(self):
        self.assertIn("PK1", codigos(PK, PK_OK + "ui --> dat : accede\n"))

    def test_ciclo(self):
        self.assertIn("PK2", codigos(PK, PK_OK + "dom ..> ui\n"))


class Repositorio(unittest.TestCase):
    def test_diagramas_del_repo_sin_errores(self):
        base = Path(__file__).resolve().parent.parent / "diagramas"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_uml.main([str(base)]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
