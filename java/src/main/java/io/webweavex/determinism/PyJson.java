package io.webweavex.determinism;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Faithful Python {@code json.dumps} for the native value tree — configurable
 * separators and {@code ensure_ascii}, always {@code sort_keys=True}.
 *
 * <p>Unlike {@link CanonicalJson} this does <em>not</em> canonicalize numbers or
 * strip volatile keys; it reproduces {@code json.dumps} verbatim, which several
 * canonical runtimes hash directly (e.g. {@code compute_global_runtime_fingerprint}
 * uses {@code separators=(",",":")} and the default {@code ensure_ascii=True};
 * {@code _graph_hash} uses the default {@code (", ", ": ")} separators).
 */
public final class PyJson {

    private PyJson() {
    }

    /** {@code json.dumps(v, sort_keys=True, separators=(",",":"))} (ensure_ascii default True). */
    public static String dumpsCompactAscii(Object v) {
        return dumps(v, ",", ":", true);
    }

    /** {@code json.dumps(v, sort_keys=True)} — default separators {@code (", ", ": ")}, ascii. */
    public static String dumpsDefaultAscii(Object v) {
        return dumps(v, ", ", ": ", true);
    }

    /** {@code json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",",":"))}. */
    public static String dumpsCompactUnicode(Object v) {
        return dumps(v, ",", ":", false);
    }

    public static String dumps(Object value, String itemSep, String kvSep, boolean ensureAscii) {
        StringBuilder sb = new StringBuilder();
        encode(value, sb, itemSep, kvSep, ensureAscii);
        return sb.toString();
    }

    private static void encode(Object v, StringBuilder sb, String itemSep, String kvSep,
                               boolean ensureAscii) {
        if (v == null) {
            sb.append("null");
        } else if (v instanceof Boolean) {
            sb.append(((Boolean) v) ? "true" : "false");
        } else if (v instanceof Double || v instanceof Float) {
            sb.append(floatRepr(((Number) v).doubleValue()));
        } else if (v instanceof Number) {
            sb.append(v.toString());
        } else if (v instanceof String) {
            escape((String) v, sb, ensureAscii);
        } else if (v instanceof List) {
            List<?> list = (List<?>) v;
            sb.append('[');
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) {
                    sb.append(itemSep);
                }
                encode(list.get(i), sb, itemSep, kvSep, ensureAscii);
            }
            sb.append(']');
        } else if (v instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) v;
            List<String> keys = new ArrayList<>(map.size());
            for (Object k : map.keySet()) {
                keys.add(String.valueOf(k));
            }
            keys.sort(Normalization::codePointCompare);
            sb.append('{');
            boolean first = true;
            for (String k : keys) {
                if (!first) {
                    sb.append(itemSep);
                }
                first = false;
                escape(k, sb, ensureAscii);
                sb.append(kvSep);
                encode(lookup(map, k), sb, itemSep, kvSep, ensureAscii);
            }
            sb.append('}');
        } else {
            escape(v.toString(), sb, ensureAscii);
        }
    }

    /** Python {@code json} float form: {@code repr} for finite, {@code NaN}/{@code Infinity} otherwise. */
    private static String floatRepr(double d) {
        if (Double.isNaN(d)) {
            return "NaN";
        }
        if (d == Double.POSITIVE_INFINITY) {
            return "Infinity";
        }
        if (d == Double.NEGATIVE_INFINITY) {
            return "-Infinity";
        }
        return PyFloat.pyFloatRepr(d);
    }

    private static Object lookup(Map<?, ?> map, String key) {
        if (map.containsKey(key)) {
            return map.get(key);
        }
        for (Map.Entry<?, ?> e : map.entrySet()) {
            if (String.valueOf(e.getKey()).equals(key)) {
                return e.getValue();
            }
        }
        return null;
    }

    private static void escape(String s, StringBuilder sb, boolean ensureAscii) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"':
                    sb.append("\\\"");
                    break;
                case '\\':
                    sb.append("\\\\");
                    break;
                case '\b':
                    sb.append("\\b");
                    break;
                case '\t':
                    sb.append("\\t");
                    break;
                case '\n':
                    sb.append("\\n");
                    break;
                case '\f':
                    sb.append("\\f");
                    break;
                case '\r':
                    sb.append("\\r");
                    break;
                default:
                    if (c < 0x20 || (ensureAscii && c > 0x7E)) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
    }
}
