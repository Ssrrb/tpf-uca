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
 * y mensajes que llaman a la operación importada cuando existe.
 */
final class Dibujante {
    private final DiagramManager dm = ApplicationManager.instance().getDiagramManager();
    private final IModelElementFactory fab = IModelElementFactory.instance();
    private final IProject proyecto = ApplicationManager.instance().getProjectManager().getProject();
    private final Map<String, List<IModelElement>> porNombre = new HashMap<>();
    final List<String> log = new ArrayList<>();

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
    }

    // ------------------------------------------------------------ clases

    private void clases(String cu, IModelElement paquete, Map<String, Object> cu_) {
        IDiagramUIModel d = dm.createDiagram(DiagramManager.DIAGRAM_TYPE_CLASS_DIAGRAM);
        d.setName(cu + " clases");
        ubicar(d, paquete);
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
        dm.layout(d, DiagramManager.LAYOUT_AUTO);
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

    private void secuencia(IModelElement paquete, Map<String, Object> s) {
        sd = (IInteractionDiagramUIModel) dm.createDiagram(DiagramManager.DIAGRAM_TYPE_INTERACTION_DIAGRAM);
        String nombre = (String) s.get("nombre");
        sd.setName(nombre);
        ubicar(sd, paquete);
        sd.setAutoExtendActivations(false);
        sd.setShowActivations(false);
        IFrame raiz = sd.getRootFrame(true);
        lifelines.clear();
        columna.clear();
        formasLl.clear();
        numero = 0;
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
        m.setSequenceNumber(String.valueOf(++numero));
        m.setFrom(de);
        m.setTo(a);
        String clase = (String) it.get("clase");
        if ("reply".equals(clase)) {
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
            usadas.addAll(items(raiz, operando, lista(op, "items"), nivel + 1));
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
    private void ubicar(IDiagramUIModel d, IModelElement paquete) {
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
