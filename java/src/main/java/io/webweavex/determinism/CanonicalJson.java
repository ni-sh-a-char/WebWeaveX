package io.webweavex.determinism;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Compact canonical JSON encoder — byte-identical to Python
 * {@code json.dumps(value, ensure_ascii=False, separators=(",", ":"),
 * sort_keys=True)} and the aligned JavaScript and Dart runtimes.
 *
 * <p>Values are the native Java tree: {@link Map} (string keys), {@link List},
 * {@link String}, {@link Boolean}, integral {@link Number}s, {@link Double}/
 * {@link Float}, or {@code null}. Floats are rendered via {@link PyFloat}; keys
 * are sorted by Unicode code point; integral floats below 2^63 collapse to
 * integers; non-finite doubles become {@code null}.
 */
public final class CanonicalJson {

    private CanonicalJson() {
    }

    public static String canonicalJsonEncode(Object value) {
        StringBuilder sb = new StringBuilder();
        encode(value, sb);
        return sb.toString();
    }

    private static void encode(Object raw, StringBuilder sb) {
        Object v = Normalization.canonicalizeNumber(raw);
        if (v == null) {
            sb.append("null");
        } else if (v instanceof Boolean) {
            sb.append(((Boolean) v) ? "true" : "false");
        } else if (v instanceof Double) {
            // canonicalizeNumber has already collapsed Float -> Double/Long and
            // non-finite -> null, so only finite non-integral doubles arrive here.
            sb.append(PyFloat.pyFloatRepr((Double) v));
        } else if (v instanceof Number) {
            sb.append(v.toString());
        } else if (v instanceof String) {
            escapeJsonString((String) v, sb);
        } else if (v instanceof List) {
            sb.append('[');
            List<?> list = (List<?>) v;
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) {
                    sb.append(',');
                }
                encode(list.get(i), sb);
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
                    sb.append(',');
                }
                first = false;
                escapeJsonString(k, sb);
                sb.append(':');
                encode(lookup(map, k), sb);
            }
            sb.append('}');
        } else {
            escapeJsonString(v.toString(), sb);
        }
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

    /**
     * JSON string escaping identical to Python {@code json.dumps} with
     * {@code ensure_ascii=False}: {@code " \ \b \t \n \f \r} use short escapes,
     * other control characters below {@code U+0020} use lowercase
     * {@code \\uXXXX}, and everything else (including all non-ASCII) is emitted
     * verbatim. The forward slash is never escaped.
     */
    static void escapeJsonString(String s, StringBuilder sb) {
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
                    if (c < 0x20) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
    }
}
