/**
 * Converted from Python: core/evidence/deterministic_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { combineEvidence } from "./evidenceAlgebraEngine.js";
import { inferFromEvidence } from "./semanticInferenceCalculus.js";

export function reasonDeterministically(observed: any, evidence: any, ambiguities: any): any {
  var algebra: any = combineEvidence(evidence);
  var inference: any = inferFromEvidence(observed, evidence, (py.truthy(py.at(algebra, "sufficient")) ? 1 : 2));
  var conservative: any = py.or2(py.truthy(ambiguities), () => (!py.truthy(py.at(algebra, "sufficient"))));
  return {"algebra": algebra, "inference": inference, "conservative": conservative, "chain_depth": 1, "opaque": false, "deterministic_inputs": py.add(py.at(algebra, "deterministic_inputs"), py.at(inference, "deterministic_inputs"))};
}
export { combineEvidence, inferFromEvidence };
