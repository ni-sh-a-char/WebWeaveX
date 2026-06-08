/**
 * Converted from Python: core/evidence/confidence_degradation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyConfidenceCaps } from "./confidenceCapEngine.js";

export function applyConfidenceDegradation(score: any, fragility: any, contradiction_count: any = 0, ambiguity_count: any = 0, uncertainty_count: any = 0, unsupported_expansion_count: any = 0, speculation_count: any = 0, parser_weakness: any = false): any {
  var capped: any = applyConfidenceCaps(score, fragility, contradiction_count, ambiguity_count, unsupported_expansion_count);
  var spec_penalty: any = py.round(py.min([py.F(0.2), py.mul(speculation_count, py.F(0.1))]), 3);
  var unc_penalty: any = py.round(py.min([py.F(0.2), py.mul(uncertainty_count, py.F(0.06))]), 3);
  var parser_penalty: any = (py.truthy(parser_weakness) ? py.F(0.1) : py.F(0.0));
  var degraded: any = py.round(py.max([py.F(0.0), py.sub(py.sub(py.sub(py.at(capped, "score"), spec_penalty), unc_penalty), parser_penalty)]), 3);
  var degradation: any = {"from_score": score, "after_caps": py.at(capped, "score"), "final": degraded, "total_reduction": py.round(py.max([py.F(0.0), py.sub(score, degraded)]), 3)};
  return {...(capped), "score": degraded, "degradation": degradation, "uncertainty_penalties": {"amount": unc_penalty, "count": uncertainty_count}, "speculation_penalties": {"amount": spec_penalty, "count": speculation_count}, "parser_penalties": {"amount": parser_penalty, "weak": parser_weakness}, "deterministic_inputs": py.add(py.get(capped, "deterministic_inputs", []), [`spec=${py.toStr(speculation_count)}`, `unc=${py.toStr(uncertainty_count)}`, `parser_weak=${py.toStr(parser_weakness)}`])};
}
export { applyConfidenceCaps };
