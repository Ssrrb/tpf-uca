"""Paso 6: build/model.json → XMI 2.5.1 canónico con UML 2.5.1.

Namespaces normativos de OMG:
  XMI 2.5.1  http://www.omg.org/spec/XMI/20131001
  UML 2.5.1  http://www.omg.org/spec/UML/20161101
Los tipos primitivos se referencian a PrimitiveTypes.xmi de OMG.

Estructura del modelo generado:
  Model "Ctrl+"
    Package Tipos           DataTypes y Enumerations generadas (R2, R3)
    Package Actores         Actores de las secuencias
    Package ERP, ECMS, ...  Clases, enumeraciones y asociaciones (de los diagramas de clases)
    Package Comportamiento
      Package CU-xx         Interactions, StateMachines, Activities y sus eventos
"""
import re
import unicodedata
import xml.etree.ElementTree as ET

XMI_NS = 'http://www.omg.org/spec/XMI/20131001'
UML_NS = 'http://www.omg.org/spec/UML/20161101'
PRIMITIVOS_HREF = 'http://www.omg.org/spec/UML/20161101/PrimitiveTypes.xmi#'
X = f'{{{XMI_NS}}}'
U = f'{{{UML_NS}}}'
VISIBILIDAD = {'+': 'public', '-': 'private', '#': 'protected', '~': 'package'}

ET.register_namespace('xmi', XMI_NS)
ET.register_namespace('uml', UML_NS)


def slug(texto):
    s = unicodedata.normalize('NFKD', texto or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^A-Za-z0-9_.-]+', '_', s).strip('_')
    return s if s and (s[0].isalpha() or s[0] == '_') else f'_{s}'


def una_linea(texto):
    return re.sub(r'\s+', ' ', texto or '').strip()


def sin_corchetes(guarda):
    if guarda is None:
        return None
    g = guarda.strip()
    if g.startswith('[') and g.endswith(']'):
        g = g[1:-1].strip()
    return g or None


def camel(texto):
    s = re.sub(r'[^\w]+', ' ', texto or '').split()
    if not s:
        return 'extremo'
    return s[0][:1].lower() + s[0][1:] + ''.join(p[:1].upper() + p[1:] for p in s[1:])


class Generador:
    def __init__(self, modelo, nombre='Ctrl+'):
        self.m = modelo
        self.ids = set()
        self.idx = {}          # nombre de clasificador -> xmi:id
        self.ops = {}          # 'Clase.op' -> xmi:id
        self.no_validado = []
        self.eventos = {}
        self.raiz = ET.Element(f'{X}XMI', {f'{X}version': '20131001'})
        self.model = self.el(self.raiz, f'{U}Model', 'uml:Model', 'Ctrl', name=nombre)

    # ------------------------------------------------------------- utilidades
    def nuevo_id(self, base):
        base = slug(base)
        i, cand = 1, base
        while cand in self.ids:
            i += 1
            cand = f'{base}_{i}'
        self.ids.add(cand)
        return cand

    def el(self, padre, tag, tipo, base, **attrs):
        e = ET.SubElement(padre, tag)
        e.set(f'{X}type', tipo)
        e.set(f'{X}id', self.nuevo_id(base))
        for k, v in attrs.items():
            if v is not None and v is not False:
                e.set(k, 'true' if v is True else str(v))
        return e

    @staticmethod
    def id_de(e):
        return e.get(f'{X}id')

    def comentario(self, padre, texto, anota=(), base='comentario'):
        c = self.el(padre, 'ownedComment', 'uml:Comment', f'{self.id_de(padre)}.{base}')
        if anota:
            c.set('annotatedElement', ' '.join(anota))
        b = ET.SubElement(c, 'body')
        b.text = texto
        return c

    def tipo(self, e, ref):
        """Pone el tipo de un TypedElement según una referencia del modelo."""
        if not ref:
            return
        if 'primitivo' in ref:
            ET.SubElement(e, 'type', {'href': PRIMITIVOS_HREF + ref['primitivo']})
        elif 'ref' in ref and ref['ref'] in self.idx:
            e.set('type', self.idx[ref['ref']])

    def multiplicidad(self, e, mult, coleccion=False):
        if coleccion and not mult:
            mult = {'lower': 0, 'upper': '*'}
        if not mult or mult.get('invalida'):
            return
        base = self.id_de(e)
        self.el(e, 'lowerValue', 'uml:LiteralInteger', f'{base}.lower', value=mult['lower'])
        self.el(e, 'upperValue', 'uml:LiteralUnlimitedNatural', f'{base}.upper', value=mult['upper'])

    def opaca(self, padre, tag, texto, base):
        e = self.el(padre, tag, 'uml:OpaqueExpression', base)
        ET.SubElement(e, 'language').text = 'Natural'
        ET.SubElement(e, 'body').text = texto
        return e

    # ----------------------------------------------------------------- partes
    def generar(self):
        d = self.m
        tipos = self.el(self.model, 'packagedElement', 'uml:Package', 'Tipos', name='Tipos')
        for t in d['tipos']:
            if t['kind'] == 'enum':
                e = self.el(tipos, 'packagedElement', 'uml:Enumeration', t['name'], name=t['name'])
                for lit in t['literales']:
                    self.el(e, 'ownedLiteral', 'uml:EnumerationLiteral', f'{t["name"]}.{lit}', name=lit)
            else:
                e = self.el(tipos, 'packagedElement', 'uml:DataType', t['name'], name=t['name'])
                self.comentario(e, f'Tipo de la notación del modelo: "{t["origen"]}".')
            self.idx[t['name']] = self.id_de(e)

        actores = self.el(self.model, 'packagedElement', 'uml:Package', 'Actores', name='Actores')
        for a in d['actores']:
            e = self.el(actores, 'packagedElement', 'uml:Actor', a['name'], name=a['name'])
            self.idx[a['name']] = self.id_de(e)

        paquetes = {}
        for p in d['paquetes']:
            padre = paquetes.get(p['padre'], self.model)
            paquetes[p['qname']] = self.el(padre, 'packagedElement', 'uml:Package', p['qname'],
                                           name=p['name'])
        self.paquetes = paquetes
        clases = {}
        for c in d['clasificadores']:
            padre = paquetes.get(c['package'], self.model)
            tipo = {'class': 'uml:Class', 'interface': 'uml:Interface',
                    'enum': 'uml:Enumeration'}[c['kind']]
            e = self.el(padre, 'packagedElement', tipo, c['name'], name=c['name'],
                        isAbstract=c['abstract'] or None)
            clases[c['name']] = e
            self.idx[c['name']] = self.id_de(e)
        for c in d['clasificadores']:
            self.clasificador(clases[c['name']], c)
        self.relaciones(clases)
        for com in d['comentarios']:
            # La nota la posee la primera clase que anota (así VP la muestra dentro de
            # esa clase y no suelta en la raíz); sin clase, el modelo.
            anota = [x for x in com['anota'] if x in clases]
            duenio = clases[anota[0]] if anota else self.model
            self.comentario(duenio, com['texto'], [self.idx[x] for x in anota])

        comp = self.el(self.model, 'packagedElement', 'uml:Package', 'Comportamiento',
                       name='Comportamiento')
        self.por_cu = {}
        for inter in d['interacciones']:
            self.interaccion(self.paquete_cu(comp, inter['cu']), inter)
        for maq in d['maquinas_de_estados']:
            self.maquina(self.paquete_cu(comp, maq['cu']), maq)
        for act in d['actividades']:
            self.actividad(self.paquete_cu(comp, act['cu']), act)
        self.resolver_refs()
        return self.raiz

    def paquete_cu(self, comp, cu):
        if cu not in self.por_cu:
            self.por_cu[cu] = self.el(comp, 'packagedElement', 'uml:Package', cu, name=cu)
        return self.por_cu[cu]

    def clasificador(self, e, c):
        base = self.id_de(e)
        if c['labels']:
            self.comentario(e, 'Nombre en el documento: ' + ', '.join(c['labels']) + '.',
                            [base], 'etiqueta')
        if c['kind'] == 'enum':
            for lit in c['literales']:
                self.el(e, 'ownedLiteral', 'uml:EnumerationLiteral', f'{base}.{lit["name"]}',
                        name=lit['name'])
            return
        for a in c['atributos']:
            p = self.el(e, 'ownedAttribute', 'uml:Property', f'{base}.{a["name"]}', name=a['name'],
                        visibility=VISIBILIDAD.get(a['visibility']),
                        isReadOnly=('inmutable' in a['modificadores'] or 'readOnly' in a['modificadores']) or None,
                        isStatic=a['static'] or None, isDerived=a['derivado'] or None)
            ref = a.get('type_ref')
            self.tipo(p, ref)
            self.multiplicidad(p, a['mult'], (ref or {}).get('coleccion'))
            if a['default']:
                self.opaca(p, 'defaultValue', a['default'], f'{self.id_de(p)}.default')
            otros = [m for m in a['modificadores'] if m not in ('inmutable', 'readOnly')]
            if otros:
                self.comentario(p, 'Restricción del modelo: {' + ', '.join(otros) + '}', [self.id_de(p)])
        for o in c['operaciones']:
            op = self.el(e, 'ownedOperation', 'uml:Operation', f'{base}.{o["name"]}', name=o['name'],
                         visibility=VISIBILIDAD.get(o['visibility']),
                         isStatic=o['static'] or None, isAbstract=o['abstract'] or None)
            self.ops[f'{c["name"]}.{o["name"]}'] = self.id_de(op)
            for prm in o['params']:
                pe = self.el(op, 'ownedParameter', 'uml:Parameter', f'{self.id_de(op)}.{prm["name"]}',
                             name=prm['name'], direction='in')
                ref = prm.get('type_ref')
                self.tipo(pe, ref)
                self.multiplicidad(pe, prm['mult'], (ref or {}).get('coleccion'))
            if o.get('return'):
                pe = self.el(op, 'ownedParameter', 'uml:Parameter', f'{self.id_de(op)}.return',
                             direction='return')
                ref = o.get('return_ref')
                self.tipo(pe, ref)
                self.multiplicidad(pe, o.get('return_mult'), (ref or {}).get('coleccion'))

    def relaciones(self, clases):
        self.etiquetas_repetidas = {}
        for r in self.m['relaciones']:
            if r['kind'] not in ('generalization', 'realization', 'dependency') and r.get('label'):
                k = (self.paquete_de(r['a']), r['label'])
                self.etiquetas_repetidas.setdefault(k, []).append(r)
        for r in self.m['relaciones']:
            a, b = clases.get(r['a']), clases.get(r['b'])
            if a is None or b is None:
                continue
            k = r['kind']
            if k == 'generalization':
                self.el(a, 'generalization', 'uml:Generalization', f'{r["a"]}.gen.{r["b"]}',
                        general=self.id_de(b))
            elif k == 'realization':
                self.el(a, 'interfaceRealization', 'uml:InterfaceRealization',
                        f'{r["a"]}.realiza.{r["b"]}', contract=self.id_de(b),
                        client=self.id_de(a), supplier=self.id_de(b))
            elif k == 'dependency':
                es_uso = (r.get('label') or '').strip() in ('<<use>>', '«use»')
                padre = self.paquetes.get(self.paquete_de(r['a']), self.model)
                self.el(padre, 'packagedElement', 'uml:Usage' if es_uso else 'uml:Dependency',
                        f'{r["a"]}.usa.{r["b"]}', client=self.id_de(a), supplier=self.id_de(b))
            else:
                self.asociacion(r, a, b)

    def paquete_de(self, nombre):
        for c in self.m['clasificadores']:
            if c['name'] == nombre:
                return c['package']
        return None

    def asociacion(self, r, a, b):
        """a es el origen (o el todo) y b el destino (o la parte)."""
        padre = self.paquetes.get(self.paquete_de(r['a']), self.model)
        nombre = r.get('label')
        grupo = self.etiquetas_repetidas.get((self.paquete_de(r['a']), nombre), [])
        if nombre and len(grupo) > 1:
            # Namespace::members_distinguishable: dos asociaciones no pueden llamarse
            # igual en el mismo paquete. Se agrega la clase que las distingue.
            if len({x['b'] for x in grupo}) == len(grupo):
                nombre = f'{nombre} ({r["b"]})'
            elif len({x['a'] for x in grupo}) == len(grupo):
                nombre = f'{nombre} ({r["a"]})'
            else:
                nombre = f'{nombre} ({r["a"]} - {r["b"]})'
        assoc = self.el(padre, 'packagedElement', 'uml:Association',
                        f'{r["a"]}_{r["b"]}', name=nombre)
        navegable_b = r['kind'] in ('association', 'association-bi', 'composition', 'aggregation')
        navegable_a = r['kind'] == 'association-bi'
        agregacion = {'composition': 'composite', 'aggregation': 'shared'}.get(r['kind'])

        def extremo(duenio_el, tipo_el, mult, nav, agg, owner_name):
            nombre_ext = self.nombre_extremo(duenio_el if nav else None, tipo_el.get('name'))
            if nav:
                p = self.el(duenio_el, 'ownedAttribute', 'uml:Property',
                            f'{owner_name}.{nombre_ext}', name=nombre_ext, aggregation=agg,
                            association=self.id_de(assoc), type=self.id_de(tipo_el))
            else:
                p = self.el(assoc, 'ownedEnd', 'uml:Property', f'{self.id_de(assoc)}.{nombre_ext}',
                            name=nombre_ext, aggregation=agg, association=self.id_de(assoc),
                            type=self.id_de(tipo_el))
            self.multiplicidad(p, mult)
            return self.id_de(p)

        fin_b = extremo(a, b, r['mult_b'], navegable_b, agregacion, r['a'])
        fin_a = extremo(b, a, r['mult_a'], navegable_a, None, r['b'])
        extremos = [x for x in self.raiz.iter() if self.id_de(x) in (fin_a, fin_b)]
        if len(extremos) == 2 and extremos[0].get('name') == extremos[1].get('name'):
            extremos[1].set('name', extremos[1].get('name') + '2')
        assoc.set('memberEnd', f'{fin_b} {fin_a}')

    def nombre_extremo(self, duenio_el, tipo_nombre):
        base = camel(tipo_nombre)
        if duenio_el is None:
            return base
        usados = {x.get('name') for x in duenio_el.findall('ownedAttribute')}
        nombre, i = base, 2
        while nombre in usados:
            nombre = f'{base}{i}'
            i += 1
        return nombre

    # ------------------------------------------------------------ secuencias
    def interaccion(self, padre, inter):
        e = self.el(padre, 'packagedElement', 'uml:Interaction', inter['name'], name=inter['name'])
        base = self.id_de(e)
        lifelines = {}
        for ll in inter['lifelines']:
            prop = self.el(e, 'ownedAttribute', 'uml:Property', f'{base}.{ll["alias"]}.rol',
                           name=ll['rol'] or ll['alias'])
            if ll.get('tipo_ref') in self.idx:
                prop.set('type', self.idx[ll['tipo_ref']])
            lifelines[ll['alias']] = (prop, ll)
        ll_el = {}
        for alias, (prop, ll) in lifelines.items():
            ll_el[alias] = self.el(e, 'lifeline', 'uml:Lifeline', f'{base}.{alias}',
                                   name=ll['label'], represents=self.id_de(prop))
        self.cubre = defaultdict_list()
        self.mensajes_de = []
        self.items(e, e, inter['items'], ll_el, base)
        for alias, l in ll_el.items():
            frags = self.cubre.get(alias, [])
            if frags:
                l.set('coveredBy', ' '.join(frags))
        e.set('_inter', inter['name'])

    def items(self, inter, contenedor, items, ll_el, base):
        """Agrega fragmentos a `contenedor` (Interaction o InteractionOperand).
        Devuelve el conjunto de lifelines usadas."""
        usadas = set()
        for it in items:
            t = it['tipo']
            if t == 'message':
                usadas |= self.mensaje(inter, contenedor, it, ll_el, base)
            elif t == 'fragment':
                cf = self.el(contenedor, 'fragment', 'uml:CombinedFragment',
                             f'{base}.{it["operador"]}', interactionOperator=it['operador'])
                usadas_cf = set()
                for k, op in enumerate(it['operandos']):
                    oe = self.el(cf, 'operand', 'uml:InteractionOperand', f'{self.id_de(cf)}.op{k + 1}')
                    if op['guarda']:
                        g = self.el(oe, 'guard', 'uml:InteractionConstraint', f'{self.id_de(oe)}.guarda')
                        self.opaca(g, 'specification', sin_corchetes(op['guarda']),
                                   f'{self.id_de(g)}.expr')
                    usadas_cf |= self.items(inter, oe, op['items'], ll_el, base)
                if not usadas_cf:
                    usadas_cf = set(ll_el)
                cf.set('covered', ' '.join(self.id_de(ll_el[x]) for x in sorted(usadas_cf)))
                for x in usadas_cf:
                    self.cubre.setdefault(x, []).append(self.id_de(cf))
                usadas |= usadas_cf
            elif t == 'ref' and not it.get('refersTo'):
                # InteractionUse exige refersTo [1]: sin destino queda como Comment.
                self.comentario(inter, it['texto'], [self.id_de(ll_el[x]) for x in it['lifelines']
                                                     if x in ll_el])
            elif t == 'ref':
                cubiertas = [x for x in it['lifelines'] if x in ll_el]
                iu = self.el(contenedor, 'fragment', 'uml:InteractionUse', f'{base}.ref',
                             name=una_linea(it['texto']),
                             covered=' '.join(self.id_de(ll_el[x]) for x in cubiertas))
                iu.set('_refersTo', it['refersTo'])
                for x in cubiertas:
                    self.cubre.setdefault(x, []).append(self.id_de(iu))
                usadas |= set(cubiertas)
            elif t == 'comment':
                anota = [self.id_de(ll_el[x]) for x in it.get('anota', []) if x in ll_el]
                self.comentario(inter, it['texto'], anota)
            elif t in ('activate', 'deactivate', 'destroy'):
                self.no_validado.append(f'{it["src"]}: {t} no se exporta')
        return usadas

    def mensaje(self, inter, contenedor, it, ll_el, base):
        a, b = ll_el[it['from']], ll_el[it['to']]
        texto = una_linea(it['texto'])
        nombre = texto or it.get('operacion') or it['sort']
        msg = self.el(inter, 'message', 'uml:Message', f'{base}.msg', name=nombre,
                      messageSort=it['sort'])
        mid = self.id_de(msg)
        envio = self.el(contenedor, 'fragment', 'uml:MessageOccurrenceSpecification', f'{mid}.envio',
                        covered=self.id_de(a), message=mid)
        recibo = self.el(contenedor, 'fragment', 'uml:MessageOccurrenceSpecification', f'{mid}.recibo',
                         covered=self.id_de(b), message=mid)
        msg.set('sendEvent', self.id_de(envio))
        msg.set('receiveEvent', self.id_de(recibo))
        if it.get('signature') in self.ops:
            msg.set('signature', self.ops[it['signature']])
        self.cubre.setdefault(it['from'], []).append(self.id_de(envio))
        self.cubre.setdefault(it['to'], []).append(self.id_de(recibo))
        return {it['from'], it['to']}

    def resolver_refs(self):
        por_nombre = {e.get('_inter'): self.id_de(e) for e in self.raiz.iter('packagedElement')
                      if e.get('_inter')}
        for e in self.raiz.iter():
            if e.get('_inter'):
                del e.attrib['_inter']
            r = e.attrib.pop('_refersTo', None)
            if r and r in por_nombre:
                e.set('refersTo', por_nombre[r])

    # ---------------------------------------------------------------- estados
    def maquina(self, padre, maq):
        sm = self.el(padre, 'packagedElement', 'uml:StateMachine', maq['name'], name=maq['name'])
        base = self.id_de(sm)
        region = self.el(sm, 'region', 'uml:Region', f'{base}.region', name='principal')
        vertices = {}
        for e in maq['estados']:
            if e['kind'] == 'state':
                v = self.el(region, 'subvertex', 'uml:State', f'{base}.{e["name"]}', name=e['name'])
                for k in ('entry', 'do', 'exit'):
                    if e[k]:
                        tag = 'doActivity' if k == 'do' else k
                        ob = self.el(v, tag, 'uml:OpaqueBehavior', f'{self.id_de(v)}.{k}',
                                     name=e[k])
                        ET.SubElement(ob, 'language').text = 'Natural'
                        ET.SubElement(ob, 'body').text = e[k]
                textos = ([f'Nombre en el documento: {e["label"]}.'] if e['label'] else []) + \
                    [x['texto'] for x in e['descripciones']]
                if textos:
                    self.comentario(v, '\n'.join(textos), [self.id_de(v)])
            else:
                v = self.el(region, 'subvertex', 'uml:Pseudostate', f'{base}.{e["name"]}',
                            name=e['name'], kind=e['kind'])
            vertices[e['name']] = v
        for t in maq['transiciones']:
            for clave in (t['from'], t['to']):
                if clave.startswith('[*]') and clave not in vertices:
                    if 'fin' in clave:
                        vertices[clave] = self.el(region, 'subvertex', 'uml:FinalState',
                                                  f'{base}.final', name='final')
                    else:
                        vertices[clave] = self.el(region, 'subvertex', 'uml:Pseudostate',
                                                  f'{base}.inicial', name='inicial', kind='initial')
        for t in maq['transiciones']:
            src, dst = vertices[t['from']], vertices[t['to']]
            tr = self.el(region, 'transition', 'uml:Transition', f'{base}.tr',
                         source=self.id_de(src), target=self.id_de(dst), kind='external')
            desde_pseudo = src.get(f'{X}type') == 'uml:Pseudostate' and src.get('kind') == 'initial'
            evento = t['evento']
            if evento and desde_pseudo:
                # UML 2.5.1 (§14): la transición inicial de la región superior no lleva trigger.
                tr.set('name', evento)
                self.comentario(tr, f'Evento de creación: {evento}', [self.id_de(tr)])
            elif evento:
                self.trigger(tr, evento, padre)
            if t['guarda']:
                if desde_pseudo:
                    self.comentario(tr, f'Guarda en la transición inicial: [{t["guarda"]}]',
                                    [self.id_de(tr)])
                else:
                    g = self.el(tr, 'guard', 'uml:Constraint', f'{self.id_de(tr)}.guarda')
                    self.opaca(g, 'specification', t['guarda'], f'{self.id_de(g)}.expr')
            if t['efecto']:
                ob = self.el(tr, 'effect', 'uml:OpaqueBehavior', f'{self.id_de(tr)}.efecto',
                             name=t['efecto'])
                ET.SubElement(ob, 'language').text = 'Natural'
                ET.SubElement(ob, 'body').text = t['efecto']
        for n in maq['notas']:
            anota = [self.id_de(vertices[x]) for x in n['anota'] if x in vertices]
            self.comentario(sm, n['texto'], anota)

    def trigger(self, tr, evento, paquete):
        """Evento con forma op(...) y operación única en el modelo → CallEvent;
        cualquier otro texto → AnyReceiveEvent con ese nombre."""
        m = re.match(r'^\s*([^\s(]+)\s*\(', evento)
        op = None
        if m:
            cands = [v for k, v in self.ops.items() if k.split('.', 1)[1] == m.group(1)]
            op = cands[0] if len(cands) == 1 else None
        clave = (self.id_de(paquete), evento)
        ev = self.eventos.get(clave)
        if ev is None and op:
            ev = self.el(paquete, 'packagedElement', 'uml:CallEvent', f'evento.{m.group(1)}',
                         name=evento, operation=op)
        elif ev is None:
            ev = self.el(paquete, 'packagedElement', 'uml:AnyReceiveEvent', f'evento.{evento}',
                         name=evento)
        self.eventos[clave] = ev
        self.el(tr, 'trigger', 'uml:Trigger', f'{self.id_de(tr)}.trigger', name=evento,
                event=self.id_de(ev))

    # ------------------------------------------------------------ actividades
    def actividad(self, padre, act):
        a = self.el(padre, 'packagedElement', 'uml:Activity', act['name'], name=act['name'])
        base = self.id_de(a)
        particiones = {p: self.el(a, 'group', 'uml:ActivityPartition', f'{base}.{p}', name=p)
                       for p in act['particiones']}
        nodos, en_particion = {}, {}
        for n in act['nodos']:
            e = self.el(a, 'node', f'uml:{n["kind"]}', f'{base}.{n["id"]}',
                        name=una_linea(n['name']) if n['name'] else None)
            nodos[n['id']] = e
            if n['particion'] in particiones:
                e.set('inPartition', self.id_de(particiones[n['particion']]))
                en_particion.setdefault(n['particion'], []).append(self.id_de(e))
        for p, ids in en_particion.items():
            particiones[p].set('node', ' '.join(ids))
        # Activity::partition no es compuesta (subsets group): va como referencia.
        if particiones:
            a.set('partition', ' '.join(self.id_de(e) for e in particiones.values()))
        entrantes, salientes = {}, {}
        for f in act['flujos']:
            cf = self.el(a, 'edge', 'uml:ControlFlow', f'{base}.flujo',
                         source=self.id_de(nodos[f['from']]), target=self.id_de(nodos[f['to']]))
            g = sin_corchetes(f['guarda'])
            if g:
                self.opaca(cf, 'guard', g, f'{self.id_de(cf)}.guarda')
            salientes.setdefault(f['from'], []).append(self.id_de(cf))
            entrantes.setdefault(f['to'], []).append(self.id_de(cf))
        for nid, e in nodos.items():
            if nid in entrantes:
                e.set('incoming', ' '.join(entrantes[nid]))
            if nid in salientes:
                e.set('outgoing', ' '.join(salientes[nid]))
        for n in act['notas']:
            self.comentario(a, n['texto'])


def defaultdict_list():
    return {}


def generar(modelo):
    g = Generador(modelo)
    raiz = g.generar()
    ET.indent(raiz, space=' ')
    return ET.tostring(raiz, encoding='unicode', xml_declaration=False), g
