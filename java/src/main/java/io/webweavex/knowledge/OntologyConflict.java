package io.webweavex.knowledge;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.knowledge.ontology_conflict_engine.detect_ontology_conflicts}. */
public final class OntologyConflict {

    private OntologyConflict() {
    }

    public static Map<String, Object> detect(List<Object> edges) {
        List<Object> pairs = new ArrayList<>();
        for (Object eo : edges == null ? List.of() : edges) {
            Map<String, Object> c = Py.asMap(Py.get(eo, "contradictions", null));
            if (c == null) {
                continue;
            }
            List<Object> cpairs = Py.asList(Py.get(c, "pairs", new ArrayList<>()));
            if (cpairs == null) {
                continue;
            }
            for (Object po : cpairs) {
                List<Object> p = Py.asList(po);
                if (p != null && p.size() >= 2) {
                    pairs.add(List.of(Py.str(p.get(0)), Py.str(p.get(1))));
                }
            }
        }
        Map<String, Object> lattice = ContradictionLattice.build(pairs);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("conflicts", lattice.get("pairs"));
        out.put("pressure", lattice.get("pressure"));
        out.put("contradiction_pressure", lattice.get("pressure"));
        Map<String, Object> uncertainty = new LinkedHashMap<>();
        uncertainty.put("visible", ((Number) lattice.get("count")).longValue() > 0);
        out.put("uncertainty", uncertainty);
        return out;
    }
}
