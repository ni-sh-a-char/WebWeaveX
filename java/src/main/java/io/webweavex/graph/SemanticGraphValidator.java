package io.webweavex.graph;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.graph.semantic_graph_validator.validate_semantic_graph}. */
public final class SemanticGraphValidator {

    private SemanticGraphValidator() {
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> validate(Map<String, Object> graph) {
        Map<String, Object> inv = GraphInvariants.check(graph);

        List<Object> edgeResults = new ArrayList<>();
        for (Object e : GraphUtil.list(graph, "edges")) {
            if (e instanceof Map) {
                edgeResults.add(SemanticEdge.validate((Map<String, Object>) e));
            }
        }
        List<Object> invalid = new ArrayList<>();
        for (int i = 0; i < edgeResults.size(); i++) {
            if (!Boolean.TRUE.equals(Py.get(edgeResults.get(i), "valid", null))) {
                invalid.add((long) i);
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("valid", Boolean.TRUE.equals(inv.get("valid")) && invalid.isEmpty());
        out.put("invariants", inv);
        out.put("invalid_edges", invalid);
        out.put("edge_count", (long) edgeResults.size());
        out.put("deterministic_inputs", Py.get(inv, "deterministic_inputs", new ArrayList<>()));
        return out;
    }
}
