/**
 * Converted from Python: core/evidence/semantic_monopoly_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _record(reason: any): any {
  return {"reason": reason, "capture_pressure": {"level": py.F(0.85)}, "authority_pressure": {"level": py.F(0.8)}, "monopoly_pressure": {"level": py.F(0.9)}, "decentralization_pressure": {"preserve": true}, "autonomy_pressure": {"preserve": true}, "plurality_pressure": {"preserve": true}};
}
export function detectSemanticMonopoly(interpretation_count: any, depth: any, evidence_count: any): any {
  var monopoly: any = py.and2((interpretation_count <= 1), () => (py.and2((depth >= 2), () => ((evidence_count < 2)))));
  return {"monopoly": monopoly, "suppressed": (py.truthy(monopoly) ? [_record("semantic_monopoly")] : [])};
}
