/**
 * Converted from Python: core/evidence/recursive_drift_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveDrift(depth: any, evidence_count: any, inferred_count: any): any {
  var drift: any = py.round(py.min([py.F(1.0), py.add(py.mul(depth, py.F(0.1)), py.mul(py.max([0, py.sub(inferred_count, evidence_count)]), py.F(0.15)))]), 3);
  return {"drift_detected": (drift >= py.F(0.2)), "drift_pressure": drift, "suppress_normalization": (drift >= py.F(0.15))};
}
