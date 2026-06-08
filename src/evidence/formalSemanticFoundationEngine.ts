/**
 * Converted from Python: core/evidence/formal_semantic_foundation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildContradictionLattice } from "./contradictionLatticeEngine.js";
import { reasonDeterministically } from "./deterministicReasoningEngine.js";
import { weightEvidenceCalculus } from "./evidenceWeightingCalculus.js";
import { assessSemanticConsistency } from "./semanticConsistencyEngine.js";
import { modelSemanticEntropy } from "./semanticEntropyEngine.js";
import { buildJustification } from "./semanticJustificationEngine.js";
import { propagateUncertaintyMath } from "./uncertaintyPropagationMath.js";
import { validateInference } from "./inferenceValidationEngine.js";
import { proveSemanticClaim } from "./semanticProofEngine.js";

export function applyFormalSemanticFoundation(bundle: any): any {
  var observed: any = py.or2(py.get(bundle, "observed", {}), () => ({}));
  var inferred: any = py.or2(py.get(bundle, "inferred", {}), () => ({}));
  var reconciled: any = py.or2(py.get(bundle, "reconciled", {}), () => ({}));
  var evidence: any = [...py.iter(py.or2(py.get(bundle, "evidence", []), () => ([])))];
  var ambiguities: any = [...py.iter(py.or2(py.get(bundle, "ambiguities", []), () => ([])))];
  var contradicted: any = py.or2(py.get(bundle, "contradicted", py.get(bundle, "contradictions", {})), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var parser_basis: any = py.or2(py.get(bundle, "parser_basis", {}), () => ({}));
  var parser_backed: any = py.truthy(py.or2(py.get(parser_basis, "symbol_count", 0), () => (py.get(parser_basis, "flags"))));
  var lattice: any = buildContradictionLattice(pairs);
  var uncertainty: any = propagateUncertaintyMath(py.len(evidence), py.len(ambiguities), py.at(lattice, "count"));
  var entropy: any = modelSemanticEntropy(ambiguities, [...py.iter(py.get(uncertainty, "factors", ambiguities))], contradicted);
  var consistency: any = assessSemanticConsistency(observed, inferred, reconciled);
  var weights: any = weightEvidenceCalculus(evidence, parser_backed);
  var reasoning: any = reasonDeterministically(observed, evidence, ambiguities);
  var justification: any = buildJustification(evidence, lineage, uncertainty, entropy);
  py.setItem(bundle, "uncertainty", uncertainty);
  py.setItem(bundle, "entropy", entropy);
  py.setItem(bundle, "contradictions", {...(contradicted), ...(lattice)});
  py.setItem(bundle, "justification", justification);
  py.setItem(bundle, "formal_reasoning", reasoning);
  py.setItem(bundle, "evidence_weights", weights);
  py.setItem(bundle, "semantic_consistency", consistency);
  var validation: any = validateInference(observed, evidence);
  var proof: any = proveSemanticClaim("semantic_integrity", evidence, 1);
  py.setItem(bundle, "inference_validation", validation);
  py.setItem(bundle, "semantic_proof", proof);
  py.setItem(bundle, "deterministic_inputs", py.sorted(py.toSet(py.add(py.add(py.add(py.add(py.add([...py.iter(py.or2(py.get(bundle, "deterministic_inputs", []), () => ([])))], py.get(uncertainty, "deterministic_inputs", [])), py.get(justification, "deterministic_inputs", [])), py.get(reasoning, "deterministic_inputs", [])), py.get(validation, "deterministic_inputs", [])), py.get(proof, "deterministic_inputs", [])))));
  return bundle;
}
export { assessSemanticConsistency, buildContradictionLattice, buildJustification, modelSemanticEntropy, propagateUncertaintyMath, proveSemanticClaim, reasonDeterministically, validateInference, weightEvidenceCalculus };
