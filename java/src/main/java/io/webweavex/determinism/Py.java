package io.webweavex.determinism;

import java.util.List;
import java.util.Map;

/**
 * Small Python-semantics helpers shared by the higher runtime layers — faithful
 * to CPython's {@code str()} coercion and truthiness so ported dictionary/list
 * logic stays byte-exact.
 */
public final class Py {

    private Py() {
    }

    /** CPython {@code str(obj)} for the value shapes that occur in runtime dicts. */
    public static String str(Object o) {
        if (o == null) {
            return "None";
        }
        if (o instanceof Boolean) {
            return ((Boolean) o) ? "True" : "False";
        }
        return o.toString();
    }

    /** CPython truthiness: {@code None}, {@code ""}, {@code False}, {@code 0}, empty containers are falsy. */
    public static boolean truthy(Object o) {
        if (o == null || Boolean.FALSE.equals(o)) {
            return false;
        }
        if (o instanceof String) {
            return !((String) o).isEmpty();
        }
        if (o instanceof Number) {
            return ((Number) o).doubleValue() != 0.0;
        }
        if (o instanceof Map) {
            return !((Map<?, ?>) o).isEmpty();
        }
        if (o instanceof List) {
            return !((List<?>) o).isEmpty();
        }
        return true;
    }

    /** {@code dict.get(key, default)} returning the default only when the key is absent. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : null;
    }

    @SuppressWarnings("unchecked")
    public static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : null;
    }

    /** {@code container.get(key, default)} where container may be null or non-dict. */
    public static Object get(Object container, String key, Object dflt) {
        Map<String, Object> m = asMap(container);
        if (m == null || !m.containsKey(key)) {
            return dflt;
        }
        return m.get(key);
    }
}
