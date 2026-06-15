package io.webweavex.ir;

import io.webweavex.determinism.Py;
import io.webweavex.knowledge.OntologyConflict;
import io.webweavex.knowledge.OntologyReconciliation;
import io.webweavex.knowledge.SemanticIdentity;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.ir.knowledge_ir} — {@code empty_knowledge_ir} + {@code compile_knowledge_ir}. */
public final class KnowledgeIr {

    private KnowledgeIr() {
    }

    public static Map<String, Object> emptyKnowledgeIr() {
        Map<String, Object> ir = new LinkedHashMap<>();
        ir.put("entities", new ArrayList<>());
        ir.put("relations", new ArrayList<>());
        ir.put("ontology", new ArrayList<>());
        ir.put("semantic_identity", new ArrayList<>());
        ir.put("contradictions", new ArrayList<>());
        ir.put("evidence", new ArrayList<>());
        ir.put("lineage", new ArrayList<>());
        ir.put("reconciliation", new LinkedHashMap<>());
        ir.put("confidence", IrBase.emptyConfidence());
        return ir;
    }

    public static Map<String, Object> compile(List<Object> entities, List<Object> edges) {
        Map<String, Object> recon = OntologyReconciliation.reconcile(edges);
        Map<String, Object> ids = SemanticIdentity.resolve(entities, "");
        Map<String, Object> conflicts = OntologyConflict.detect(edges);

        List<Object> evidence = new ArrayList<>();
        for (Object e : edges == null ? List.of() : edges) {
            if (e instanceof Map) {
                evidence.add(Py.get(e, "evidence", new ArrayList<>()));
            }
        }

        List<Object> conflictList = Py.asList(Py.get(conflicts, "conflicts", new ArrayList<>()));
        boolean noConflicts = conflictList == null || conflictList.isEmpty();

        Map<String, Object> confidence = new LinkedHashMap<>();
        confidence.put("score", noConflicts ? 0.9 : 0.5);
        confidence.put("basis", new ArrayList<>());
        confidence.put("deterministic", true);

        Map<String, Object> ir = emptyKnowledgeIr();
        ir.put("entities", entities == null ? new ArrayList<>() : entities);
        ir.put("relations", Py.get(recon, "reconciled", new ArrayList<>()));
        ir.put("ontology", edges == null ? new ArrayList<>() : edges);
        ir.put("semantic_identity", Py.get(ids, "entities", new ArrayList<>()));
        ir.put("contradictions", Py.get(conflicts, "conflicts", new ArrayList<>()));
        ir.put("evidence", evidence);
        ir.put("lineage", new ArrayList<>(List.of(Py.get(recon, "lineage", new LinkedHashMap<>()))));
        ir.put("reconciliation", recon);
        ir.put("confidence", confidence);
        return ir;
    }
}
