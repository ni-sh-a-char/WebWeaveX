package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.reconstruction.ReconstructionRuntime;
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
 * Session-16 cross-language parity: the {@code core.reconstruction} orchestrator
 * (io.webweavex.reconstruction.ReconstructionRuntime) + its sub-engines are byte-identical to
 * canonical Python 2.1.0 ({@code golden_vectors_s16.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS16Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS16Test.class
                .getResourceAsStream("/parity/golden_vectors_s16.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s16.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s16 golden vectors", e);
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

    // ---- manifest APIs ----

    @TestFactory
    List<DynamicTest> runReconstructionRuntime() {
        return section("run_reconstruction_runtime", in -> ReconstructionRuntime.runReconstructionRuntime(
                m(in, "sources"), m(in, "stored"), m(in, "runtime_graph"), s(in, "runtime_type", "browser"),
                lng(in, "tick", 0), b(in, "fabricate", false), b(in, "clone", false)));
    }

    @TestFactory
    List<DynamicTest> runReconstructionForExtraction() {
        return section("run_reconstruction_for_extraction", in -> ReconstructionRuntime.runReconstructionForExtraction(
                b(in, "reconstruction_runtime", true), s(in, "memory_path", ""), s(in, "memory_key", ""),
                m(in, "sources"), m(in, "runtime_graph"), s(in, "runtime_type", "browser"), lng(in, "tick", 0),
                b(in, "fabricate_runtime", false), b(in, "clone_runtime", false), b(in, "merge_graph", true)));
    }

    @TestFactory
    List<DynamicTest> saveReconstructionSnapshot() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_reconstruction_snapshot")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = ReconstructionRuntime.saveReconstructionSnapshot(
                        target.toString(), m(in, "snapshot"), in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> loadReconstructionSnapshot() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_reconstruction_snapshot")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = ReconstructionRuntime.loadReconstructionSnapshot(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = ReconstructionRuntime.loadReconstructionSnapshot(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }

    // ---- engine-level parity ----

    @TestFactory
    List<DynamicTest> engineSections() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("reconstruct_application_runtime", in -> ReconstructionRuntime.reconstructApplicationRuntime(
                m(in, "application_ir"), m(in, "workflow_ir"), m(in, "execution_ir"), s(in, "runtime_type", "browser"))));
        t.addAll(section("build_runtime_environment", in -> ReconstructionRuntime.buildRuntimeEnvironment(
                s(in, "runtime", "browser"), l(in, "connectors"), l(in, "workers"))));
        t.addAll(section("reconstruct_runtime_session", in -> ReconstructionRuntime.reconstructRuntimeSession(
                m(in, "session"), m(in, "identity"), m(in, "sync_state"), m(in, "adaptive_memory"))));
        t.addAll(section("reconstruct_runtime_identity", in -> ReconstructionRuntime.reconstructRuntimeIdentity(
                m(in, "browser_identity"), m(in, "session"), s(in, "runtime_id", ""), s(in, "execution_id", ""),
                s(in, "worker_id", ""))));
        t.addAll(section("reconstruct_runtime_topology", in -> ReconstructionRuntime.reconstructRuntimeTopology(
                m(in, "runtime_graph"), l(in, "workers"), l(in, "connectors"), m(in, "execution_topology"),
                m(in, "sync_topology"))));
        t.addAll(section("reconstruct_connector_runtime", in -> ReconstructionRuntime.reconstructConnectorRuntime(
                l(in, "connectors"), m(in, "live_ir"))));
        t.addAll(section("recover_reconstructed_runtime", in -> ReconstructionRuntime.recoverReconstructedRuntime(
                m(in, "checkpoint"), l(in, "failed_segments"))));
        t.addAll(section("build_runtime_timeline", in -> ReconstructionRuntime.buildRuntimeTimeline(
                l(in, "events"), l(in, "actions"), l(in, "mutations"), l(in, "synchronization"), l(in, "execution"),
                l(in, "recovery"), l(in, "replay"), lng(in, "tick", 0))));
        t.addAll(section("build_runtime_replay", in -> ReconstructionRuntime.buildRuntimeReplay(
                l(in, "actions"), l(in, "transactions"), m(in, "timeline"), lng(in, "tick", 0))));
        t.addAll(section("rebuild_runtime_state", in -> ReconstructionRuntime.rebuildRuntimeState(
                l(in, "queues"), m(in, "synchronization"), l(in, "mutations"), l(in, "transactions"), m(in, "memory"),
                l(in, "execution_lineage"), l(in, "workflows"))));
        t.addAll(section("clone_runtime_environment", in -> ReconstructionRuntime.cloneRuntimeEnvironment(
                m(in, "source"))));
        t.addAll(section("fabricate_runtime_reality", in -> ReconstructionRuntime.fabricateRuntimeReality(
                m(in, "runtime"), m(in, "environment"), m(in, "browser"), m(in, "application"), true)));
        t.addAll(section("capture_reconstruction_snapshot", in -> ReconstructionRuntime.captureReconstructionSnapshot(
                m(in, "state"))));
        t.addAll(section("restore_reconstruction_snapshot", in -> ReconstructionRuntime.restoreReconstructionSnapshot(
                m(in, "snapshot"))));
        t.addAll(section("compile_reconstruction_runtime_ir", in -> ReconstructionRuntime.compileReconstructionRuntimeIr(
                m(in, "payload"))));
        t.addAll(section("reconstruction_runtime_ir_to_graph", in -> ReconstructionRuntime.reconstructionRuntimeIrToGraph(
                m(in, "ir"))));
        return t;
    }
}
