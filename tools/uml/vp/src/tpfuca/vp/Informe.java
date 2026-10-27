package tpfuca.vp;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

import com.vp.plugin.ApplicationManager;
import com.vp.plugin.diagram.IConnectorUIModel;
import com.vp.plugin.diagram.IDiagramElement;
import com.vp.plugin.diagram.IDiagramUIModel;
import com.vp.plugin.diagram.IShapeUIModel;
import com.vp.plugin.model.IModelElement;

/**
 * Vuelca la estructura de los diagramas (tipo de forma, padre, posición y
 * elemento de modelo) a un texto junto al proyecto, para comparar lo que arma
 * el plugin con lo que arma el editor de VP sin depender de capturas.
 */
final class Informe {
    private Informe() {
    }

    static String volcar(IDiagramUIModel d) {
        StringBuilder b = new StringBuilder();
        b.append("## ").append(d.getName()).append(" [").append(d.getType()).append("] ").append(d.getId()).append('\n');
        for (IDiagramElement e : d.toDiagramElementArray()) {
            b.append(e.getShapeType()).append(' ').append(e.getId());
            if (e instanceof IShapeUIModel && ((IShapeUIModel) e).getParent() != null) {
                b.append(" padre=").append(((IShapeUIModel) e).getParent().getId());
            }
            b.append(" xywh=").append(e.getX()).append(',').append(e.getY()).append(',').append(e.getWidth())
                .append(',').append(e.getHeight());
            if (e instanceof IConnectorUIModel) {
                IConnectorUIModel c = (IConnectorUIModel) e;
                b.append(" de=").append(c.getFromShape() == null ? "-" : c.getFromShape().getId())
                    .append(" a=").append(c.getToShape() == null ? "-" : c.getToShape().getId()).append(" puntos=");
                if (c.getPoints() != null) {
                    for (java.awt.Point p : c.getPoints()) {
                        b.append('(').append(p.x).append(',').append(p.y).append(')');
                    }
                }
            }
            IModelElement m = e.getMetaModelElement();
            if (m != null) {
                b.append(" modelo=").append(m.getModelType()).append(" \"").append(m.getName()).append('"');
                if (m.getParent() != null) {
                    b.append(" en=").append(m.getParent().getModelType()).append(" \"").append(m.getParent().getName())
                        .append('"');
                }
            }
            b.append(" ui=").append(e.getClass().getSimpleName()).append('\n');
        }
        return b.toString();
    }

    /** Escribe el texto en la carpeta del proyecto abierto y en la del plugin; devuelve dónde quedó. */
    static List<File> escribir(String nombre, String texto) {
        List<File> dest = new ArrayList<>();
        File proyecto = ApplicationManager.instance().getProjectManager().getProject().getProjectFile();
        if (proyecto != null && proyecto.getParentFile() != null) {
            dest.add(new File(proyecto.getParentFile(), nombre));
        }
        dest.add(new File(Plugin.carpeta, nombre));
        List<File> ok = new ArrayList<>();
        for (File f : dest) {
            try {
                Files.write(f.toPath(), texto.getBytes(StandardCharsets.UTF_8));
                ok.add(f);
            } catch (Exception ex) {
                // Carpeta sin permiso de escritura: queda la otra copia.
            }
        }
        return ok;
    }
}
