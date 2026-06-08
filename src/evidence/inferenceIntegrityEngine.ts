/**
 * Converted from Python: core/evidence/inference_integrity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelInferenceIntegrity(evidence: any, supporting: any, contradicting: any, fragility: any, missing_evidence: any = null): any {
  var caps: any = py.get(fragility, "confidence_limits", {});
  return {"basis": py.get(fragility, "basis", {}), "supporting_evidence": py.sorted(py.toSet(py.or2(supporting, () => (evidence)))), "contradicting_evidence": py.sorted(py.toSet(py.or2(contradicting, () => ([])))), "missing_evidence": py.sorted(py.toSet(py.or2(missing_evidence, () => (py.get(fragility, "missing_support", []))))), "uncertainty_factors": py.get(fragility, "contradiction_pressure", []), "confidence_caps": [py.get(caps, "max_score", py.F(1.0))], "unsupported_dimensions": py.get(fragility, "missing_support", []), "fragility": fragility};
}
