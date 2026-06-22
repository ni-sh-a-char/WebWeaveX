package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.memory.MemoryPersistence;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-17 cross-language parity: the four dependency-clean memory-persistence engine pairs
 * (io.webweavex.memory.MemoryPersistence — runtime/semantic/adaptive/application) are byte-identical
 * to canonical Python 2.1.0 ({@code golden_vectors_s17.json}). Save asserts written file content
 * byte-for-byte; load asserts the recovered output via {@code stable_serialize} +
 * {@code compute_kaalka_hash}, including the missing-file branch.
 */
class CrossLanguageParityS17Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS17Test.class
                .getResourceAsStream("/parity/golden_vectors_s17.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s17.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s17 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMemory(JsonNode n) {
        return (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    /** save_*_memory: file content is byte-exact vs the Python oracle. */
    private List<DynamicTest> saveSection(String section,
            io.webweavex.parity.CrossLanguageParityS17Test.Save save) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(section)) {
            tests.add(DynamicTest.dynamicTest(section + ":" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = save.apply(target.toString(), asMemory(in.get("memory")),
                        in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
            }));
        }
        return tests;
    }

    /** load_*_memory: recovered output is byte-exact; missing-file branch covered. */
    private List<DynamicTest> loadSection(String section, BiFunction<String, String, Map<String, Object>> load) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(section)) {
            tests.add(DynamicTest.dynamicTest(section + ":" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = load.apply(tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + "_" + section + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = load.apply(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }

    @FunctionalInterface
    interface Save {
        Map<String, Object> apply(String path, Map<String, Object> memory, String key);
    }

    @TestFactory
    List<DynamicTest> saveRuntimeMemory() {
        return saveSection("save_runtime_memory", MemoryPersistence::saveRuntimeMemory);
    }

    @TestFactory
    List<DynamicTest> loadRuntimeMemory() {
        return loadSection("load_runtime_memory", MemoryPersistence::loadRuntimeMemory);
    }

    @TestFactory
    List<DynamicTest> saveSemanticMemory() {
        return saveSection("save_semantic_memory", MemoryPersistence::saveSemanticMemory);
    }

    @TestFactory
    List<DynamicTest> loadSemanticMemory() {
        return loadSection("load_semantic_memory", MemoryPersistence::loadSemanticMemory);
    }

    @TestFactory
    List<DynamicTest> saveAdaptiveMemory() {
        return saveSection("save_adaptive_memory", MemoryPersistence::saveAdaptiveMemory);
    }

    @TestFactory
    List<DynamicTest> loadAdaptiveMemory() {
        return loadSection("load_adaptive_memory", MemoryPersistence::loadAdaptiveMemory);
    }

    @TestFactory
    List<DynamicTest> saveApplicationMemory() {
        return saveSection("save_application_memory", MemoryPersistence::saveApplicationMemory);
    }

    @TestFactory
    List<DynamicTest> loadApplicationMemory() {
        return loadSection("load_application_memory", MemoryPersistence::loadApplicationMemory);
    }
}
