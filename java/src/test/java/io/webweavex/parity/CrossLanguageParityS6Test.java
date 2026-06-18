package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.interaction.InteractionGraph;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-6 cross-language parity: {@code build_interaction_graph}
 * (io.webweavex.interaction.InteractionGraph) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s6.json}). Every assertion compares Java output to recorded Python
 * output via {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS6Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS6Test.class
                .getResourceAsStream("/parity/golden_vectors_s6.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s6.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s6 golden vectors", e);
        }
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

    @SuppressWarnings("unchecked")
    private static List<Object> listField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    @TestFactory
    List<DynamicTest> buildInteractionGraph() {
        return section("build_interaction_graph", in -> InteractionGraph.buildInteractionGraph(
                listField(in, "interactions")));
    }
}
