/**
 * Converted from Python: core/evidence/truth_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applyConfidenceCollapse } from "./confidenceCollapseEngine.js";
import { detectConfidenceEcho } from "./confidenceEchoEngine.js";
import { modelEvidenceDecay } from "./evidenceDecayEngine.js";
import { preserveInstability } from "./instabilityPreservationEngine.js";
import { modelSemanticDecay } from "./semanticDecayEngine.js";
import { modelSemanticEntropy } from "./semanticEntropyEngine.js";
import { modelSemanticInstability } from "./semanticInstabilityEngine.js";
import { detectSemanticSelfReinforcement } from "./semanticSelfReinforcementEngine.js";
import { semanticTruthLimits } from "./semanticTruthLimitEngine.js";
import { terminateStabilization } from "./stabilizationTerminationEngine.js";
import { modelTruthBoundaries } from "./truthBoundaryEngine.js";
import { refuseUnsupportedStabilization } from "./truthRefusalEngine.js";
import { detectUnsupportedStabilization } from "./unsupportedStabilizationEngine.js";
import { computeEvidenceDecayPressure } from "../semantic/evidenceDecayPressureEngine.js";
import { computeTruthBoundaryPressure } from "../semantic/truthBoundaryPressureEngine.js";

export function applyTruthPreservation(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var uncertainties: any = [...py.iter(py.or2(py.get(bundle, "uncertainties", py.get(bundle, "uncertain", [])), () => ([])))];
  if (((uncertainties !== null && typeof uncertainties === "object" && !Array.isArray(uncertainties) && !(uncertainties instanceof Set) && !(uncertainties instanceof Map)))) {
    uncertainties = [...py.iter(py.keys(uncertainties))];
  }
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", py.get(bundle, "contradictions", {})), () => ({}));
  var unstable_regions: any = [...py.iter(py.or2(py.get(bundle, "unstable_regions", []), () => ([])))];
  var fragility: any = py.or2(py.get(bundle, "fragility", py.get(bundle, "semantic_fragility", {})), () => ({}));
  if (!((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map)))) {
    fragility = {"level": "medium", "confidence_limits": {"max_score": py.F(0.7)}};
  }
  var stabilization: any = detectUnsupportedStabilization(evidence, inferred, reconciled);
  var suppressed_stab: any = py.get(stabilization, "suppressed_stabilizations", []);
  var reinforcement: any = detectSemanticSelfReinforcement(inferred, reconciled, evidence);
  var entropy: any = modelSemanticEntropy(ambiguities, uncertainties, contradicted);
  var ev_decay: any = modelEvidenceDecay(evidence);
  var sem_decay: any = modelSemanticDecay(evidence, inferred, py.get(stabilization, "count", 0));
  var truth_bound: any = modelTruthBoundaries(evidence);
  var instability: any = preserveInstability(unstable_regions, evidence, suppressed_stab);
  var sem_instability: any = modelSemanticInstability(py.at(instability, "regions"), entropy, evidence);
  var ev_pressure: any = computeEvidenceDecayPressure(py.len(evidence));
  var truth_pressure: any = computeTruthBoundaryPressure(py.at(truth_bound, "truth_bounded"), py.at(entropy, "entropy"));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.len(py.get(contradicted, "pairs", [])) : 0);
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var raw_score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var echo: any = detectConfidenceEcho(raw_score, []);
  if (py.truthy(py.get(echo, "suppress"))) {
    raw_score = py.at(echo, "collapse_to");
  }
  var collapsed: any = applyConfidenceCollapse(raw_score, fragility, (py.truthy(py.get(reinforcement, "reinforcement_detected")) ? 1 : 0), py.get(stabilization, "count", 0), py.at(sem_decay, "decay_rate"), py.get(truth_pressure, "pressure", 0), pairs, py.len(ambiguities), py.len(uncertainties), py.get(ev_decay, "incomplete", false));
  var refusal: any = refuseUnsupportedStabilization(suppressed_stab);
  var termination: any = terminateStabilization(suppressed_stab, py.at(sem_instability, "regions"));
  var truth_limits: any = semanticTruthLimits(entropy, instability);
  py.setItem(bundle, "truth_preservation", {"preserved": true, "prefer_truthfully_incomplete": true, "stabilization_suppressed": py.get(stabilization, "count", 0), "echo_suppressed": py.get(echo, "suppress", false)});
  py.setItem(bundle, "semantic_decay", sem_decay);
  py.setItem(bundle, "confidence_collapse", py.get(collapsed, "collapse_pressure", {}));
  py.setItem(bundle, "instability", {...(instability), ...(sem_instability)});
  py.setItem(bundle, "truth_boundaries", truth_bound);
  py.setItem(bundle, "unsupported_stabilization", suppressed_stab);
  py.setItem(bundle, "semantic_entropy", entropy);
  py.setItem(bundle, "evidence_decay", ev_decay);
  py.setItem(bundle, "semantic_instability", sem_instability);
  py.setItem(bundle, "truth_pressure", truth_pressure);
  py.setItem(bundle, "entropy", entropy);
  py.setItem(bundle, "truth_refusals", py.get(refusal, "truth_refusals", []));
  py.setItem(bundle, "stabilization_failures", py.get(refusal, "stabilization_failures", []));
  py.setItem(bundle, "truth_boundary_failures", py.get(refusal, "truth_boundary_failures", []));
  py.setItem(bundle, "termination_reasons", py.sorted(py.toSet(py.add(py.get(bundle, "termination_reasons", []), py.get(refusal, "termination_reasons", [])))));
  py.setItem(bundle, "semantic_limits", {...(py.get(bundle, "semantic_limits", {})), ...(truth_limits)});
  py.setItem(bundle, "confidence_basis", {...(cb), ...(collapsed)});
  return bundle;
}
export { applyConfidenceCollapse, computeEvidenceDecayPressure, computeTruthBoundaryPressure, detectConfidenceEcho, detectSemanticSelfReinforcement, detectUnsupportedStabilization, modelEvidenceDecay, modelSemanticDecay, modelSemanticEntropy, modelSemanticInstability, modelTruthBoundaries, preserveInstability, refuseUnsupportedStabilization, semanticTruthLimits, terminateStabilization };
