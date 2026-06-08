/**
 * Converted from Python: core/evidence/semantic_honesty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function assessSemanticHonesty(evidence: any, supported: any, unsupported: any, fragile: any): any {
  var honest: any = py.and2(!py.truthy(py.get(unsupported, "claims")), () => (!py.eq(py.get(fragile, "level"), "high")));
  return {"honest": honest, "prefers_insufficient_over_certainty": true, "supported_claims": py.len(py.or2(py.get(supported, "keys", []), () => ([]))), "unsupported_claims": py.len(py.or2(py.get(unsupported, "claims", []), () => ([]))), "message": (py.truthy(honest) ? "sufficient_honesty" : "semantic_honesty_warning"), "deterministic_inputs": [`evidence=${py.toStr(py.len(evidence))}`, `fragility=${py.toStr(py.get(fragile, "level", "unknown"))}`]};
}
