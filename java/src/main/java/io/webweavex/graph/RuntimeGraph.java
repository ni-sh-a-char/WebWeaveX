package io.webweavex.graph;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Canonical runtime graph — byte-exact port of the Python parity graph
 * ({@code core.determinism.runtime_graph_parity}, "matches javascript
 * runtimeGraph.ts") and the merge/replay contract
 * ({@code core.contracts.graph_contracts.RuntimeGraphContract}).
 *
 * <p>Graphs are plain {@code Map}/{@code List} trees (as in Python) so they hash
 * and serialize identically through {@code StableSerialize}.
 */
public final class RuntimeGraph {

    private RuntimeGraph() {
    }

    /**
     * Port of {@code build_parity_runtime_graph(sources)}: one node per source
     * (id {@code node:<kind>:<idx>}, sources iterated in sorted-key order), a
     * {@code runtime_link} edge from the first node to every other, then
     * {@link #normalizeRuntimeGraph}.
     */
    public static Map<String, Object> buildParityRuntimeGraph(Map<String, Object> sources) {
        List<String> kinds = new ArrayList<>(sources.keySet());
        kinds.sort(Normalization::codePointCompare);

        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        int idx = 0;
        for (String kind : kinds) {
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", "node:" + kind + ":" + idx);
            node.put("type", kind);
            node.put("payload", sources.get(kind));
            nodes.add(node);
            idx++;
        }
        if (nodes.size() > 1) {
            String firstId = (String) ((Map<?, ?>) nodes.get(0)).get("id");
            for (int i = 1; i < nodes.size(); i++) {
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("source", firstId);
                edge.put("target", ((Map<?, ?>) nodes.get(i)).get("id"));
                edge.put("type", "runtime_link");
                edges.add(edge);
            }
        }
        Map<String, Object> graph = new LinkedHashMap<>();
        graph.put("nodes", nodes);
        graph.put("edges", edges);
        graph.put("bounded", true);
        return normalizeRuntimeGraph(graph);
    }

    /**
     * Port of {@code normalize_runtime_graph}: nodes sorted by the joined key
     * {@code id|type|name}, edges by {@code (source or from)|(target or to)|type},
     * using Python {@code or} fallback and code-point string ordering.
     */
    public static Map<String, Object> normalizeRuntimeGraph(Map<String, Object> graph) {
        List<Object> nodes = listOf(Py.get(graph, "nodes", null));
        List<Object> edges = listOf(Py.get(graph, "edges", null));

        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort(Comparator.comparing(
                n -> Py.str(getOr(n, "id", "")) + "|"
                        + Py.str(getOr(n, "type", "")) + "|"
                        + Py.str(getOr(n, "name", "")),
                Normalization::codePointCompare));

        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing(RuntimeGraph::parityEdgeKey,
                Normalization::codePointCompare));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    private static String parityEdgeKey(Object e) {
        Object source = orFallback(getOr(e, "source", null), getOr(e, "from", ""));
        Object target = orFallback(getOr(e, "target", null), getOr(e, "to", ""));
        return Py.str(source) + "|" + Py.str(target) + "|" + Py.str(getOr(e, "type", ""));
    }

    /**
     * Port of {@code RuntimeGraphContract.normalize}: nodes sorted by the tuple
     * {@code (str(id), str(type), str(name))}, edges by
     * {@code (str(source|from), str(target|to), str(type))} using {@code .get}
     * (key-absent) fallback semantics.
     */
    public static Map<String, Object> normalizeContract(Map<String, Object> graph) {
        List<Object> nodes = listOf(Py.get(graph, "nodes", null));
        List<Object> edges = listOf(Py.get(graph, "edges", null));

        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort(tupleComparator(
                n -> Py.str(getOr(n, "id", "")),
                n -> Py.str(getOr(n, "type", "")),
                n -> Py.str(getOr(n, "name", ""))));

        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(tupleComparator(
                e -> Py.str(getOrDefaultKey(e, "source", "from", "")),
                e -> Py.str(getOrDefaultKey(e, "target", "to", "")),
                e -> Py.str(getOr(e, "type", ""))));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    /** Deterministic graph fingerprint: {@code compute_kaalka_hash(normalize_runtime_graph(graph))}. */
    public static String graphFingerprint(Map<String, Object> graph) {
        return Kaalka.computeKaalkaHash(normalizeRuntimeGraph(graph));
    }

    // --- helpers -----------------------------------------------------------

    @SafeVarargs
    private static Comparator<Object> tupleComparator(
            java.util.function.Function<Object, String>... keys) {
        return (a, b) -> {
            for (java.util.function.Function<Object, String> k : keys) {
                int c = Normalization.codePointCompare(k.apply(a), k.apply(b));
                if (c != 0) {
                    return c;
                }
            }
            return 0;
        };
    }

    private static List<Object> listOf(Object o) {
        List<Object> l = Py.asList(o);
        return l == null ? new ArrayList<>() : l;
    }

    /** {@code obj.get(key, default)} when obj is a dict, else default. */
    private static Object getOr(Object obj, String key, Object dflt) {
        Map<String, Object> m = Py.asMap(obj);
        if (m == null || !m.containsKey(key)) {
            return dflt;
        }
        return m.get(key);
    }

    /** Python {@code a or b}: returns a when truthy, else b. */
    private static Object orFallback(Object a, Object b) {
        return Py.truthy(a) ? a : b;
    }

    /** Python {@code dict.get(primary, dict.get(fallback, default))}. */
    private static Object getOrDefaultKey(Object obj, String primary, String fallback, Object dflt) {
        Map<String, Object> m = Py.asMap(obj);
        if (m == null) {
            return dflt;
        }
        if (m.containsKey(primary)) {
            return m.get(primary);
        }
        return m.containsKey(fallback) ? m.get(fallback) : dflt;
    }
}
