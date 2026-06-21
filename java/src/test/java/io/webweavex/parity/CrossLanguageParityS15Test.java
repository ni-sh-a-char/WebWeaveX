package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.adaptive.ModalRecovery;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-15 cross-language parity: {@code recover_modal_runtime}
 * (io.webweavex.adaptive.ModalRecovery) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s15.json}) via {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS15Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS15Test.class
                .getResourceAsStream("/parity/golden_vectors_s15.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s15.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s15 golden vectors", e);
        }
    }

    @TestFactory
    List<DynamicTest> recoverModalRuntime() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("recover_modal_runtime")) {
            tests.add(DynamicTest.dynamicTest("recover_modal_runtime:" + v.get("name").asText(), () -> {
                Object output = ModalRecovery.recoverModalRuntime(v.get("inputs").get("html").asText());
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }
}
