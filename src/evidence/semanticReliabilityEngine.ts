/**
 * Converted from Python: core/evidence/semantic_reliability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { assessEvidenceSufficiency } from "./evidenceSufficiencyEngine.js";
import { buildSupport } from "./semanticSupportEngine.js";

export function scoreReliability(evidence: any, ambiguities: any, contradiction_count: any = 0): any {
  var support: any = buildSupport(evidence);
  var sufficiency: any = assessEvidenceSufficiency(evidence);
  var penalty: any = py.min([py.F(0.5), py.add(py.mul(contradiction_count, py.F(0.15)), py.mul(py.len(py.or2(ambiguities, () => ([]))), py.F(0.1)))]);
  var score: any = py.round(py.max([py.F(0.0), py.sub(py.mul(py.at(support, "support_strength"), (py.truthy(py.at(sufficiency, "sufficient")) ? py.F(1.0) : py.F(0.5))), penalty)]), 3);
  return {"reliability_score": score, "support": support, "sufficiency": sufficiency, "deterministic_inputs": py.get(sufficiency, "deterministic_inputs", [])};
}
export { assessEvidenceSufficiency, buildSupport };
