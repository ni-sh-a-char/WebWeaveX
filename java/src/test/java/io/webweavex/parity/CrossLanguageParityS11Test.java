package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.workflow.WorkflowRuntime;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-11 cross-language parity: the entire {@code core.workflows} family
 * (io.webweavex.workflow.WorkflowRuntime) and its sub-engines are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s11.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS11Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS11Test.class
                .getResourceAsStream("/parity/golden_vectors_s11.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s11.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s11 golden vectors", e);
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

    // ---- 7 public APIs ----

    @TestFactory
    List<DynamicTest> buildRuntimeObjective() {
        return section("build_runtime_objective", in -> WorkflowRuntime.buildRuntimeObjective(
                s(in, "objective", "extract_dashboard"), lng(in, "priority", 0)));
    }

    @TestFactory
    List<DynamicTest> buildWorkflowPlan() {
        return section("build_workflow_plan", in -> WorkflowRuntime.buildWorkflowPlan(
                s(in, "objective", "extract_dashboard"), m(in, "semantic_runtime"), m(in, "causality"),
                m(in, "application_runtime")));
    }

    @TestFactory
    List<DynamicTest> replayWorkflowRuntime() {
        return section("replay_workflow_runtime", in -> WorkflowRuntime.replayWorkflowRuntime(m(in, "memory")));
    }

    @TestFactory
    List<DynamicTest> runAutonomousWorkflow() {
        return section("run_autonomous_workflow", in -> WorkflowRuntime.runAutonomousWorkflow(
                s(in, "objective", "extract_dashboard"), lng(in, "priority", 0), m(in, "semantic_runtime"),
                m(in, "causality_result"), m(in, "application_result"), m(in, "distributed_result"),
                m(in, "native_cognition"), s(in, "url", ""), m(in, "memory"), lng(in, "tick", 0),
                l(in, "failures")));
    }

    @TestFactory
    List<DynamicTest> runWorkflowForExtraction() {
        return section("run_workflow_for_extraction", in -> WorkflowRuntime.runWorkflowForExtraction(
                b(in, "autonomous_workflow", true), s(in, "objective", "extract_dashboard"),
                s(in, "memory_path", ""), s(in, "memory_key", ""), s(in, "url", ""), m(in, "semantic_runtime"),
                m(in, "causality_result"), m(in, "application_result"), m(in, "distributed_result"),
                m(in, "native_cognition"), b(in, "merge_graph", true), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> saveWorkflowMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_workflow_memory")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = WorkflowRuntime.saveWorkflowMemory(
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
    List<DynamicTest> loadWorkflowMemory() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_workflow_memory")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = WorkflowRuntime.loadWorkflowMemory(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = WorkflowRuntime.loadWorkflowMemory(target.toString(), v.get("key").asText());
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
        List<DynamicTest> tests = new ArrayList<>();
        tests.addAll(section("execute_workflow_plan", in -> WorkflowRuntime.executeWorkflowPlan(
                m(in, "plan"), lng(in, "tick", 0))));
        tests.addAll(section("build_workflow_state", in -> WorkflowRuntime.buildWorkflowState(
                m(in, "plan"), m(in, "execution"))));
        tests.addAll(section("navigate_runtime_workflow", in -> WorkflowRuntime.navigateRuntimeWorkflow(
                m(in, "plan"), lng(in, "tick", 0))));
        tests.addAll(section("build_workflow_transitions", in -> {
            Map<String, Object> wrap = new LinkedHashMap<>();
            wrap.put("transitions", WorkflowRuntime.buildWorkflowTransitions(m(in, "execution")));
            return wrap;
        }));
        tests.addAll(section("build_workflow_dependencies", in -> WorkflowRuntime.buildWorkflowDependencies(
                m(in, "plan"))));
        tests.addAll(section("recover_workflow_runtime", in -> WorkflowRuntime.recoverWorkflowRuntime(
                m(in, "state"), l(in, "failures"))));
        tests.addAll(section("align_workflow_runtime", in -> WorkflowRuntime.alignWorkflowRuntime(
                m(in, "plan"), m(in, "state"), m(in, "execution"))));
        tests.addAll(section("align_workflow_semantics", in -> WorkflowRuntime.alignWorkflowSemantics(
                m(in, "plan"), m(in, "semantic_runtime"), m(in, "causality"))));
        tests.addAll(section("federate_workflow_runtime", in -> WorkflowRuntime.federateWorkflowRuntime(
                m(in, "browser"), m(in, "native"), m(in, "distributed"), m(in, "semantic"), l(in, "workers"))));
        tests.addAll(section("schedule_workflow_execution", in -> WorkflowRuntime.scheduleWorkflowExecution(
                l(in, "plans"), lng(in, "tick", 0))));
        tests.addAll(section("build_workflow_runtime_context", in -> WorkflowRuntime.buildWorkflowRuntimeContext(
                s(in, "url", ""), s(in, "runtime", "browser"), m(in, "sources"))));
        tests.addAll(section("build_workflow_graph", in -> WorkflowRuntime.buildWorkflowGraph(
                m(in, "objective"), m(in, "plan"), m(in, "state"), m(in, "execution"), l(in, "transitions"))));
        tests.addAll(section("remember_workflow_runtime", in -> WorkflowRuntime.rememberWorkflowRuntime(
                m(in, "memory"), m(in, "update"))));
        return tests;
    }
}
