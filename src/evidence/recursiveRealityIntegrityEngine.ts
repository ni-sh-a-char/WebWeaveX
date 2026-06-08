/**
 * Converted from Python: core/evidence/recursive_reality_integrity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectRecursiveCoherenceInflation } from "./recursiveCoherenceInflationEngine.js";
import { applyRecursiveConfidenceDecay } from "./recursiveConfidenceDecayEngine.js";
import { detectRecursiveConfidenceEcho } from "./recursiveConfidenceEchoEngine.js";
import { detectRecursiveDrift } from "./recursiveDriftEngine.js";
import { modelRecursiveEntropy } from "./recursiveEntropyEngine.js";
import { trackRecursiveEvidenceAncestry } from "./recursiveEvidenceAncestryEngine.js";
import { modelRecursiveInstability } from "./recursiveInstabilityEngine.js";
import { preserveRecursiveLineage } from "./recursiveLineageEngine.js";
import { preserveRecursiveProvenance } from "./recursiveProvenanceEngine.js";
import { recursiveRealityLimits } from "./recursiveRealityLimitEngine.js";
import { detectRecursiveSelfConfirmation } from "./recursiveSelfConfirmationEngine.js";
import { detectRecursiveSemanticClosure } from "./recursiveSemanticClosureEngine.js";
import { terminateRecursiveStabilization } from "./recursiveStabilizationTerminationEngine.js";
import { modelRecursiveTruthBoundaries } from "./recursiveTruthBoundaryEngine.js";
import { refuseRecursiveStabilization } from "./recursiveTruthRefusalEngine.js";
import { preserveRecursiveUncertainty } from "./recursiveUncertaintyPreservationEngine.js";
import { recursiveOntologyLimits } from "./recursiveOntologyLimitEngine.js";
import { recursiveTopologyLimits } from "./recursiveTopologyLimitEngine.js";
import { computeRecursiveBoundaryPressure } from "../semantic/recursiveBoundaryPressureEngine.js";

export function _lineageDepth(bundle: any): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var stages: any = py.get(lineage, "stages", []);
  if (((Array.isArray(stages)) && py.truthy(stages))) {
    return py.len(stages);
  }
  return py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0)));
}
export function applyRecursiveRealityIntegrity(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var uncertainties: any = [...py.iter(py.or2(py.get(bundle, "uncertainties", py.get(bundle, "uncertain", [])), () => ([])))];
  if (((uncertainties !== null && typeof uncertainties === "object" && !Array.isArray(uncertainties) && !(uncertainties instanceof Set) && !(uncertainties instanceof Map)))) {
    uncertainties = [...py.iter(py.keys(uncertainties))];
  }
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", py.get(bundle, "contradictions", {})), () => ({}));
  var instability_obj: any = py.get(bundle, "instability", {});
  var unstable_regions: any = [...py.iter(py.get(bundle, "unstable_regions", (((instability_obj !== null && typeof instability_obj === "object" && !Array.isArray(instability_obj) && !(instability_obj instanceof Set) && !(instability_obj instanceof Map))) ? py.get(instability_obj, "regions", []) : [])))];
  var fragility: any = py.or2(py.get(bundle, "fragility", py.get(bundle, "semantic_fragility", {})), () => ({}));
  if (!((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map)))) {
    fragility = {"level": "medium", "confidence_limits": {"max_score": py.F(0.7)}};
  }
  var depth: any = _lineageDepth(bundle);
  var closure: any = detectRecursiveSemanticClosure(depth, inferred, reconciled, evidence);
  var suppressed: any = py.get(closure, "suppressed_closures", []);
  var drift: any = detectRecursiveDrift(depth, py.len(evidence), py.len(inferred));
  var rentropy: any = modelRecursiveEntropy(ambiguities, uncertainties, contradicted, depth);
  var rinstability: any = modelRecursiveInstability(unstable_regions, depth, py.len(evidence));
  var rboundaries: any = modelRecursiveTruthBoundaries(depth, py.len(evidence));
  var runcertainty: any = preserveRecursiveUncertainty(uncertainties, depth);
  var lineage_p: any = preserveRecursiveLineage(py.get(bundle, "lineage", {}), evidence, ambiguities, uncertainties, contradicted);
  var provenance_p: any = preserveRecursiveProvenance(py.get(bundle, "sources", []), lineage_p);
  var ancestry: any = trackRecursiveEvidenceAncestry(evidence, depth);
  var self_confirm: any = detectRecursiveSelfConfirmation(depth, py.eq(reconciled, inferred), py.len(evidence));
  var coherence_inf: any = detectRecursiveCoherenceInflation(depth, py.get(closure, "closure_pressure", 0));
  var bound_pressure: any = computeRecursiveBoundaryPressure(py.get(rboundaries, "erosion", 0), depth);
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.len(py.get(contradicted, "pairs", [])) : 0);
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var raw_score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var echo: any = detectRecursiveConfidenceEcho(raw_score, depth, []);
  if (py.truthy(py.get(echo, "suppress"))) {
    raw_score = py.at(echo, "decay_to");
  }
  var decayed: any = applyRecursiveConfidenceDecay(raw_score, fragility, depth, py.or2(py.and2(py.get(closure, "closure_detected"), () => (py.len(suppressed))), () => (0)), py.at(drift, "drift_pressure"), py.at(rentropy, "entropy"), pairs, py.len(ambiguities), py.len(uncertainties));
  var refusal: any = refuseRecursiveStabilization(suppressed);
  var termination: any = terminateRecursiveStabilization(suppressed, depth);
  var limits: any = recursiveRealityLimits(depth, rentropy);
  py.setItem(bundle, "recursive_reality_integrity", {"preserved": true, "depth": depth, "closure_suppressed": py.get(closure, "closure_detected", false), "echo_suppressed": py.get(echo, "suppress", false), "self_confirmation_suppressed": py.get(self_confirm, "suppress", false)});
  py.setItem(bundle, "recursive_entropy", rentropy);
  py.setItem(bundle, "recursive_instability", rinstability);
  py.setItem(bundle, "recursive_truth_boundaries", rboundaries);
  py.setItem(bundle, "recursive_drift", drift);
  py.setItem(bundle, "recursive_semantic_closure", closure);
  py.setItem(bundle, "recursive_confidence_decay", py.get(decayed, "recursive_decay", {}));
  py.setItem(bundle, "recursive_uncertainty", runcertainty);
  py.setItem(bundle, "recursive_lineage", lineage_p);
  py.setItem(bundle, "recursive_provenance", provenance_p);
  py.setItem(bundle, "recursive_evidence_ancestry", ancestry);
  py.setItem(bundle, "recursive_truth_refusals", py.get(refusal, "recursive_truth_refusals", []));
  py.setItem(bundle, "recursive_stabilization_failures", py.get(refusal, "recursive_stabilization_failures", []));
  py.setItem(bundle, "recursive_limits", {...(limits), "ontology": recursiveOntologyLimits(depth), "topology": recursiveTopologyLimits(depth)});
  py.setItem(bundle, "recursive_termination_reasons", py.sorted(py.toSet(py.add(py.get(bundle, "recursive_termination_reasons", []), py.get(refusal, "recursive_termination_reasons", [])))));
  py.setItem(bundle, "recursive_boundary_failures", py.get(refusal, "recursive_boundary_failures", []));
  py.setItem(bundle, "confidence_basis", {...(cb), ...(decayed)});
  return bundle;
}
export { applyRecursiveConfidenceDecay, computeRecursiveBoundaryPressure, detectRecursiveCoherenceInflation, detectRecursiveConfidenceEcho, detectRecursiveDrift, detectRecursiveSelfConfirmation, detectRecursiveSemanticClosure, modelRecursiveEntropy, modelRecursiveInstability, modelRecursiveTruthBoundaries, preserveRecursiveLineage, preserveRecursiveProvenance, preserveRecursiveUncertainty, recursiveOntologyLimits, recursiveRealityLimits, recursiveTopologyLimits, refuseRecursiveStabilization, terminateRecursiveStabilization, trackRecursiveEvidenceAncestry };
