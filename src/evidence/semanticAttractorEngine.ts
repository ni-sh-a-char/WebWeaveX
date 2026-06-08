/**
 * Converted from Python: core/evidence/semantic_attractor_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _record(reason: any): any {
  return {"reason": reason, "attractor_pressure": {"level": py.F(0.85)}, "gravity_pressure": {"level": py.F(0.8)}, "stabilization_pressure": {"level": py.F(0.75)}, "fixation_pressure": {"level": py.F(0.7)}, "phase_space_pressure": {"preserve": true}, "exploration_pressure": {"maintain": true}};
}
export function detectSemanticAttractor(depth: any, interpretation_count: any, evidence_count: any): any {
  var attractor: any = py.and2((depth >= 2), () => (py.and2((interpretation_count <= 1), () => ((evidence_count < 2)))));
  return {"attractor": attractor, "suppressed": (py.truthy(attractor) ? [_record("semantic_attractor")] : [])};
}
