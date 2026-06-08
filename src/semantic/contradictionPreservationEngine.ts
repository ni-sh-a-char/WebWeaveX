/**
 * Converted from Python: core/semantic/contradiction_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectContradictionEvidence } from "../evidence/contradictionEvidenceEngine.js";
import { buildLineage } from "../evidence/lineageEngine.js";
import { reconcileEvidence } from "../evidence/reconciliationEvidenceEngine.js";

export function preserveContradictions(snippets: any): any {
  var detection: any = detectContradictionEvidence(snippets);
  var pairs: any = py.or2(py.get(detection, "contradiction_pairs", []), () => ([]));
  var conflicts: any = py.or2(py.get(detection, "conflicts", []), () => ([]));
  var conflicting_claims: any = py.iter(conflicts).map((c: any) => ({"polarity_a": py.get(c, "polarity_a"), "polarity_b": py.get(c, "polarity_b"), "evidence": py.get(c, "evidence")}));
  var reconciliation: any = reconcileEvidence(py.enumerate(pairs).map(([i, p]: any) => ({"key": py.toStr(p), "value": "conflict", "source": `snippet:${py.toStr(i)}`})));
  var lineage: any = buildLineage([{"stage": "detect", "inputs": py.range(py.len(py.or2(snippets, () => ([])))).map((i: any) => `snippet:${py.toStr(i)}`), "outputs": py.iter(pairs).map((p: any) => py.toStr(p))}]);
  return {"observed": {"snippets": snippets}, "parsed": {}, "inferred": {}, "reconciled": {}, "contradicted": {"pairs": pairs, "preserved": py.truthy(pairs), "collapsed": false}, "derived": {"conflict_count": py.len(conflicts)}, "ambiguities": (py.truthy(pairs) ? ["competing_interpretations"] : []), "conflicting_claims": conflicting_claims, "evidence": [...py.iter(py.get(detection, "evidence", []))], "lineage": lineage, "reconciliation": reconciliation, "confidence_basis": {"basis": "contradiction_preservation", "pair_count": py.len(pairs), "score": py.round(py.max([py.F(0.0), py.sub(py.F(1.0), py.mul(py.len(pairs), py.F(0.2)))]), 3), "deterministic_inputs": [`pairs=${py.toStr(py.len(pairs))}`]}, "why": {"summary": "contradictions_preserved_not_collapsed"}, "parser_basis": {}, "graph_basis": {}, "semantic_basis": {"conflict_count": py.len(conflicts)}};
}
export { buildLineage, detectContradictionEvidence, reconcileEvidence };
