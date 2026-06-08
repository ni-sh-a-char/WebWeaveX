/**
 * Converted from Python: core/internet/contradiction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectContradictionEvidence } from "../evidence/contradictionEvidenceEngine.js";

export function detectContradictions(snippets: any): any {
  var result: any = detectContradictionEvidence(snippets);
  return {"contradiction_pairs": py.get(result, "contradiction_pairs", []), "conflicts": py.get(result, "conflicts", []), "evidence": py.get(result, "evidence", []), "sources": py.get(result, "sources", []), "grounding": py.get(result, "grounding", {}), "lineage": py.get(result, "lineage", {}), "confidence_basis": py.get(result, "confidence_basis", {})};
}
export { detectContradictionEvidence };
