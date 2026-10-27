#!/usr/bin/env python3
"""Pruebas del pipeline .puml → modelo → XMI con errores inyectados.

Cada caso arma un directorio con diagramas mínimos y comprueba qué códigos
reporta tools/modelo.py y en qué archivo:línea.
Uso: python3 tools/uml/test_modelo.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modelo import construir  # noqa: E402
from uml import xmi  # noqa: E402

CLASES = """@startuml
title CU-01 · Clases
package "ERP" {
  class Obra {
    código: texto
    estado: abierta | cerrada
    --
    + cerrar(motivo: texto): vacío
  }
  class Cliente {
    ruc: texto
  }
}
Obra "0..*" --> "1" Cliente : contratada por
@enduml
"""

SECUENCIA = """@startuml
actor "Administrador" as Adm
participant "obra:\\nObra" as O
Adm -> O: cerrar(motivo)
alt motivo válido
  O --> Adm: cerrada
else motivo vacío
  O --> Adm: error
end
@enduml
"""

ESTADOS = """@startuml
state "Abierta" as abierta
state "Cerrada" as cerrada
[*] --> abierta
abierta --> cerrada : cerrar(motivo) [motivo válido] / registrar fecha
cerrada --> [*]
@enduml
"""

ACTIVIDADES = """@startuml
|Administrador|
start
:Elegir la obra;
if (¿Tiene motivo?) then ([sí])
  :Cerrar la obra;
else ([no])
  :Pedir el motivo;
endif
stop
@enduml
"""


def armar(dir_, extra=None):
    archivos = {'CU-01-clases.puml': CLASES, 'CU-01-secuencia.puml': SECUENCIA,
                'CU-01-estados.puml': ESTADOS, 'CU-01-actividades.puml': ACTIVIDADES}
    archivos.update(extra or {})
    for nombre, texto in archivos.items():
        (Path(dir_) / nombre).write_text(texto, encoding='utf-8')


def correr(extra=None):
    with tempfile.TemporaryDirectory() as d:
        armar(d, extra)
        modelo, problemas, _ = construir(d, raiz=d)
        return modelo, [p for p in problemas.lista if p['nivel'] == 'error']


class Pruebas(unittest.TestCase):
    def test_limpio(self):
        modelo, errores = correr()
        self.assertEqual(errores, [])
        texto, gen = xmi.generar(modelo.a_json())
        self.assertIn('uml:Interaction', texto)
        self.assertIn('ObraEstado', texto)          # R3: unión → Enumeration
        self.assertIn('PrimitiveTypes.xmi#String', texto)  # R2

    def test_construccion_prohibida(self):
        _, errores = correr({'CU-02-clases.puml': '@startuml\nentity Factura\n@enduml\n'})
        self.assertIn(('P1', 'CU-02-clases.puml:2'), [(e['codigo'], e['src']) for e in errores])

    def test_mensaje_a_operacion_inexistente(self):
        sec = SECUENCIA.replace('cerrar(motivo)', 'archivar(motivo)')
        _, errores = correr({'CU-01-secuencia.puml': sec})
        self.assertIn(('C3', 'CU-01-secuencia.puml:4'), [(e['codigo'], e['src']) for e in errores])

    def test_lifeline_sin_clase(self):
        sec = SECUENCIA.replace('obra:\\nObra', 'obra:\\nObraa')
        _, errores = correr({'CU-01-secuencia.puml': sec})
        self.assertIn('C3', [e['codigo'] for e in errores])

    def test_relacion_a_elemento_no_definido(self):
        cl = CLASES.replace('Obra "0..*" --> "1" Cliente', 'Obra "0..*" --> "1" Proveedor')
        _, errores = correr({'CU-01-clases.puml': cl})
        self.assertIn(('C4', 'CU-01-clases.puml:14'), [(e['codigo'], e['src']) for e in errores])

    def test_multiplicidades_incompatibles(self):
        otro = CLASES.replace('"0..*" --> "1"', '"1" --> "1"').replace('CU-01', 'CU-02')
        _, errores = correr({'CU-02-clases.puml': otro})
        self.assertIn('C5', [e['codigo'] for e in errores])

    def test_convencion_de_nombres(self):
        cl = CLASES.replace('class Cliente {', 'class cliente_erp {').replace(
            '--> "1" Cliente', '--> "1" cliente_erp')
        _, errores = correr({'CU-01-clases.puml': cl})
        self.assertIn('C6', [e['codigo'] for e in errores])

    def test_variantes_de_escritura(self):
        otro = '@startuml\npackage "ERP" {\n  class "Obra" as OBRA\n}\n@enduml\n'
        _, errores = correr({'CU-02-clases.puml': otro})
        self.assertIn('C1', [e['codigo'] for e in errores])


if __name__ == '__main__':
    unittest.main(verbosity=2)
