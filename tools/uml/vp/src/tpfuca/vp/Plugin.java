package tpfuca.vp;

import java.io.File;

import com.vp.plugin.VPPlugin;
import com.vp.plugin.VPPluginInfo;

/** Plugin de VP que dibuja los diagramas de cada CU a partir de vp-diagramas.json. */
public class Plugin implements VPPlugin {
    static File carpeta;

    @Override
    public void loaded(VPPluginInfo info) {
        carpeta = info.getPluginDir();
    }

    @Override
    public void unloaded() {
    }
}
