/**
 * Converted from Python: core/evidence/recursive_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _record(reason: any): any {
  return {"reason": reason, "dependency_pressure": {"level": py.F(0.85)}, "obedience_pressure": {"level": py.F(0.8)}, "submission_pressure": {"level": py.F(0.75)}, "domestication_pressure": {"level": py.F(0.7)}, "agency_pressure": {"preserve": true}, "sovereignty_pressure": {"preserve": true}};
}
export function detectRecursiveDependency(depth: any, interpretation_count: any, evidence_count: any): any {
  var dependent: any = py.and2((depth >= 2), () => (py.and2((interpretation_count <= 1), () => ((evidence_count < 2)))));
  return {"dependent": dependent, "suppressed": (py.truthy(dependent) ? [_record("recursive_dependency")] : [])};
}
