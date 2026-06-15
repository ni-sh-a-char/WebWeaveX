package io.webweavex.persistence;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.PyJson;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.nio.charset.StandardCharsets;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.crypto.kaalka_engine.hex_fingerprint} (exported as the
 * public Python {@code fingerprint}) and the {@code dumps_deterministic}
 * serializer it depends on ({@code core.serialize.deterministic_serializer}).
 *
 * <p>{@code fingerprint(payload, token) = kaalka_encrypt_bytes(raw, token).hex()}
 * where {@code raw} is the UTF-8 of a String/bytes payload verbatim, or of
 * {@code dumps_deterministic(payload)} otherwise.
 *
 * <p>NOTE: this uses the Kaalka <b>v1</b> byte cipher
 * ({@code (n ^ tk) + i*31 + lnMod}), a different primitive from the Kaalka v5
 * path in {@link io.webweavex.crypto.Kaalka}. And {@code dumps_deterministic}
 * uses <b>NFC</b> + {@code .15g} float rounding + list-element sorting — distinct
 * from the NFKC {@code stable_serialize} used for hashing.
 */
public final class FingerprintHex {

    private FingerprintHex() {
    }

    public static final String DEFAULT_TOKEN = "webweavex";

    public static String fingerprint(Object payload) {
        return hexFingerprint(payload, DEFAULT_TOKEN);
    }

    public static String hexFingerprint(Object payload, String token) {
        String rawText;
        if (payload instanceof String) {
            rawText = (String) payload;
        } else if (payload instanceof byte[]) {
            rawText = new String((byte[]) payload, StandardCharsets.UTF_8);
        } else {
            rawText = dumpsDeterministic(payload);
        }
        byte[] raw = rawText.getBytes(StandardCharsets.UTF_8);
        return toHex(kaalkaEncryptBytes(raw, token.getBytes(StandardCharsets.UTF_8)));
    }

    /** Port of {@code kaalka_encrypt_bytes(data, token)} (Kaalka v1). */
    public static byte[] kaalkaEncryptBytes(byte[] data, byte[] token) {
        byte[] out = new byte[data.length];
        int lnMod = data.length % 251;
        for (int i = 0; i < data.length; i++) {
            int n = data[i] & 0xFF;
            int tk = token.length == 0 ? 0 : (token[i % token.length] & 0xFF);
            int value = ((n ^ tk) + (i * 31) + lnMod) % 256;
            out[i] = (byte) Math.floorMod(value, 256);
        }
        return out;
    }

    private static String toHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(Character.forDigit((b >> 4) & 0xF, 16));
            sb.append(Character.forDigit(b & 0xF, 16));
        }
        return sb.toString();
    }

    // --- dumps_deterministic ----------------------------------------------

    /** Port of {@code dumps_deterministic(value)} = compact JSON of {@code _stable(value)}. */
    public static String dumpsDeterministic(Object value) {
        return PyJson.dumpsCompactUnicode(stable(value, 0));
    }

    /** Port of {@code _stable(value, _depth)} — NFC strings, .15g floats, sorted lists. */
    private static Object stable(Object value, int depth) {
        if (depth > 64) {
            return nfc(String.valueOf(value));
        }
        if (value instanceof String) {
            return nfc((String) value);
        }
        if (value instanceof Boolean || value == null) {
            return value;
        }
        if (value instanceof Double || value instanceof Float) {
            double d = ((Number) value).doubleValue();
            if (Double.isNaN(d) || Double.isInfinite(d)) {
                return 0L;
            }
            if (d == Math.floor(d) && Math.abs(d) < 9223372036854775808.0) {
                return (long) d;
            }
            double rounded = round15g(d);
            if (rounded == Math.floor(rounded) && Math.abs(rounded) < 9223372036854775808.0) {
                return (long) rounded;
            }
            return rounded;
        }
        if (value instanceof Number) {
            return value;
        }
        if (value instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) value;
            Map<String, Object> byNorm = new LinkedHashMap<>();
            for (Map.Entry<?, ?> e : map.entrySet()) {
                byNorm.put(nfc(String.valueOf(e.getKey())), e.getValue());
            }
            List<String> keys = new ArrayList<>(byNorm.keySet());
            keys.sort(Normalization::codePointCompare);
            Map<String, Object> out = new LinkedHashMap<>();
            for (String k : keys) {
                out.put(k, stable(byNorm.get(k), depth + 1));
            }
            return out;
        }
        if (value instanceof List) {
            List<Object> items = new ArrayList<>();
            for (Object v : (List<?>) value) {
                items.add(stable(v, depth + 1));
            }
            items.sort(Comparator.comparing(
                    PyJson::dumpsCompactUnicode, Normalization::codePointCompare));
            return items;
        }
        return nfc(String.valueOf(value));
    }

    private static String nfc(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFC);
    }

    /** Python {@code float(format(x, ".15g"))} — round to 15 significant digits. */
    private static double round15g(double x) {
        if (x == 0.0) {
            return 0.0;
        }
        return new BigDecimal(x).round(new MathContext(15, RoundingMode.HALF_EVEN)).doubleValue();
    }
}
