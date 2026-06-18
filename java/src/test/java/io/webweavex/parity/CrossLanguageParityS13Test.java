package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.causality.CausalityRuntime;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
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
 * Session-13 cross-language parity: the entire {@code core.causality} family
 * (io.webweavex.causality.CausalityRuntime) and its sub-engines are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s13.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS13Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS13Test.class
                .getResourceAsStream("/parity/golden_vectors_s13.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s13.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s13 golden vectors", e);
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

    private static boolean b(JsonNode in, String f, boolean d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asBoolean();
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    // ---- 5 public APIs ----

    @TestFactory
    List<DynamicTest> runCausalityRuntime() {
        return section("run_causality_runtime", in -> CausalityRuntime.runCausalityRuntime(
                l(in, "browser_events"), m(in, "native_cognition"), m(in, "application_result"),
                m(in, "distributed_result"), m(in, "memory"), l(in, "interactions")));
    }

    @TestFactory
    List<DynamicTest> replayCausalRuntime() {
        return section("replay_causal_runtime", in -> CausalityRuntime.replayCausalRuntime(m(in, "memory")));
    }

    @TestFactory
    List<DynamicTest> runCausalityForExtraction() {
        return section("run_causality_for_extraction", in -> CausalityRuntime.runCausalityForExtraction(
                b(in, "causality_runtime", true), s(in, "memory_path", ""), s(in, "memory_key", ""),
                l(in, "browser_events"), m(in, "native_cognition"), m(in, "application_result"),
                m(in, "distributed_result"), l(in, "interactions"), b(in, "merge_graph", true)));
    }

    @TestFactory
    List<DynamicTest> saveCausalMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_causal_memory")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = CausalityRuntime.saveCausalMemory(
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
    List<DynamicTest> loadCausalMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_causal_memory")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = CausalityRuntime.loadCausalMemory(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = CausalityRuntime.loadCausalMemory(target.toString(), v.get("key").asText());
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
        t.addAll(section("build_runtime_causality", in -> CausalityRuntime.buildRuntimeCausality(
                l(in, "events"), m(in, "origins"))));
        t.addAll(section("build_event_chain", in -> CausalityRuntime.buildEventChain(l(in, "events"))));
        t.addAll(section("align_cross_runtime_events", in -> CausalityRuntime.alignCrossRuntimeEvents(l(in, "events"))));
        t.addAll(section("build_runtime_dependencies", in -> CausalityRuntime.buildRuntimeDependencies(
                l(in, "events"), m(in, "propagation"))));
        t.addAll(section("build_workflow_propagation", in -> CausalityRuntime.buildWorkflowPropagation(
                m(in, "aligned"), m(in, "dependencies"))));
        t.addAll(section("build_causal_graph", in -> CausalityRuntime.buildCausalGraph(
                l(in, "events"), m(in, "causality"))));
        t.addAll(section("build_state_transitions", in -> CausalityRuntime.buildStateTransitions(l(in, "events"))));
        t.addAll(section("build_runtime_sequence", in -> CausalityRuntime.buildRuntimeSequence(l(in, "events"))));
        t.addAll(section("build_runtime_timeline", in -> CausalityRuntime.buildRuntimeTimeline(
                l(in, "events"), m(in, "propagation"))));
        t.addAll(section("correlate_runtime_mutations", in -> CausalityRuntime.correlateRuntimeMutations(
                l(in, "browser_events"), l(in, "native_events"), l(in, "notifications"), l(in, "terminal_lines"),
                l(in, "process_events"))));
        t.addAll(section("build_distributed_causality", in -> CausalityRuntime.buildDistributedCausality(
                m(in, "distributed_result"), l(in, "worker_events"))));
        t.addAll(section("bridge_browser_native_runtime", in -> CausalityRuntime.bridgeBrowserNativeRuntime(
                l(in, "browser_events"), l(in, "native_events"))));
        t.addAll(section("bridge_electron_terminal_runtime", in -> CausalityRuntime.bridgeElectronTerminalRuntime(
                l(in, "electron_events"), l(in, "terminal_events"))));
        t.addAll(section("track_notification_causality", in -> CausalityRuntime.trackNotificationCausality(
                l(in, "notifications"), l(in, "origin_events"))));
        t.addAll(section("track_process_causality", in -> CausalityRuntime.trackProcessCausality(
                l(in, "processes"), l(in, "events"))));
        t.addAll(section("recover_causal_runtime", in -> CausalityRuntime.recoverCausalRuntime(
                m(in, "causality"), l(in, "events"))));
        t.addAll(section("remember_causal_runtime", in -> CausalityRuntime.rememberCausalRuntime(
                m(in, "memory"), m(in, "update"))));
        return t;
    }
}
