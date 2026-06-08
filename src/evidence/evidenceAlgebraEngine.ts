/**
 * Converted from Python: core/evidence/evidence_algebra_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function combineEvidence(evidence: any, weights: any = null): any {
  var w: any = py.or2(weights, () => ({}));
  var items: any = py.sorted(py.toSet(py.iter(evidence).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var total: any = py.round(py.sum(py.iter(items).map((e: any) => py.get(w, e, py.F(1.0)))), 3);
  return {"items": items, "count": py.len(items), "weight_sum": total, "sufficient": (py.len(items) >= 2), "deterministic_inputs": [`count=${py.toStr(py.len(items))}`, `weight_sum=${py.toStr(total)}`]};
}
