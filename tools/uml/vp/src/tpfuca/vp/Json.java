package tpfuca.vp;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Lector JSON mínimo (objetos, listas, textos, números, true/false/null): VP no trae uno. */
final class Json {
    private final String s;
    private int i;

    private Json(String s) {
        this.s = s;
    }

    static Object leer(String texto) {
        Json j = new Json(texto);
        Object v = j.valor();
        j.blancos();
        if (j.i != j.s.length()) {
            throw j.error("sobra texto");
        }
        return v;
    }

    private Object valor() {
        blancos();
        char c = s.charAt(i);
        if (c == '{') {
            return objeto();
        }
        if (c == '[') {
            return lista();
        }
        if (c == '"') {
            return texto();
        }
        if (s.startsWith("true", i)) {
            i += 4;
            return Boolean.TRUE;
        }
        if (s.startsWith("false", i)) {
            i += 5;
            return Boolean.FALSE;
        }
        if (s.startsWith("null", i)) {
            i += 4;
            return null;
        }
        int ini = i;
        while (i < s.length() && "+-0123456789.eE".indexOf(s.charAt(i)) >= 0) {
            i++;
        }
        if (ini == i) {
            throw error("valor inesperado");
        }
        return Double.valueOf(s.substring(ini, i));
    }

    private Map<String, Object> objeto() {
        Map<String, Object> m = new LinkedHashMap<>();
        i++;
        blancos();
        if (s.charAt(i) == '}') {
            i++;
            return m;
        }
        while (true) {
            blancos();
            String k = texto();
            blancos();
            esperar(':');
            m.put(k, valor());
            blancos();
            if (s.charAt(i) == ',') {
                i++;
                continue;
            }
            esperar('}');
            return m;
        }
    }

    private List<Object> lista() {
        List<Object> l = new ArrayList<>();
        i++;
        blancos();
        if (s.charAt(i) == ']') {
            i++;
            return l;
        }
        while (true) {
            l.add(valor());
            blancos();
            if (s.charAt(i) == ',') {
                i++;
                continue;
            }
            esperar(']');
            return l;
        }
    }

    private String texto() {
        esperar('"');
        StringBuilder b = new StringBuilder();
        while (true) {
            char c = s.charAt(i++);
            if (c == '"') {
                return b.toString();
            }
            if (c != '\\') {
                b.append(c);
                continue;
            }
            char e = s.charAt(i++);
            switch (e) {
                case 'n': b.append('\n'); break;
                case 't': b.append('\t'); break;
                case 'r': b.append('\r'); break;
                case 'b': b.append('\b'); break;
                case 'f': b.append('\f'); break;
                case 'u':
                    b.append((char) Integer.parseInt(s.substring(i, i + 4), 16));
                    i += 4;
                    break;
                default: b.append(e);
            }
        }
    }

    private void blancos() {
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) {
            i++;
        }
    }

    private void esperar(char c) {
        if (s.charAt(i) != c) {
            throw error("se esperaba '" + c + "'");
        }
        i++;
    }

    private IllegalArgumentException error(String msg) {
        return new IllegalArgumentException("JSON inválido en la posición " + i + ": " + msg);
    }
}
