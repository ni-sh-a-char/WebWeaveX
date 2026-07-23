package io.webweavex.replay;

import static org.junit.jupiter.api.Assertions.*;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** Direct unit tests for ReplayEquivalence edge cases. */
class ReplayEquivalenceCoverageTest {

    @Test
    void emptyGraphHash() {
        String hash = ReplayEquivalence.graphHash(Map.of());
        assertEquals(64, hash.length());
    }

    @Test
    void graphHashNormalized() {
        Map<String, Object> g1 = Map.of("nodes", List.of(Map.of("id", "b", "type", "file")), "edges", List.of());
        Map<String, Object> g2 = Map.of("nodes", List.of(Map.of("id", "b", "type", "module")), "edges", List.of());
        // Same ID, different type — both get normalized
        String h1 = ReplayEquivalence.graphHash(g1);
        String h2 = ReplayEquivalence.graphHash(g2);
        // Types differ, so hashes differ
        assertNotEquals(h1, h2);
    }

    @Test
    void validateWithMissingGraphKeys() {
        Map<String, Object> result = ReplayEquivalence.validate(Map.of(), Map.of());
        assertEquals(true, result.get("equivalent"));
        assertEquals(true, result.get("bounded"));
    }

    @Test
    void validateWithPartialEnvelope() {
        Map<String, Object> env = Map.of("pipeline_hash", "test");
        Map<String, Object> result = ReplayEquivalence.validate(env, env);
        assertEquals(true, result.get("equivalent"));
    }

    @Test
    void validateWithNestedGraph() {
        Map<String, Object> g = Map.of(
            "nodes", List.of(
                Map.of("id", "n1", "type", "file", "name", "test.dart"),
                Map.of("id", "n2", "type", "module", "name", "core")
            ),
            "edges", List.of(Map.of("source", "n1", "target", "n2", "type", "imports"))
        );
        Map<String, Object> env = Map.of("unified_runtime_graph", g);
        Map<String, Object> result = ReplayEquivalence.validate(env, env);
        assertEquals(true, result.get("equivalent"));
    }

    @Test
    void validateWithUnicodeContent() {
        Map<String, Object> g = Map.of(
            "nodes", List.of(Map.of("id", "n1", "name", "\u4e16\u754c")),
            "edges", List.of()
        );
        Map<String, Object> env = Map.of("unified_runtime_graph", g);
        Map<String, Object> result = ReplayEquivalence.validate(env, env);
        assertEquals(true, result.get("equivalent"));
    }

    @Test
    void checksListStructure() {
        Map<String, Object> result = ReplayEquivalence.validate(Map.of(), Map.of());
        List<Object> checks = (List<Object>) result.get("checks");
        assertEquals(3, checks.size());
        Map<String, Object> check0 = (Map<String, Object>) checks.get(0);
        assertEquals("graph_hash", check0.get("name"));
        assertEquals(true, check0.get("ok"));
    }

    @Test
    void validateLargeGraph() {
        var nodes = new java.util.ArrayList<Map<String, Object>>();
        for (int i = 0; i < 1000; i++) {
            nodes.add(Map.of("id", "n" + i, "type", "file"));
        }
        var edges = new java.util.ArrayList<Map<String, Object>>();
        for (int i = 0; i < 999; i++) {
            edges.add(Map.of("source", "n" + i, "target", "n" + (i + 1), "type", "depends"));
        }
        Map<String, Object> g = Map.of("nodes", nodes, "edges", edges);
        Map<String, Object> env = Map.of("unified_runtime_graph", g);
        Map<String, Object> result = ReplayEquivalence.validate(env, env);
        assertEquals(true, result.get("equivalent"));
    }
}
