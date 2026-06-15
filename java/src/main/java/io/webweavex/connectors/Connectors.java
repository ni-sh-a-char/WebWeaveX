package io.webweavex.connectors;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Python-semantics helpers shared by the connector-runtime extraction engines —
 * faithful to CPython {@code list()}/{@code dict()} copies, {@code int()}/{@code str()}
 * coercion, {@code x or default} truthiness, {@code sorted(key=str)} (code-point order),
 * and list slicing, so the ported envelopes stay byte-exact.
 */
final class Connectors {

    private Connectors() {
    }

    /** {@code snap = snapshot or {}} — null (or empty) snapshot becomes an empty dict. */
    static Map<String, Object> snap(Map<String, Object> snapshot) {
        return snapshot == null ? new LinkedHashMap<>() : snapshot;
    }

    /** {@code list(snap.get(key, dflt))} — copy; default applies only when key is absent. */
    @SuppressWarnings("unchecked")
    static List<Object> getList(Map<String, Object> s, String key, List<Object> dflt) {
        Object v = Py.get(s, key, dflt);
        if (v instanceof List) {
            return new ArrayList<>((List<Object>) v);
        }
        return new ArrayList<>(dflt);
    }

    /** {@code dict(snap.get(key, {}))} — copy; empty dict when absent or non-map. */
    @SuppressWarnings("unchecked")
    static Map<String, Object> getMap(Map<String, Object> s, String key) {
        Object v = Py.get(s, key, null);
        if (v instanceof Map) {
            return new LinkedHashMap<>((Map<String, Object>) v);
        }
        return new LinkedHashMap<>();
    }

    /** {@code sorted(xs, key=str)} — stable, by Unicode code point (identical to plain
     * {@code sorted} for string lists). */
    static List<Object> sortedByStr(List<Object> xs) {
        List<Object> c = new ArrayList<>(xs);
        c.sort((a, b) -> Normalization.codePointCompare(Py.str(a), Py.str(b)));
        return c;
    }

    /** {@code int(x)} — truncate toward zero. */
    static long pyInt(Object v) {
        if (v instanceof Long || v instanceof Integer) {
            return ((Number) v).longValue();
        }
        if (v instanceof Number) {
            return (long) ((Number) v).doubleValue();
        }
        if (v instanceof Boolean) {
            return ((Boolean) v) ? 1L : 0L;
        }
        if (v instanceof String) {
            return Long.parseLong(((String) v).trim());
        }
        return 0L;
    }

    /** {@code xs[:n]}. */
    static List<Object> slice(List<Object> xs, int n) {
        return new ArrayList<>(xs.subList(0, Math.min(n, xs.size())));
    }

    /** {@code v or dflt} — default when null OR empty (Python falsy list). */
    static List<Object> orDefault(List<Object> v, List<Object> dflt) {
        return (v == null || v.isEmpty()) ? dflt : v;
    }

    /** Convenience for an immutable-ish literal list. */
    static List<Object> list(Object... items) {
        List<Object> l = new ArrayList<>(items.length);
        for (Object i : items) {
            l.add(i);
        }
        return l;
    }
}
