package io.webweavex.graph;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.graph.topology_proof_engine.prove_topology}. */
public final class TopologyProof {

    private TopologyProof() {
    }

    public static Map<String, Object> prove(Map<String, Object> graph) {
        List<Object> edges = GraphUtil.list(graph, "edges");
        Map<String, Integer> degree = new LinkedHashMap<>();
        for (Object eo : edges) {
            if (!(eo instanceof Map)) {
                continue;
            }
            Map<?, ?> e = (Map<?, ?>) eo;
            Object f = e.get("from");
            Object t = e.get("to");
            if (Py.truthy(f)) {
                degree.merge(Py.str(f), 1, Integer::sum);
            }
            if (Py.truthy(t)) {
                degree.merge(Py.str(t), 1, Integer::sum);
            }
        }
        List<String> hubs = new ArrayList<>();
        for (Map.Entry<String, Integer> en : degree.entrySet()) {
            if (en.getValue() >= 3) {
                hubs.add(en.getKey());
            }
        }
        hubs.sort(Normalization::codePointCompare);
        int maxDeg = 0;
        for (int d : degree.values()) {
            maxDeg = Math.max(maxDeg, d);
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("proved", true);
        out.put("max_degree", (long) maxDeg);
        out.put("hubs", new ArrayList<Object>(hubs.subList(0, Math.min(20, hubs.size()))));
        out.put("edge_count", (long) edges.size());
        out.put("deterministic_inputs", List.of("max_degree=" + maxDeg, "hubs=" + hubs.size()));
        return out;
    }
}
