package io.webweavex.determinism;

import io.webweavex.crypto.Kaalka;
import io.webweavex.graph.RuntimeGraph;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.determinism.global_runtime_fingerprint.compute_global_runtime_fingerprint}
 * — a cross-machine stable runtime fingerprint over a canonical, sorted payload
 * hashed via {@code compute_kaalka_hash(json.dumps(..., separators=(",",":")))}
 * (Python default {@code ensure_ascii=True}).
 */
public final class GlobalRuntimeFingerprint {

    private GlobalRuntimeFingerprint() {
    }

    public static String compute(Map<String, Object> extraction) {
        return compute(extraction, null, null, null, null, "");
    }

    public static String compute(
            Map<String, Object> extraction,
            Map<String, Object> graph,
            Map<String, Object> memory,
            Map<String, Object> sync,
            Map<String, Object> reconstruction,
            String kaalkaSeal) {

        Map<String, Object> ext = extraction == null ? new LinkedHashMap<>() : extraction;

        Object graphInput = Py.truthy(graph) ? graph : Py.get(ext, "unified_runtime_graph", Map.of());
        Map<String, Object> g = RuntimeGraph.normalizeContract(Py.asMap(graphInput) == null
                ? new LinkedHashMap<>() : Py.asMap(graphInput));

        Object runtime = Py.get(ext, "runtime", Map.of());
        String domHash = "";
        if (runtime instanceof Map) {
            Object v1 = Py.get(Py.get(runtime, "dom_stabilization", Map.of()), "stabilized_hash", "");
            Object v2 = Py.get(Py.get(runtime, "spa_stabilization", Map.of()), "stable_dom_hash", "");
            domHash = Py.str(Py.truthy(v1) ? v1 : v2);
        }

        Object browserIr = Py.get(ext, "browser_ir", Map.of());
        Object identity = browserIr instanceof Map
                ? Py.get(browserIr, "runtime_identity", "") : "";

        Map<String, Object> memoryBlock = new LinkedHashMap<>();
        if (Py.truthy(memory)) {
            Object inner = Py.get(memory, "memory", Map.of());
            Object stableHash = Py.get(memory, "stable_hash", Py.get(inner, "stable_hash", ""));
            List<Object> history = Py.asList(Py.get(inner, "runtime_history", null));
            memoryBlock.put("stable_hash", stableHash);
            memoryBlock.put("history_len", (long) (history == null ? 0 : history.size()));
        }

        List<Object> graphNodes = new ArrayList<>();
        for (Object n : nodes(g)) {
            graphNodes.add(getOrNull(n, "id"));
        }
        List<Object> graphEdges = new ArrayList<>();
        for (Object e : edges(g)) {
            List<Object> triple = new ArrayList<>();
            triple.add(getOrKey(e, "source", "from"));
            triple.add(getOrKey(e, "target", "to"));
            triple.add(getOrNull(e, "type"));
            graphEdges.add(triple);
        }

        Map<String, Object> canonical = new LinkedHashMap<>();
        canonical.put("dom_hash", domHash);
        canonical.put("runtime_identity", identity);
        canonical.put("graph_nodes", graphNodes);
        canonical.put("graph_edges", graphEdges);
        canonical.put("memory", memoryBlock);
        canonical.put("sync_converged",
                Py.get(Py.get(sync == null ? Map.of() : sync, "convergence", Map.of()),
                        "converged", null));
        canonical.put("reconstruction_id",
                Py.get(Py.get(reconstruction == null ? Map.of() : reconstruction, "runtime", Map.of()),
                        "runtime_id", ""));
        canonical.put("kaalka_seal", kaalkaSeal);
        canonical.put("pipeline_hash", Py.get(ext, "pipeline_hash", ""));

        return Kaalka.computeKaalkaHash(PyJson.dumpsCompactAscii(canonical));
    }

    private static List<Object> nodes(Map<String, Object> g) {
        List<Object> l = Py.asList(Py.get(g, "nodes", null));
        return l == null ? List.of() : l;
    }

    private static List<Object> edges(Map<String, Object> g) {
        List<Object> l = Py.asList(Py.get(g, "edges", null));
        return l == null ? List.of() : l;
    }

    private static Object getOrNull(Object obj, String key) {
        Map<String, Object> m = Py.asMap(obj);
        return (m != null && m.containsKey(key)) ? m.get(key) : null;
    }

    /** Python {@code e.get(primary, e.get(fallback))} — both default to null. */
    private static Object getOrKey(Object obj, String primary, String fallback) {
        Map<String, Object> m = Py.asMap(obj);
        if (m == null) {
            return null;
        }
        if (m.containsKey(primary)) {
            return m.get(primary);
        }
        return m.containsKey(fallback) ? m.get(fallback) : null;
    }
}
