package io.webweavex.graph;

import io.webweavex.determinism.Py;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.graph.semantic_edge_validation_engine.validate_semantic_edge}. */
public final class SemanticEdge {

    private SemanticEdge() {
    }

    public static Map<String, Object> validate(Map<String, Object> edge) {
        Map<String, Object> out = new LinkedHashMap<>();
        if (edge.containsKey("type")) {
            out.put("valid", false);
            out.put("reason", "forbidden_type_field");
            return out;
        }
        if (!Py.truthy(Py.get(edge, "from", null)) || !Py.truthy(Py.get(edge, "to", null))) {
            out.put("valid", false);
            out.put("reason", "missing_endpoints");
            return out;
        }
        // ev = edge.get("evidence", []) or []  (falsy "" / None / [] -> [])
        Object evRaw = Py.get(edge, "evidence", new java.util.ArrayList<>());
        List<Object> ev;
        if (!Py.truthy(evRaw)) {
            ev = new java.util.ArrayList<>();
        } else if (evRaw instanceof String) {
            ev = List.of(evRaw);
        } else {
            ev = Py.asList(evRaw);
            if (ev == null) {
                ev = new java.util.ArrayList<>();
            }
        }
        out.put("valid", !ev.isEmpty());
        out.put("evidence_count", (long) ev.size());
        out.put("grounding", Py.get(edge, "grounding", new LinkedHashMap<>()));
        out.put("uncertainty", Py.get(edge, "uncertainty", new LinkedHashMap<>()));
        out.put("justification", Py.get(edge, "justification", new LinkedHashMap<>()));
        return out;
    }
}
