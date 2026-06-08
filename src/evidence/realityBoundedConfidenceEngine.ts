/**
 * Converted from Python: core/evidence/reality_bounded_confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyConfidenceDegradation } from "./confidenceDegradationEngine.js";

export function applyRealityBoundedConfidence(score: any, fragility: any, drift_pressure: any = py.F(0.0), continuity_count: any = 0, parser_gap: any = false, boundary_pressure: any = py.F(0.0), contradiction_count: any = 0, ambiguity_count: any = 0, uncertainty_count: any = 0): any {
  var base: any = applyConfidenceDegradation(score, fragility, contradiction_count, ambiguity_count, uncertainty_count, continuity_count, continuity_count, parser_gap);
  var drift_pen: any = py.round(py.min([py.F(0.25), py.mul(drift_pressure, py.F(0.3))]), 3);
  var boundary_pen: any = py.round(py.min([py.F(0.2), py.mul(boundary_pressure, py.F(0.25))]), 3);
  var reality_pen: any = py.round(py.add(drift_pen, boundary_pen), 3);
  var final: any = py.round(py.max([py.F(0.0), py.sub(py.at(base, "score"), reality_pen)]), 3);
  return {...(base), "score": final, "reality_penalties": {"drift": drift_pen, "boundary": boundary_pen, "total": reality_pen}, "stability_penalties": {"continuity": py.round(py.min([py.F(0.2), py.mul(continuity_count, py.F(0.08))]), 3)}, "drift_penalties": {"amount": drift_pen, "pressure": drift_pressure}, "boundary_penalties": {"amount": boundary_pen, "pressure": boundary_pressure}, "deterministic_inputs": py.add(py.get(base, "deterministic_inputs", []), [`drift=${py.floatStr(drift_pressure)}`, `boundary=${py.floatStr(boundary_pressure)}`, `parser_gap=${py.toStr(parser_gap)}`])};
}
export { applyConfidenceDegradation };
