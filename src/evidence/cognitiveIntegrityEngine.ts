/**
 * Converted from Python: core/evidence/cognitive_integrity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelEpistemicLimits } from "./epistemicLimitEngine.js";
import { modelInferenceIntegrity } from "./inferenceIntegrityEngine.js";
import { modelInferenceLimits } from "./inferenceLimitEngine.js";
import { modelFragility } from "./semanticFragilityEngine.js";
import { assessSemanticHonesty } from "./semanticHonestyEngine.js";
import { detectSemanticOverreach } from "./semanticOverreachEngine.js";
import { suppressUnsupportedInference } from "./unsupportedInferenceEngine.js";
import { modelUnsupportedScope } from "./unsupportedScopeEngine.js";

export function applyCognitiveIntegrity(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => (py.or2(py.get(bundle, "contradictions", {}), () => ({}))));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var parser_basis: any = py.or2(py.get(bundle, "parser_basis", {}), () => ({}));
  var parser_density: any = py.toInt(py.or2(py.get(parser_basis, "symbol_count", 0), () => (0)));
  var fragility: any = modelFragility(evidence, ambiguities, py.len(pairs), parser_density);
  var suppression: any = suppressUnsupportedInference(evidence, inferred, observed);
  var overreach: any = detectSemanticOverreach(evidence, inferred, reconciled);
  var supported: any = {"keys": py.sorted(py.keys(observed)), "evidence": evidence};
  var unsupported: any = {"claims": py.get(suppression, "unsupported_dimensions", []), "dimensions": modelUnsupportedScope(py.get(suppression, "unsupported_dimensions", []))};
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var supporting: any = [...py.iter(py.get(cb, "supporting_evidence", evidence))];
  var contradicting: any = [...py.iter(py.get(cb, "contradicting_evidence", []))];
  var inference: any = modelInferenceIntegrity(evidence, supporting, contradicting, fragility);
  var limits: any = modelEpistemicLimits(evidence, parser_density, fragility);
  var boundaries: any = modelInferenceLimits((py.truthy(py.get(suppression, "allowed_inference")) ? inferred : {}), py.len(evidence));
  var honesty: any = assessSemanticHonesty(evidence, supported, unsupported, fragility);
  var cap: any = py.toFloat(py.get(py.get(fragility, "confidence_limits", {}), "max_score", py.F(1.0)));
  var score: any = py.round(py.min([py.toFloat(py.get(cb, "score", py.F(0.5))), cap]), 3);
  cb = {...(cb), "score": score, "support_basis": py.get(inference, "basis", {}), "fragility_basis": py.get(fragility, "basis", {}), "uncertainty_basis": py.get(bundle, "uncertainties", {}), "contradiction_basis": {"count": py.len(pairs)}, "confidence_limits": py.get(fragility, "confidence_limits", {})};
  py.setItem(bundle, "supported", supported);
  py.setItem(bundle, "unsupported", unsupported);
  py.setItem(bundle, "fragile", fragility);
  py.setItem(bundle, "uncertain", py.get(bundle, "uncertainties", {}));
  py.setItem(bundle, "contradicted", contradicted);
  py.setItem(bundle, "incomplete", py.get(py.get(bundle, "epistemic_state", {}), "incomplete", false));
  py.setItem(bundle, "confidence_limits", py.get(fragility, "confidence_limits", {}));
  py.setItem(bundle, "semantic_honesty", honesty);
  py.setItem(bundle, "fragility", fragility);
  py.setItem(bundle, "inference_integrity", inference);
  py.setItem(bundle, "epistemic_limits", limits);
  py.setItem(bundle, "unsupported_scope", py.get(unsupported, "dimensions", {}));
  py.setItem(bundle, "inference_boundaries", boundaries);
  py.setItem(bundle, "confidence_basis", cb);
  if (py.truthy(py.get(overreach, "overreach_detected"))) {
    ambiguities = py.sorted(py.toSet(py.add(ambiguities, py.get(overreach, "overreach_flags", []))));
    py.setItem(bundle, "ambiguities", ambiguities);
  }
  if ((!py.truthy(py.get(suppression, "allowed_inference")) && py.truthy(inferred))) {
    py.setItem(unsupported, "inferred_keys", py.sorted(py.keys(inferred)));
    ambiguities = py.sorted(py.toSet(py.add(ambiguities, ["unsupported_inference"])));
    py.setItem(bundle, "ambiguities", ambiguities);
  }
  return bundle;
}
export { assessSemanticHonesty, detectSemanticOverreach, modelEpistemicLimits, modelFragility, modelInferenceIntegrity, modelInferenceLimits, modelUnsupportedScope, suppressUnsupportedInference };
