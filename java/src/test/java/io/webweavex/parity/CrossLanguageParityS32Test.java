package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.multimodal.MultimodalRuntime;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-32 cross-language parity: the OCR cluster ({@code extract_multimodal}, {@code ingest_input},
 * {@code detect_input_type}) is byte-identical to canonical Python 2.1.0 ({@code golden_vectors_s32.json})
 * under the canonical OCR-absent contract (matches the JS port's hardcoded {@code pytesseract = null}).
 * Frontier reduction: the OCR family is portable for this contract — superseding the prior blocker.
 */
class CrossLanguageParityS32Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS32Test.class
                .getResourceAsStream("/parity/golden_vectors_s32.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s32.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s32 golden vectors", e);
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

    private static String path(JsonNode in) {
        return in.get("path").asText();
    }

    @TestFactory
    List<DynamicTest> ocrCluster() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("extract_multimodal", in -> MultimodalRuntime.extractMultimodal(path(in))));
        t.addAll(section("ingest_input", in -> MultimodalRuntime.ingestInput(path(in))));
        t.addAll(section("detect_input_type", in -> MultimodalRuntime.detectInputType(path(in))));
        return t;
    }
}
