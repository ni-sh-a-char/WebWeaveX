/**
 * Converted from Python: core/semantic/semantic_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconcileEvidence } from "../evidence/reconciliationEvidenceEngine.js";

export function resolveSemanticClaims(claims: any): any {
  var reconciled: any = reconcileEvidence(claims);
  var resolved: any = Object.fromEntries(py.iter(py.get(reconciled, "reconciled", [])).filter((item: any) => ((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))).map((item: any) => ([py.at(item, "key"), py.at(item, "value")] as [any, any])));
  return {"resolved": resolved, "reconciliation": reconciled, "evidence": py.get(reconciled, "evidence", []), "sources": py.get(reconciled, "sources", []), "grounding": py.get(reconciled, "grounding", {}), "lineage": py.get(reconciled, "lineage", {})};
}
export { reconcileEvidence };
