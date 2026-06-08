/**
 * Converted from Python: core/evidence/noninference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelNoninference(evidence: any, inferred: any, observed: any, reconciled: any, min_evidence: any = 2): any {
  var refused: any[] = [];
  var noninferences: any[] = [];
  if (((py.len(evidence) < min_evidence) && py.truthy(inferred))) {
    py.extend(refused, py.sorted(py.keys(inferred).map((k: any) => `infer:${py.toStr(k)}`)));
    py.listAppend(noninferences, "entity_link_without_evidence");
  }
  if ((!py.eq(reconciled, observed) && (py.len(evidence) < min_evidence))) {
    py.listAppend(noninferences, "reconcile_without_evidence");
    py.listAppend(refused, "reconcile:unsupported");
  }
  if ((py.truthy(inferred) && !py.truthy(observed))) {
    py.listAppend(noninferences, "inferred_without_observation");
  }
  return {"noninferences": py.sorted(py.toSet(noninferences)), "refused_inferences": py.sorted(py.toSet(refused)), "boundary_conditions": [`min_evidence=${py.toStr(min_evidence)}`], "suppression_basis": {"evidence_count": py.len(evidence), "allowed": (py.len(evidence) >= min_evidence)}};
}
