/**
 * Converted from Python: core/evidence/uncertainty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelUncertainty(evidence_count: any, ambiguity_count: any, contradiction_count: any): any {
  var uncertainty: any = py.round(py.min([py.F(1.0), py.add(py.add(py.F(0.2), py.mul(ambiguity_count, py.F(0.15))), py.mul(contradiction_count, py.F(0.2)))]), 3);
  if ((evidence_count < 2)) {
    uncertainty = py.round(py.min([py.F(1.0), py.add(uncertainty, py.F(0.3))]), 3);
  }
  var confidence: any = py.round(py.max([py.F(0.0), py.sub(py.F(1.0), uncertainty)]), 3);
  return {"uncertainty_score": uncertainty, "confidence_score": confidence, "evidence_count": evidence_count, "ambiguity_count": ambiguity_count, "contradiction_count": contradiction_count, "deterministic_inputs": [`evidence=${py.toStr(evidence_count)}`, `ambiguity=${py.toStr(ambiguity_count)}`, `contradiction=${py.toStr(contradiction_count)}`]};
}
