package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.memory.RuntimeMemoryRuntime;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-20 cross-language parity: the {@code core.memory} orchestrator
 * (io.webweavex.memory.RuntimeMemoryRuntime) + its sub-engines — the final dependency-clean slice —
 * is byte-identical to canonical Python 2.1.0 ({@code golden_vectors_s20.json}) via
 * {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS20Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS20Test.class
                .getResourceAsStream("/parity/golden_vectors_s20.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s20.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s20 golden vectors", e);
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

    @TestFactory
    List<DynamicTest> orchestrator() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("run_runtime_memory", in -> RuntimeMemoryRuntime.runRuntimeMemory(
                m(in, "sources"), m(in, "stored"), l(in, "nodes"), lng(in, "tick", 0))));
        t.addAll(section("run_memory_for_extraction", in -> RuntimeMemoryRuntime.runMemoryForExtraction(
                b(in, "federated_memory", true), "", "", m(in, "sources"), l(in, "nodes"), lng(in, "tick", 0),
                b(in, "merge_graph", true))));
        return t;
    }

    @TestFactory
    List<DynamicTest> engineSections() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("append_runtime_history", in -> {
            Map<String, Object> w = new LinkedHashMap<>();
            w.put("history", RuntimeMemoryRuntime.appendRuntimeHistory(l(in, "history"), m(in, "entry")));
            return w;
        }));
        t.addAll(section("build_knowledge_memory", in -> RuntimeMemoryRuntime.buildKnowledgeMemory(
                l(in, "entities"), l(in, "relations"), m(in, "topology"))));
        t.addAll(section("build_semantic_memory", in -> RuntimeMemoryRuntime.buildSemanticMemory(
                m(in, "semantic"), l(in, "history"))));
        t.addAll(section("build_runtime_lineage_memory", in -> RuntimeMemoryRuntime.buildRuntimeLineageMemory(
                l(in, "selector"), l(in, "workflow"), l(in, "sync"), l(in, "evolution"), l(in, "extraction"))));
        t.addAll(section("build_runtime_memory_graph", in -> RuntimeMemoryRuntime.buildRuntimeMemoryGraph(
                l(in, "entities"), l(in, "relations"))));
        t.addAll(section("build_runtime_index", in -> RuntimeMemoryRuntime.buildRuntimeIndex(
                l(in, "entities"), l(in, "workflows"), l(in, "graphs"), l(in, "streams"), l(in, "connectors"))));
        t.addAll(section("replicate_runtime_memory", in -> RuntimeMemoryRuntime.replicateRuntimeMemory(
                m(in, "source"), l(in, "nodes"))));
        t.addAll(section("converge_runtime_memory", in -> RuntimeMemoryRuntime.convergeRuntimeMemory(l(in, "replicas"))));
        t.addAll(section("build_distributed_memory", in -> RuntimeMemoryRuntime.buildDistributedMemory(l(in, "nodes"))));
        t.addAll(section("federate_runtime_memory", in -> RuntimeMemoryRuntime.federateRuntimeMemory(l(in, "memories"))));
        t.addAll(section("merge_runtime_memories", in -> RuntimeMemoryRuntime.mergeRuntimeMemories(l(in, "memories"))));
        t.addAll(section("build_runtime_memory_policy", in -> RuntimeMemoryRuntime.buildRuntimeMemoryPolicy()));
        t.addAll(section("enforce_memory_policy", in -> RuntimeMemoryRuntime.enforceMemoryPolicy(
                m(in, "policy"), l(in, "history"), l(in, "lineage"), lng(in, "replicas", 0))));
        t.addAll(section("diff_runtime_memory", in -> RuntimeMemoryRuntime.diffRuntimeMemory(
                m(in, "previous"), m(in, "current"))));
        t.addAll(section("capture_memory_snapshot", in -> RuntimeMemoryRuntime.captureMemorySnapshot(
                m(in, "state"), lng(in, "tick", 0))));
        t.addAll(section("compile_runtime_memory_ir", in -> RuntimeMemoryRuntime.compileRuntimeMemoryIr(m(in, "payload"))));
        t.addAll(section("runtime_memory_ir_to_graph", in -> RuntimeMemoryRuntime.runtimeMemoryIrToGraph(m(in, "ir"))));
        return t;
    }
}
