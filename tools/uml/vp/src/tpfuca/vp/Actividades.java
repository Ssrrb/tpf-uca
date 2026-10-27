package tpfuca.vp;

import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.vp.plugin.ApplicationManager;
import com.vp.plugin.DiagramManager;
import com.vp.plugin.diagram.IDiagramElement;
import com.vp.plugin.diagram.IDiagramUIModel;
import com.vp.plugin.diagram.IShapeTypeConstants;
import com.vp.plugin.diagram.IShapeUIModel;
import com.vp.plugin.diagram.shape.IActivityPartitionHeaderUIModel;
import com.vp.plugin.diagram.shape.IActivitySwimlane2CompartmentUIModel;
import com.vp.plugin.diagram.shape.IActivitySwimlane2NewUIModel;
import com.vp.plugin.model.IActivityPartition;
import com.vp.plugin.model.IActivitySwimlane2;
import com.vp.plugin.model.IControlFlow;
import com.vp.plugin.model.IModelElement;
import com.vp.plugin.model.factory.IModelElementFactory;

/**
 * Diagrama de actividad con carriles verticales, como los arma el editor de VP
 * (ver sample.vpp): un ActivitySwimlane2 que tiene las particiones y los nodos;
 * en el dibujo, una cabecera y un compartimento por partición, y cada nodo
 * dentro del compartimento de su partición, con coordenadas relativas a él.
 *
 * La distribución es propia: cada nodo va a la fila de su distancia más larga
 * desde el inicio (sin contar los flujos que vuelven atrás) y a la columna de
 * su partición.
 */
final class Actividades {
    private static final int X0 = 20, Y0 = 20, CABECERA = 30, MARGEN = 30, SEP_H = 30, SEP_V = 40;
    private static final int ANCHO_MIN_CARRIL = 240;

    private final DiagramManager dm = ApplicationManager.instance().getDiagramManager();
    private final IModelElementFactory fab = IModelElementFactory.instance();
    private final List<String> log;

    Actividades(List<String> log) {
        this.log = log;
    }

    private static final class Nodo {
        String id, tipo, nombre, particion;
        int ancho, alto, rango, x, y;
        IModelElement modelo;
        IDiagramElement forma;
        final List<Nodo> salen = new ArrayList<>(), entran = new ArrayList<>();
    }

    void dibujar(IModelElement paquete, Map<String, Object> a) {
        String nombre = (String) a.get("nombre");
        List<String> particiones = new ArrayList<>();
        for (Object p : Dibujante.lista(a, "particiones")) {
            particiones.add((String) p);
        }
        Map<String, Nodo> nodos = new LinkedHashMap<>();
        for (Object o : Dibujante.lista(a, "nodos")) {
            Map<String, Object> m = Dibujante.mapa(o);
            Nodo n = new Nodo();
            n.id = (String) m.get("id");
            n.tipo = (String) m.get("tipo");
            n.nombre = (String) m.get("nombre");
            n.particion = (String) m.get("particion");
            medir(n);
            nodos.put(n.id, n);
        }
        List<Object> flujos = Dibujante.lista(a, "flujos");
        for (Object o : flujos) {
            Map<String, Object> f = Dibujante.mapa(o);
            Nodo de = nodos.get(f.get("de")), hacia = nodos.get(f.get("a"));
            if (de != null && hacia != null) {
                de.salen.add(hacia);
                hacia.entran.add(de);
            }
        }
        if (particiones.isEmpty()) {
            particiones.add("");
        }
        completarParticiones(nodos.values(), particiones);
        Set<String> vuelta = rangos(nodos);
        int[] anchos = distribuir(nodos.values(), particiones);
        int altoTotal = 0;
        for (Nodo n : nodos.values()) {
            altoTotal = Math.max(altoTotal, n.y + n.alto);
        }
        altoTotal += MARGEN;

        // Modelo
        IActivitySwimlane2 carril = fab.createActivitySwimlane2();
        carril.setName(nombre);
        if (paquete != null) {
            paquete.addChild(carril);
        }
        Map<String, IActivityPartition> parts = new LinkedHashMap<>();
        for (String p : particiones) {
            IActivityPartition ap = fab.createActivityPartition();
            ap.setName(p);
            carril.addChild(ap);
            carril.addVerticalPartition(ap);
            parts.put(p, ap);
        }
        for (Nodo n : nodos.values()) {
            n.modelo = crearNodo(carril, n);
            parts.get(n.particion).addContainedElement(n.modelo);
        }

        // Dibujo
        IDiagramUIModel d = dm.createDiagram(DiagramManager.DIAGRAM_TYPE_ACTIVITY_DIAGRAM);
        d.setName(nombre);
        Dibujante.ubicar(d, paquete, log);
        int anchoTotal = 0;
        for (int w : anchos) {
            anchoTotal += w;
        }
        IDiagramElement forma = dm.createDiagramElement(d, carril);
        forma.setBounds(X0, Y0, anchoTotal, CABECERA + altoTotal);
        List<IShapeUIModel> compartimentos = carriles(d, forma, parts, anchos, altoTotal);

        for (Nodo n : nodos.values()) {
            n.forma = dm.createDiagramElement(d, n.modelo);
            int i = particiones.indexOf(n.particion);
            IShapeUIModel c = compartimentos == null ? null : compartimentos.get(i);
            if (c != null && c.addChild((IShapeUIModel) n.forma)) {
                n.forma.setBounds(n.x, n.y, n.ancho, n.alto);
            } else {
                n.forma.setBounds(X0 + inicio(anchos, i) + n.x, Y0 + CABECERA + n.y, n.ancho, n.alto);
            }
        }
        int k = 0;
        for (Object o : flujos) {
            Map<String, Object> f = Dibujante.mapa(o);
            Nodo de = nodos.get(f.get("de")), hacia = nodos.get(f.get("a"));
            if (de == null || hacia == null) {
                log.add(nombre + ": flujo con nodo desconocido " + f.get("de") + " → " + f.get("a"));
                continue;
            }
            IControlFlow cf = fab.createControlFlow();
            cf.setFrom(de.modelo);
            cf.setTo(hacia.modelo);
            String guarda = (String) f.get("guarda");
            if (guarda != null) {
                cf.setGuard(guarda.replaceAll("^\\[|\\]$", ""));
            }
            Point[] puntos;
            if (vuelta.contains(de.id + ">" + hacia.id)) {
                // Vuelve por el borde derecho del carril para no cruzar los nodos intermedios.
                int id = particiones.indexOf(de.particion), ia = particiones.indexOf(hacia.particion);
                int xd = X0 + inicio(anchos, id) + de.x + de.ancho;
                int xa = X0 + inicio(anchos, ia) + hacia.x + hacia.ancho;
                int xr = X0 + inicio(anchos, Math.max(id, ia)) + anchos[Math.max(id, ia)] - 10 - 6 * (k++ % 4);
                int yd = Y0 + CABECERA + de.y + de.alto / 2, ya = Y0 + CABECERA + hacia.y + hacia.alto / 2;
                puntos = new Point[] {new Point(xd, yd), new Point(xr, yd), new Point(xr, ya), new Point(xa, ya)};
            } else {
                puntos = new Point[] {centro(de, anchos, particiones), centro(hacia, anchos, particiones)};
            }
            try {
                dm.createConnector(d, cf, de.forma, hacia.forma, puntos);
            } catch (RuntimeException ex) {
                log.add(nombre + ": no pude dibujar el flujo " + de.id + " → " + hacia.id + ": " + ex);
            }
        }
        log.add(nombre + ": " + particiones.size() + " carriles, " + nodos.size() + " nodos, " + flujos.size()
            + " flujos");
    }

    /**
     * Cabeceras y compartimentos de los carriles. VP los crea solo cuando el
     * carril se dibuja con el editor; si al crear la forma no aparecen, se arman
     * como en sample.vpp. Devuelve los compartimentos en el orden de las particiones.
     */
    private List<IShapeUIModel> carriles(IDiagramUIModel d, IDiagramElement forma, Map<String, IActivityPartition> parts,
                                         int[] anchos, int alto) {
        String nombre = d.getName();
        log.add(nombre + ": forma del carril " + forma.getClass().getName() + " con " + forma.childrenCount()
            + " hijos");
        Map<IModelElement, IShapeUIModel> cabeceras = new HashMap<>();
        List<IShapeUIModel> comps = new ArrayList<>();
        for (IShapeUIModel h : forma.toChildArray()) {
            if (h instanceof IActivityPartitionHeaderUIModel) {
                cabeceras.put(h.getMetaModelElement(), h);
            } else if (h instanceof IActivitySwimlane2CompartmentUIModel) {
                comps.add(h);
            }
        }
        if (!(forma instanceof IActivitySwimlane2NewUIModel)) {
            log.add(nombre + ": la forma del carril no es IActivitySwimlane2NewUIModel; nodos sin carril");
            return null;
        }
        IActivitySwimlane2NewUIModel sl = (IActivitySwimlane2NewUIModel) forma;
        if (cabeceras.size() == parts.size() && comps.size() == parts.size()) {
            log.add(nombre + ": VP creó cabeceras y compartimentos");
            List<IShapeUIModel> orden = new ArrayList<>();
            String[] ids = sl.getVerticalPartitionIds();
            for (String id : ids) {
                for (IShapeUIModel c : comps) {
                    if (id.equals(((IActivitySwimlane2CompartmentUIModel) c).getVerticalPartitionId())) {
                        orden.add(c);
                    }
                }
            }
            if (orden.size() == parts.size()) {
                int x = 0, i = 0;
                for (IShapeUIModel c : orden) {
                    c.setBounds(x, CABECERA, anchos[i], alto);
                    x += anchos[i++];
                }
                return orden;
            }
            log.add(nombre + ": no pude ordenar los compartimentos de VP; armo los míos");
        }
        List<String> idsCab = new ArrayList<>(), idsComp = new ArrayList<>();
        List<IShapeUIModel> out = new ArrayList<>();
        int x = 0, i = 0;
        for (IActivityPartition p : parts.values()) {
            IShapeUIModel h = cabeceras.get(p);
            if (h == null) {
                h = (IShapeUIModel) dm.createDiagramElement(d, IShapeTypeConstants.SHAPE_TYPE_ACTIVITY_PARTITION_HEADER);
                h.setMetaModelElement(p);
                forma.addChild(h);
            }
            if (h instanceof IActivityPartitionHeaderUIModel) {
                ((IActivityPartitionHeaderUIModel) h).setHorizontal(false);
                ((IActivityPartitionHeaderUIModel) h).setSwimlane(sl);
            }
            h.setBounds(x, 0, anchos[i], CABECERA);
            IShapeUIModel c = (IShapeUIModel) dm.createDiagramElement(d,
                IShapeTypeConstants.SHAPE_TYPE_ACTIVITY_SWIMLANE2_COMPARTMENT);
            forma.addChild(c);
            ((IActivitySwimlane2CompartmentUIModel) c).setVerticalPartitionId(h.getId());
            c.setBounds(x, CABECERA, anchos[i], alto);
            idsCab.add(h.getId());
            idsComp.add(c.getId());
            out.add(c);
            x += anchos[i++];
        }
        sl.setVerticalPartitionIds(idsCab.toArray(new String[0]));
        sl.setCompartmentIds(idsComp.toArray(new String[0]));
        log.add(nombre + ": armé " + out.size() + " cabeceras y compartimentos");
        return out;
    }

    private IModelElement crearNodo(IActivitySwimlane2 c, Nodo n) {
        IModelElement m;
        switch (n.tipo) {
            case "InitialNode": m = c.createInitialNode(); break;
            case "ActivityFinalNode": m = c.createActivityFinalNode(); break;
            case "FlowFinalNode": m = c.createFlowFinalNode(); break;
            case "DecisionNode": m = c.createDecisionNode(); break;
            case "MergeNode": m = c.createMergeNode(); break;
            case "ForkNode": m = c.createForkNode(); break;
            case "JoinNode": m = c.createJoinNode(); break;
            default: m = c.createActivityAction();
        }
        if (n.nombre != null) {
            m.setName(n.nombre);
        }
        return m;
    }

    private static void medir(Nodo n) {
        switch (n.tipo) {
            case "InitialNode":
            case "ActivityFinalNode":
            case "FlowFinalNode":
                n.ancho = n.alto = 20;
                return;
            case "DecisionNode":
            case "MergeNode":
                n.ancho = n.alto = 30;
                return;
            case "ForkNode":
            case "JoinNode":
                n.ancho = 80;
                n.alto = 8;
                return;
            default:
                String[] lineas = (n.nombre == null ? "" : n.nombre).split("\n");
                int largo = 0;
                for (String l : lineas) {
                    largo = Math.max(largo, l.length());
                }
                n.ancho = Math.max(100, Math.min(300, largo * 7 + 24));
                n.alto = 18 * lineas.length + 22;
        }
    }

    /** Nodos sin partición (p. ej. una decisión en el borde): toman la de su vecino. */
    private static void completarParticiones(Iterable<Nodo> nodos, List<String> particiones) {
        boolean cambio = true;
        while (cambio) {
            cambio = false;
            for (Nodo n : nodos) {
                if (n.particion != null && particiones.contains(n.particion)) {
                    continue;
                }
                for (List<Nodo> vecinos : List.of(n.entran, n.salen)) {
                    for (Nodo v : vecinos) {
                        if (v.particion != null && particiones.contains(v.particion)) {
                            n.particion = v.particion;
                            cambio = true;
                            break;
                        }
                    }
                    if (cambio) {
                        break;
                    }
                }
            }
        }
        for (Nodo n : nodos) {
            if (n.particion == null || !particiones.contains(n.particion)) {
                n.particion = particiones.get(0);
            }
        }
    }

    /** Fila de cada nodo: camino más largo desde el inicio sin los flujos de vuelta, que devuelve. */
    private static Set<String> rangos(Map<String, Nodo> nodos) {
        Set<String> vuelta = new HashSet<>();
        Set<Nodo> visto = new HashSet<>(), pila = new HashSet<>();
        List<Nodo> orden = new ArrayList<>();
        List<Nodo> raices = new ArrayList<>();
        for (Nodo n : nodos.values()) {
            if ("InitialNode".equals(n.tipo)) {
                raices.add(n);
            }
        }
        raices.addAll(nodos.values());
        for (Nodo r : raices) {
            dfs(r, visto, pila, orden, vuelta);
        }
        java.util.Collections.reverse(orden);
        for (Nodo n : orden) {
            for (Nodo s : n.salen) {
                if (!vuelta.contains(n.id + ">" + s.id)) {
                    s.rango = Math.max(s.rango, n.rango + 1);
                }
            }
        }
        return vuelta;
    }

    private static void dfs(Nodo n, Set<Nodo> visto, Set<Nodo> pila, List<Nodo> orden, Set<String> vuelta) {
        if (!visto.add(n)) {
            return;
        }
        pila.add(n);
        for (Nodo s : n.salen) {
            if (pila.contains(s)) {
                vuelta.add(n.id + ">" + s.id);
            } else {
                dfs(s, visto, pila, orden, vuelta);
            }
        }
        pila.remove(n);
        orden.add(n);
    }

    /** Posición de cada nodo relativa a su compartimento; devuelve el ancho de cada carril. */
    private static int[] distribuir(Iterable<Nodo> nodos, List<String> particiones) {
        Map<Integer, List<Nodo>> filas = new java.util.TreeMap<>();
        for (Nodo n : nodos) {
            filas.computeIfAbsent(n.rango, k -> new ArrayList<>()).add(n);
        }
        int[] anchos = new int[particiones.size()];
        java.util.Arrays.fill(anchos, ANCHO_MIN_CARRIL);
        for (List<Nodo> fila : filas.values()) {
            int[] uso = new int[particiones.size()];
            for (Nodo n : fila) {
                int i = particiones.indexOf(n.particion);
                uso[i] += (uso[i] == 0 ? 0 : SEP_H) + n.ancho;
            }
            for (int i = 0; i < uso.length; i++) {
                anchos[i] = Math.max(anchos[i], uso[i] + 2 * MARGEN);
            }
        }
        int y = MARGEN;
        for (List<Nodo> fila : filas.values()) {
            int alto = 0;
            int[] uso = new int[particiones.size()];
            for (Nodo n : fila) {
                int i = particiones.indexOf(n.particion);
                uso[i] += (uso[i] == 0 ? 0 : SEP_H) + n.ancho;
                alto = Math.max(alto, n.alto);
            }
            int[] x = new int[particiones.size()];
            for (int i = 0; i < x.length; i++) {
                x[i] = (anchos[i] - uso[i]) / 2;
            }
            for (Nodo n : fila) {
                int i = particiones.indexOf(n.particion);
                n.x = x[i];
                n.y = y + (alto - n.alto) / 2;
                x[i] += n.ancho + SEP_H;
            }
            y += alto + SEP_V;
        }
        return anchos;
    }

    private static int inicio(int[] anchos, int i) {
        int x = 0;
        for (int j = 0; j < i; j++) {
            x += anchos[j];
        }
        return x;
    }

    private static Point centro(Nodo n, int[] anchos, List<String> particiones) {
        return new Point(X0 + inicio(anchos, particiones.indexOf(n.particion)) + n.x + n.ancho / 2,
            Y0 + CABECERA + n.y + n.alto / 2);
    }
}
