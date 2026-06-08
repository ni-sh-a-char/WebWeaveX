/**
 * Converted from Python: core/evidence/civilizational_epistemic_openness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectCognitiveGravityWell } from "./cognitiveGravityEngine.js";
import { applyExplanatoryAntigravity } from "./explanatoryAntigravityEngine.js";
import { modelExplanatoryDivergence } from "./explanatoryDivergenceEngine.js";
import { detectExplanatoryFixation } from "./explanatoryFixationEngine.js";
import { modelInterpretiveDivergence } from "./interpretiveDivergenceEngine.js";
import { applyOntologyAntigravity } from "./ontologyAntigravityEngine.js";
import { modelOntologyDivergence } from "./ontologyDivergenceEngine.js";
import { detectOntologyFixation } from "./ontologyFixationEngine.js";
import { preserveRecursiveDivergence } from "./recursiveDivergencePreservationEngine.js";
import { preserveRecursiveEntropy } from "./recursiveEntropyPreservationEngine.js";
import { resistExplorationDecay } from "./recursiveExplorationDecayEngine.js";
import { resistNoveltyDecay } from "./recursiveNoveltyDecayEngine.js";
import { modelRecursiveNovelty } from "./recursiveNoveltyEngine.js";
import { preserveRecursiveNovelty } from "./recursiveNoveltyPreservationEngine.js";
import { modelRecursiveOpennessStability } from "./recursiveOpennessStabilityEngine.js";
import { modelRecursivePhaseSpace } from "./recursivePhaseSpaceEngine.js";
import { detectRecursiveStabilization } from "./recursiveStabilizationEngine.js";
import { applySemanticAntigravity } from "./semanticAntigravityEngine.js";
import { detectSemanticAttractor } from "./semanticAttractorEngine.js";
import { modelSemanticDivergence } from "./semanticDivergenceEngine.js";
import { detectSemanticFixation } from "./semanticFixationEngine.js";
import { applyWorldviewAntigravity } from "./worldviewAntigravityEngine.js";
import { modelWorldviewVariance } from "./worldviewVarianceEngine.js";
import { computeRecursiveConvergencePressure } from "../semantic/recursiveConvergencePressureEngine.js";

export function _depth(bundle: any): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var stages: any = py.get(lineage, "stages", []);
  return ((Array.isArray(stages)) ? py.len(stages) : py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0))));
}
export function applyCivilizationalEpistemicOpenness(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var uncertainties: any = [...py.iter(py.or2(py.get(bundle, "uncertainties", py.get(bundle, "uncertain", [])), () => ([])))];
  if (((uncertainties !== null && typeof uncertainties === "object" && !Array.isArray(uncertainties) && !(uncertainties instanceof Set) && !(uncertainties instanceof Map)))) {
    uncertainties = [...py.iter(py.keys(uncertainties))];
  }
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", py.get(bundle, "contradictions", {})), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var interpretive: any = py.or2(py.get(bundle, "interpretive_diversity", {}), () => ({}));
  var interpretations: any = (((interpretive !== null && typeof interpretive === "object" && !Array.isArray(interpretive) && !(interpretive instanceof Set) && !(interpretive instanceof Map))) ? py.get(interpretive, "interpretations", []) : []);
  var explanatory: any = py.or2(py.get(bundle, "explanatory_diversity", {}), () => ({}));
  var alternatives: any = (((explanatory !== null && typeof explanatory === "object" && !Array.isArray(explanatory) && !(explanatory instanceof Set) && !(explanatory instanceof Map))) ? py.get(explanatory, "alternatives", []) : []);
  var entities: any = [...py.iter(py.keys(inferred))];
  var depth: any = _depth(bundle);
  var interp_count: any = py.or2(py.len(interpretations), () => (py.len(inferred)));
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var sem_div: any = modelSemanticDivergence(observed, inferred, ambiguities);
  var novelty: any = modelRecursiveNovelty(depth, py.len(py.bitor(py.toSet(observed), py.toSet(inferred))), py.len(ambiguities));
  var wv: any = modelWorldviewVariance(interp_count, py.len(pairs));
  var interp_div: any = modelInterpretiveDivergence(interpretations);
  var onto_div: any = modelOntologyDivergence(entities, depth);
  var expl_div: any = modelExplanatoryDivergence(alternatives);
  var attractor: any = detectSemanticAttractor(depth, interp_count, py.len(evidence));
  var gravity: any = detectCognitiveGravityWell((score > py.F(0.75)), (interp_count <= 1), depth);
  var stabilization: any = detectRecursiveStabilization(py.eq(reconciled, inferred), depth);
  var sem_fix: any = detectSemanticFixation((py.len(py.toSet(py.keys(inferred))) <= 1), depth);
  var expl_fix: any = detectExplanatoryFixation(py.len(alternatives), depth);
  var onto_fix: any = detectOntologyFixation(py.len(entities), depth);
  var phase_space: any = modelRecursivePhaseSpace(py.len(py.bitor(py.toSet(observed), py.toSet(inferred))), py.len(ambiguities), depth);
  var r_entropy: any = preserveRecursiveEntropy(ambiguities, uncertainties, depth);
  var div_pres: any = preserveRecursiveDivergence(py.at(sem_div, "divergence_score"));
  var nov_pres: any = preserveRecursiveNovelty(novelty, depth);
  var conv_pressure: any = computeRecursiveConvergencePressure(depth, py.at(sem_div, "divergence_score"));
  var expl_decay: any = resistExplorationDecay(py.or2((interp_count > 1), () => ((py.len(ambiguities) > 0))), depth);
  var nov_decay: any = resistNoveltyDecay(py.at(novelty, "novelty"), depth);
  var antigrav_sem: any = applySemanticAntigravity(py.get(gravity, "suppress", false));
  var antigrav_onto: any = applyOntologyAntigravity(py.get(onto_fix, "suppress", false));
  var antigrav_expl: any = applyExplanatoryAntigravity(py.get(expl_fix, "suppress", false));
  var antigrav_wv: any = applyWorldviewAntigravity(py.get(bundle, "worldview_convergence_suppressed", false));
  var openness_stable: any = modelRecursiveOpennessStability(py.at(sem_div, "preserved"), depth);
  var exploratory: any = py.or2((interp_count > 1), () => (py.or2((py.len(ambiguities) > 0), () => ((py.len(alternatives) > 1)))));
  py.setItem(bundle, "civilizational_openness", {"open": true, "anti_convergence": true, "attractors_suppressed": py.len(py.get(attractor, "suppressed", [])), "phase_space_preserved": py.at(phase_space, "preserved")});
  py.setItem(bundle, "semantic_divergence", sem_div);
  py.setItem(bundle, "recursive_novelty", {...(novelty), ...(nov_pres)});
  py.setItem(bundle, "worldview_variance", wv);
  py.setItem(bundle, "interpretive_divergence", interp_div);
  py.setItem(bundle, "ontology_divergence", onto_div);
  py.setItem(bundle, "explanatory_divergence", expl_div);
  py.setItem(bundle, "semantic_attractors_suppressed", py.get(attractor, "suppressed", []));
  py.setItem(bundle, "cognitive_gravity_suppressed", py.get(gravity, "suppress", false));
  py.setItem(bundle, "recursive_stabilization_suppressed", py.get(stabilization, "suppress", false));
  py.setItem(bundle, "semantic_fixation_suppressed", py.get(sem_fix, "suppress", false));
  py.setItem(bundle, "explanatory_fixation_suppressed", py.get(expl_fix, "suppress", false));
  py.setItem(bundle, "ontology_fixation_suppressed", py.get(onto_fix, "suppress", false));
  py.setItem(bundle, "recursive_phase_space", phase_space);
  py.setItem(bundle, "recursive_entropy_preservation", r_entropy);
  py.setItem(bundle, "exploratory_capacity", {"capacity": exploratory, "preserved": exploratory, "collapse_blocked": true});
  py.setItem(bundle, "semantic_exploration", {"active": exploratory, "novelty": py.at(novelty, "novelty")});
  py.setItem(bundle, "ontology_exploration", {"active": py.at(onto_div, "preserved"), "entities": py.len(entities)});
  py.setItem(bundle, "interpretive_exploration", {"active": py.at(interp_div, "exploration_maintained")});
  py.setItem(bundle, "worldview_exploration", {"active": py.at(wv, "preserved")});
  py.setItem(bundle, "novelty_preservation", nov_pres);
  py.setItem(bundle, "antigravity", {"semantic": antigrav_sem, "ontology": antigrav_onto, "explanatory": antigrav_expl, "worldview": antigrav_wv});
  py.setItem(bundle, "openness_stability", openness_stable);
  py.setItem(bundle, "exploration_decay_resisted", py.get(expl_decay, "resist", true));
  py.setItem(bundle, "novelty_decay_resisted", py.get(nov_decay, "resist", true));
  py.setItem(bundle, "recursive_convergence_pressure", conv_pressure);
  py.setItem(bundle, "divergence_preservation", div_pres);
  return bundle;
}
export { applyExplanatoryAntigravity, applyOntologyAntigravity, applySemanticAntigravity, applyWorldviewAntigravity, computeRecursiveConvergencePressure, detectCognitiveGravityWell, detectExplanatoryFixation, detectOntologyFixation, detectRecursiveStabilization, detectSemanticAttractor, detectSemanticFixation, modelExplanatoryDivergence, modelInterpretiveDivergence, modelOntologyDivergence, modelRecursiveNovelty, modelRecursiveOpennessStability, modelRecursivePhaseSpace, modelSemanticDivergence, modelWorldviewVariance, preserveRecursiveDivergence, preserveRecursiveEntropy, preserveRecursiveNovelty, resistExplorationDecay, resistNoveltyDecay };
