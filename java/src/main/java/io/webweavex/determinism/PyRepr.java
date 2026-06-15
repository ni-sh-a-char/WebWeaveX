package io.webweavex.determinism;

import java.util.List;
import java.util.Map;

/**
 * CPython {@code repr()} / {@code str()} for the native value tree — needed where
 * a runtime sorts by {@code str(dict)} (e.g. {@code query_runtime_memory}).
 *
 * <p>Strings render single-quoted (double-quoted only when they contain a single
 * quote but no double quote), dicts as {@code {k: v, ...}} in insertion order,
 * lists as {@code [a, b]} — matching CPython exactly for the value shapes that
 * occur in runtime payloads.
 */
public final class PyRepr {

    private PyRepr() {
    }

    /** CPython {@code str(obj)}: identity for strings, otherwise {@link #repr}. */
    public static String str(Object o) {
        return o instanceof String ? (String) o : repr(o);
    }

    public static String repr(Object o) {
        if (o == null) {
            return "None";
        }
        if (o instanceof Boolean) {
            return ((Boolean) o) ? "True" : "False";
        }
        if (o instanceof Double || o instanceof Float) {
            return PyFloat.pyFloatRepr(((Number) o).doubleValue());
        }
        if (o instanceof Number) {
            return o.toString();
        }
        if (o instanceof String) {
            return reprString((String) o);
        }
        if (o instanceof Map) {
            StringBuilder sb = new StringBuilder("{");
            boolean first = true;
            for (Map.Entry<?, ?> e : ((Map<?, ?>) o).entrySet()) {
                if (!first) {
                    sb.append(", ");
                }
                first = false;
                sb.append(repr(e.getKey())).append(": ").append(repr(e.getValue()));
            }
            return sb.append('}').toString();
        }
        if (o instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            boolean first = true;
            for (Object item : (List<?>) o) {
                if (!first) {
                    sb.append(", ");
                }
                first = false;
                sb.append(repr(item));
            }
            return sb.append(']').toString();
        }
        return reprString(o.toString());
    }

    private static String reprString(String s) {
        boolean hasSingle = s.indexOf('\'') >= 0;
        boolean hasDouble = s.indexOf('"') >= 0;
        char quote = (hasSingle && !hasDouble) ? '"' : '\'';
        StringBuilder sb = new StringBuilder();
        sb.append(quote);
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\\') {
                sb.append("\\\\");
            } else if (c == quote) {
                sb.append('\\').append(quote);
            } else if (c == '\n') {
                sb.append("\\n");
            } else if (c == '\r') {
                sb.append("\\r");
            } else if (c == '\t') {
                sb.append("\\t");
            } else if (c < 0x20 || c == 0x7f) {
                sb.append(String.format("\\x%02x", (int) c));
            } else {
                sb.append(c);
            }
        }
        sb.append(quote);
        return sb.toString();
    }
}
