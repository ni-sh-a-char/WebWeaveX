package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.synchronization.SyncRuntime;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-10 cross-language parity: the entire {@code core.synchronization} family
 * (io.webweavex.synchronization.SyncRuntime) and its sub-engines are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s10.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}. save/load assert the written file content + recovered output.
 */
class CrossLanguageParityS10Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS10Test.class
                .getResourceAsStream("/parity/golden_vectors_s10.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s10.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s10 golden vectors", e);
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

    @SuppressWarnings("unchecked")
    private static List<Object> l(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static long lng(JsonNode in, String f, long d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asLong();
    }

    private static boolean b(JsonNode in, String f, boolean d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asBoolean();
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    // ---- 6 public APIs ----

    @TestFactory
    List<DynamicTest> buildRuntimeDelta() {
        return section("build_runtime_delta", in -> SyncRuntime.buildRuntimeDelta(
                m(in, "previous"), m(in, "current"), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> replaySynchronizedRuntime() {
        return section("replay_synchronized_runtime", in -> SyncRuntime.replaySynchronizedRuntime(m(in, "memory")));
    }

    @TestFactory
    List<DynamicTest> runSynchronizedRuntime() {
        return section("run_synchronized_runtime", in -> SyncRuntime.runSynchronizedRuntime(
                lng(in, "tick", 0), m(in, "browser"), m(in, "native"), m(in, "semantic_result"),
                m(in, "workflow_result"), m(in, "causality_result"), m(in, "distributed_result"),
                m(in, "session"), m(in, "identity"), m(in, "memory"), l(in, "workers")));
    }

    @TestFactory
    List<DynamicTest> runSyncForExtraction() {
        return section("run_sync_for_extraction", in -> SyncRuntime.runSyncForExtraction(
                b(in, "synchronized_runtime", true), s(in, "memory_path", ""), s(in, "memory_key", ""),
                lng(in, "tick", 0), m(in, "browser"), m(in, "native"), m(in, "semantic_result"),
                m(in, "workflow_result"), m(in, "causality_result"), m(in, "distributed_result"),
                m(in, "session"), m(in, "identity"), b(in, "merge_graph", true)));
    }

    @TestFactory
    List<DynamicTest> saveSyncMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_sync_memory")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = SyncRuntime.saveSyncMemory(
                        target.toString(), m(in, "memory"), in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
                assertEquals(target.toString(), ret.get("path"));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> loadSyncMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_sync_memory")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = SyncRuntime.loadSyncMemory(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = SyncRuntime.loadSyncMemory(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }

    // ---- engine-level parity ----

    @TestFactory
    List<DynamicTest> captureRuntimeSnapshot() {
        return section("capture_runtime_snapshot", in -> SyncRuntime.captureRuntimeSnapshot(
                m(in, "browser"), m(in, "native"), m(in, "semantic"), m(in, "workflow"), m(in, "causality"),
                m(in, "sync_state"), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> engineSections() {
        List<DynamicTest> tests = new ArrayList<>();
        tests.addAll(section("detect_runtime_drift", in -> SyncRuntime.detectRuntimeDrift(
                m(in, "baseline"), m(in, "current"))));
        tests.addAll(section("diff_runtime_state", in -> SyncRuntime.diffRuntimeState(
                m(in, "previous"), m(in, "current"))));
        tests.addAll(section("track_runtime_mutations", in -> SyncRuntime.trackRuntimeMutations(
                l(in, "changes"), lng(in, "tick", 0))));
        tests.addAll(section("merge_runtime_realities", in -> SyncRuntime.mergeRuntimeRealities(l(in, "realities"))));
        tests.addAll(section("converge_runtime_state", in -> SyncRuntime.convergeRuntimeState(l(in, "realities"))));
        tests.addAll(section("synchronize_runtime", in -> SyncRuntime.synchronizeRuntime(
                l(in, "snapshots"), lng(in, "tick", 0))));
        tests.addAll(section("replicate_runtime_reality", in -> SyncRuntime.replicateRuntimeReality(
                m(in, "source"), l(in, "workers"))));
        tests.addAll(section("federate_runtime_realities", in -> SyncRuntime.federateRuntimeRealities(
                l(in, "workers"), m(in, "browser"), m(in, "native"), m(in, "semantic"), m(in, "application"))));
        tests.addAll(section("align_runtime_layers", in -> SyncRuntime.alignRuntimeLayers(
                m(in, "browser"), m(in, "native"), m(in, "semantic"), m(in, "workflow"))));
        tests.addAll(section("maintain_runtime_continuity", in -> SyncRuntime.maintainRuntimeContinuity(
                m(in, "session"), m(in, "identity"), m(in, "workflow"), m(in, "semantic"), m(in, "checkpoint"))));
        tests.addAll(section("build_runtime_history", in -> SyncRuntime.buildRuntimeHistory(
                l(in, "deltas"), l(in, "workflows"))));
        tests.addAll(section("build_sync_timeline", in -> SyncRuntime.buildSyncTimeline(m(in, "history"))));
        tests.addAll(section("build_runtime_state_graph", in -> SyncRuntime.buildRuntimeStateGraph(
                m(in, "snapshot"), m(in, "delta"), m(in, "convergence"))));
        tests.addAll(section("verify_runtime_consistency", in -> SyncRuntime.verifyRuntimeConsistency(
                m(in, "history"), m(in, "convergence"), m(in, "replay"))));
        tests.addAll(section("remember_sync_runtime", in -> SyncRuntime.rememberSyncRuntime(
                m(in, "memory"), m(in, "update"))));
        return tests;
    }
}
