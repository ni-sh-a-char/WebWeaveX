/**
 * Converted from Python: core/evidence/semantic_restraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyConfidenceCaps } from "./confidenceCapEngine.js";
import { refuseInference } from "./inferenceRefusalEngine.js";
import { modelNoninference } from "./noninferenceEngine.js";
import { modelSemanticBoundaries } from "./semanticBoundaryEngine.js";
import { detectUnsupportedExpansion } from "./unsupportedExpansionEngine.js";
import { modelUnsupportedScope } from "./unsupportedScopeEngine.js";
import { computeContradictionPressure } from "../semantic/contradictionPressureEngine.js";

export function applyEpistemicRestraint(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => (py.or2(py.get(bundle, "contradictions", {}), () => ({}))));
  var fragility: any = py.or2(py.get(bundle, "fragility", py.get(bundle, "fragile", {})), () => ({}));
  var noninf: any = modelNoninference(evidence, inferred, observed, reconciled);
  var pressure: any = computeContradictionPressure(contradicted);
  var pairs: any = py.get(pressure, "pair_count", 0);
  var topo_exp: any = detectUnsupportedExpansion(evidence, "topology", py.len(inferred));
  var onto_exp: any = detectUnsupportedExpansion(evidence, "ontology", 0);
  var unsupported_expansions: any = py.add(py.get(topo_exp, "unsupported_expansions", []), py.get(onto_exp, "unsupported_expansions", []));
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var capped: any = applyConfidenceCaps(py.toFloat(py.get(cb, "score", py.F(0.5))), (((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map))) ? fragility : {}), pairs, py.len(ambiguities), py.len(unsupported_expansions));
  var refusal: any = refuseInference(py.get(noninf, "noninferences", []), py.len(evidence));
  var boundaries: any = modelSemanticBoundaries(inferred, py.get(py.at(noninf, "suppression_basis"), "allowed", false));
  var restraint: any = {"conservative_default": true, "suppress_propagation": py.or2(py.get(pressure, "suppress_propagation", false), () => (py.get(topo_exp, "suppressed"))), "suppress_reconciliation": py.get(pressure, "suppress_reconciliation", false), "noninference_count": py.len(py.get(noninf, "noninferences", []))};
  py.setItem(bundle, "restraint", restraint);
  py.setItem(bundle, "suppressed_inferences", py.get(noninf, "refused_inferences", []));
  py.setItem(bundle, "unsupported_expansions", unsupported_expansions);
  py.setItem(bundle, "confidence_caps", py.get(capped, "caps", {}));
  py.setItem(bundle, "fragility_pressure", {"level": (((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map))) ? py.get(fragility, "level", "unknown") : "unknown"), "contradiction": py.get(pressure, "pressure", 0)});
  py.setItem(bundle, "noninference_reasons", py.get(noninf, "noninferences", []));
  py.setItem(bundle, "semantic_boundaries", boundaries);
  py.setItem(bundle, "noninferences", py.get(noninf, "noninferences", []));
  py.setItem(bundle, "refused_inferences", py.get(noninf, "refused_inferences", []));
  py.setItem(bundle, "boundary_conditions", py.get(noninf, "boundary_conditions", []));
  py.setItem(bundle, "suppression_basis", py.get(noninf, "suppression_basis", {}));
  py.setItem(bundle, "contradiction_pressure", pressure);
  py.setItem(bundle, "boundaries", {...(py.get(bundle, "boundaries", {})), "inference": boundaries, "unsupported_scope": modelUnsupportedScope(py.get(noninf, "noninferences", []))});
  py.setItem(bundle, "noninferable_dimensions", py.get(noninf, "noninferences", []));
  py.setItem(bundle, "inference_refusal", refusal);
  cb = {...(cb), ...(capped)};
  py.setItem(bundle, "confidence_basis", cb);
  return bundle;
}
export { applyConfidenceCaps, computeContradictionPressure, detectUnsupportedExpansion, modelNoninference, modelSemanticBoundaries, modelUnsupportedScope, refuseInference };
