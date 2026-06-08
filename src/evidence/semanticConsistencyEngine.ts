/**
 * Converted from Python: core/evidence/semantic_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function assessSemanticConsistency(observed: any, inferred: any, reconciled: any): any {
  const _d1 = py.iter([py.toSet(py.keys(observed)), py.toSet(py.keys(inferred)), py.toSet(py.keys(reconciled))]) as any[];
  var ko: any = _d1[0];
  var ki: any = _d1[1];
  var kr: any = _d1[2];
  var overlap_oi: any = py.len(py.bitand(ko, ki));
  var overlap_or: any = py.len(py.bitand(ko, kr));
  var total: any = py.max([1, py.len(py.bitor(py.bitor(ko, ki), kr))]);
  var score: any = py.round(py.div(py.add(overlap_oi, overlap_or), py.mul(2, total)), 3);
  var consistent: any = py.or2((score >= py.F(0.5)), () => (!py.truthy(inferred)));
  return {"consistent": consistent, "consistency_score": score, "overlap_observed_inferred": overlap_oi, "overlap_observed_reconciled": overlap_or, "deterministic_inputs": [`score=${py.floatStr(score)}`, `keys_total=${py.toStr(total)}`]};
}
