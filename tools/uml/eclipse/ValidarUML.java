import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.eclipse.emf.common.util.Diagnostic;
import org.eclipse.emf.common.util.TreeIterator;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.util.Diagnostician;
import org.eclipse.emf.ecore.util.EcoreUtil;
import org.eclipse.uml2.uml.NamedElement;
import org.eclipse.uml2.uml.UMLPlugin;
import org.eclipse.uml2.uml.resource.XMI2UMLResource;
import org.eclipse.uml2.uml.resources.util.UMLResourcesUtil;

/**
 * Carga un XMI de OMG con Eclipse UML2 (sin OSGi) y corre el validador de EMF
 * (Diagnostician): restricciones estructurales del metamodelo (multiplicidad,
 * tipos de referencias, contención) y las restricciones OCL de UML que UML2
 * implementa como métodos de validación.
 *
 * Eclipse UML2 5.5 implementa UML 2.5 (namespace de OMG 20131001). UML 2.5.1
 * (20161101) no cambia metaclases respecto de 2.5, así que el XMI se lee
 * reemplazando el namespace 2.5.1 por el 2.5. Esa equivalencia se informa.
 * También se agregan las referencias que Eclipse necesita en las actividades
 * (ver adaptarActividades).
 *
 * Uso: java ValidarUML model.xmi    (sale con 1 si hay errores)
 */
public class ValidarUML {
    static final String UML_251 = "http://www.omg.org/spec/UML/20161101";
    static final String UML_25 = "http://www.omg.org/spec/UML/20131001";

    public static void main(String[] args) throws Exception {
        Path entrada = Path.of(args[0]);
        String xmi = Files.readString(entrada, StandardCharsets.UTF_8);
        boolean era251 = xmi.contains(UML_251);
        Path temp = Files.createTempFile("modelo-uml25-", ".xmi");
        Files.writeString(temp, adaptarActividades(xmi.replace(UML_251, UML_25)),
            StandardCharsets.UTF_8);

        ResourceSet rs = new ResourceSetImpl();
        UMLResourcesUtil.init(rs);
        rs.getResourceFactoryRegistry().getExtensionToFactoryMap()
            .put("xmi", XMI2UMLResource.Factory.INSTANCE);

        System.out.println("Eclipse UML2 " + version(UMLPlugin.class) + " (implementa UML 2.5, "
            + "namespace " + UML_25 + ")");
        if (era251) {
            System.out.println("Namespace UML 2.5.1 (" + UML_251 + ") leído como UML 2.5.");
        }

        URI uri = URI.createFileURI(temp.toString());
        int errores = 0, avisos = 0;
        Resource r;
        try {
            r = rs.getResource(uri, true);
        } catch (RuntimeException e) {
            // La carga falla ante un valor fuera del metamodelo (p. ej. un literal
            // de enumeración inexistente); los detalles quedan en r.getErrors().
            r = rs.getResource(uri, false);
            if (r == null || r.getErrors().isEmpty()) {
                System.out.println("ERROR carga: " + e.getMessage());
                errores++;
            }
        }
        for (Resource.Diagnostic d : r.getErrors()) {
            System.out.println("ERROR carga: " + d.getMessage() + " (línea " + d.getLine() + ")");
            errores++;
        }
        for (Resource.Diagnostic d : r.getWarnings()) {
            System.out.println("AVISO carga: " + d.getMessage() + " (línea " + d.getLine() + ")");
            avisos++;
        }
        EcoreUtil.resolveAll(rs);
        for (Map.Entry<EObject, java.util.Collection<org.eclipse.emf.ecore.EStructuralFeature.Setting>> e
                : EcoreUtil.UnresolvedProxyCrossReferencer.find(rs).entrySet()) {
            System.out.println("ERROR referencia sin resolver: " + EcoreUtil.getURI(e.getKey()));
            errores++;
        }

        int elementos = 0;
        for (TreeIterator<EObject> it = r.getAllContents(); it.hasNext(); it.next()) {
            elementos++;
        }
        for (EObject raiz : new ArrayList<>(r.getContents())) {
            Diagnostic diag = Diagnostician.INSTANCE.validate(raiz);
            List<Diagnostic> hojas = new ArrayList<>();
            juntar(diag, hojas);
            for (Diagnostic d : hojas) {
                String nivel = d.getSeverity() >= Diagnostic.ERROR ? "ERROR" : "AVISO";
                if (d.getSeverity() >= Diagnostic.ERROR) {
                    errores++;
                } else if (d.getSeverity() == Diagnostic.WARNING) {
                    avisos++;
                } else {
                    continue;
                }
                System.out.println(nivel + " " + d.getSource() + " #" + d.getCode() + " "
                    + donde(d) + ": " + d.getMessage());
            }
        }
        System.out.println("Elementos validados: " + elementos + "; errores: " + errores
            + "; avisos: " + avisos);
        Files.deleteIfExists(temp);
        System.exit(errores > 0 ? 1 : 0);
    }

    /**
     * En UML 2.5.1 Activity::node y Activity::group son compuestas: el XMI canónico
     * solo escribe los hijos <node> y <group>. Eclipse UML2 los carga en ownedNode y
     * ownedGroup y además espera las referencias derivadas node y group (opuestas de
     * ActivityNode::activity y ActivityGroup::inActivity), que su propio exportador
     * escribe como atributos. Se agregan acá, solo para esta carga.
     */
    static String adaptarActividades(String xmi) throws Exception {
        javax.xml.parsers.DocumentBuilderFactory f = javax.xml.parsers.DocumentBuilderFactory.newInstance();
        f.setNamespaceAware(true);
        org.w3c.dom.Document doc = f.newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xmi.getBytes(StandardCharsets.UTF_8)));
        String xmiNs = "http://www.omg.org/spec/XMI/20131001";
        org.w3c.dom.NodeList todos = doc.getElementsByTagName("*");
        for (int i = 0; i < todos.getLength(); i++) {
            org.w3c.dom.Element e = (org.w3c.dom.Element) todos.item(i);
            if (!"uml:Activity".equals(e.getAttributeNS(xmiNs, "type"))) {
                continue;
            }
            for (String rol : new String[] {"node", "group"}) {
                StringBuilder ids = new StringBuilder();
                for (org.w3c.dom.Node h = e.getFirstChild(); h != null; h = h.getNextSibling()) {
                    if (h instanceof org.w3c.dom.Element he && rol.equals(he.getLocalName())) {
                        ids.append(ids.length() == 0 ? "" : " ").append(he.getAttributeNS(xmiNs, "id"));
                    }
                }
                if (ids.length() > 0) {
                    e.setAttribute(rol, ids.toString());
                }
            }
        }
        java.io.StringWriter w = new java.io.StringWriter();
        javax.xml.transform.TransformerFactory.newInstance().newTransformer()
            .transform(new javax.xml.transform.dom.DOMSource(doc),
                new javax.xml.transform.stream.StreamResult(w));
        return w.toString();
    }

    static void juntar(Diagnostic d, List<Diagnostic> out) {
        if (d.getChildren().isEmpty()) {
            if (d.getSeverity() != Diagnostic.OK) {
                out.add(d);
            }
        } else {
            for (Diagnostic c : d.getChildren()) {
                juntar(c, out);
            }
        }
    }

    static String donde(Diagnostic d) {
        for (Object o : d.getData()) {
            if (o instanceof EObject eo) {
                String id = eo.eResource() == null ? null : eo.eResource().getURIFragment(eo);
                String nombre = eo instanceof NamedElement ne && ne.getQualifiedName() != null
                    ? ne.getQualifiedName() : eo.eClass().getName();
                return "[" + id + "] " + nombre;
            }
        }
        return "";
    }

    static String version(Class<?> c) {
        String v = c.getPackage() == null ? null : c.getPackage().getImplementationVersion();
        if (v != null) {
            return v;
        }
        String jar = c.getProtectionDomain().getCodeSource().getLocation().getPath();
        return jar.substring(jar.lastIndexOf('/') + 1);
    }
}
