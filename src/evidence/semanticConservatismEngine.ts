/**
 * Converted from Python: core/evidence/semantic_conservatism_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function applySemanticConservatism(bundle: any, min_evidence: any = 2): any {
  var evidence: any = py.or2(py.get(bundle, "evidence", []), () => ([]));
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  if ((py.len(evidence) < min_evidence)) {
    py.listAppend(ambiguities, "weak_evidence");
  }
  if ((py.truthy(py.get(contradicted, "preserved")) || py.truthy(py.get(contradicted, "pairs")))) {
    py.listAppend(ambiguities, "unresolved_contradiction");
  }
  var confidence: any = py.pyDict(py.or2(py.get(bundle, "confidence_basis", {}), () => ({})));
  var score: any = py.toFloat(py.get(confidence, "score", py.F(0.5)));
  if ((py.len(evidence) < min_evidence)) {
    score = py.round(py.min([score, py.F(0.35)]), 3);
  }
  if (py.truthy(py.get(contradicted, "preserved"))) {
    score = py.round(py.min([score, py.F(0.45)]), 3);
  }
  py.setItem(confidence, "score", score);
  py.setItem(confidence, "conservative", true);
  py.setItem(confidence, "deterministic_inputs", py.sorted(py.bitor(py.toSet(py.or2(py.get(confidence, "deterministic_inputs", []), () => ([]))), new Set([`evidence_count=${py.toStr(py.len(evidence))}`]))));
  py.setItem(bundle, "ambiguities", py.sorted(py.toSet(py.iter(ambiguities).filter((a: any) => py.truthy(a)).map((a: any) => py.toStr(a)))));
  py.setItem(bundle, "confidence_basis", confidence);
  if (py.truthy(py.get(bundle, "semantic_basis"))) {
    py.setItem(bundle, "semantic_basis", {...(py.at(bundle, "semantic_basis")), "conservative_score": score});
  }
  return bundle;
}
