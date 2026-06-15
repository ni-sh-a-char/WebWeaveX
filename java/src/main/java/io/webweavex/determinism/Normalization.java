package io.webweavex.determinism;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Cross-language normalization primitives — byte-identical to the Python
 * canonical runtime ({@code core/determinism/normalization.py}) and the aligned
 * JavaScript and Dart runtimes.
 *
 * <p>The deterministic core depends on the JDK alone: {@link Normalizer} for
 * NFKC and explicit code-point handling for ordering and whitespace, so no third
 * party library can perturb the canonical bytes.
 */
public final class Normalization {

    private Normalization() {
    }

    /** Keys stripped from every dictionary level before canonicalization. */
    public static final Set<String> VOLATILE_RUNTIME_KEYS = Set.of(
            "timestamp",
            "created_at",
            "updated_at",
            "nonce",
            "request_id",
            "csrf",
            "generated_at",
            "runtime_id",
            "random",
            "uuid");

    /**
     * NFKC + CRLF&rarr;LF + trailing-whitespace strip, in that order.
     *
     * <p>Matches Python {@code normalize_runtime_value}: NFKC first, then
     * {@code \r\n}/{@code \r} &rarr; {@code \n}, then a trailing {@code \s+$}
     * strip using Python's str {@code \s} set (curated below — ECMAScript's
     * {@code \s} differs, so the set is spelled out by code point).
     */
    public static String normalizeRuntimeValue(String value) {
        String s = Normalizer.normalize(value, Normalizer.Form.NFKC);
        s = s.replace("\r\n", "\n").replace("\r", "\n");
        return stripTrailingWhitespace(s);
    }

    /** True for the exact code-point set matched by Python str {@code \s}. */
    private static boolean isPyWhitespace(int cp) {
        return (cp >= 0x09 && cp <= 0x0D)   // \t \n \v \f \r
                || (cp >= 0x1C && cp <= 0x1F) // FS GS RS US
                || cp == 0x20
                || cp == 0x85
                || cp == 0xA0
                || cp == 0x1680
                || (cp >= 0x2000 && cp <= 0x200A)
                || cp == 0x2028
                || cp == 0x2029
                || cp == 0x202F
                || cp == 0x205F
                || cp == 0x3000;
    }

    private static String stripTrailingWhitespace(String s) {
        int end = s.length();
        while (end > 0) {
            int cp = s.codePointBefore(end);
            if (!isPyWhitespace(cp)) {
                break;
            }
            end -= Character.charCount(cp);
        }
        return s.substring(0, end);
    }

    /**
     * Unicode code-point string comparison (Python {@code sorted()} semantics).
     *
     * <p>{@link String#compareTo} orders by UTF-16 code units, which inverts
     * astral-plane characters relative to {@code U+E000}&ndash;{@code U+FFFF};
     * the canonical contract is code-point order, matching Python, JavaScript,
     * and Dart.
     */
    public static int codePointCompare(String a, String b) {
        int i = 0;
        int j = 0;
        while (i < a.length() && j < b.length()) {
            int ca = a.codePointAt(i);
            int cb = b.codePointAt(j);
            if (ca != cb) {
                return Integer.compare(ca, cb);
            }
            i += Character.charCount(ca);
            j += Character.charCount(cb);
        }
        return Integer.compare(a.length() - i, b.length() - j);
    }

    /**
     * Cross-language numeric canonicalization: integral doubles below 2^63
     * become integers, non-finite doubles become {@code null}, everything else
     * is returned unchanged. JavaScript has a single number type, so {@code 2.0}
     * must not serialize differently from {@code 2} in any runtime.
     */
    public static Object canonicalizeNumber(Object v) {
        double d;
        if (v instanceof Double) {
            d = (Double) v;
        } else if (v instanceof Float) {
            d = ((Float) v).doubleValue();
        } else {
            return v;
        }
        if (Double.isNaN(d) || Double.isInfinite(d)) {
            return null;
        }
        if (d == Math.floor(d) && Math.abs(d) < 9223372036854775808.0) {
            return (long) d;
        }
        return v instanceof Float ? (Double) d : v;
    }

    /**
     * Recursively sort keys by code point, drop volatile keys at every dict
     * level, and canonicalize numbers — mirroring Python {@code stable_sort_keys}
     * and the Dart {@code stableSortKeys} (one level of list handling).
     */
    public static Map<String, Object> stableSortKeys(Map<?, ?> obj) {
        List<String> keys = new ArrayList<>(obj.size());
        for (Object k : obj.keySet()) {
            keys.add(String.valueOf(k));
        }
        keys.sort(Normalization::codePointCompare);

        LinkedHashMap<String, Object> sorted = new LinkedHashMap<>();
        for (String k : keys) {
            if (VOLATILE_RUNTIME_KEYS.contains(k)) {
                continue;
            }
            Object val = get(obj, k);
            if (val instanceof Map) {
                sorted.put(k, stableSortKeys((Map<?, ?>) val));
            } else if (val instanceof List) {
                List<?> list = (List<?>) val;
                List<Object> mapped = new ArrayList<>(list.size());
                for (Object item : list) {
                    if (item instanceof Map) {
                        mapped.add(stableSortKeys((Map<?, ?>) item));
                    } else {
                        mapped.add(canonicalizeNumber(item));
                    }
                }
                sorted.put(k, mapped);
            } else {
                sorted.put(k, canonicalizeNumber(val));
            }
        }
        return sorted;
    }

    /** Looks up a value whose original key may be a non-String (e.g. number). */
    private static Object get(Map<?, ?> obj, String key) {
        if (obj.containsKey(key)) {
            return obj.get(key);
        }
        for (Map.Entry<?, ?> e : obj.entrySet()) {
            if (String.valueOf(e.getKey()).equals(key)) {
                return e.getValue();
            }
        }
        return null;
    }
}
