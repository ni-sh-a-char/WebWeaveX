/**
 * Converted from Python: core/evidence/recursive_epistemic_sovereignty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelCognitiveSovereignty } from "./cognitiveSovereigntyEngine.js";
import { resistExplanatoryDomestication } from "./explanatoryNondomesticationEngine.js";
import { modelExplanatorySelfDetermination } from "./explanatorySelfDeterminationEngine.js";
import { resistInterpretiveDomestication } from "./interpretiveNondomesticationEngine.js";
import { modelInterpretiveSelfDetermination } from "./interpretiveSelfDeterminationEngine.js";
import { resistOntologyDomestication } from "./ontologyNondomesticationEngine.js";
import { modelOntologySelfDetermination } from "./ontologySelfDeterminationEngine.js";
import { resistAgencyDecay } from "./recursiveAgencyDecayEngine.js";
import { modelRecursiveAgency } from "./recursiveAgencyEngine.js";
import { preserveRecursiveAgency } from "./recursiveAgencyPreservationEngine.js";
import { preserveRecursiveAutonomy } from "./recursiveAutonomyPreservationEngine.js";
import { detectRecursiveDependency } from "./recursiveDependencyEngine.js";
import { detectRecursiveDomestication } from "./recursiveDomesticationEngine.js";
import { detectRecursiveGuardianship } from "./recursiveGuardianshipEngine.js";
import { resistIndependenceDecay } from "./recursiveIndependenceDecayEngine.js";
import { modelRecursiveInterpretiveIndependence } from "./recursiveInterpretiveIndependenceEngine.js";
import { detectRecursiveObedience } from "./recursiveObedienceEngine.js";
import { modelRecursiveSemanticIndependence } from "./recursiveSemanticIndependenceEngine.js";
import { modelSovereigntyStability } from "./recursiveSovereigntyStabilityEngine.js";
import { detectRecursiveSubmission } from "./recursiveSubmissionEngine.js";
import { suppressSemanticDependency } from "./semanticDependencySuppressionEngine.js";
import { resistSemanticDomestication } from "./semanticNondomesticationEngine.js";
import { modelSemanticSelfDetermination } from "./semanticSelfDeterminationEngine.js";
import { computeRecursiveDependencyPressure } from "../semantic/recursiveDependencyPressureEngine.js";

export function _depth(bundle: any): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var stages: any = py.get(lineage, "stages", []);
  return ((Array.isArray(stages)) ? py.len(stages) : py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0))));
}
export function applyRecursiveEpistemicSovereignty(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var interpretive: any = py.or2(py.get(bundle, "interpretive_diversity", {}), () => ({}));
  var interpretations: any = (((interpretive !== null && typeof interpretive === "object" && !Array.isArray(interpretive) && !(interpretive instanceof Set) && !(interpretive instanceof Map))) ? py.get(interpretive, "interpretations", []) : []);
  var explanatory: any = py.or2(py.get(bundle, "explanatory_diversity", {}), () => ({}));
  var alternatives: any = (((explanatory !== null && typeof explanatory === "object" && !Array.isArray(explanatory) && !(explanatory instanceof Set) && !(explanatory instanceof Map))) ? py.get(explanatory, "alternatives", []) : []);
  var entities: any = [...py.iter(py.keys(inferred))];
  var depth: any = _depth(bundle);
  var interp_count: any = py.or2(py.len(interpretations), () => (py.len(inferred)));
  var cb: any = py.or2(py.get(bundle, "confidence_basis", {}), () => ({}));
  var score: any = py.toFloat(py.get(cb, "score", py.F(0.5)));
  var independent: any = py.or2((interp_count > 1), () => ((py.len(evidence) >= 2)));
  var sem_self: any = modelSemanticSelfDetermination(independent, depth);
  var interp_self: any = modelInterpretiveSelfDetermination(interp_count);
  var onto_self: any = modelOntologySelfDetermination(py.len(entities));
  var expl_self: any = modelExplanatorySelfDetermination(py.len(alternatives));
  var agency: any = modelRecursiveAgency(independent, depth);
  var sovereignty: any = modelCognitiveSovereignty(independent);
  var dependency: any = detectRecursiveDependency(depth, interp_count, py.len(evidence));
  var obedience: any = detectRecursiveObedience((score > py.F(0.7)), (py.len(evidence) < 2), depth);
  var submission: any = detectRecursiveSubmission(py.eq(reconciled, inferred), depth, py.len(evidence));
  var domestication: any = detectRecursiveDomestication((interp_count <= 1), depth);
  var guardianship: any = detectRecursiveGuardianship((((py.get(bundle, "cognitive_decentralization") !== null && typeof py.get(bundle, "cognitive_decentralization") === "object" && !Array.isArray(py.get(bundle, "cognitive_decentralization")) && !(py.get(bundle, "cognitive_decentralization") instanceof Set) && !(py.get(bundle, "cognitive_decentralization") instanceof Map))) ? py.get(py.get(bundle, "cognitive_decentralization", {}), "dominance_without_evidence", false) : false), depth);
  var dep_pressure: any = computeRecursiveDependencyPressure(depth, interp_count);
  var sem_indep: any = modelRecursiveSemanticIndependence([...py.iter(py.keys(inferred))], depth);
  var interp_indep: any = modelRecursiveInterpretiveIndependence(interp_count);
  var agency_pres: any = preserveRecursiveAgency(independent);
  var autonomy_pres: any = preserveRecursiveAutonomy(independent);
  var dep_suppress: any = suppressSemanticDependency(py.get(dependency, "suppressed", []));
  var nondom_sem: any = resistSemanticDomestication(py.get(domestication, "suppress", false));
  var nondom_interp: any = resistInterpretiveDomestication(py.get(domestication, "suppress", false));
  var nondom_onto: any = resistOntologyDomestication(py.get(submission, "suppress", false));
  var nondom_expl: any = resistExplanatoryDomestication(py.get(bundle, "narrative_monopoly_suppressed", false));
  var stab: any = modelSovereigntyStability(independent, depth);
  var indep_decay: any = resistIndependenceDecay(independent, depth);
  var agency_decay: any = resistAgencyDecay(independent, depth);
  py.setItem(bundle, "epistemic_sovereignty", {"preserved": true, "anti_dependent": true, "dependency_suppressed": py.len(py.get(dependency, "suppressed", []))});
  py.setItem(bundle, "semantic_self_determination", sem_self);
  py.setItem(bundle, "interpretive_self_determination", interp_self);
  py.setItem(bundle, "ontology_self_determination", onto_self);
  py.setItem(bundle, "explanatory_self_determination", expl_self);
  py.setItem(bundle, "recursive_agency", agency);
  py.setItem(bundle, "cognitive_sovereignty", sovereignty);
  py.setItem(bundle, "recursive_dependency_suppressed", py.get(dependency, "suppressed", []));
  py.setItem(bundle, "recursive_obedience_suppressed", py.get(obedience, "suppress", false));
  py.setItem(bundle, "recursive_submission_suppressed", py.get(submission, "suppress", false));
  py.setItem(bundle, "recursive_domestication_suppressed", py.get(domestication, "suppress", false));
  py.setItem(bundle, "recursive_guardianship_suppressed", py.get(guardianship, "suppress", false));
  py.setItem(bundle, "recursive_semantic_independence", sem_indep);
  py.setItem(bundle, "recursive_interpretive_independence", interp_indep);
  py.setItem(bundle, "recursive_agency_preservation", agency_pres);
  py.setItem(bundle, "recursive_autonomy_preservation", autonomy_pres);
  py.setItem(bundle, "dependency_resistance", dep_suppress);
  py.setItem(bundle, "sovereignty_stability", stab);
  py.setItem(bundle, "independence_decay_resisted", py.get(indep_decay, "resist", true));
  py.setItem(bundle, "agency_decay_resisted", py.get(agency_decay, "resist", true));
  py.setItem(bundle, "recursive_dependency_pressure", dep_pressure);
  py.setItem(bundle, "nondomestication", {"semantic": nondom_sem, "interpretive": nondom_interp, "ontology": nondom_onto, "explanatory": nondom_expl});
  return bundle;
}
export { computeRecursiveDependencyPressure, detectRecursiveDependency, detectRecursiveDomestication, detectRecursiveGuardianship, detectRecursiveObedience, detectRecursiveSubmission, modelCognitiveSovereignty, modelExplanatorySelfDetermination, modelInterpretiveSelfDetermination, modelOntologySelfDetermination, modelRecursiveAgency, modelRecursiveInterpretiveIndependence, modelRecursiveSemanticIndependence, modelSemanticSelfDetermination, modelSovereigntyStability, preserveRecursiveAgency, preserveRecursiveAutonomy, resistAgencyDecay, resistExplanatoryDomestication, resistIndependenceDecay, resistInterpretiveDomestication, resistOntologyDomestication, resistSemanticDomestication, suppressSemanticDependency };
