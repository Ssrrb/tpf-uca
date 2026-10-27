package tpfuca.vp;

import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.vp.plugin.ApplicationManager;
import com.vp.plugin.DiagramManager;
import com.vp.plugin.diagram.IDiagramElement;
import com.vp.plugin.diagram.IDiagramUIModel;
import com.vp.plugin.diagram.IInteractionDiagramUIModel;
import com.vp.plugin.model.IActivation;
import com.vp.plugin.model.ICombinedFragment;
import com.vp.plugin.model.IFrame;
import com.vp.plugin.model.IInteractionActor;
import com.vp.plugin.model.IInteractionConstraint;
import com.vp.plugin.model.IInteractionLifeLine;
import com.vp.plugin.model.IInteractionOccurrence;
import com.vp.plugin.model.IInteractionOperand;
import com.vp.plugin.model.IMessage;
import com.vp.plugin.model.IModelElement;
import com.vp.plugin.model.INOTE;
import com.vp.plugin.model.IProject;
import com.vp.plugin.model.IRelationship;
import com.vp.plugin.model.IRelationshipEnd;
import com.vp.plugin.model.factory.IModelElementFactory;

/**
 * Arma los diagramas de un CU sobre el modelo importado del XMI.
 *
 * Clases: dibuja las clases importadas (buscadas por nombre) y las relaciones
 * que ya existen entre ellas; no crea elementos de modelo.
 * Secuencia: VP solo dibuja interacciones creadas con su propio editor, así que
 * se arma una nueva con lifelines cuyo clasificador base es la clase importada,
 * mensajes numerados como los numera VP y barras de activación.
 * Actividad: ver {@link Actividades}.
 */
final class Dibujante {
    private final DiagramManager dm = ApplicationManager.instance().getDiagramManager();
    private final IModelElementFactory fab = IModelElementFactory.instance();
    private final IProject proyecto = ApplicationManager.instance().getProjectManager().getProject();
    private final Map<String, List<IModelElement>> porNombre = new HashMap<>();
    final List<String> log = new ArrayList<>();
    /** Diagramas armados en esta corrida, para el informe. */
    static final List<IDiagramUIModel> creados = new ArrayList<>();

    Dibujante() {
        for (IModelElement e : proyecto.toAllLevelModelElementArray()) {
            if (e.getName() != null) {
                porNombre.computeIfAbsent(e.getName() + "|" + e.getModelType(), k -> new ArrayList<>()).add(e);
            }
        }
    }

    void dibujar(Map<String, Object> cu) {
        String nombre = (String) cu.get("cu");
        IModelElement paquete = paqueteDe(nombre);
        if (!lista(cu, "clases").isEmpty()) {
            clases(nombre, paquete, cu);
        }
        for (Object s : lista(cu, "secuencias")) {
            secuencia(paquete, mapa(s));
        }
        for (Object a : lista(cu, "actividades")) {
            try {
                new Actividades(log).dibujar(paquete, mapa(a));
            } catch (RuntimeException ex) {
                log.add(nombre + ": falló la actividad " + mapa(a).get("nombre") + ": " + ex);
            }
        }
    }

    // ------------------------------------------------------------ clases

    private void clases(String cu, IModelElement paquete, Map<String, Object> cu_) {
        IDiagramUIModel d = dm.createDiagram(DiagramManager.DIAGRAM_TYPE_CLASS_DIAGRAM);
        d.setName(cu + " clases");
        ubicar(d, paquete, log);
        Map<IModelElement, IDiagramElement> formas = new LinkedHashMap<>();
        for (Object o : lista(cu_, "clases")) {
            Map<String, Object> c = mapa(o);
            IModelElement e = buscar((String) c.get("nombre"), IModelElementFactory.MODEL_TYPE_CLASS,
                (String) c.get("paquete"));
            if (e == null) {
                log.add(cu + ": no encontré la clase " + c.get("nombre"));
                continue;
            }
            formas.put(e, dm.createDiagramElement(d, e));
        }
        Set<IModelElement> dibujadas = new LinkedHashSet<>();
        for (IModelElement e : formas.keySet()) {
            for (IModelElement r : relaciones(e)) {
                if (!dibujadas.add(r)) {
                    continue;
                }
                IModelElement[] ext = extremos(r);
                if (ext == null || !formas.containsKey(ext[0]) || !formas.containsKey(ext[1])) {
                    continue;
                }
                try {
                    dm.createConnector(d, r, formas.get(ext[0]), formas.get(ext[1]), null);
                } catch (RuntimeException ex) {
                    log.add(cu + ": no pude dibujar la relación " + r.getName() + ": " + ex);
                }
            }
        }
        // Jerárquico: las generalizaciones y composiciones quedan de arriba hacia abajo.
        dm.layout(d, DiagramManager.LAYOUT_HIERARCHIC);
        log.add(cu + " clases: " + formas.size() + " clases");
    }

    private List<IModelElement> relaciones(IModelElement e) {
        List<IModelElement> out = new ArrayList<>();
        for (IRelationship r : e.toFromRelationshipArray()) {
            out.add(r);
        }
        for (IRelationship r : e.toToRelationshipArray()) {
            out.add(r);
        }
        for (IRelationshipEnd x : e.toFromRelationshipEndArray()) {
            out.add(x.getEndRelationship());
        }
        for (IRelationshipEnd x : e.toToRelationshipEndArray()) {
            out.add(x.getEndRelationship());
        }
        return out;
    }

    private IModelElement[] extremos(IModelElement r) {
        if (r instanceof com.vp.plugin.model.IEndRelationship) {
            com.vp.plugin.model.IEndRelationship er = (com.vp.plugin.model.IEndRelationship) r;
            return new IModelElement[] {er.getFromEnd().getModelElement(), er.getToEnd().getModelElement()};
        }
        if (r instanceof IRelationship) {
            return new IModelElement[] {((IRelationship) r).getFrom(), ((IRelationship) r).getTo()};
        }
        return null;
    }

    // ------------------------------------------------------------ secuencia
    //
    // Geometría propia: el auto-layout de VP apila las lifelines y reordena los
    // mensajes. Cada lifeline es una columna y cada mensaje una fila; los
    // fragmentos y las refs se dibujan como recuadros que abarcan sus filas.

    private static final int X0 = 40, ANCHO_COL = 190, ANCHO_LL = 130, Y_LL = 40, CABEZA = 50;
    private static final int FILA = 34, MARGEN_FRAG = 12;

    private IInteractionDiagramUIModel sd;
    private final Map<String, IModelElement> lifelines = new HashMap<>();
    private final Map<IModelElement, Integer> columna = new HashMap<>();
    private final Map<IModelElement, IDiagramElement> formasLl = new HashMap<>();
    private int numero;
    private int y;

    /** Llamada en curso: la lifeline que la atiende, su número, cuántos mensajes salieron de ella y su tramo. */
    private static final class Marco {
        final IModelElement ll;
        final String num;
        final int desde;
        int hijos;
        int hasta = -1;

        Marco(IModelElement ll, String num, int desde) {
            this.ll = ll;
            this.num = num;
            this.desde = desde;
        }
    }

    private final java.util.ArrayDeque<Marco> pila = new java.util.ArrayDeque<>();
    private final List<Marco> marcos = new ArrayList<>();
    /** Mensaje, emisor, receptor y fila: las activaciones se asignan al final, cuando se conocen las barras. */
    private final List<Object[]> extremos = new ArrayList<>();
    private int primeros;

    private void secuencia(IModelElement paquete, Map<String, Object> s) {
        sd = (IInteractionDiagramUIModel) dm.createDiagram(DiagramManager.DIAGRAM_TYPE_INTERACTION_DIAGRAM);
        String nombre = (String) s.get("nombre");
        sd.setName(nombre);
        ubicar(sd, paquete, log);
        sd.setAutoExtendActivations(false);
        sd.setShowActivations(true);
        IFrame raiz = sd.getRootFrame(true);
        lifelines.clear();
        columna.clear();
        formasLl.clear();
        numero = 0;
        primeros = 0;
        pila.clear();
        marcos.clear();
        extremos.clear();
        int alto = CABEZA + FILA * (filas(lista(s, "items")) + 2);
        int i = 0;
        for (Object o : lista(s, "lifelines")) {
            Map<String, Object> l = mapa(o);
            IModelElement m;
            if (Boolean.TRUE.equals(l.get("actor"))) {
                IInteractionActor a = fab.createInteractionActor();
                raiz.addChild(a);
                a.setName((String) l.get("nombre"));
                m = a;
            } else {
                IInteractionLifeLine ll = fab.createInteractionLifeLine();
                raiz.addChild(ll);
                ll.setName((String) l.get("nombre"));
                IModelElement base = buscar((String) l.get("tipo"), IModelElementFactory.MODEL_TYPE_CLASS, null);
                if (base != null) {
                    ll.setBaseClassifier(base);
                } else {
                    log.add(nombre + ": lifeline " + l.get("nombre") + " sin clase " + l.get("tipo"));
                }
                m = ll;
            }
            lifelines.put((String) l.get("alias"), m);
            columna.put(m, i);
            IDiagramElement f = dm.createDiagramElement(sd, m);
            f.setBounds(X0 + i * ANCHO_COL, Y_LL, ANCHO_LL, alto);
            formasLl.put(m, f);
            i++;
        }
        y = Y_LL + CABEZA + FILA;
        items(raiz, null, lista(s, "items"), 0);
        activaciones(y - FILA / 2);
        dm.openDiagram(sd);
        log.add(nombre + ": " + lifelines.size() + " lifelines, " + numero + " mensajes");
    }

    /** Filas que ocupa una lista de ítems, para dar a las lifelines el largo justo. */
    private int filas(List<Object> items) {
        int n = 0;
        for (Object o : items) {
            Map<String, Object> it = mapa(o);
            String tipo = (String) it.get("tipo");
            if ("fragmento".equals(tipo)) {
                for (Object op : lista(it, "operandos")) {
                    n += 1 + filas(lista(mapa(op), "items"));
                }
                n += 1;
            } else if ("mensaje".equals(tipo) && it.get("de") != null && it.get("de").equals(it.get("a"))) {
                n += 2;
            } else {
                n += "ref".equals(tipo) ? 2 : 1;
            }
        }
        return n;
    }

    private int centro(IModelElement l) {
        return X0 + columna.get(l) * ANCHO_COL + ANCHO_LL / 2;
    }

    /** Agrega los ítems a `raiz` (nivel superior) o a `operando`; devuelve las lifelines usadas. */
    private Set<IModelElement> items(IFrame raiz, IInteractionOperand operando, List<Object> items, int nivel) {
        Set<IModelElement> usadas = new LinkedHashSet<>();
        for (Object o : items) {
            Map<String, Object> it = mapa(o);
            String tipo = (String) it.get("tipo");
            if ("mensaje".equals(tipo)) {
                IMessage m = mensaje(it);
                if (m != null) {
                    usadas.add(m.getFrom());
                    usadas.add(m.getTo());
                    if (operando != null) {
                        operando.addMessage(m);
                    }
                }
            } else if ("fragmento".equals(tipo)) {
                usadas.addAll(fragmento(raiz, operando, it, nivel));
            } else if ("ref".equals(tipo)) {
                IInteractionOccurrence ref = fab.createInteractionOccurrence();
                if (operando != null) {
                    operando.addInteractionOccurrence(ref);
                } else {
                    raiz.addChild(ref);
                }
                ref.setName((String) it.get("texto"));
                List<IModelElement> cub = new ArrayList<>();
                for (Object a : lista(it, "lifelines")) {
                    IModelElement l = lifelines.get(a);
                    if (l != null) {
                        ref.addCoveredLifeLine(l);
                        cub.add(l);
                    }
                }
                if (!cub.isEmpty()) {
                    int[] xs = rango(cub, nivel);
                    dm.createDiagramElement(sd, ref).setBounds(xs[0], y - FILA / 2, xs[1] - xs[0], FILA * 3 / 2);
                }
                y += FILA * 2;
                usadas.addAll(cub);
            } else if ("nota".equals(tipo)) {
                INOTE n = fab.createNOTE();
                n.setDescription((String) it.get("texto"));
                dm.createDiagramElement(sd, n).setBounds(X0 + lifelines.size() * ANCHO_COL, y - FILA / 2, 240, FILA);
                y += FILA;
            }
        }
        return usadas;
    }

    private IMessage mensaje(Map<String, Object> it) {
        IModelElement de = lifelines.get(it.get("de"));
        IModelElement a = lifelines.get(it.get("a"));
        if (de == null || a == null) {
            log.add(sd.getName() + ": mensaje sin lifeline: " + it.get("texto"));
            return null;
        }
        IMessage m = fab.createMessage();
        // El texto de PlantUML tal cual: con ActionTypeCall VP mostraría la firma
        // tipada de la operación en lugar del mensaje con sus argumentos.
        m.setName((String) it.get("texto"));
        numero++;
        m.setFrom(de);
        m.setTo(a);
        String clase = (String) it.get("clase");
        boolean respuesta = "reply".equals(clase);
        // Numeración anidada como la de VP (1, 1.1, 1.1.1): un mensaje cuelga de la
        // llamada que está atendiendo quien lo envía, y la respuesta es el último
        // mensaje de la llamada que responde (así numera VP el return en sample.vpp).
        // Las llamadas que quien envía ya no atiende se dan por terminadas.
        while (!pila.isEmpty() && pila.peekLast().ll != de) {
            pila.removeLast().hasta = y - FILA / 3;
        }
        if (pila.isEmpty()) {
            Marco inicial = new Marco(de, null, y);
            marcos.add(inicial);
        }
        Marco padre = pila.peekLast();
        String num = padre == null ? String.valueOf(++primeros) : padre.num + "." + (++padre.hijos);
        m.setSequenceNumber(num);
        if (respuesta && padre != null) {
            pila.removeLast().hasta = y;
        } else if (!respuesta && de != a) {
            Marco f = new Marco(a, num, y);
            pila.addLast(f);
            marcos.add(f);
        }
        extremos.add(new Object[] {m, de, a, y});
        if (respuesta) {
            m.setActionType(fab.createActionTypeReturn());
        } else if ("createMessage".equals(clase)) {
            m.setType(IMessage.TYPE_CREATE_MESSAGE);
            m.setActionType(fab.createActionTypeCreate());
        } else if (de == a) {
            m.setType(IMessage.TYPE_SELF_MESSAGE);
        }
        Point[] puntos = de == a
            ? new Point[] {new Point(centro(de), y), new Point(centro(de), y + FILA / 2)}
            : new Point[] {new Point(centro(de), y), new Point(centro(a), y)};
        dm.createConnector(sd, m, formasLl.get(de), formasLl.get(a), puntos);
        y += de == a ? FILA * 2 : FILA;
        return m;
    }

    /**
     * Barras de activación: por lifeline, la unión de los tramos de las llamadas
     * que atendió (y del tramo inicial de quien arranca la interacción). Cada
     * mensaje sale de la barra del emisor y llega a la del receptor en su fila.
     */
    private void activaciones(int fin) {
        for (Marco f : pila) {
            f.hasta = fin;
        }
        pila.clear();
        Map<IModelElement, List<int[]>> tramos = new LinkedHashMap<>();
        Set<IModelElement> iniciales = new java.util.HashSet<>();
        for (Marco f : marcos) {
            if (!(f.ll instanceof IInteractionLifeLine)) {
                continue;
            }
            if (f.num == null) {
                if (!iniciales.add(f.ll)) {
                    continue;
                }
                f.hasta = fin;
            }
            int hasta = f.hasta < 0 ? fin : f.hasta;
            tramos.computeIfAbsent(f.ll, k -> new ArrayList<>()).add(new int[] {f.desde - FILA / 4, hasta});
        }
        Map<IModelElement, List<Object[]>> barras = new HashMap<>();
        for (Map.Entry<IModelElement, List<int[]>> e : tramos.entrySet()) {
            List<int[]> l = e.getValue();
            l.sort((p, q) -> Integer.compare(p[0], q[0]));
            List<int[]> unidos = new ArrayList<>();
            for (int[] t : l) {
                int[] u = unidos.isEmpty() ? null : unidos.get(unidos.size() - 1);
                if (u != null && t[0] <= u[1] + FILA / 2) {
                    u[1] = Math.max(u[1], t[1]);
                } else {
                    unidos.add(new int[] {t[0], t[1]});
                }
            }
            for (int[] u : unidos) {
                try {
                    IActivation act = fab.createActivation();
                    ((IInteractionLifeLine) e.getKey()).addActivation(act);
                    dm.createDiagramElement(sd, act).setBounds(centro(e.getKey()) - 4, u[0], 8, Math.max(12, u[1] - u[0]));
                    barras.computeIfAbsent(e.getKey(), k -> new ArrayList<>()).add(new Object[] {act, u});
                } catch (RuntimeException ex) {
                    log.add(sd.getName() + ": no pude dibujar una activación de " + e.getKey().getName() + ": " + ex);
                }
            }
        }
        for (Object[] x : extremos) {
            IMessage m = (IMessage) x[0];
            int fila = (Integer) x[3];
            try {
                IActivation de = barraEn(barras.get(x[1]), fila), a = barraEn(barras.get(x[2]), fila);
                if (de != null) {
                    m.setFromActivation(de);
                }
                if (a != null) {
                    m.setToActivation(a);
                }
            } catch (RuntimeException ex) {
                log.add(sd.getName() + ": activación del mensaje " + m.getSequenceNumber() + ": " + ex);
            }
        }
    }

    private static IActivation barraEn(List<Object[]> barras, int fila) {
        if (barras == null) {
            return null;
        }
        for (Object[] b : barras) {
            int[] u = (int[]) b[1];
            if (u[0] <= fila && fila <= u[1]) {
                return (IActivation) b[0];
            }
        }
        return null;
    }

    private Set<IModelElement> fragmento(IFrame raiz, IInteractionOperand padre, Map<String, Object> it, int nivel) {
        ICombinedFragment cf = fab.createCombinedFragment();
        if (padre != null) {
            padre.addCombinedFragment(cf);
        } else {
            raiz.addCombinedFragment(cf);
        }
        cf.setInteractionOperator((String) it.get("operador"));
        int arriba = y - FILA / 2;
        y += FILA / 2;
        Set<IModelElement> usadas = new LinkedHashSet<>();
        for (Object o : lista(it, "operandos")) {
            Map<String, Object> op = mapa(o);
            IInteractionOperand operando = cf.createInteractionOperand();
            String guarda = (String) op.get("guarda");
            if (guarda != null) {
                IInteractionConstraint g = fab.createInteractionConstraint();
                g.setConstraint(guarda);
                operando.setGuard(g);
            }
            y += FILA / 2;
            // Cada operando arranca con las llamadas que había al entrar al fragmento:
            // una respuesta dentro de un break o de una rama del alt no termina la
            // llamada para lo que sigue después.
            List<Marco> antes = new ArrayList<>(pila);
            usadas.addAll(items(raiz, operando, lista(op, "items"), nivel + 1));
            for (Marco f : pila) {
                if (!antes.contains(f)) {
                    f.hasta = y - FILA / 3;
                }
            }
            pila.clear();
            pila.addAll(antes);
            for (Marco f : antes) {
                f.hasta = -1;
            }
        }
        usadas.remove(null);
        for (IModelElement l : usadas) {
            cf.addCoveredLifeLine(l);
        }
        if (!usadas.isEmpty()) {
            int[] xs = rango(usadas, nivel);
            dm.createDiagramElement(sd, cf).setBounds(xs[0], arriba, xs[1] - xs[0], y - arriba);
        }
        y += FILA;
        return usadas;
    }

    /** Extremos horizontales de un recuadro que cubre estas lifelines, con sangría por anidamiento. */
    private int[] rango(java.util.Collection<IModelElement> ls, int nivel) {
        int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
        for (IModelElement l : ls) {
            min = Math.min(min, columna.get(l));
            max = Math.max(max, columna.get(l));
        }
        int sangria = MARGEN_FRAG * (4 - Math.min(nivel, 3));
        return new int[] {X0 + min * ANCHO_COL + ANCHO_LL / 2 - 20 - sangria,
            X0 + max * ANCHO_COL + ANCHO_LL / 2 + 20 + sangria};
    }

    // ------------------------------------------------------------ utilidades

    private IModelElement paqueteDe(String cu) {
        for (IModelElement p : porNombre.getOrDefault(cu + "|" + IModelElementFactory.MODEL_TYPE_PACKAGE,
                new ArrayList<>())) {
            return p;
        }
        log.add("No encontré el paquete " + cu + ": los diagramas quedan en la raíz.");
        return null;
    }

    /** Pone el diagrama dentro del paquete del CU: en VP, un diagrama cuelga del elemento que lo tiene como subdiagrama. */
    static void ubicar(IDiagramUIModel d, IModelElement paquete, List<String> log) {
        creados.add(d);
        if (paquete == null) {
            return;
        }
        try {
            paquete.addSubDiagram(d);
        } catch (RuntimeException ex) {
            log.add("No pude ubicar " + d.getName() + " en " + paquete.getName() + ": " + ex);
        }
    }

    private IModelElement buscar(String nombre, String tipo, String paquete) {
        if (nombre == null) {
            return null;
        }
        List<IModelElement> l = porNombre.get(nombre + "|" + tipo);
        if (l == null || l.isEmpty()) {
            return null;
        }
        if (paquete != null) {
            for (IModelElement e : l) {
                if (e.getParent() != null && paquete.equals(e.getParent().getName())) {
                    return e;
                }
            }
        }
        return l.get(0);
    }

    @SuppressWarnings("unchecked")
    static Map<String, Object> mapa(Object o) {
        return (Map<String, Object>) o;
    }

    @SuppressWarnings("unchecked")
    static List<Object> lista(Map<String, Object> m, String k) {
        Object v = m.get(k);
        return v == null ? new ArrayList<>() : (List<Object>) v;
    }
}
