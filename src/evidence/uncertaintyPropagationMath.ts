/**
 * Converted from Python: core/evidence/uncertainty_propagation_math.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelUncertainty } from "./uncertaintyEngine.js";

export function propagateUncertaintyMath(evidence_count: any, ambiguity_count: any, contradiction_count: any, parent_uncertainty: any = py.F(0.0)): any {
  var local: any = modelUncertainty(evidence_count, ambiguity_count, contradiction_count);
  var u_local: any = py.at(local, "uncertainty_score");
  var u_combined: any = py.round(py.sub(py.F(1.0), py.mul(py.sub(py.F(1.0), parent_uncertainty), py.sub(py.F(1.0), u_local))), 3);
  var confidence: any = py.round(py.max([py.F(0.0), py.sub(py.F(1.0), u_combined)]), 3);
  return {...(local), "uncertainty_score": u_combined, "confidence_score": confidence, "parent_uncertainty": parent_uncertainty, "propagation": "multiplicative_complement", "deterministic_inputs": py.add(py.at(local, "deterministic_inputs"), [`parent=${py.floatStr(parent_uncertainty)}`, `combined=${py.floatStr(u_combined)}`])};
}
export { modelUncertainty };
