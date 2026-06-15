package io.webweavex.determinism;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Canonical string serialization used for hashing, encryption, and fingerprints
 * — byte-identical to Python {@code stable_serialize}
 * ({@code core/determinism/normalization.py}) and the Dart {@code stableSerialize}.
 *
 * <ul>
 *   <li>{@link String} &rarr; {@link Normalization#normalizeRuntimeValue}</li>
 *   <li>{@link Map} &rarr; canonical JSON of its key-stabilized form</li>
 *   <li>{@link List} &rarr; canonical JSON of the array re-keyed as an object
 *       ({@code {"0": ..., "1": ...}}), matching the JavaScript runtime's
 *       {@code fast-json-stable-stringify} array handling</li>
 *   <li>any scalar &rarr; canonical JSON of its canonicalized number form</li>
 * </ul>
 */
public final class StableSerialize {

    private StableSerialize() {
    }

    public static String stableSerialize(Object value) {
        if (value instanceof String) {
            return Normalization.normalizeRuntimeValue((String) value);
        }
        if (value instanceof Map) {
            return CanonicalJson.canonicalJsonEncode(
                    Normalization.stableSortKeys((Map<?, ?>) value));
        }
        if (value instanceof List) {
            List<?> list = (List<?>) value;
            LinkedHashMap<String, Object> asMap = new LinkedHashMap<>();
            for (int i = 0; i < list.size(); i++) {
                Object item = list.get(i);
                if (item instanceof Map) {
                    asMap.put(String.valueOf(i),
                            Normalization.stableSortKeys((Map<?, ?>) item));
                } else {
                    asMap.put(String.valueOf(i), Normalization.canonicalizeNumber(item));
                }
            }
            return CanonicalJson.canonicalJsonEncode(asMap);
        }
        return CanonicalJson.canonicalJsonEncode(value);
    }
}
