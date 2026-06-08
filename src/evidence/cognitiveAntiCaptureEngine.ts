/**
 * Converted from Python: core/evidence/cognitive_anti_capture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectAuthorityConcentration } from "./authorityConcentrationEngine.js";
import { resistAutonomyErosion } from "./autonomyErosionEngine.js";
import { modelCognitiveDecentralization } from "./cognitiveDecentralizationEngine.js";
import { modelExplanatoryCompetition } from "./explanatoryCompetitionEngine.js";
import { preserveExplanatoryFreedom } from "./explanatoryFreedomEngine.js";
import { modelInterpretiveAutonomy } from "./interpretiveAutonomyEngine.js";
import { preserveInterpretiveFreedom } from "./interpretiveFreedomEngine.js";
import { modelOntologyCompetition } from "./ontologyCompetitionEngine.js";
import { preserveOntologyFreedom } from "./ontologyFreedomEngine.js";
import { detectOntologyMonopoly } from "./ontologyMonopolyEngine.js";
import { diffuseRecursiveAuthority } from "./recursiveAuthorityDiffusionEngine.js";
import { modelCaptureResistance } from "./recursiveCaptureResistanceEngine.js";
import { detectRecursiveCentralization } from "./recursiveCentralizationEngine.js";
import { distributeRecursiveCognition } from "./recursiveCognitiveDistributionEngine.js";
import { detectRecursiveNarrativeMonopoly } from "./recursiveNarrativeMonopolyEngine.js";
import { modelRecursiveSemanticDecentralization } from "./recursiveSemanticDecentralizationEngine.js";
import { distributeRecursiveSemantics } from "./recursiveSemanticDistributionEngine.js";
import { detectRecursiveTrustMonopoly } from "./recursiveTrustMonopolyEngine.js";
import { modelSemanticAutonomy } from "./semanticAutonomyEngine.js";
import { modelSemanticFreedom } from "./semanticFreedomEngine.js";
import { suppressSemanticGovernance } from "./semanticGovernanceEngine.js";
import { detectSemanticHierarchyPermanence } from "./semanticHierarchyEngine.js";
import { detectSemanticMonopoly } from "./semanticMonopolyEngine.js";

export function _depth(bundle: any): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var stages: any = py.get(lineage, "stages", []);
  return ((Array.isArray(stages)) ? py.len(stages) : py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0))));
}
export function applyCognitiveAntiCapture(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var interpretive: any = py.or2(py.get(bundle, "interpretive_diversity", {}), () => ({}));
  var interpretations: any = (((interpretive !== null && typeof interpretive === "object" && !Array.isArray(interpretive) && !(interpretive instanceof Set) && !(interpretive instanceof Map))) ? py.get(interpretive, "interpretations", []) : []);
  var explanatory: any = py.or2(py.get(bundle, "explanatory_diversity", {}), () => ({}));
  var alternatives: any = (((explanatory !== null && typeof explanatory === "object" && !Array.isArray(explanatory) && !(explanatory instanceof Set) && !(explanatory instanceof Map))) ? py.get(explanatory, "alternatives", []) : []);
  var entities: any = [...py.iter(py.toSet(py.keys(inferred).map((k: any) => py.toStr(k))))];
  var depth: any = _depth(bundle);
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var trust_score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var sem_autonomy: any = modelSemanticAutonomy(interpretations, py.len(evidence));
  var interp_autonomy: any = modelInterpretiveAutonomy(interpretations);
  var onto_comp: any = modelOntologyCompetition(entities, depth);
  var expl_comp: any = modelExplanatoryCompetition(alternatives);
  var sem_freedom: any = modelSemanticFreedom(sem_autonomy, expl_comp);
  var cognitive_decent: any = modelCognitiveDecentralization(py.or2(py.len(interpretations), () => (py.len(inferred))), py.len(evidence));
  var sem_monopoly: any = detectSemanticMonopoly(py.or2(py.len(interpretations), () => (py.len(inferred))), depth, py.len(evidence));
  var onto_monopoly: any = detectOntologyMonopoly(py.len(entities), depth);
  var authority: any = detectAuthorityConcentration(py.get(sem_autonomy, "dominant_cluster", false), depth);
  var trust_monopoly: any = detectRecursiveTrustMonopoly(trust_score, depth, py.len(evidence));
  var narrative_monopoly: any = detectRecursiveNarrativeMonopoly(py.or2(py.len(alternatives), () => (py.len(interpretations))), depth);
  var hierarchy: any = detectSemanticHierarchyPermanence(depth, (((py.get(bundle, "semantic_decentralization") !== null && typeof py.get(bundle, "semantic_decentralization") === "object" && !Array.isArray(py.get(bundle, "semantic_decentralization")) && !(py.get(bundle, "semantic_decentralization") instanceof Set) && !(py.get(bundle, "semantic_decentralization") instanceof Map))) ? py.get(py.get(bundle, "semantic_decentralization", {}), "hierarchy_lock_in", false) : false));
  var r_decent: any = modelRecursiveSemanticDecentralization(entities, py.len(evidence));
  var r_auth_diff: any = diffuseRecursiveAuthority(py.len(interpretations));
  var r_sem_dist: any = distributeRecursiveSemantics([...py.iter(py.keys(inferred))]);
  var r_cog_dist: any = distributeRecursiveCognition(py.len(py.or2(py.get(bundle, "unstable_regions", []), () => ([]))));
  var expl_freedom: any = preserveExplanatoryFreedom(alternatives);
  var onto_freedom: any = preserveOntologyFreedom(onto_comp);
  var interp_freedom: any = preserveInterpretiveFreedom(interp_autonomy);
  var autonomy_erosion: any = resistAutonomyErosion(py.get(sem_autonomy, "autonomous", true), depth);
  var governance: any = suppressSemanticGovernance(false, depth);
  var centralization: any = detectRecursiveCentralization(py.get(r_decent, "decentralized", true), depth);
  var suppressed: any = py.get(sem_monopoly, "suppressed", []);
  var capture_resistance: any = modelCaptureResistance(suppressed);
  py.setItem(bundle, "cognitive_anti_capture", {"active": true, "capture_suppressed": py.len(suppressed), "monopolies_blocked": py.or2(py.get(sem_monopoly, "monopoly", false), () => (py.get(onto_monopoly, "monopoly", false)))});
  py.setItem(bundle, "semantic_autonomy", sem_autonomy);
  py.setItem(bundle, "interpretive_autonomy", interp_autonomy);
  py.setItem(bundle, "ontology_competition", onto_comp);
  py.setItem(bundle, "explanatory_competition", expl_comp);
  py.setItem(bundle, "semantic_freedom", sem_freedom);
  py.setItem(bundle, "cognitive_decentralization", cognitive_decent);
  py.setItem(bundle, "recursive_semantic_decentralization", r_decent);
  py.setItem(bundle, "recursive_authority_diffusion", r_auth_diff);
  py.setItem(bundle, "recursive_semantic_distribution", r_sem_dist);
  py.setItem(bundle, "recursive_cognitive_distribution", r_cog_dist);
  py.setItem(bundle, "explanatory_freedom", expl_freedom);
  py.setItem(bundle, "ontology_freedom", onto_freedom);
  py.setItem(bundle, "interpretive_freedom", interp_freedom);
  py.setItem(bundle, "capture_resistance", capture_resistance);
  py.setItem(bundle, "semantic_monopoly_suppressed", suppressed);
  py.setItem(bundle, "ontology_monopoly_suppressed", py.get(onto_monopoly, "suppress", false));
  py.setItem(bundle, "trust_monopoly_suppressed", py.get(trust_monopoly, "suppress", false));
  py.setItem(bundle, "narrative_monopoly_suppressed", py.get(narrative_monopoly, "suppress", false));
  py.setItem(bundle, "authority_concentration_suppressed", py.get(authority, "suppress", false));
  py.setItem(bundle, "hierarchy_permanence_suppressed", py.get(hierarchy, "suppress", false));
  py.setItem(bundle, "semantic_governance_suppressed", py.get(governance, "suppress", false));
  py.setItem(bundle, "recursive_centralization_suppressed", py.get(centralization, "suppress", false));
  py.setItem(bundle, "autonomy_erosion_resisted", py.get(autonomy_erosion, "resist", true));
  py.setItem(bundle, "anti_capture_stability", {"stable": py.get(capture_resistance, "resistant", true), "freedom_preserved": py.get(sem_freedom, "free", true)});
  return bundle;
}
export { detectAuthorityConcentration, detectOntologyMonopoly, detectRecursiveCentralization, detectRecursiveNarrativeMonopoly, detectRecursiveTrustMonopoly, detectSemanticHierarchyPermanence, detectSemanticMonopoly, diffuseRecursiveAuthority, distributeRecursiveCognition, distributeRecursiveSemantics, modelCaptureResistance, modelCognitiveDecentralization, modelExplanatoryCompetition, modelInterpretiveAutonomy, modelOntologyCompetition, modelRecursiveSemanticDecentralization, modelSemanticAutonomy, modelSemanticFreedom, preserveExplanatoryFreedom, preserveInterpretiveFreedom, preserveOntologyFreedom, resistAutonomyErosion, suppressSemanticGovernance };
