/**
 * Converted from Python: core/evidence/semantic_drift_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectSemanticDrift(observed: any, inferred: any, reconciled: any, evidence: any): any {
  var drift_keys: any[] = [];
  if ((py.truthy(inferred) && !py.truthy(observed))) {
    py.listAppend(drift_keys, "inferred_without_observation");
  }
  if ((!py.eq(reconciled, observed) && (py.len(evidence) < 2))) {
    py.listAppend(drift_keys, "reconcile_drift");
  }
  var k: any;
  for (k of py.iter(inferred)) {
    if ((!py.contains(observed, k) && !py.contains(reconciled, k))) {
      py.listAppend(drift_keys, `drift:${py.toStr(k)}`);
    }
  }
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(py.len(drift_keys), py.F(0.2))]), 3);
  return {"drift_detected": py.truthy(drift_keys), "drift_keys": py.sorted(py.toSet(drift_keys)), "drift_pressure": pressure, "suppress_continuation": (pressure >= py.F(0.2))};
}
