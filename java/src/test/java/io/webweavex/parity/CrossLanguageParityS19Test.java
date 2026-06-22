package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.application.ObjectiveExecution;
import io.webweavex.auth.AuthenticationRuntime;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.distributed.DistributedCheckpoint;
import io.webweavex.memory.NativeRuntimePersistence;
import io.webweavex.repository.RepositoryQuery;
import io.webweavex.semantic.SemanticReplay;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-19 cross-language parity: the dependency-clean remainder slice — distributed-checkpoint
 * and native-runtime persistence, semantic replay, objective execution, repository query, and the
 * page-independent authenticate path — is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s19.json}).
 */
class CrossLanguageParityS19Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS19Test.class
                .getResourceAsStream("/parity/golden_vectors_s19.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s19.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s19 golden vectors", e);
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
    private static Map<String, Object> m(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    @TestFactory
    List<DynamicTest> pureTransforms() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("replay_semantic_runtime", in -> SemanticReplay.replaySemanticRuntime(m(in, "memory"))));
        t.addAll(section("execute_runtime_objective", in -> ObjectiveExecution.executeRuntimeObjective(
                s(in, "objective", ""), m(in, "workflow_graph"), m(in, "action_graph"), m(in, "navigation"),
                m(in, "adaptive_runtime"))));
        t.addAll(section("query_repository", in -> {
            Map<String, Object> wrap = new LinkedHashMap<>();
            wrap.put("repo", RepositoryQuery.queryRepository(m(in, "result"), s(in, "key", "")));
            return wrap;
        }));
        t.addAll(section("authenticate_runtime", in -> AuthenticationRuntime.authenticateRuntime(
                m(in, "credentials"), m(in, "config"))));
        return t;
    }

    // ---- persistence ----

    private List<DynamicTest> saveSection(String section, Save save) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(section)) {
            tests.add(DynamicTest.dynamicTest(section + ":" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = save.apply(target.toString(), m(in, "payload"), in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
            }));
        }
        return tests;
    }

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
        Map<String, Object> apply(String path, Map<String, Object> payload, String key);
    }

    @TestFactory
    List<DynamicTest> saveDistributedCheckpoint() {
        return saveSection("save_distributed_checkpoint", DistributedCheckpoint::saveDistributedCheckpoint);
    }

    @TestFactory
    List<DynamicTest> loadDistributedCheckpoint() {
        return loadSection("load_distributed_checkpoint", DistributedCheckpoint::loadDistributedCheckpoint);
    }

    @TestFactory
    List<DynamicTest> saveNativeRuntime() {
        return saveSection("save_native_runtime", NativeRuntimePersistence::saveNativeRuntime);
    }

    @TestFactory
    List<DynamicTest> loadNativeRuntime() {
        return loadSection("load_native_runtime", NativeRuntimePersistence::loadNativeRuntime);
    }
}
