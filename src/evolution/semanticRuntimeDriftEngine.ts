/**
 * Converted from Python: core/evolution/semantic_runtime_drift_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRuntimeDrift(current: any, baseline: any): any {
  var drift: any = py.sorted(py.bitxor(py.toSet(py.keys(current)), py.toSet(py.keys(baseline))));
  return {"drift": drift, "drift_detected": py.truthy(drift)};
}
