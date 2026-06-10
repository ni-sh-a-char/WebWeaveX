// Execute JS semantic-IR engine functions; emit output + hash.
//   cp run_js.mjs <js-ref>/ && (cd <js-ref> && npx tsx run_js.mjs <abs fixtures.json>)
//
// Hashing: the canonical digest is Python's compute_kaalka_hash =
// sha256(stable_serialize(value)). The JS branch's computeKaalkaHash diverges
// from that definition for float-typed outputs of py2ts-generated engines
// (PyFloat boxes are recursed as plain objects, and fast-json-stable-stringify
// renders integral floats as "0" where Python emits "0.0"). pyStableHash below
// applies the canonical Python payload definition to the JS engine's typed
// output using the engine's own Python-faithful serializer (pyCompat.jsonDumps,
// PyFloat -> "0.0"), so hash equality proves float-typed value equality.
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import * as py from "./src/runtime/pyCompat.ts";
// A.1 — document parser leaves
import { extractRhetoricalStructure } from "./src/documents/rhetoricalStructureEngine.ts";
import { assignSemanticRoles } from "./src/documents/semanticRoleEngine.ts";
import { extractHeadings } from "./src/documents/headingEngine.ts";
import { reconstructArgumentDependencies } from "./src/documents/argumentDependencyEngine.ts";
import { resolveCoreferences } from "./src/documents/coreferenceResolutionEngine.ts";
// A.2 — semantic pressure leaves
import { computeAmbiguityPressure } from "./src/semantic/ambiguityPressureEngine.ts";
import { computeContradictionPressure } from "./src/semantic/contradictionPressureEngine.ts";
import { computeEvidenceBoundaryPressure } from "./src/semantic/evidenceBoundaryPressureEngine.ts";
import { computeEvidenceDecayPressure } from "./src/semantic/evidenceDecayPressureEngine.ts";
import { computeRecursiveBoundaryPressure } from "./src/semantic/recursiveBoundaryPressureEngine.ts";
import { computeRecursiveConvergencePressure } from "./src/semantic/recursiveConvergencePressureEngine.ts";
import { computeRecursiveDependencyPressure } from "./src/semantic/recursiveDependencyPressureEngine.ts";
import { computeSemanticBoundaryPressure } from "./src/semantic/semanticBoundaryPressureEngine.ts";
import { computeTruthBoundaryPressure } from "./src/semantic/truthBoundaryPressureEngine.ts";
import { computeUncertaintyPressure } from "./src/semantic/uncertaintyPressureEngine.ts";
// A.2 — ir/_base leaves
import { emptyConfidence, emptyLineage, mergeEvidence } from "./src/ir/_base.ts";
// A.2 — graph leaves
import { modelGraphEntropy } from "./src/graph/graphEntropyEngine.ts";
import { detectCycles } from "./src/graph/semanticCycleAnalysisEngine.ts";
import { proveTopology } from "./src/graph/topologyProofEngine.ts";
// A.2 — repository leaves
import { reasonApiSurface } from "./src/repository/apiSurfaceReasoningEngine.ts";
import { reconstructExecutionFlow } from "./src/repository/executionFlowEngine.ts";
import { detectInfraSignals } from "./src/repository/infraSemanticEngine.ts";
import { resolveRuntimeDependencies } from "./src/repository/runtimeDependencyEngine.ts";
import { inferServiceInteractions } from "./src/repository/serviceInteractionEngine.ts";
// A.2 — ast leaves
import { buildControlFlowGraph } from "./src/ast/controlFlowEngine.ts";
import { reconstructExecutionPaths } from "./src/ast/executionPathEngine.ts";
import { resolveSymbols } from "./src/ast/symbolResolutionEngine.ts";
// A.3 batch 1 — evidence trivial leaves
import { detectAuthorityConcentration } from "./src/evidence/authorityConcentrationEngine.ts";
import { diffuseAuthority } from "./src/evidence/authorityDiffusionEngine.ts";
import { resistAutonomyErosion } from "./src/evidence/autonomyErosionEngine.ts";
import { modelCausalPlurality } from "./src/evidence/causalPluralityEngine.ts";
import { modelCognitiveDecentralization } from "./src/evidence/cognitiveDecentralizationEngine.ts";
import { detectCognitiveGravityWell } from "./src/evidence/cognitiveGravityEngine.ts";
import { modelCognitiveSovereignty } from "./src/evidence/cognitiveSovereigntyEngine.ts";
import { detectConfidenceEcho } from "./src/evidence/confidenceEchoEngine.ts";
import { refuseUnsupportedContinuity } from "./src/evidence/continuityRefusalEngine.ts";
import { modelEpistemicOpenness } from "./src/evidence/epistemicOpennessEngine.ts";
import { modelEvidenceDecay } from "./src/evidence/evidenceDecayEngine.ts";
import { applyExplanatoryAntigravity } from "./src/evidence/explanatoryAntigravityEngine.ts";
import { modelExplanatoryCompetition } from "./src/evidence/explanatoryCompetitionEngine.ts";
import { modelExplanatoryDivergence } from "./src/evidence/explanatoryDivergenceEngine.ts";
import { modelExplanatoryDiversity } from "./src/evidence/explanatoryDiversityEngine.ts";
import { detectExplanatoryFixation } from "./src/evidence/explanatoryFixationEngine.ts";
import { preserveExplanatoryFreedom } from "./src/evidence/explanatoryFreedomEngine.ts";
import { resistExplanatoryDomestication } from "./src/evidence/explanatoryNondomesticationEngine.ts";
import { modelExplanatorySelfDetermination } from "./src/evidence/explanatorySelfDeterminationEngine.ts";
import { refuseInference } from "./src/evidence/inferenceRefusalEngine.ts";
import { modelInterpretiveAutonomy } from "./src/evidence/interpretiveAutonomyEngine.ts";
import { detectInterpretiveClosure } from "./src/evidence/interpretiveClosureEngine.ts";
import { resistInterpretiveDecay } from "./src/evidence/interpretiveDecayEngine.ts";
import { distributeInterpretations } from "./src/evidence/interpretiveDistributionEngine.ts";
import { modelInterpretiveDivergence } from "./src/evidence/interpretiveDivergenceEngine.ts";
import { preserveInterpretiveFreedom } from "./src/evidence/interpretiveFreedomEngine.ts";
import { resistInterpretiveDomestication } from "./src/evidence/interpretiveNondomesticationEngine.ts";
import { modelInterpretiveSelfDetermination } from "./src/evidence/interpretiveSelfDeterminationEngine.ts";
import { applyOntologyAntigravity } from "./src/evidence/ontologyAntigravityEngine.ts";
import { modelOntologyBoundaries } from "./src/evidence/ontologyBoundaryEngine.ts";
import { modelOntologyCompetition } from "./src/evidence/ontologyCompetitionEngine.ts";
import { modelOntologyDivergence } from "./src/evidence/ontologyDivergenceEngine.ts";
import { detectOntologyFixation } from "./src/evidence/ontologyFixationEngine.ts";
import { preserveOntologyFreedom } from "./src/evidence/ontologyFreedomEngine.ts";
import { detectOntologyHardening } from "./src/evidence/ontologyHardeningEngine.ts";
import { modelOntologyInstability } from "./src/evidence/ontologyInstabilityEngine.ts";
import { ontologyLimits } from "./src/evidence/ontologyLimitEngine.ts";
import { detectOntologyMonopoly } from "./src/evidence/ontologyMonopolyEngine.ts";
import { resistOntologyDomestication } from "./src/evidence/ontologyNondomesticationEngine.ts";
import { modelOntologySelfDetermination } from "./src/evidence/ontologySelfDeterminationEngine.ts";
import { resistPluralityDecay } from "./src/evidence/pluralityDecayEngine.ts";
import { resistAgencyDecay } from "./src/evidence/recursiveAgencyDecayEngine.ts";
import { modelRecursiveAgency } from "./src/evidence/recursiveAgencyEngine.ts";
import { preserveRecursiveAgency } from "./src/evidence/recursiveAgencyPreservationEngine.ts";
import { diffuseRecursiveAuthority } from "./src/evidence/recursiveAuthorityDiffusionEngine.ts";
import { preserveRecursiveAutonomy } from "./src/evidence/recursiveAutonomyPreservationEngine.ts";
import { modelCaptureResistance } from "./src/evidence/recursiveCaptureResistanceEngine.ts";
import { detectRecursiveCentralization } from "./src/evidence/recursiveCentralizationEngine.ts";
import { distributeRecursiveCognition } from "./src/evidence/recursiveCognitiveDistributionEngine.ts";
import { detectRecursiveCoherenceInflation } from "./src/evidence/recursiveCoherenceInflationEngine.ts";
import { detectRecursiveConfidenceEcho } from "./src/evidence/recursiveConfidenceEchoEngine.ts";
import { detectRecursiveConsensus } from "./src/evidence/recursiveConsensusEngine.ts";
import { modelStabilityBoundary } from "./src/evidence/stabilityBoundaryEngine.ts";
import { modelTopologyBoundaries } from "./src/evidence/topologyBoundaryEngine.ts";
import { topologyLimits } from "./src/evidence/topologyLimitEngine.ts";
import { modelTruthBoundaries } from "./src/evidence/truthBoundaryEngine.ts";
import { applyWorldviewAntigravity } from "./src/evidence/worldviewAntigravityEngine.ts";
import { suppressWorldviewConvergence } from "./src/evidence/worldviewConvergenceEngine.ts";
import { modelWorldviewDiversity } from "./src/evidence/worldviewDiversityEngine.ts";
import { modelWorldviewVariance } from "./src/evidence/worldviewVarianceEngine.ts";

// A.3 leaves take plain positional args — dispatch generically.
const A3_REGISTRY = {
  detect_authority_concentration: detectAuthorityConcentration,
  diffuse_authority: diffuseAuthority,
  resist_autonomy_erosion: resistAutonomyErosion,
  model_causal_plurality: modelCausalPlurality,
  model_cognitive_decentralization: modelCognitiveDecentralization,
  detect_cognitive_gravity_well: detectCognitiveGravityWell,
  model_cognitive_sovereignty: modelCognitiveSovereignty,
  detect_confidence_echo: detectConfidenceEcho,
  refuse_unsupported_continuity: refuseUnsupportedContinuity,
  model_epistemic_openness: modelEpistemicOpenness,
  model_evidence_decay: modelEvidenceDecay,
  apply_explanatory_antigravity: applyExplanatoryAntigravity,
  model_explanatory_competition: modelExplanatoryCompetition,
  model_explanatory_divergence: modelExplanatoryDivergence,
  model_explanatory_diversity: modelExplanatoryDiversity,
  detect_explanatory_fixation: detectExplanatoryFixation,
  preserve_explanatory_freedom: preserveExplanatoryFreedom,
  resist_explanatory_domestication: resistExplanatoryDomestication,
  model_explanatory_self_determination: modelExplanatorySelfDetermination,
  refuse_inference: refuseInference,
  model_interpretive_autonomy: modelInterpretiveAutonomy,
  detect_interpretive_closure: detectInterpretiveClosure,
  resist_interpretive_decay: resistInterpretiveDecay,
  distribute_interpretations: distributeInterpretations,
  model_interpretive_divergence: modelInterpretiveDivergence,
  preserve_interpretive_freedom: preserveInterpretiveFreedom,
  resist_interpretive_domestication: resistInterpretiveDomestication,
  model_interpretive_self_determination: modelInterpretiveSelfDetermination,
  apply_ontology_antigravity: applyOntologyAntigravity,
  model_ontology_boundaries: modelOntologyBoundaries,
  model_ontology_competition: modelOntologyCompetition,
  model_ontology_divergence: modelOntologyDivergence,
  detect_ontology_fixation: detectOntologyFixation,
  preserve_ontology_freedom: preserveOntologyFreedom,
  detect_ontology_hardening: detectOntologyHardening,
  model_ontology_instability: modelOntologyInstability,
  ontology_limits: ontologyLimits,
  detect_ontology_monopoly: detectOntologyMonopoly,
  resist_ontology_domestication: resistOntologyDomestication,
  model_ontology_self_determination: modelOntologySelfDetermination,
  resist_plurality_decay: resistPluralityDecay,
  resist_agency_decay: resistAgencyDecay,
  model_recursive_agency: modelRecursiveAgency,
  preserve_recursive_agency: preserveRecursiveAgency,
  diffuse_recursive_authority: diffuseRecursiveAuthority,
  preserve_recursive_autonomy: preserveRecursiveAutonomy,
  model_capture_resistance: modelCaptureResistance,
  detect_recursive_centralization: detectRecursiveCentralization,
  distribute_recursive_cognition: distributeRecursiveCognition,
  detect_recursive_coherence_inflation: detectRecursiveCoherenceInflation,
  detect_recursive_confidence_echo: detectRecursiveConfidenceEcho,
  detect_recursive_consensus: detectRecursiveConsensus,
  model_stability_boundary: modelStabilityBoundary,
  model_topology_boundaries: modelTopologyBoundaries,
  topology_limits: topologyLimits,
  model_truth_boundaries: modelTruthBoundaries,
  apply_worldview_antigravity: applyWorldviewAntigravity,
  suppress_worldview_convergence: suppressWorldviewConvergence,
  model_worldview_diversity: modelWorldviewDiversity,
  model_worldview_variance: modelWorldviewVariance,
};

const VOLATILE = new Set([
  "timestamp", "created_at", "updated_at", "nonce", "request_id",
  "csrf", "generated_at", "runtime_id", "random", "uuid",
]);

const isPlainObj = (v) =>
  v !== null && typeof v === "object" && !Array.isArray(v) && !py.isF(v);

// Python core.determinism.normalization.stable_sort_keys (PyFloat-preserving).
function stableSortKeysPy(obj) {
  const out = {};
  for (const k of Object.keys(obj).sort()) {
    if (VOLATILE.has(k)) continue;
    const v = obj[k];
    if (isPlainObj(v)) out[k] = stableSortKeysPy(v);
    else if (Array.isArray(v)) out[k] = v.map((it) => (isPlainObj(it) ? stableSortKeysPy(it) : it));
    else out[k] = v;
  }
  return out;
}

// Python core.determinism.normalization.stable_serialize + sha256.
function pyStableHash(value) {
  const opts = { sortKeys: true, ensureAscii: false, separators: [",", ":"] };
  let payload;
  if (typeof value === "string") {
    payload = value.normalize("NFKC").replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\s+$/, "");
  } else if (isPlainObj(value)) {
    payload = py.jsonDumps(stableSortKeysPy(value), opts);
  } else if (Array.isArray(value)) {
    const keyed = {};
    value.forEach((it, i) => { keyed[String(i)] = isPlainObj(it) ? stableSortKeysPy(it) : it; });
    payload = py.jsonDumps(keyed, opts);
  } else {
    payload = py.jsonDumps(value, { ensureAscii: false, separators: [",", ":"] });
  }
  return createHash("sha256").update(payload, "utf8").digest("hex");
}

function call(fn, args) {
  if (fn in A3_REGISTRY) return A3_REGISTRY[fn](...args);
  switch (fn) {
    case "extract_rhetorical_structure":
      return extractRhetoricalStructure(args[0]);
    case "assign_semantic_roles":
      return assignSemanticRoles(args[0]);
    case "extract_headings":
      return extractHeadings(args[0]);
    case "reconstruct_argument_dependencies":
      return reconstructArgumentDependencies(args[0]);
    case "resolve_coreferences":
      return resolveCoreferences(args[0]);
    case "compute_ambiguity_pressure":
      return computeAmbiguityPressure(args[0]);
    case "compute_contradiction_pressure":
      return computeContradictionPressure(args[0]);
    case "compute_evidence_boundary_pressure":
      return args.length > 1 ? computeEvidenceBoundaryPressure(args[0], args[1]) : computeEvidenceBoundaryPressure(args[0]);
    case "compute_evidence_decay_pressure":
      return args.length > 1 ? computeEvidenceDecayPressure(args[0], args[1]) : computeEvidenceDecayPressure(args[0]);
    case "compute_recursive_boundary_pressure":
      return computeRecursiveBoundaryPressure(args[0], args[1]);
    case "compute_recursive_convergence_pressure":
      return computeRecursiveConvergencePressure(args[0], args[1]);
    case "compute_recursive_dependency_pressure":
      return computeRecursiveDependencyPressure(args[0], args[1]);
    case "compute_semantic_boundary_pressure":
      return computeSemanticBoundaryPressure(args[0], args[1]);
    case "compute_truth_boundary_pressure":
      return computeTruthBoundaryPressure(args[0], args[1]);
    case "compute_uncertainty_pressure":
      return computeUncertaintyPressure(args[0], args[1]);
    case "empty_confidence":
      return emptyConfidence();
    case "empty_lineage":
      return args.length ? emptyLineage(args[0]) : emptyLineage();
    case "merge_evidence":
      return mergeEvidence(...args);
    case "model_graph_entropy":
      return modelGraphEntropy(args[0]);
    case "detect_cycles":
      return detectCycles(args[0]);
    case "prove_topology":
      return proveTopology(args[0]);
    case "reason_api_surface":
      return reasonApiSurface(args[0]);
    case "reconstruct_execution_flow":
      return reconstructExecutionFlow(args[0]);
    case "detect_infra_signals":
      return detectInfraSignals(args[0]);
    case "resolve_runtime_dependencies":
      return args.length > 1 ? resolveRuntimeDependencies(args[0], args[1]) : resolveRuntimeDependencies(args[0]);
    case "infer_service_interactions":
      return inferServiceInteractions(args[0], args[1]);
    case "build_control_flow_graph":
      return buildControlFlowGraph(args[0]);
    case "reconstruct_execution_paths":
      return reconstructExecutionPaths(args[0]);
    case "resolve_symbols":
      return resolveSymbols(args[0]);
    default:
      throw new Error("unknown fn " + fn);
  }
}

const fixtures = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const out = [];
for (const fx of fixtures) {
  try {
    const result = call(fx.fn, fx.args);
    out.push({ id: fx.id, fn: fx.fn, output: result, hash: pyStableHash(result) });
  } catch (e) {
    out.push({ id: fx.id, fn: fx.fn, error: String(e && e.message ? e.message : e) });
  }
}
process.stdout.write(JSON.stringify(out));
