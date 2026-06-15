package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.connectors.ApiConnectors;
import io.webweavex.connectors.DatabaseConnectors;
import io.webweavex.connectors.StreamConnectors;
import io.webweavex.connectors.TelemetryConnector;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-4 cross-language parity: the connector-runtime extraction family
 * (database / api / streams / telemetry) is byte-identical to canonical Python
 * 2.1.0 ({@code golden_vectors_s4.json}). Cross-language proof only — every
 * assertion compares Java output to recorded Python output (stable serialization
 * + hash).
 */
class CrossLanguageParityS4Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS4Test.class
                .getResourceAsStream("/parity/golden_vectors_s4.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s4.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s4 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> listField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String str(JsonNode inputs, String field, String dflt) {
        JsonNode n = inputs.get(field);
        return n == null || n.isNull() ? dflt : n.asText();
    }

    private List<DynamicTest> section(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs"));
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> extractDatabaseRuntime() {
        return section("extract_database_runtime", in -> DatabaseConnectors.extractDatabaseRuntime(
                str(in, "database_type", "postgresql"), mapField(in, "snapshot")));
    }

    @TestFactory
    List<DynamicTest> extractApiRuntime() {
        return section("extract_api_runtime", in -> ApiConnectors.extractApiRuntime(
                str(in, "api_type", "rest"), mapField(in, "snapshot")));
    }

    @TestFactory
    List<DynamicTest> extractRuntimeStreams() {
        return section("extract_runtime_streams", in -> StreamConnectors.extractRuntimeStreams(
                listField(in, "stream_types"), mapField(in, "snapshot")));
    }

    @TestFactory
    List<DynamicTest> extractTelemetryRuntime() {
        return section("extract_telemetry_runtime", in -> TelemetryConnector.extractTelemetryRuntime(
                listField(in, "backends"), mapField(in, "snapshot")));
    }
}
