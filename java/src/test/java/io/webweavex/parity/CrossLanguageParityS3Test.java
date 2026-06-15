package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.graph.GraphReconstruction;
import io.webweavex.memory.MemoryQuery;
import io.webweavex.memory.MemorySearch;
import io.webweavex.memory.RuntimeMemory;
import io.webweavex.query.GraphQuery;
import io.webweavex.query.OntologyQuery;
import io.webweavex.query.TopologyReasoning;
import io.webweavex.reconstruction.BrowserReconstruction;
import io.webweavex.reconstruction.MemoryReconstruction;
import io.webweavex.reconstruction.RuntimeReconstruction;
import io.webweavex.reconstruction.RuntimeValidation;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-3 cross-language parity: query / memory / reconstruction are
 * byte-identical to canonical Python 2.1.0 ({@code golden_vectors_s3.json}).
 * Cross-language proof only — every assertion compares Java output to recorded
 * Python output (stable serialization + hash).
 */
class CrossLanguageParityS3Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS3Test.class
                .getResourceAsStream("/parity/golden_vectors_s3.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s3.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s3 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> listField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String str(JsonNode inputs, String field, String dflt) {
        JsonNode n = inputs.get(field);
        return n == null || n.isNull() ? dflt : n.asText();
    }

    private static long lng(JsonNode inputs, String field, long dflt) {
        JsonNode n = inputs.get(field);
        return n == null || n.isNull() ? dflt : n.asLong();
    }

    /** Builds dynamic tests for one section, applying {@code fn} to each entry's inputs. */
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

    @TestFactory
    List<DynamicTest> queryGraph() {
        return section("query_graph", in ->
                GraphQuery.queryGraph(mapField(in, "graph"), str(in, "node", "")));
    }

    @TestFactory
    List<DynamicTest> queryRuntimeGraph() {
        return section("query_runtime_graph", in ->
                GraphQuery.queryRuntimeGraph(mapField(in, "graph"), mapField(in, "query")));
    }

    @TestFactory
    List<DynamicTest> queryKnowledge() {
        return section("query_knowledge", in ->
                OntologyQuery.queryKnowledge(listField(in, "entities"), listField(in, "edges")));
    }

    @TestFactory
    List<DynamicTest> reasonTopology() {
        return section("reason_topology", in -> TopologyReasoning.reasonTopology(mapField(in, "graph")));
    }

    @TestFactory
    List<DynamicTest> buildRuntimeMemory() {
        return section("build_runtime_memory", in -> RuntimeMemory.build(
                listField(in, "runtime_history"), listField(in, "lineage"),
                listField(in, "semantic_relations")));
    }

    @TestFactory
    List<DynamicTest> queryRuntimeMemory() {
        return section("query_runtime_memory", in -> MemoryQuery.queryRuntimeMemory(
                mapField(in, "memory"), str(in, "query_type", "semantic"), str(in, "term", "")));
    }

    @TestFactory
    List<DynamicTest> searchRuntimeMemory() {
        return section("search_runtime_memory", in -> MemorySearch.searchRuntimeMemory(
                mapField(in, "index"), str(in, "term", ""), str(in, "search_type", "structural")));
    }

    @TestFactory
    List<DynamicTest> reconstructRuntime() {
        return section("reconstruct_runtime", in -> RuntimeReconstruction.reconstructRuntime(
                mapField(in, "semantic_ir"), mapField(in, "workflow_ir"),
                mapField(in, "synchronization_ir"), mapField(in, "execution_ir"),
                mapField(in, "memory_ir"), mapField(in, "runtime_graph"),
                str(in, "runtime_type", "browser"), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> reconstructRuntimeMemory() {
        return section("reconstruct_runtime_memory", in -> MemoryReconstruction.reconstructRuntimeMemory(
                mapField(in, "memory_ir"), mapField(in, "semantic"), mapField(in, "lineage")));
    }

    @TestFactory
    List<DynamicTest> reconstructGraph() {
        return section("reconstruct_graph", in ->
                GraphReconstruction.reconstructGraph(mapField(in, "system_graph")));
    }

    @TestFactory
    List<DynamicTest> reconstructBrowser() {
        return section("reconstruct_browser", in -> BrowserReconstruction.reconstructBrowserRuntime(
                mapField(in, "browser_ir"), mapField(in, "interaction_ir"),
                mapField(in, "identity"), mapField(in, "session"),
                mapField(in, "streaming"), mapField(in, "dom")));
    }

    @TestFactory
    List<DynamicTest> validateReconstructedRuntime() {
        return section("validate_reconstructed_runtime", in -> {
            JsonNode mut = in.get("mutations");
            Object mutations = (mut == null || mut.isNull())
                    ? null : CrossLanguageParityTest.toNative(mut);
            return RuntimeValidation.validateReconstructedRuntime(
                    mapField(in, "runtime"), mapField(in, "replay"),
                    mapField(in, "topology"), mapField(in, "execution"), mutations);
        });
    }
}
