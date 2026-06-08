/**
 * Converted from Python: core/documents/semantic_edge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { scoreSemanticConfidence } from "../evidence/semanticConfidenceEngine.js";

export function buildSemanticEdge(from_id: any, to_id: any, relation: any, evidence: any = null, parser_basis: any = null, ambiguities: any = null, contradictions: any = null): any {
  var ev: any = py.sorted(py.toSet(py.iter(py.or2(evidence, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  if (!py.truthy(ev)) {
    ev = [`relation:${py.toStr(relation)}`];
  }
  var confidence: any = scoreSemanticConfidence(undefined, undefined, ev);
  return {"from": from_id, "to": to_id, "relation": relation, "observed": {"from": from_id, "to": to_id, "relation": relation}, "inferred": (!py.truthy(parser_basis) ? {"from": from_id, "to": to_id} : {}), "reconciled": {"from": from_id, "to": to_id, "relation": relation}, "evidence": ev, "lineage": {"stage": "semantic_edge", "relation": relation}, "parser_basis": py.or2(parser_basis, () => ({})), "semantic_basis": {"relation": relation}, "confidence_basis": confidence, "contradictions": py.or2(contradictions, () => ({})), "ambiguities": py.sorted(py.toSet(py.or2(ambiguities, () => ((py.truthy(ev) ? [] : ["weak_edge_evidence"])))))};
}
export { scoreSemanticConfidence };
