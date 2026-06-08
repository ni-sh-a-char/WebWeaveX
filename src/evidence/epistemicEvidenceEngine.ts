/**
 * Converted from Python: core/evidence/epistemic_evidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { scoreEpistemicConfidence } from "./epistemicConfidenceEngine.js";
import { assessEvidenceSufficiency } from "./evidenceSufficiencyEngine.js";
import { preserveIncompleteness } from "./incompletenessEngine.js";
import { markInsufficiency } from "./insufficiencyEngine.js";
import { scoreReliability } from "./semanticReliabilityEngine.js";
import { buildSupport } from "./semanticSupportEngine.js";
import { propagateUncertainty } from "./semanticUncertaintyPropagationEngine.js";
import { applyCognitiveIntegrity } from "./cognitiveIntegrityEngine.js";
import { applyEpistemicRestraint } from "./semanticRestraintEngine.js";
import { applyCognitiveHumility } from "./cognitiveHumilityEngine.js";
import { applyRealityAlignment } from "./realityAlignmentEngine.js";
import { applyTruthPreservation } from "./truthPreservationEngine.js";
import { applyRecursiveRealityIntegrity } from "./recursiveRealityIntegrityEngine.js";
import { applyEpistemicCivilizationStability } from "./epistemicCivilizationStabilityEngine.js";
import { applyCognitiveAntiCapture } from "./cognitiveAntiCaptureEngine.js";
import { applyRecursiveEpistemicSovereignty } from "./recursiveEpistemicSovereigntyEngine.js";
import { applyCivilizationalEpistemicOpenness } from "./civilizationalEpistemicOpennessEngine.js";
import { applyContradictionRestraint } from "../semantic/contradictionRestraintEngine.js";
import { buildWeaknesses } from "./semanticWeaknessEngine.js";

export function attachEpistemicState(bundle: any): any {
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var contradicting: any = py.iter(pairs).map((p: any) => `contradiction:${py.toStr(p)}`);
  var parser_basis: any = py.or2(py.get(bundle, "parser_basis", {}), () => ({}));
  var parser_density: any = py.toInt(py.or2(py.get(parser_basis, "symbol_count", 0), () => (0)));
  var support: any = buildSupport(evidence);
  var weaknesses: any = buildWeaknesses(evidence, ambiguities);
  var sufficiency: any = assessEvidenceSufficiency(evidence);
  var reliability: any = scoreReliability(evidence, ambiguities, py.len(pairs));
  var incompleteness: any = preserveIncompleteness(bundle);
  var insufficiency: any = markInsufficiency(bundle);
  var epistemic_confidence: any = scoreEpistemicConfidence(evidence, undefined, contradicting, ambiguities, parser_density);
  var lineage: any = py.get(bundle, "lineage", {});
  var how: any = {"stages": py.get(lineage, "stages", []), "depth": py.get(lineage, "depth", 0)};
  py.setItem(bundle, "support", support);
  py.setItem(bundle, "weaknesses", weaknesses);
  py.setItem(bundle, "evidence_sufficiency", sufficiency);
  py.setItem(bundle, "reliability", reliability);
  py.setItem(bundle, "epistemic_state", {...(incompleteness), "insufficient": py.at(insufficiency, "insufficient"), "confidence": py.at(epistemic_confidence, "score")});
  py.setItem(bundle, "confidence_basis", epistemic_confidence);
  py.setItem(bundle, "how", how);
  bundle = propagateUncertainty(bundle);
  if (py.truthy(py.at(insufficiency, "insufficient"))) {
    ambiguities = py.sorted(py.toSet(py.add(ambiguities, ["insufficient_evidence"])));
    py.setItem(bundle, "ambiguities", ambiguities);
  }
  bundle = applyCognitiveIntegrity(bundle);
  bundle = applyContradictionRestraint(bundle);
  var chain: any = applyRealityAlignment(applyCognitiveHumility(applyEpistemicRestraint(bundle)));
  return applyCivilizationalEpistemicOpenness(applyRecursiveEpistemicSovereignty(applyCognitiveAntiCapture(applyEpistemicCivilizationStability(applyRecursiveRealityIntegrity(applyTruthPreservation(chain))))));
}
export { applyCivilizationalEpistemicOpenness, applyCognitiveAntiCapture, applyCognitiveHumility, applyCognitiveIntegrity, applyContradictionRestraint, applyEpistemicCivilizationStability, applyEpistemicRestraint, applyRealityAlignment, applyRecursiveEpistemicSovereignty, applyRecursiveRealityIntegrity, applyTruthPreservation, assessEvidenceSufficiency, buildSupport, buildWeaknesses, markInsufficiency, preserveIncompleteness, propagateUncertainty, scoreEpistemicConfidence, scoreReliability };
