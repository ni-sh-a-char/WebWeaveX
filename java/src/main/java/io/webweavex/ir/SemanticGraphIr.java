package io.webweavex.ir;

import io.webweavex.determinism.Py;
import io.webweavex.graph.GraphConsistency;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/** Port of {@code core.ir.semantic_graph_ir.compile_semantic_graph_ir}. */
public final class SemanticGraphIr {

    private SemanticGraphIr() {
    }

    public static Map<String, Object> compile(Map<String, Object> graph) {
        Map<String, Object> proof = GraphConsistency.prove(graph);

        Map<String, Object> confidence = new LinkedHashMap<>();
        confidence.put("score", Boolean.TRUE.equals(proof.get("proved")) ? 1.0 : 0.3);
        confidence.put("basis", Py.get(proof, "deterministic_inputs", new ArrayList<>()));
        confidence.put("deterministic", true);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", Py.get(graph, "nodes", new ArrayList<>()));
        out.put("edges", Py.get(graph, "edges", new ArrayList<>()));
        out.put("proof", proof);
        out.put("lineage", IrBase.emptyLineage("semantic_graph_ir"));
        out.put("confidence", confidence);
        return out;
    }
}
