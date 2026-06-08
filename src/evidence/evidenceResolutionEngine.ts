/**
 * Converted from Python: core/evidence/evidence_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { combineEvidence } from "./evidenceAlgebraEngine.js";
import { weightEvidenceCalculus } from "./evidenceWeightingCalculus.js";

export function resolveEvidence(evidence: any, parser_backed: any = false): any {
  var algebra: any = combineEvidence(evidence);
  var weights: any = weightEvidenceCalculus(evidence, parser_backed);
  var resolved: any = (py.truthy(py.at(algebra, "sufficient")) ? py.at(algebra, "items") : py.slice(py.at(algebra, "items"), null, 1));
  return {"resolved": resolved, "sufficient": py.at(algebra, "sufficient"), "weights": py.at(weights, "weights"), "deterministic_inputs": py.add(py.at(algebra, "deterministic_inputs"), py.at(weights, "deterministic_inputs"))};
}
export { combineEvidence, weightEvidenceCalculus };
