package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.connectors.ContainerConnector;
import io.webweavex.connectors.IdeConnector;
import io.webweavex.connectors.KubernetesConnector;
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
 * Session-7 cross-language parity: the remaining dependency-clean connector-runtime cluster
 * (container / ide / kubernetes) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s7.json}). Every assertion compares Java output to recorded Python
 * output via {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS7Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS7Test.class
                .getResourceAsStream("/parity/golden_vectors_s7.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s7.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s7 golden vectors", e);
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
    List<DynamicTest> extractContainerRuntime() {
        return section("extract_container_runtime", in -> ContainerConnector.extractContainerRuntime(
                str(in, "runtime", "docker"), mapField(in, "snapshot")));
    }

    @TestFactory
    List<DynamicTest> extractIdeRuntime() {
        return section("extract_ide_runtime", in -> IdeConnector.extractIdeRuntime(
                str(in, "ide", "vscode"), mapField(in, "snapshot")));
    }

    @TestFactory
    List<DynamicTest> extractKubernetesRuntime() {
        return section("extract_kubernetes_runtime", in -> KubernetesConnector.extractKubernetesRuntime(
                mapField(in, "snapshot")));
    }
}
