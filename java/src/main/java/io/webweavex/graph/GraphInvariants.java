package io.webweavex.graph;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Port of {@code core.graph.graph_invariant_engine.check_graph_invariants}. */
public final class GraphInvariants {

    private GraphInvariants() {
    }

    public static Map<String, Object> check(Map<String, Object> graph) {
        List<Object> nodes = GraphUtil.list(graph, "nodes");
        List<Object> edges = GraphUtil.list(graph, "edges");

        Set<Object> nodeIds = new HashSet<>();
        for (Object n : nodes) {
            if (n instanceof Map) {
                Object id = Py.get(n, "id", null);
                if (Py.truthy(id)) {
                    nodeIds.add(id);
                }
            }
        }

        List<Object> violations = new ArrayList<>();
        for (Object eo : edges) {
            if (!(eo instanceof Map)) {
                continue;
            }
            Map<?, ?> e = (Map<?, ?>) eo;
            if (e.containsKey("type")) {
                Map<String, Object> v = new LinkedHashMap<>();
                v.put("rule", "no_edge_type");
                v.put("edge", Py.str(e.get("from")));
                violations.add(v);
            }
            if (!nodeIds.contains(e.get("from")) || !nodeIds.contains(e.get("to"))) {
                if (!nodeIds.isEmpty()) {
                    Map<String, Object> v = new LinkedHashMap<>();
                    v.put("rule", "dangling_edge");
                    v.put("from", Py.str(e.get("from")));
                    v.put("to", Py.str(e.get("to")));
                    violations.add(v);
                }
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("valid", violations.isEmpty());
        out.put("violations", violations);
        out.put("node_count", (long) nodes.size());
        out.put("edge_count", (long) edges.size());
        out.put("deterministic_inputs", List.of("violations=" + violations.size()));
        return out;
    }
}
