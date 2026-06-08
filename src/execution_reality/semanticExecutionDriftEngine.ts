/**
 * Converted from Python: core/execution_reality/semantic_execution_drift_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectExecutionDrift(current: any, baseline: any): any {
  var drift: any = py.sorted(py.bitxor(py.toSet(py.keys(current)), py.toSet(py.keys(baseline))));
  return {"drift_keys": drift, "drift_detected": py.truthy(drift)};
}
