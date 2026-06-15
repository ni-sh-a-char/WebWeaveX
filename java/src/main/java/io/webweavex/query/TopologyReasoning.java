package io.webweavex.query;

import io.webweavex.determinism.Py;
import io.webweavex.graph.GraphEntropy;
import io.webweavex.graph.TopologyProof;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/** Port of {@code core.graph.topology_reasoning_engine.reason_topology}. */
public final class TopologyReasoning {

    private TopologyReasoning() {
    }

    public static Map<String, Object> reasonTopology(Map<String, Object> graph) {
        Map<String, Object> proof = TopologyProof.prove(graph);
        Map<String, Object> entropy = GraphEntropy.model(graph);
        Object entropyValue = Py.get(entropy, "entropy", 0L);

        Map<String, Object> out = new LinkedHashMap<>(proof);
        out.put("entropy", entropyValue);
        out.put("evidence", new ArrayList<>(java.util.List.of("graph:topology_proof")));

        Map<String, Object> justification = new LinkedHashMap<>();
        justification.put("hubs", Py.get(proof, "hubs", new ArrayList<>()));
        justification.put("max_degree", Py.get(proof, "max_degree", 0L));
        out.put("justification", justification);

        Map<String, Object> uncertainty = new LinkedHashMap<>();
        uncertainty.put("visible", toDouble(entropyValue) > 0);
        out.put("uncertainty", uncertainty);

        out.put("deterministic_inputs", Py.get(proof, "deterministic_inputs", new ArrayList<>()));
        return out;
    }

    private static double toDouble(Object o) {
        return o instanceof Number ? ((Number) o).doubleValue() : 0.0;
    }
}
