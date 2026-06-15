package io.webweavex.graph;

import io.webweavex.determinism.PyFloat;
import io.webweavex.determinism.PyRound;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Port of {@code core.graph.graph_entropy_engine.model_graph_entropy}. */
public final class GraphEntropy {

    private GraphEntropy() {
    }

    public static Map<String, Object> model(Map<String, Object> graph) {
        List<Object> nodes = GraphUtil.list(graph, "nodes");
        List<Object> edges = GraphUtil.list(graph, "edges");

        // {n.get("kind") for n in nodes if isinstance(n, dict)} — includes null.
        Set<Object> kinds = new HashSet<>();
        for (Object n : nodes) {
            if (n instanceof Map) {
                kinds.add(((Map<?, ?>) n).get("kind"));
            }
        }
        double entropy = PyRound.round(
                Math.min(1.0, nodes.size() * 0.02 + edges.size() * 0.03 + kinds.size() * 0.05), 3);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("entropy", entropy);
        out.put("kind_diversity", (long) kinds.size());
        out.put("deterministic_inputs", List.of("H=" + PyFloat.pyFloatRepr(entropy)));
        return out;
    }
}
