/**
 * Converted from Python: core/evidence/recursive_confidence_decay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyConfidenceCollapse } from "./confidenceCollapseEngine.js";

export function applyRecursiveConfidenceDecay(score: any, fragility: any, depth: any = 0, closure_count: any = 0, drift_pressure: any = py.F(0.0), entropy: any = py.F(0.0), contradiction_count: any = 0, ambiguity_count: any = 0, uncertainty_count: any = 0): any {
  var base: any = applyConfidenceCollapse(score, fragility, undefined, closure_count, drift_pressure, py.mul(depth, py.F(0.05)), contradiction_count, ambiguity_count, uncertainty_count);
  var depth_pen: any = py.round(py.min([py.F(0.35), py.mul(depth, py.F(0.08))]), 3);
  var entropy_pen: any = py.round(py.min([py.F(0.2), py.mul(entropy, py.F(0.25))]), 3);
  var final: any = py.round(py.max([py.F(0.0), py.sub(py.sub(py.at(base, "score"), depth_pen), entropy_pen)]), 3);
  return {...(base), "score": final, "recursive_decay": {"depth_penalty": depth_pen, "entropy_penalty": entropy_pen, "final": final}, "recursive_pressure": {"depth": depth, "closure": closure_count}, "recursive_penalties": {"depth": depth_pen, "entropy": entropy_pen}, "recursive_entropy": {"level": entropy}, "recursive_instability": {"pressure": drift_pressure}, "deterministic_inputs": py.add(py.get(base, "deterministic_inputs", []), [`depth=${py.toStr(depth)}`, `entropy=${py.floatStr(entropy)}`])};
}
export { applyConfidenceCollapse };
