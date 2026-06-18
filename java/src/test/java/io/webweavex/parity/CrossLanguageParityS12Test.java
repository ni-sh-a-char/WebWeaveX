package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.evolution.EvolutionRuntime;
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
 * Session-12 cross-language parity: the entire {@code core.evolution_runtime} family
 * (io.webweavex.evolution.EvolutionRuntime) and its sub-engines are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s12.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS12Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS12Test.class
                .getResourceAsStream("/parity/golden_vectors_s12.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s12.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s12 golden vectors", e);
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

    private static Map<String, Object> wrap(String key, Object value) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put(key, value);
        return m;
    }

    // ---- 6 public APIs ----

    @TestFactory
    List<DynamicTest> buildRuntimeEvolution() {
        return section("build_runtime_evolution", in -> EvolutionRuntime.buildRuntimeEvolution(
                l(in, "mutations"), l(in, "lineage")));
    }

    @TestFactory
    List<DynamicTest> evolveSelectorRuntime() {
        return section("evolve_selector_runtime", in -> EvolutionRuntime.evolveSelectorRuntime(
                m(in, "selectors"), m(in, "healed")));
    }

    @TestFactory
    List<DynamicTest> runEvolutionRuntime() {
        return section("run_evolution_runtime", in -> EvolutionRuntime.runEvolutionRuntime(
                m(in, "adaptive_memory"), m(in, "workflow_result"), m(in, "semantic_result"), m(in, "sync_result"),
                m(in, "distributed_result"), l(in, "failures"), m(in, "memory"), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> runEvolutionForExtraction() {
        return section("run_evolution_for_extraction", in -> EvolutionRuntime.runEvolutionForExtraction(
                b(in, "evolving_runtime", true), s(in, "memory_path", ""), s(in, "memory_key", ""),
                m(in, "adaptive_memory"), m(in, "workflow_result"), m(in, "semantic_result"), m(in, "sync_result"),
                m(in, "distributed_result"), l(in, "failures"), lng(in, "tick", 0), b(in, "merge_graph", true)));
    }

    @TestFactory
    List<DynamicTest> saveEvolutionRuntime() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_evolution_runtime")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = EvolutionRuntime.saveEvolutionRuntime(
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
    List<DynamicTest> loadEvolutionRuntime() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_evolution_runtime")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = EvolutionRuntime.loadEvolutionRuntime(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = EvolutionRuntime.loadEvolutionRuntime(target.toString(), v.get("key").asText());
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
        tests.addAll(section("evolve_workflow_runtime", in -> EvolutionRuntime.evolveWorkflowRuntime(
                m(in, "plan"), m(in, "execution"), l(in, "history"))));
        tests.addAll(section("evolve_semantic_runtime", in -> EvolutionRuntime.evolveSemanticRuntime(
                m(in, "semantic"), l(in, "history"))));
        tests.addAll(section("evolve_runtime_topology", in -> EvolutionRuntime.evolveRuntimeTopology(
                l(in, "workers"), m(in, "sync"), m(in, "causality"))));
        tests.addAll(section("build_runtime_strategy", in -> EvolutionRuntime.buildRuntimeStrategy(
                m(in, "evidence"))));
        tests.addAll(section("repair_runtime_failures", in -> EvolutionRuntime.repairRuntimeFailures(
                l(in, "failures"), m(in, "selectors"))));
        tests.addAll(section("evolve_recovery_order", in -> EvolutionRuntime.evolveRecoveryOrder(l(in, "repairs"))));
        tests.addAll(section("optimize_runtime_execution", in -> EvolutionRuntime.optimizeRuntimeExecution(
                lng(in, "depth", 0), lng(in, "replay_cost", 0), lng(in, "sync_overhead", 0))));
        tests.addAll(section("adapt_runtime_strategy", in -> EvolutionRuntime.adaptRuntimeStrategy(
                m(in, "strategy"), m(in, "optimization"))));
        tests.addAll(section("build_runtime_mutations", in -> wrap("mutations",
                EvolutionRuntime.buildRuntimeMutations(m(in, "selector"), m(in, "workflow"), m(in, "semantic"),
                        m(in, "sync")))));
        tests.addAll(section("build_runtime_lineage", in -> wrap("lineage",
                EvolutionRuntime.buildRuntimeLineage(s(in, "evolution_id", ""), l(in, "mutations"),
                        s(in, "parent_id", "")))));
        tests.addAll(section("build_runtime_policy", in -> EvolutionRuntime.buildRuntimePolicy()));
        tests.addAll(section("enforce_runtime_policy", in -> EvolutionRuntime.enforceRuntimePolicy(
                m(in, "policy"), l(in, "mutations"), l(in, "repairs"), lng(in, "depth", 0))));
        tests.addAll(section("build_runtime_patterns", in -> EvolutionRuntime.buildRuntimePatterns(
                m(in, "ui"), l(in, "workflows"), m(in, "semantic"), l(in, "sync_history"))));
        tests.addAll(section("converge_runtime_evolution", in -> EvolutionRuntime.convergeRuntimeEvolution(
                l(in, "evolutions"))));
        tests.addAll(section("diff_evolution_runtime", in -> EvolutionRuntime.diffEvolutionRuntime(
                m(in, "previous"), m(in, "current"))));
        tests.addAll(section("build_runtime_evolution_graph", in -> EvolutionRuntime.buildRuntimeEvolutionGraph(
                m(in, "evolution"), m(in, "repairs"), m(in, "optimization"))));
        tests.addAll(section("remember_evolution_runtime", in -> EvolutionRuntime.rememberEvolutionRuntime(
                m(in, "memory"), m(in, "update"))));
        return tests;
    }
}
