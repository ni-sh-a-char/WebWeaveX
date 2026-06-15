package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.crypto.TimeKey;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Asserts the Java runtime is byte-identical to canonical Python 2.1.0.
 *
 * <p>The fixtures in {@code parity/golden_vectors.json} are produced by
 * {@code tools/gen_java_parity_vectors.py} run against a materialized Python
 * branch ({@code compute_kaalka_hash == compute_deterministic_hash}). Each
 * vector carries the canonical {@code stable_serialize} string, the SHA-256
 * digest, and — for crypto — the derived time key and base64 ciphertext.
 */
class CrossLanguageParityTest {

    private static JsonNode loadGolden() {
        try (InputStream in = CrossLanguageParityTest.class
                .getResourceAsStream("/parity/golden_vectors.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load golden vectors", e);
        }
    }

    /** Jackson {@link JsonNode} → native value tree (Map/List/String/Long/Double/Boolean/null). */
    static Object toNative(JsonNode node) {
        if (node == null || node.isNull() || node.isMissingNode()) {
            return null;
        }
        if (node.isObject()) {
            Map<String, Object> map = new LinkedHashMap<>();
            node.fields().forEachRemaining(e -> map.put(e.getKey(), toNative(e.getValue())));
            return map;
        }
        if (node.isArray()) {
            List<Object> list = new ArrayList<>();
            node.forEach(child -> list.add(toNative(child)));
            return list;
        }
        if (node.isTextual()) {
            return node.textValue();
        }
        if (node.isBoolean()) {
            return node.booleanValue();
        }
        if (node.isIntegralNumber()) {
            return node.canConvertToLong() ? (Object) node.asLong() : node.bigIntegerValue();
        }
        return node.asDouble();
    }

    @TestFactory
    List<DynamicTest> serializationAndHashParity() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : loadGolden().get("vectors")) {
            String name = v.get("name").asText();
            Object input = toNative(v.get("input"));
            String expectedSerialized = v.get("serialized").asText();
            String expectedHash = v.get("hash").asText();
            tests.add(DynamicTest.dynamicTest("serialize:" + name, () ->
                    assertEquals(expectedSerialized, StableSerialize.stableSerialize(input))));
            tests.add(DynamicTest.dynamicTest("hash:" + name, () ->
                    assertEquals(expectedHash, Kaalka.computeKaalkaHash(input))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> specialScalarParity() {
        Map<String, Double> values = Map.of(
                "nan", Double.NaN,
                "inf", Double.POSITIVE_INFINITY,
                "neg_inf", Double.NEGATIVE_INFINITY);
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : loadGolden().get("special_scalars")) {
            String name = v.get("name").asText();
            Double input = values.get(name);
            String expectedSerialized = v.get("serialized").asText();
            String expectedHash = v.get("hash").asText();
            tests.add(DynamicTest.dynamicTest("serialize:" + name, () ->
                    assertEquals(expectedSerialized, StableSerialize.stableSerialize(input))));
            tests.add(DynamicTest.dynamicTest("hash:" + name, () ->
                    assertEquals(expectedHash, Kaalka.computeKaalkaHash(input))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> cryptoParity() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : loadGolden().get("crypto")) {
            String name = v.get("name").asText();
            Object input = toNative(v.get("input"));
            String key = v.get("key").asText();
            String expectedTimeKey = v.get("time_key").asText();
            String expectedEncrypted = v.get("encrypted").asText();
            String expectedHash = v.get("hash").asText();

            tests.add(DynamicTest.dynamicTest("timekey:" + name, () ->
                    assertEquals(expectedTimeKey, TimeKey.deriveKaalkaTimeKey(key))));
            tests.add(DynamicTest.dynamicTest("encrypt:" + name, () ->
                    assertEquals(expectedEncrypted, Kaalka.encryptValue(input, key))));
            tests.add(DynamicTest.dynamicTest("roundtrip:" + name, () ->
                    assertEquals(StableSerialize.stableSerialize(input),
                            Kaalka.decryptValue(expectedEncrypted, key))));
            tests.add(DynamicTest.dynamicTest("hash:" + name, () ->
                    assertEquals(expectedHash, Kaalka.computeKaalkaHash(input))));
        }
        return tests;
    }
}
