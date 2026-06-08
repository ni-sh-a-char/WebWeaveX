/**
 * Converted from Python: core/runtime/runtime_proof_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function proveRuntimeConsistency(transitions: any, evidence: any): any {
  var invalid: any = py.iter(transitions).filter((t: any) => !py.truthy(py.get(t, "valid", true))).map((t: any) => t);
  return {"valid": py.eq(py.len(invalid), 0), "invalid_count": py.len(invalid), "evidence": py.sorted(py.toSet(evidence)), "grounded": py.truthy(evidence), "deterministic": true};
}
