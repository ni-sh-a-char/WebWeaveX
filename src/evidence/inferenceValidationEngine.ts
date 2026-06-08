/**
 * Converted from Python: core/evidence/inference_validation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { inferFromEvidence } from "./semanticInferenceCalculus.js";

export function validateInference(observed: any, evidence: any): any {
  var r: any = inferFromEvidence(observed, evidence);
  return {"valid": py.at(r, "allowed"), "inference": r, "opaque": false, "deterministic_inputs": py.at(r, "deterministic_inputs")};
}
export { inferFromEvidence };
