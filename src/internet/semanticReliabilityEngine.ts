/**
 * Converted from Python: core/internet/semantic_reliability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { scoreEvidenceReliability } from "./evidenceReliabilityEngine.js";

export function scoreSemanticReliability(evidence: any, parser_backed: any = false): any {
  var r: any = scoreEvidenceReliability(evidence, parser_backed);
  return {...(r), "reliability_basis": "evidence_weight_calculus", "opaque": false};
}
export { scoreEvidenceReliability };
