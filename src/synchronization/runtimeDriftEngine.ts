/**
 * Converted from Python: core/synchronization/runtime_drift_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRuntimeDrift(baseline: any, current: any): any {
  var drifts: any[] = [];
  var checks: any = [["selector_drift", "selectors"], ["semantic_drift", "semantic"], ["workflow_drift", "workflow"], ["topology_drift", "topology"], ["application_drift", "application"], ["runtime_divergence", "runtime"]];
  var drift_type: any;
  var field: any;
  for ([drift_type, field] of py.iter(checks)) {
    if (!py.eq(py.get(baseline, field), py.get(current, field))) {
      py.listAppend(drifts, {"type": drift_type, "field": field, "detected": true});
    }
  }
  return {"drifts": drifts, "drift_count": py.len(drifts), "diverged": (py.len(drifts) > 0), "bounded": true};
}
