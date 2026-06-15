package io.webweavex.graph;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Ports of {@code core.graph.graph_consistency_engine.assess_graph_consistency}
 * and {@code core.graph.graph_consistency_prover.prove_graph_consistency}.
 */
public final class GraphConsistency {

    private GraphConsistency() {
    }

    public static Map<String, Object> assess(Map<String, Object> graph) {
        Map<String, Object> inv = GraphInvariants.check(graph);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("consistent", inv.get("valid"));
        out.put("invariants", inv);
        out.put("deterministic_inputs", inv.get("deterministic_inputs"));
        return out;
    }

    public static Map<String, Object> prove(Map<String, Object> graph) {
        Map<String, Object> validation = SemanticGraphValidator.validate(graph);
        Map<String, Object> consistency = assess(graph);
        boolean proved = Boolean.TRUE.equals(validation.get("valid"))
                && Boolean.TRUE.equals(consistency.get("consistent"));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("proved", proved);
        out.put("validation", validation);
        out.put("consistency", consistency);
        out.put("deterministic_inputs", Py.get(validation, "deterministic_inputs", new ArrayList<>()));
        return out;
    }
}
