package io.webweavex.query;

import io.webweavex.determinism.Py;
import io.webweavex.ir.KnowledgeIr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.query.ontology_query_engine.query_knowledge}. */
public final class OntologyQuery {

    private OntologyQuery() {
    }

    public static Map<String, Object> queryKnowledge(List<Object> entities, List<Object> edges) {
        Map<String, Object> ir = KnowledgeIr.compile(entities, edges);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", ir);
        out.put("relations", Py.get(ir, "relations", new ArrayList<>()));
        out.put("contradictions", Py.get(ir, "contradictions", new ArrayList<>()));
        out.put("explainable", true);
        return out;
    }
}
