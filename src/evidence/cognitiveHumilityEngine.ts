/**
 * Converted from Python: core/evidence/cognitive_humility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { exposeAmbiguityVisibility } from "./ambiguityVisibilityEngine.js";
import { applyConfidenceDegradation } from "./confidenceDegradationEngine.js";
import { terminateInferenceChain } from "./inferenceTerminationEngine.js";
import { modelNoninferableRegions } from "./noninferableScopeEngine.js";
import { semanticLimits } from "./semanticLimitEngine.js";
import { refuseUnsupportedConclusions } from "./semanticRefusalEngine.js";
import { applySemanticSelfLimitation } from "./semanticSelfLimitationEngine.js";
import { detectSemanticSpeculation } from "./semanticSpeculationEngine.js";
import { exposeUncertaintyVisibility } from "./uncertaintyVisibilityEngine.js";
import { blockUnsupportedConfidenceEscalation } from "./unsupportedConfidenceEngine.js";
import { modelFragility } from "./semanticFragilityEngine.js";
import { computeAmbiguityPressure } from "../semantic/ambiguityPressureEngine.js";
import { computeUncertaintyPressure } from "../semantic/uncertaintyPressureEngine.js";

export function applyCognitiveHumility(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var uncertainties: any = [...py.iter(py.or2(py.get(bundle, "uncertainties", py.get(bundle, "uncertain", [])), () => ([])))];
  if (((uncertainties !== null && typeof uncertainties === "object" && !Array.isArray(uncertainties) && !(uncertainties instanceof Set) && !(uncertainties instanceof Map)))) {
    uncertainties = [...py.iter(py.keys(uncertainties))];
  }
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var noninferences: any = [...py.iter(py.or2(py.get(bundle, "noninferences", py.get(bundle, "noninference_reasons", [])), () => ([])))];
  var fragility: any = py.or2(py.get(bundle, "fragility", py.get(bundle, "fragile", {})), () => ({}));
  if (!((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map)))) {
    fragility = modelFragility(evidence, ambiguities, py.len(uncertainties));
  }
  var speculation: any = detectSemanticSpeculation(evidence, inferred, reconciled);
  var suppressed_speculation: any = py.get(speculation, "suppressed_speculation", []);
  var scope: any = modelNoninferableRegions(inferred, evidence, noninferences);
  var noninferable_regions: any = py.get(scope, "noninferable_regions", []);
  var unc_vis: any = exposeUncertaintyVisibility(uncertainties, ambiguities, py.F(0.5));
  var amb_vis: any = exposeAmbiguityVisibility(ambiguities, py.F(0.5));
  var unc_pressure: any = computeUncertaintyPressure(uncertainties, ambiguities);
  var amb_pressure: any = computeAmbiguityPressure(ambiguities);
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.len(py.get(contradicted, "pairs", [])) : 0);
  var parser_basis: any = py.or2(py.get(bundle, "parser_basis", {}), () => ({}));
  var parser_weak: any = (py.toInt(py.or2(py.get(parser_basis, "symbol_count", 0), () => (0))) < 1);
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var raw_score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var escalation: any = blockUnsupportedConfidenceEscalation(raw_score, py.len(evidence));
  var degraded: any = applyConfidenceDegradation(py.at(escalation, "capped_score"), fragility, pairs, py.len(ambiguities), py.len(uncertainties), py.len(py.or2(py.get(bundle, "unsupported_expansions", []), () => ([]))), py.len(suppressed_speculation), parser_weak);
  var self_limitation: any = applySemanticSelfLimitation(evidence, suppressed_speculation, noninferable_regions);
  var refusal: any = refuseUnsupportedConclusions(noninferable_regions, suppressed_speculation);
  var termination: any = terminateInferenceChain([...py.iter(py.or2(py.get(bundle, "refused_inferences", []), () => ([])))], suppressed_speculation);
  var limits: any = semanticLimits(py.len(evidence), noninferable_regions, self_limitation);
  py.setItem(bundle, "humility", {"self_limiting": true, "prefer_cannot_determine": true, "speculation_suppressed": py.len(suppressed_speculation), "uncertainty_pressure": py.get(unc_pressure, "pressure", 0), "ambiguity_pressure": py.get(amb_pressure, "pressure", 0)});
  py.setItem(bundle, "noninferable_regions", noninferable_regions);
  py.setItem(bundle, "suppressed_speculation", suppressed_speculation);
  py.setItem(bundle, "confidence_degradation", py.get(degraded, "degradation", {}));
  py.setItem(bundle, "uncertainty_visibility", unc_vis);
  py.setItem(bundle, "ambiguity_visibility", amb_vis);
  py.setItem(bundle, "semantic_fragility", fragility);
  py.setItem(bundle, "self_limitation", self_limitation);
  py.setItem(bundle, "refusals", py.get(refusal, "refusals", []));
  py.setItem(bundle, "terminated_inferences", py.get(termination, "terminated_inferences", []));
  py.setItem(bundle, "semantic_limits", limits);
  py.setItem(bundle, "termination_reasons", py.get(refusal, "termination_reasons", []));
  py.setItem(bundle, "unsupported_regions", py.get(refusal, "unsupported_regions", []));
  py.setItem(bundle, "inference_voids", py.get(scope, "inference_voids", []));
  py.setItem(bundle, "epistemic_limits", py.get(scope, "epistemic_limits", {}));
  py.setItem(bundle, "boundaries", {...(py.get(bundle, "boundaries", {})), ...(py.get(scope, "semantic_boundaries", {}))});
  py.setItem(bundle, "confidence_basis", {...(cb), ...(degraded)});
  return bundle;
}
export { applyConfidenceDegradation, applySemanticSelfLimitation, blockUnsupportedConfidenceEscalation, computeAmbiguityPressure, computeUncertaintyPressure, detectSemanticSpeculation, exposeAmbiguityVisibility, exposeUncertaintyVisibility, modelFragility, modelNoninferableRegions, refuseUnsupportedConclusions, semanticLimits, terminateInferenceChain };
