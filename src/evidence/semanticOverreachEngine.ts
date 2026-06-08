/**
 * Converted from Python: core/evidence/semantic_overreach_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectSemanticOverreach(evidence: any, inferred: any, reconciled: any): any {
  var overreach: any[] = [];
  if ((!py.eq(reconciled, inferred) && (py.len(evidence) < 2))) {
    py.listAppend(overreach, "reconciled_beyond_evidence");
  }
  if (((py.len(inferred) > 0) && (py.len(evidence) < 2))) {
    py.listAppend(overreach, "inference_expansion");
  }
  if ((py.truthy(inferred) && py.eq(py.len(evidence), 0))) {
    py.listAppend(overreach, "pure_heuristic_inference");
  }
  return {"overreach_detected": py.truthy(overreach), "overreach_flags": py.sorted(py.toSet(overreach)), "deterministic_inputs": [`inferred_keys=${py.toStr(py.len(inferred))}`, `evidence=${py.toStr(py.len(evidence))}`]};
}
