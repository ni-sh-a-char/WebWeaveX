/**
 * Converted from Python: core/internet/trust_uncertainty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { propagateUncertaintyMath } from "../evidence/uncertaintyPropagationMath.js";

export function modelTrustUncertainty(evidence_count: any, contradiction_count: any, corroboration: any): any {
  var amb: any = py.max([0, py.sub(2, corroboration)]);
  var u: any = propagateUncertaintyMath(evidence_count, amb, contradiction_count);
  return {...(u), "trust_uncertainty": py.at(u, "uncertainty_score"), "contradiction_pressure": py.min([py.F(1.0), py.mul(contradiction_count, py.F(0.25))])};
}
export { propagateUncertaintyMath };
