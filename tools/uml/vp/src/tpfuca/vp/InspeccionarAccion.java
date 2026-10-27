package tpfuca.vp;

import java.io.File;
import java.util.List;

import com.vp.plugin.ApplicationManager;
import com.vp.plugin.ViewManager;
import com.vp.plugin.action.VPAction;
import com.vp.plugin.action.VPActionController;
import com.vp.plugin.diagram.IDiagramUIModel;

/** Vuelca la estructura del diagrama abierto, para aprender cómo lo guarda el editor de VP. */
public class InspeccionarAccion implements VPActionController {
    @Override
    public void performAction(VPAction accion) {
        ViewManager vm = ApplicationManager.instance().getViewManager();
        IDiagramUIModel d = ApplicationManager.instance().getDiagramManager().getActiveDiagram();
        if (d == null) {
            vm.showMessageDialog(vm.getRootFrame(), "Abrí un diagrama primero.");
            return;
        }
        List<File> donde = Informe.escribir("tpfuca-inspeccion.txt", Informe.volcar(d));
        vm.showMessageDialog(vm.getRootFrame(), "Estructura de " + d.getName() + " guardada en:\n" + donde);
    }

    @Override
    public void update(VPAction accion) {
    }
}
