package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.adaptive.SelectorHealing;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-21 cross-language parity: {@code heal_selector} for the portable empty-HTML contract
 * (io.webweavex.adaptive.SelectorHealing) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s21.json}). The empty-HTML path is bs4-independent (the semantic anchor
 * yields nothing), so this certifies the full pure {@code dom_nodes} healing logic byte-exact.
 */
class CrossLanguageParityS21Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS21Test.class
                .getResourceAsStream("/parity/golden_vectors_s21.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s21.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s21 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    @TestFactory
    List<DynamicTest> healSelector() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("heal_selector")) {
            tests.add(DynamicTest.dynamicTest("heal_selector:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                List<Object> domNodes = (List<Object>) CrossLanguageParityTest.toNative(in.get("dom_nodes"));
                Object out = SelectorHealing.healSelector(in.get("selector").asText(), domNodes);
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }
}
