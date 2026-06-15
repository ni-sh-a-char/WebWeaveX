package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.GlobalRuntimeFingerprint;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.graph.RuntimeGraph;
import io.webweavex.ir.MultimodalIr;
import io.webweavex.ir.UnifiedRuntimeIr;
import io.webweavex.kernel.UniversalInput;
import io.webweavex.persistence.FingerprintHex;
import io.webweavex.replay.ReplayEquivalence;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-2 cross-language parity: kernel / graph / ir / persistence /
 * fingerprint / replay are byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s2.json}, produced by
 * {@code tools/gen_java_parity_vectors_s2.py}).
 */
class CrossLanguageParityS2Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS2Test.class
                .getResourceAsStream("/parity/golden_vectors_s2.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s2.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s2 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> map(JsonNode node) {
        return (Map<String, Object>) CrossLanguageParityTest.toNative(node);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapField(JsonNode inputs, String field) {
        if (inputs.get(field) == null || inputs.get(field).isNull()) {
            return null;
        }
        return (Map<String, Object>) CrossLanguageParityTest.toNative(inputs.get(field));
    }

    @SuppressWarnings("unchecked")
    private static List<Map<String, Object>> listOfMaps(JsonNode inputs, String field) {
        if (inputs.get(field) == null || inputs.get(field).isNull()) {
            return null;
        }
        List<Object> raw = (List<Object>) CrossLanguageParityTest.toNative(inputs.get(field));
        List<Map<String, Object>> out = new ArrayList<>();
        for (Object o : raw) {
            out.add((Map<String, Object>) o);
        }
        return out;
    }

    private static String str(JsonNode inputs, String field, String dflt) {
        JsonNode n = inputs.get(field);
        return n == null || n.isNull() ? dflt : n.asText();
    }

    private void assertSerializedAndHash(JsonNode v, Object output) {
        assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
        assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
    }

    @TestFactory
    List<DynamicTest> universalInput() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("universal_input")) {
            JsonNode in = v.get("inputs");
            tests.add(DynamicTest.dynamicTest("universal_input:" + v.get("name").asText(), () -> {
                UniversalInput.Builder b = UniversalInput.of(str(in, "source", ""))
                        .sourceType(str(in, "source_type", "auto"))
                        .url(str(in, "url", ""))
                        .path(str(in, "path", ""))
                        .session(mapField(in, "session"))
                        .options(mapField(in, "options"))
                        .tick(in.get("tick") == null ? 0 : in.get("tick").asLong());
                assertSerializedAndHash(v, b.build().toDict());
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> graph() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("graph")) {
            Map<String, Object> sources = map(v.get("inputs"));
            tests.add(DynamicTest.dynamicTest("graph:" + v.get("name").asText(), () -> {
                Map<String, Object> built = RuntimeGraph.buildParityRuntimeGraph(sources);
                assertEquals(v.get("built_serialized").asText(),
                        StableSerialize.stableSerialize(built));
                assertEquals(v.get("built_hash").asText(), Kaalka.computeKaalkaHash(built));
                assertEquals(v.get("fingerprint").asText(), RuntimeGraph.graphFingerprint(built));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> graphContract() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("graph_contract")) {
            Map<String, Object> g = map(v.get("inputs"));
            tests.add(DynamicTest.dynamicTest("graph_contract:" + v.get("name").asText(), () ->
                    assertSerializedAndHash(v, RuntimeGraph.normalizeContract(g))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> unifiedIr() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("unified_ir")) {
            JsonNode in = v.get("inputs");
            tests.add(DynamicTest.dynamicTest("unified_ir:" + v.get("name").asText(), () -> {
                Map<String, Object> ir = UnifiedRuntimeIr.compile(
                        mapField(in, "registry"),
                        mapField(in, "graph"),
                        listOfMaps(in, "bus"),
                        listOfMaps(in, "phase_results"),
                        mapField(in, "sources"));
                assertSerializedAndHash(v, ir);
                assertEquals(v.get("to_graph_serialized").asText(),
                        StableSerialize.stableSerialize(UnifiedRuntimeIr.toGraph(ir)));
                assertEquals(v.get("to_graph_hash").asText(),
                        Kaalka.computeKaalkaHash(UnifiedRuntimeIr.toGraph(ir)));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> multimodalIr() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("multimodal_ir")) {
            JsonNode in = v.get("inputs");
            tests.add(DynamicTest.dynamicTest("multimodal_ir:" + v.get("name").asText(), () ->
                    assertSerializedAndHash(v, MultimodalIr.compile(
                            mapField(in, "layout"), mapField(in, "tables"),
                            mapField(in, "forms"), mapField(in, "charts"),
                            mapField(in, "ui")))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> fingerprint() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("fingerprint")) {
            JsonNode in = v.get("inputs");
            Object payload = CrossLanguageParityTest.toNative(in.get("payload"));
            String token = in.get("token").asText();
            tests.add(DynamicTest.dynamicTest("fingerprint:" + v.get("name").asText(), () ->
                    assertEquals(v.get("string").asText(),
                            FingerprintHex.hexFingerprint(payload, token))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> globalFingerprint() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("global_fingerprint")) {
            JsonNode in = v.get("inputs");
            tests.add(DynamicTest.dynamicTest("global_fingerprint:" + v.get("name").asText(), () ->
                    assertEquals(v.get("string").asText(), GlobalRuntimeFingerprint.compute(
                            mapField(in, "extraction"),
                            mapField(in, "graph"),
                            mapField(in, "memory"),
                            mapField(in, "sync"),
                            mapField(in, "reconstruction"),
                            str(in, "kaalka_seal", "")))));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> replay() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("replay")) {
            JsonNode in = v.get("inputs");
            tests.add(DynamicTest.dynamicTest("replay:" + v.get("name").asText(), () ->
                    assertSerializedAndHash(v, ReplayEquivalence.validate(
                            mapField(in, "original"), mapField(in, "replayed")))));
        }
        return tests;
    }
}
