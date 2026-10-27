#!/usr/bin/env python3
"""Variantes de build/model.xmi para ver qué lee VP de interacciones y actividades.

VP importa clases y tipos del XMI 2.5.1, pero no muestra lifelines, mensajes ni
carriles. Cada variante cambia una sola dimensión de la serialización:

  B  UML 2.5.1, coveredBy como hijos <coveredBy xmi:idref> (como exporta VP) y
     cada nodo de actividad con inPartition además de ActivityPartition.node.
  A  lo mismo que B, con namespaces XMI 2.1 / UML 2.1.
  C  lo mismo que A, imitando el export de VP: namespace UML 2.0 y
     MessageOccurrenceSpecification escrito como EventOccurrence (UML 2.0).

Uso: variantes.py build/model.xmi salida/
"""
import sys
from pathlib import Path

from lxml import etree

XMI251, UML251 = 'http://www.omg.org/spec/XMI/20131001', 'http://www.omg.org/spec/UML/20161101'
XMI21, UML21 = 'http://schema.omg.org/spec/XMI/2.1', 'http://schema.omg.org/spec/UML/2.1'
UML20 = 'http://schema.omg.org/spec/UML/2.0'


def ajustar(raiz):
    X = f'{{{XMI251}}}'
    ids = {e.get(X + 'id'): e for e in raiz.iter() if e.get(X + 'id')}
    for e in raiz.iter():
        cov = e.get('coveredBy')
        if cov:
            del e.attrib['coveredBy']
            for i in cov.split():
                etree.SubElement(e, 'coveredBy').set(X + 'idref', i)
        if e.get(X + 'type') == 'uml:ActivityPartition' and e.get('node'):
            for n in e.get('node').split():
                nodo = ids.get(n)
                if nodo is not None:
                    previo = nodo.get('inPartition')
                    nodo.set('inPartition', f'{previo} {e.get(X + "id")}' if previo else e.get(X + 'id'))


def main(entrada, salida):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    texto = Path(entrada).read_text(encoding='utf-8')
    raiz = etree.fromstring(texto.encode('utf-8'))
    ajustar(raiz)
    b = etree.tostring(raiz, encoding='unicode')
    cab = '<?xml version="1.0" encoding="UTF-8"?>\n'
    (salida / 'vp-B-uml251.xmi').write_text(cab + b, encoding='utf-8')
    a = b.replace(XMI251, XMI21).replace(UML251, UML21).replace(
        '<xmi:XMI ', '<xmi:XMI xmi:version="2.1" ', 1)
    a = a.replace('http://schema.omg.org/spec/UML/2.1/PrimitiveTypes.xmi', UML251 + '/PrimitiveTypes.xmi')
    (salida / 'vp-A-xmi21.xmi').write_text(cab + a, encoding='utf-8')
    c = a.replace(UML21, UML20).replace('uml:MessageOccurrenceSpecification', 'uml:EventOccurrence')
    (salida / 'vp-C-vp-uml20.xmi').write_text(cab + c, encoding='utf-8')


if __name__ == '__main__':
    main(*sys.argv[1:3])
