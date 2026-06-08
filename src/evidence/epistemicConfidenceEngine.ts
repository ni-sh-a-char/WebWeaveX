/**
 * Converted from Python: core/evidence/epistemic_confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { assessEvidenceSufficiency } from "./evidenceSufficiencyEngine.js";
import { buildSupport } from "./semanticSupportEngine.js";
import { buildWeaknesses } from "./semanticWeaknessEngine.js";

export function scoreEpistemicConfidence(evidence: any = null, supporting: any = null, contradicting: any = null, uncertainty_factors: any = null, parser_density: any = 0): any {
  var ev: any = py.sorted(py.toSet(py.iter(py.or2(evidence, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var supporting_evidence: any = py.sorted(py.toSet(py.iter(py.or2(supporting, () => (ev))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var contradicting_evidence: any = py.sorted(py.toSet(py.iter(py.or2(contradicting, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var factors: any = py.sorted(py.toSet(py.iter(py.or2(uncertainty_factors, () => ([]))).filter((f: any) => py.truthy(f)).map((f: any) => py.toStr(f))));
  var sufficiency: any = assessEvidenceSufficiency(ev);
  var support: any = buildSupport(ev);
  var weaknesses: any = buildWeaknesses(ev, factors);
  var base: any = py.at(support, "support_strength");
  if (!py.truthy(py.at(sufficiency, "sufficient"))) {
    base = py.round(py.mul(base, py.F(0.4)), 3);
  }
  base = py.round(py.max([py.F(0.0), py.sub(base, py.mul(py.len(contradicting_evidence), py.F(0.1)))]), 3);
  base = py.round(py.min([py.F(1.0), py.add(base, py.min([py.F(0.15), py.mul(parser_density, py.F(0.02))]))]), 3);
  return {"score": base, "basis": {"support_strength": py.at(support, "support_strength"), "sufficiency": py.at(sufficiency, "status"), "contradiction_pressure": py.len(contradicting_evidence), "parser_density": parser_density, ...(weaknesses)}, "supporting_evidence": supporting_evidence, "contradicting_evidence": contradicting_evidence, "uncertainty_factors": factors, "deterministic_inputs": py.sorted(py.add(py.get(sufficiency, "deterministic_inputs", []), [`support=${py.toStr(py.at(support, "support_count"))}`, `contradict=${py.toStr(py.len(contradicting_evidence))}`]))};
}
export { assessEvidenceSufficiency, buildSupport, buildWeaknesses };
