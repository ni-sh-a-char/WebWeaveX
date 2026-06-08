/**
 * Converted from Python: core/evidence/confidence_collapse_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyRealityBoundedConfidence } from "./realityBoundedConfidenceEngine.js";

export function applyConfidenceCollapse(score: any, fragility: any, reinforcement_count: any = 0, stabilization_count: any = 0, decay_pressure: any = py.F(0.0), truth_boundary_pressure: any = py.F(0.0), contradiction_count: any = 0, ambiguity_count: any = 0, uncertainty_count: any = 0, incompleteness: any = false): any {
  var base: any = applyRealityBoundedConfidence(score, fragility, decay_pressure, stabilization_count, undefined, truth_boundary_pressure, contradiction_count, ambiguity_count, uncertainty_count);
  var reinf_pen: any = py.round(py.min([py.F(0.3), py.mul(reinforcement_count, py.F(0.12))]), 3);
  var stab_pen: any = py.round(py.min([py.F(0.25), py.mul(stabilization_count, py.F(0.1))]), 3);
  var incom_pen: any = (py.truthy(incompleteness) ? py.F(0.08) : py.F(0.0));
  var collapse: any = py.round(py.add(py.add(reinf_pen, stab_pen), incom_pen), 3);
  var final: any = py.round(py.max([py.F(0.0), py.sub(py.at(base, "score"), collapse)]), 3);
  return {...(base), "score": final, "collapse_pressure": {"reinforcement": reinf_pen, "stabilization": stab_pen, "incompleteness": incom_pen, "total": collapse}, "truth_penalties": {"boundary": truth_boundary_pressure, "decay": decay_pressure}, "instability_penalties": {"amount": stab_pen}, "reinforcement_penalties": {"amount": reinf_pen, "count": reinforcement_count}, "deterministic_inputs": py.add(py.get(base, "deterministic_inputs", []), [`reinf=${py.toStr(reinforcement_count)}`, `stab=${py.toStr(stabilization_count)}`, `incomplete=${py.toStr(incompleteness)}`])};
}
export { applyRealityBoundedConfidence };
