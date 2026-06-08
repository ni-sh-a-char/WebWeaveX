/**
 * Converted from Python: core/evidence/reality_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { refuseUnsupportedContinuity } from "./continuityRefusalEngine.js";
import { preserveEpistemicBoundaries } from "./epistemicBoundaryEngine.js";
import { modelEvidenceBoundaries } from "./evidenceBoundaryEngine.js";
import { detectNarrativeHallucination } from "./narrativeHallucinationEngine.js";
import { modelOntologyBoundaries } from "./ontologyBoundaryEngine.js";
import { ontologyLimits } from "./ontologyLimitEngine.js";
import { applyRealityBoundedConfidence } from "./realityBoundedConfidenceEngine.js";
import { applyRealityConstraints } from "./realityConstraintEngine.js";
import { modelSemanticBoundaries } from "./semanticBoundaryEngine.js";
import { detectSemanticDrift } from "./semanticDriftEngine.js";
import { measureSemanticMomentum } from "./semanticMomentumEngine.js";
import { modelSemanticStability } from "./semanticStabilityEngine.js";
import { semanticStabilityLimits } from "./semanticStabilityLimitEngine.js";
import { terminateSemanticChain } from "./semanticTerminationEngine.js";
import { detectSpeculativeCoherence } from "./speculativeCoherenceEngine.js";
import { modelStabilityBoundary } from "./stabilityBoundaryEngine.js";
import { modelTopologyBoundaries } from "./topologyBoundaryEngine.js";
import { topologyLimits } from "./topologyLimitEngine.js";
import { collectUnsupportedContinuity } from "./unsupportedContinuityEngine.js";
import { computeEvidenceBoundaryPressure } from "../semantic/evidenceBoundaryPressureEngine.js";
import { computeSemanticBoundaryPressure } from "../semantic/semanticBoundaryPressureEngine.js";

export function applyRealityAlignment(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var uncertainties: any = [...py.iter(py.or2(py.get(bundle, "uncertainties", py.get(bundle, "uncertain", [])), () => ([])))];
  if (((uncertainties !== null && typeof uncertainties === "object" && !Array.isArray(uncertainties) && !(uncertainties instanceof Set) && !(uncertainties instanceof Map)))) {
    uncertainties = [...py.iter(py.keys(uncertainties))];
  }
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var noninferable: any = [...py.iter(py.or2(py.get(bundle, "noninferable_regions", []), () => ([])))];
  var fragility: any = py.or2(py.get(bundle, "fragility", py.get(bundle, "semantic_fragility", {})), () => ({}));
  if (!((fragility !== null && typeof fragility === "object" && !Array.isArray(fragility) && !(fragility instanceof Set) && !(fragility instanceof Map)))) {
    fragility = {"level": "medium", "confidence_limits": {"max_score": py.F(0.7)}};
  }
  var parser_basis: any = py.or2(py.get(bundle, "parser_basis", {}), () => ({}));
  var parser_grounded: any = py.or2((py.toInt(py.or2(py.get(parser_basis, "symbol_count", 0), () => (0))) > 0), () => (py.truthy(py.get(bundle, "grounding"))));
  var drift: any = detectSemanticDrift(observed, inferred, reconciled, evidence);
  var unsupported_continuity: any = collectUnsupportedContinuity(evidence, inferred, reconciled);
  var momentum: any = measureSemanticMomentum(py.len(inferred), py.len(evidence));
  var coherence: any = detectSpeculativeCoherence(evidence, inferred, reconciled);
  var narrative: any = detectNarrativeHallucination(inferred, evidence, parser_grounded);
  var ev_bound: any = modelEvidenceBoundaries(evidence);
  var onto_bound: any = modelOntologyBoundaries(evidence, py.and2(py.truthy(inferred), () => (!py.truthy(evidence))));
  var topo_bound: any = modelTopologyBoundaries(evidence, parser_grounded);
  var sem_bound: any = modelSemanticBoundaries(inferred, py.at(ev_bound, "bounded"));
  var stability: any = modelSemanticStability(evidence, py.at(drift, "drift_pressure"), unsupported_continuity, parser_grounded);
  var constraints: any = applyRealityConstraints(evidence, parser_grounded, py.at(drift, "drift_pressure"));
  var epistemic_bound: any = preserveEpistemicBoundaries(evidence, noninferable, py.at(stability, "unstable_regions"));
  var stab_bound: any = modelStabilityBoundary(py.at(stability, "unstable_regions"));
  var ev_pressure: any = computeEvidenceBoundaryPressure(py.len(evidence));
  var bound_pressure: any = computeSemanticBoundaryPressure(py.or2(py.and2(py.get(stab_bound, "broken", false), () => (py.F(1.0))), () => (py.F(0.0))), py.at(drift, "drift_pressure"));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.len(py.get(contradicted, "pairs", [])) : 0);
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var bounded_conf: any = applyRealityBoundedConfidence(py.toFloat(py.get(cb, "score", py.F(0.5))), fragility, py.at(drift, "drift_pressure"), py.len(unsupported_continuity), !py.truthy(parser_grounded), py.get(bound_pressure, "pressure", 0), pairs, py.len(ambiguities), py.len(uncertainties));
  var continuity_refusal: any = refuseUnsupportedContinuity(unsupported_continuity);
  var termination: any = terminateSemanticChain(py.at(stability, "unstable_regions"), py.get(continuity_refusal, "continuity_refusals", []));
  var stab_limits: any = semanticStabilityLimits(stability);
  py.setItem(bundle, "reality_alignment", {"aligned": py.and2(py.at(stability, "stable"), () => (py.at(ev_bound, "bounded"))), "parser_grounded": parser_grounded, "drift_suppressed": py.at(drift, "suppress_continuation"), "continuity_suppressed": py.truthy(unsupported_continuity), "narrative_suppressed": py.get(narrative, "suppressed", false)});
  py.setItem(bundle, "semantic_boundaries", sem_bound);
  py.setItem(bundle, "ontology_boundaries", onto_bound);
  py.setItem(bundle, "topology_boundaries", topo_bound);
  py.setItem(bundle, "evidence_boundaries", ev_bound);
  py.setItem(bundle, "semantic_stability", stability);
  py.setItem(bundle, "drift_pressure", drift);
  py.setItem(bundle, "unsupported_continuity", unsupported_continuity);
  py.setItem(bundle, "reality_constraints", constraints);
  py.setItem(bundle, "unstable_regions", py.at(stability, "unstable_regions"));
  py.setItem(bundle, "boundary_pressure", bound_pressure);
  py.setItem(bundle, "continuity_refusals", py.get(continuity_refusal, "continuity_refusals", []));
  py.setItem(bundle, "stability_failures", py.at(stability, "unstable_regions"));
  py.setItem(bundle, "boundary_failures", py.get(continuity_refusal, "boundary_failures", []));
  py.setItem(bundle, "semantic_limits", {...(py.get(bundle, "semantic_limits", {})), ...(stab_limits), "ontology": ontologyLimits(onto_bound), "topology": topologyLimits(topo_bound)});
  py.setItem(bundle, "termination_reasons", py.sorted(py.toSet(py.add(py.get(bundle, "termination_reasons", []), py.get(continuity_refusal, "termination_reasons", [])))));
  py.setItem(bundle, "epistemic_boundaries", epistemic_bound);
  py.setItem(bundle, "speculative_coherence", coherence);
  py.setItem(bundle, "narrative_hallucination", narrative);
  py.setItem(bundle, "semantic_momentum", momentum);
  py.setItem(bundle, "confidence_basis", {...(cb), ...(bounded_conf)});
  return bundle;
}
export { applyRealityBoundedConfidence, applyRealityConstraints, collectUnsupportedContinuity, computeEvidenceBoundaryPressure, computeSemanticBoundaryPressure, detectNarrativeHallucination, detectSemanticDrift, detectSpeculativeCoherence, measureSemanticMomentum, modelEvidenceBoundaries, modelOntologyBoundaries, modelSemanticBoundaries, modelSemanticStability, modelStabilityBoundary, modelTopologyBoundaries, ontologyLimits, preserveEpistemicBoundaries, refuseUnsupportedContinuity, semanticStabilityLimits, terminateSemanticChain, topologyLimits };
