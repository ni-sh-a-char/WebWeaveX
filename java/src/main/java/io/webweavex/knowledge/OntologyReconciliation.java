package io.webweavex.knowledge;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

/**
 * Ports of {@code core.knowledge.ontology_reconciliation_engine.reconcile_ontology_edges},
 * {@code semantic_merge_rigor_engine.merge_with_evidence}, and
 * {@code ontology_lineage_engine.stamp_ontology_lineage}.
 */
public final class OntologyReconciliation {

    private OntologyReconciliation() {
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> reconcile(List<Object> edges) {
        List<Object> reconciled = new ArrayList<>();
        List<Object> rejected = new ArrayList<>();
        for (Object eo : edges == null ? List.of() : edges) {
            Map<String, Object> e = Py.asMap(eo);
            Object ev = e == null ? null : Py.get(e, "evidence", new ArrayList<>());
            if (!Py.truthy(ev)) {
                Map<String, Object> r = new LinkedHashMap<>();
                r.put("edge", eo);
                r.put("reason", "missing_evidence");
                rejected.add(r);
                continue;
            }
            reconciled.add(stampOntologyLineage(e, "reconcile"));
        }

        List<Map<String, Object>> mergeSources = new ArrayList<>();
        for (Object ro : reconciled) {
            Map<String, Object> src = new LinkedHashMap<>();
            src.put("evidence", Py.get(ro, "evidence", new ArrayList<>()));
            mergeSources.add(src);
        }
        Map<String, Object> merge = mergeWithEvidence(mergeSources);

        Map<String, Object> lineage = new LinkedHashMap<>();
        lineage.put("stage", "ontology_reconciliation");
        lineage.put("count", (long) reconciled.size());

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("reconciled", reconciled);
        out.put("rejected", rejected);
        out.put("merge", merge);
        out.put("lineage", lineage);
        return out;
    }

    /** Port of {@code merge_with_evidence(sources)} — no silent merge. */
    public static Map<String, Object> mergeWithEvidence(List<Map<String, Object>> sources) {
        List<Map<String, Object>> srcs = sources == null ? List.of() : sources;
        List<String> mergedEvidence = new ArrayList<>();
        for (Map<String, Object> s : srcs) {
            // ev = s.get("evidence", []) or []; then str -> [str]
            Object evRaw = Py.get(s, "evidence", new ArrayList<>());
            List<Object> ev;
            if (!Py.truthy(evRaw)) {
                ev = new ArrayList<>();
            } else if (evRaw instanceof String) {
                ev = List.of(evRaw);
            } else {
                ev = Py.asList(evRaw);
                if (ev == null) {
                    ev = new ArrayList<>();
                }
            }
            if (ev.isEmpty()) {
                Map<String, Object> out = new LinkedHashMap<>();
                out.put("merged", false);
                out.put("reason", "silent_merge_forbidden");
                out.put("sources", (long) srcs.size());
                return out;
            }
            for (Object e : ev) {
                mergedEvidence.add(Py.str(e));
            }
        }
        TreeSet<String> dedup = new TreeSet<>(Normalization::codePointCompare);
        dedup.addAll(mergedEvidence);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("merged", true);
        out.put("evidence", new ArrayList<Object>(dedup));
        out.put("source_count", (long) srcs.size());
        out.put("deterministic_inputs", List.of("sources=" + srcs.size()));
        return out;
    }

    /** Port of {@code stamp_ontology_lineage(edge, stage)}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> stampOntologyLineage(Map<String, Object> edge, String stage) {
        Map<String, Object> lineage = Py.asMap(Py.get(edge, "lineage", null));
        if (lineage == null || !Py.truthy(lineage)) {
            lineage = new LinkedHashMap<>();
        }
        Object stagesRaw = lineage.get("stages");
        List<Object> stages = stagesRaw instanceof List
                ? new ArrayList<>((List<Object>) stagesRaw) : new ArrayList<>();
        Map<String, Object> newStage = new LinkedHashMap<>();
        newStage.put("stage", stage);
        newStage.put("from", edge.get("from"));
        newStage.put("to", edge.get("to"));
        stages.add(newStage);

        Map<String, Object> newLineage = new LinkedHashMap<>(lineage);
        newLineage.put("stages", stages);
        newLineage.put("depth", (long) stages.size());

        Map<String, Object> out = new LinkedHashMap<>(edge);
        out.put("lineage", newLineage);
        return out;
    }
}
