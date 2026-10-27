package tpfuca.vp;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.vp.plugin.ApplicationManager;
import com.vp.plugin.ViewManager;
import com.vp.plugin.action.VPAction;
import com.vp.plugin.action.VPActionController;

/** Pide qué CU dibujar (o "todos") y arma sus diagramas. */
public class DibujarAccion implements VPActionController {
    @Override
    public void performAction(VPAction accion) {
        ViewManager vm = ApplicationManager.instance().getViewManager();
        try {
            File datos = new File(Plugin.carpeta, "vp-diagramas.json");
            Map<String, Object> raiz = Dibujante.mapa(Json.leer(
                new String(Files.readAllBytes(datos.toPath()), StandardCharsets.UTF_8)));
            List<Object> cus = Dibujante.lista(raiz, "cus");
            String pedido = (String) vm.showInputDialog(vm.getRootFrame(),
                "CU a dibujar (por ejemplo CU-01), o \"todos\":", "Dibujar CU", 3, null, null, "CU-01");
            if (pedido == null || pedido.trim().isEmpty()) {
                return;
            }
            pedido = pedido.trim().toUpperCase();
            Dibujante d = new Dibujante();
            List<String> hechos = new ArrayList<>();
            for (Object o : cus) {
                Map<String, Object> cu = Dibujante.mapa(o);
                if ("TODOS".equals(pedido) || pedido.equals(cu.get("cu"))) {
                    d.dibujar(cu);
                    hechos.add((String) cu.get("cu"));
                }
            }
            if (hechos.isEmpty()) {
                vm.showMessageDialog(vm.getRootFrame(), "No hay datos para " + pedido + ".");
                return;
            }
            String informe = String.join("\n", d.log);
            Files.write(new File(Plugin.carpeta, "ultimo-dibujo.txt").toPath(),
                informe.getBytes(StandardCharsets.UTF_8));
            for (String linea : d.log) {
                vm.showMessage(linea, "tpfuca");
            }
            vm.showMessageDialog(vm.getRootFrame(), "Dibujados: " + String.join(", ", hechos)
                + "\n\n" + informe);
        } catch (Exception e) {
            vm.showMessageDialog(vm.getRootFrame(), "Error al dibujar: " + e);
            e.printStackTrace();
        }
    }

    @Override
    public void update(VPAction accion) {
    }
}
