package io.webweavex.graph;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** Direct unit tests for RuntimeGraph. */
class RuntimeGraphTest {

    @Test
    void buildParityRuntimeGraphProducesNodes() {
        Map<String, Object> input = Map.of(
            "nodes", List.of(Map.of("id", "n1", "type", "file")),
            "edges", List.of()
        );
        Map<String, Object> graph = RuntimeGraph.buildParityRuntimeGraph(input);
        assertNotNull(graph.get("nodes"));
        assertNotNull(graph.get("edges"));
    }

    @Test
    void normalizeRuntimeGraphSortsNodes() {
        Map<String, Object> input = Map.of(
            "nodes", List.of(
                Map.of("id", "z", "type", "file"),
                Map.of("id", "a", "type", "file")
            ),
            "edges", List.of()
        );
        Map<String, Object> normalized = RuntimeGraph.normalizeRuntimeGraph(input);
        List<Map<String, Object>> nodes = (List<Map<String, Object>>) normalized.get("nodes");
        assertEquals("a", nodes.get(0).get("id"));
        assertEquals("z", nodes.get(1).get("id"));
    }

    @Test
    void graphFingerprintDeterministic() {
        Map<String, Object> graph = Map.of(
            "nodes", List.of(Map.of("id", "n1")),
            "edges", List.of()
        );
        String fp1 = RuntimeGraph.graphFingerprint(graph);
        String fp2 = RuntimeGraph.graphFingerprint(graph);
        assertEquals(fp1, fp2);
    }

    @Test
    void graphFingerprintDiffersByContent() {
        Map<String, Object> g1 = Map.of("nodes", List.of(Map.of("id", "n1")), "edges", List.of());
        Map<String, Object> g2 = Map.of("nodes", List.of(Map.of("id", "n2")), "edges", List.of());
        assertNotEquals(RuntimeGraph.graphFingerprint(g1), RuntimeGraph.graphFingerprint(g2));
    }

    @Test
    void normalizeContractHandlesMissingKeys() {
        Map<String, Object> result = RuntimeGraph.normalizeContract(Map.of());
        assertNotNull(result.get("nodes"));
        assertNotNull(result.get("edges"));
    }
}
