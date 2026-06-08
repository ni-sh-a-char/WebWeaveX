/**
 * Converted from Python: core/evidence/epistemic_civilization_stability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { diffuseAuthority } from "./authorityDiffusionEngine.js";
import { modelEpistemicOpenness } from "./epistemicOpennessEngine.js";
import { modelExplanatoryDiversity } from "./explanatoryDiversityEngine.js";
import { resistInterpretiveDecay } from "./interpretiveDecayEngine.js";
import { detectInterpretiveClosure } from "./interpretiveClosureEngine.js";
import { modelInterpretiveDiversity } from "./interpretiveDiversityEngine.js";
import { distributeInterpretations } from "./interpretiveDistributionEngine.js";
import { modelOntologyAlternatives } from "./ontologyAlternativeEngine.js";
import { detectOntologyHardening } from "./ontologyHardeningEngine.js";
import { modelOntologyInstability } from "./ontologyInstabilityEngine.js";
import { resistPluralityDecay } from "./pluralityDecayEngine.js";
import { detectRecursiveConsensus } from "./recursiveConsensusEngine.js";
import { modelSemanticAlternatives } from "./semanticAlternativeEngine.js";
import { modelSemanticDecentralization } from "./semanticDecentralizationEngine.js";
import { modelSemanticDiversity } from "./semanticDiversityEngine.js";
import { detectSemanticHomogenization } from "./semanticHomogenizationEngine.js";
import { detectSemanticMonoculture } from "./semanticMonocultureEngine.js";
import { detectSemanticOrthodoxy } from "./semanticOrthodoxyEngine.js";
import { modelSemanticPlurality } from "./semanticPluralityEngine.js";
import { detectSemanticUniformity } from "./semanticUniformityEngine.js";
import { suppressWorldviewConvergence } from "./worldviewConvergenceEngine.js";
import { modelWorldviewDiversity } from "./worldviewDiversityEngine.js";
import { modelCausalPlurality } from "./causalPluralityEngine.js";

export function _depth(bundle: any): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var stages: any = py.get(lineage, "stages", []);
  return ((Array.isArray(stages)) ? py.len(stages) : py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0))));
}
export function applyEpistemicCivilizationStability(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", py.get(bundle, "contradictions", {})), () => ({}));
  var unstable: any = [...py.iter(py.or2(py.get(bundle, "unstable_regions", []), () => ([])))];
  var depth: any = _depth(bundle);
  var plurality: any = modelSemanticPlurality(observed, inferred, ambiguities, contradicted);
  var interpretive: any = modelInterpretiveDiversity(evidence, inferred);
  var interpretations: any = py.get(interpretive, "interpretations", []);
  var decentralization: any = modelSemanticDecentralization(interpretations, py.len(evidence));
  var ontology_inst: any = modelOntologyInstability(unstable, depth);
  var worldview: any = modelWorldviewDiversity(interpretations, contradicted);
  var explanatory: any = modelExplanatoryDiversity(inferred, evidence);
  var openness: any = modelEpistemicOpenness(plurality, decentralization);
  var monoculture: any = detectSemanticMonoculture(interpretations, evidence, depth);
  var hardening: any = detectOntologyHardening(depth, py.len(evidence));
  var consensus: any = detectRecursiveConsensus(py.eq(reconciled, inferred), depth, py.len(evidence));
  var orthodoxy: any = detectSemanticOrthodoxy(interpretations, depth);
  var closure: any = detectInterpretiveClosure(py.get(plurality, "alternative_count", 0), depth);
  var uniformity: any = detectSemanticUniformity([...py.iter(py.keys(inferred))], depth);
  var homogenization: any = detectSemanticHomogenization(py.get(uniformity, "uniformity_detected", false), depth);
  var plurality_decay: any = resistPluralityDecay(py.get(plurality, "alternative_count", 0), depth);
  var interpretive_decay: any = resistInterpretiveDecay(py.len(interpretations), depth);
  var worldview_conv: any = suppressWorldviewConvergence(py.get(consensus, "consensus_inflated", false), depth);
  var diversity: any = modelSemanticDiversity(observed, inferred, ambiguities);
  var alternatives: any = modelSemanticAlternatives(observed, inferred);
  var causal: any = modelCausalPlurality(inferred);
  var authority: any = diffuseAuthority(interpretations);
  var distribution: any = distributeInterpretations(interpretations);
  var suppressed: any = py.get(monoculture, "suppressed", []);
  py.setItem(bundle, "epistemic_openness", openness);
  py.setItem(bundle, "semantic_plurality", plurality);
  py.setItem(bundle, "interpretive_diversity", interpretive);
  py.setItem(bundle, "semantic_decentralization", decentralization);
  py.setItem(bundle, "ontology_instability", ontology_inst);
  py.setItem(bundle, "worldview_diversity", worldview);
  py.setItem(bundle, "explanatory_diversity", explanatory);
  py.setItem(bundle, "semantic_monoculture_suppressed", suppressed);
  py.setItem(bundle, "ontology_hardening_suppressed", py.get(hardening, "suppress", false));
  py.setItem(bundle, "recursive_consensus_suppressed", py.get(consensus, "suppress", false));
  py.setItem(bundle, "semantic_orthodoxy_suppressed", py.get(orthodoxy, "suppress", false));
  py.setItem(bundle, "interpretive_closure_suppressed", py.get(closure, "suppress", false));
  py.setItem(bundle, "semantic_diversity", diversity);
  py.setItem(bundle, "semantic_alternatives", alternatives);
  py.setItem(bundle, "causal_plurality", causal);
  py.setItem(bundle, "authority_diffusion", authority);
  py.setItem(bundle, "interpretive_distribution", distribution);
  py.setItem(bundle, "plurality_decay_resistance", plurality_decay);
  py.setItem(bundle, "interpretive_decay_resistance", interpretive_decay);
  py.setItem(bundle, "worldview_convergence_suppressed", py.get(worldview_conv, "suppress", false));
  py.setItem(bundle, "semantic_homogenization_suppressed", py.get(homogenization, "suppress", false));
  py.setItem(bundle, "civilization_stability", {"stable": py.get(openness, "open", true), "plurality_preserved": py.get(plurality, "preserved", true), "anti_monoculture": py.or2(py.truthy(suppressed), () => (!py.truthy(py.get(monoculture, "detected"))))});
  return bundle;
}
export { detectInterpretiveClosure, detectOntologyHardening, detectRecursiveConsensus, detectSemanticHomogenization, detectSemanticMonoculture, detectSemanticOrthodoxy, detectSemanticUniformity, diffuseAuthority, distributeInterpretations, modelCausalPlurality, modelEpistemicOpenness, modelExplanatoryDiversity, modelInterpretiveDiversity, modelOntologyAlternatives, modelOntologyInstability, modelSemanticAlternatives, modelSemanticDecentralization, modelSemanticDiversity, modelSemanticPlurality, modelWorldviewDiversity, resistInterpretiveDecay, resistPluralityDecay, suppressWorldviewConvergence };
