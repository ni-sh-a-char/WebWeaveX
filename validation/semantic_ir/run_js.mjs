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
// A.3 batch 2 — evidence leaves (recursive/semantic/unsupported)
import { exposeAmbiguityVisibility } from "./src/evidence/ambiguityVisibilityEngine.ts";
import { modelEvidenceBoundaries } from "./src/evidence/evidenceBoundaryEngine.ts";
import { assessEvidenceSufficiency } from "./src/evidence/evidenceSufficiencyEngine.ts";
import { detectNarrativeHallucination } from "./src/evidence/narrativeHallucinationEngine.ts";
import { detectRecursiveDrift } from "./src/evidence/recursiveDriftEngine.ts";
import { preserveRecursiveEntropy } from "./src/evidence/recursiveEntropyPreservationEngine.ts";
import { trackRecursiveEvidenceAncestry } from "./src/evidence/recursiveEvidenceAncestryEngine.ts";
import { resistExplorationDecay } from "./src/evidence/recursiveExplorationDecayEngine.ts";
import { detectRecursiveGuardianship } from "./src/evidence/recursiveGuardianshipEngine.ts";
import { resistIndependenceDecay } from "./src/evidence/recursiveIndependenceDecayEngine.ts";
import { modelRecursiveInterpretiveIndependence } from "./src/evidence/recursiveInterpretiveIndependenceEngine.ts";
import { detectRecursiveNarrativeMonopoly } from "./src/evidence/recursiveNarrativeMonopolyEngine.ts";
import { resistNoveltyDecay } from "./src/evidence/recursiveNoveltyDecayEngine.ts";
import { modelRecursiveNovelty } from "./src/evidence/recursiveNoveltyEngine.ts";
import { preserveRecursiveNovelty } from "./src/evidence/recursiveNoveltyPreservationEngine.ts";
import { detectRecursiveObedience } from "./src/evidence/recursiveObedienceEngine.ts";
import { recursiveOntologyLimits } from "./src/evidence/recursiveOntologyLimitEngine.ts";
import { modelRecursiveOpennessStability } from "./src/evidence/recursiveOpennessStabilityEngine.ts";
import { modelRecursivePhaseSpace } from "./src/evidence/recursivePhaseSpaceEngine.ts";
import { preserveRecursiveProvenance } from "./src/evidence/recursiveProvenanceEngine.ts";
import { recursiveRealityLimits } from "./src/evidence/recursiveRealityLimitEngine.ts";
import { detectRecursiveSelfConfirmation } from "./src/evidence/recursiveSelfConfirmationEngine.ts";
import { modelRecursiveSemanticDecentralization } from "./src/evidence/recursiveSemanticDecentralizationEngine.ts";
import { distributeRecursiveSemantics } from "./src/evidence/recursiveSemanticDistributionEngine.ts";
import { modelRecursiveSemanticIndependence } from "./src/evidence/recursiveSemanticIndependenceEngine.ts";
import { modelSovereigntyStability } from "./src/evidence/recursiveSovereigntyStabilityEngine.ts";
import { detectRecursiveStabilization } from "./src/evidence/recursiveStabilizationEngine.ts";
import { terminateRecursiveStabilization } from "./src/evidence/recursiveStabilizationTerminationEngine.ts";
import { detectRecursiveSubmission } from "./src/evidence/recursiveSubmissionEngine.ts";
import { recursiveTopologyLimits } from "./src/evidence/recursiveTopologyLimitEngine.ts";
import { detectRecursiveTrustMonopoly } from "./src/evidence/recursiveTrustMonopolyEngine.ts";
import { modelRecursiveTruthBoundaries } from "./src/evidence/recursiveTruthBoundaryEngine.ts";
import { refuseRecursiveStabilization } from "./src/evidence/recursiveTruthRefusalEngine.ts";
import { preserveRecursiveUncertainty } from "./src/evidence/recursiveUncertaintyPreservationEngine.ts";
import { modelSemanticAlternatives } from "./src/evidence/semanticAlternativeEngine.ts";
import { applySemanticAntigravity } from "./src/evidence/semanticAntigravityEngine.ts";
import { modelSemanticAutonomy } from "./src/evidence/semanticAutonomyEngine.ts";
import { modelSemanticBoundaries } from "./src/evidence/semanticBoundaryEngine.ts";
import { suppressSemanticDependency } from "./src/evidence/semanticDependencySuppressionEngine.ts";
import { modelSemanticDivergence } from "./src/evidence/semanticDivergenceEngine.ts";
import { modelSemanticDiversity } from "./src/evidence/semanticDiversityEngine.ts";
import { detectSemanticFixation } from "./src/evidence/semanticFixationEngine.ts";
import { modelSemanticFreedom } from "./src/evidence/semanticFreedomEngine.ts";
import { suppressSemanticGovernance } from "./src/evidence/semanticGovernanceEngine.ts";
import { detectSemanticHierarchyPermanence } from "./src/evidence/semanticHierarchyEngine.ts";
import { detectSemanticHomogenization } from "./src/evidence/semanticHomogenizationEngine.ts";
import { measureSemanticMomentum } from "./src/evidence/semanticMomentumEngine.ts";
import { resistSemanticDomestication } from "./src/evidence/semanticNondomesticationEngine.ts";
import { detectSemanticOrthodoxy } from "./src/evidence/semanticOrthodoxyEngine.ts";
import { modelSemanticSelfDetermination } from "./src/evidence/semanticSelfDeterminationEngine.ts";
import { detectSemanticSelfReinforcement } from "./src/evidence/semanticSelfReinforcementEngine.ts";
import { semanticStabilityLimits } from "./src/evidence/semanticStabilityLimitEngine.ts";
import { terminateSemanticChain } from "./src/evidence/semanticTerminationEngine.ts";
import { semanticTruthLimits } from "./src/evidence/semanticTruthLimitEngine.ts";
import { detectSemanticUniformity } from "./src/evidence/semanticUniformityEngine.ts";
import { detectUnsupportedExpansion } from "./src/evidence/unsupportedExpansionEngine.ts";
import { modelUnsupportedScope } from "./src/evidence/unsupportedScopeEngine.ts";
// A.3 batch 3 — evidence medium leaves
import { applyConfidenceCaps } from "./src/evidence/confidenceCapEngine.ts";
import { buildContradictionLattice } from "./src/evidence/contradictionLatticeEngine.ts";
import { preserveEpistemicBoundaries } from "./src/evidence/epistemicBoundaryEngine.ts";
import { modelEpistemicLimits } from "./src/evidence/epistemicLimitEngine.ts";
import { combineEvidence } from "./src/evidence/evidenceAlgebraEngine.ts";
import { weightEvidenceCalculus } from "./src/evidence/evidenceWeightingCalculus.ts";
import { buildExplainability } from "./src/evidence/explainabilityEngine.ts";
import { modelInferenceIntegrity } from "./src/evidence/inferenceIntegrityEngine.ts";
import { terminateInferenceChain } from "./src/evidence/inferenceTerminationEngine.ts";
import { preserveInstability } from "./src/evidence/instabilityPreservationEngine.ts";
import { markInsufficiency } from "./src/evidence/insufficiencyEngine.ts";
import { modelInterpretiveDiversity } from "./src/evidence/interpretiveDiversityEngine.ts";
import { buildLineage } from "./src/evidence/lineageEngine.ts";
import { modelNoninferableRegions } from "./src/evidence/noninferableScopeEngine.ts";
import { modelNoninference } from "./src/evidence/noninferenceEngine.ts";
import { buildProvenance } from "./src/evidence/provenanceEngine.ts";
import { modelRecursiveEntropy } from "./src/evidence/recursiveEntropyEngine.ts";
import { modelRecursiveInstability } from "./src/evidence/recursiveInstabilityEngine.ts";
import { preserveRecursiveLineage } from "./src/evidence/recursiveLineageEngine.ts";
import { detectSpeculativeCoherence } from "./src/evidence/speculativeCoherenceEngine.ts";
import { buildSupport } from "./src/evidence/semanticSupportEngine.ts";
import { buildWeaknesses } from "./src/evidence/semanticWeaknessEngine.ts";
import { buildTraceability } from "./src/evidence/traceabilityEngine.ts";
import { refuseUnsupportedStabilization } from "./src/evidence/truthRefusalEngine.ts";
// A.3 batch 4 — final evidence public leaves (semantic_* heavies)
import { scoreSemanticConfidence } from "./src/evidence/semanticConfidenceEngine.ts";
import { applySemanticConservatism } from "./src/evidence/semanticConservatismEngine.ts";
import { assessSemanticConsistency } from "./src/evidence/semanticConsistencyEngine.ts";
import { modelSemanticDecay } from "./src/evidence/semanticDecayEngine.ts";
import { modelSemanticDecentralization } from "./src/evidence/semanticDecentralizationEngine.ts";
import { detectSemanticDrift } from "./src/evidence/semanticDriftEngine.ts";
import { modelSemanticEntropy } from "./src/evidence/semanticEntropyEngine.ts";
import { modelFragility } from "./src/evidence/semanticFragilityEngine.ts";
import { assessSemanticHonesty } from "./src/evidence/semanticHonestyEngine.ts";
import { modelIncompleteness } from "./src/evidence/semanticIncompletenessEngine.ts";
import { inferFromEvidence } from "./src/evidence/semanticInferenceCalculus.ts";
import { modelSemanticInstability } from "./src/evidence/semanticInstabilityEngine.ts";
import { buildJustification } from "./src/evidence/semanticJustificationEngine.ts";
import { semanticLimits } from "./src/evidence/semanticLimitEngine.ts";
import { detectSemanticOverreach } from "./src/evidence/semanticOverreachEngine.ts";
import { modelSemanticPlurality } from "./src/evidence/semanticPluralityEngine.ts";
import { proveSemanticClaim } from "./src/evidence/semanticProofEngine.ts";
import { refuseUnsupportedConclusions } from "./src/evidence/semanticRefusalEngine.ts";
import { applySemanticSelfLimitation } from "./src/evidence/semanticSelfLimitationEngine.ts";
import { modelSemanticStability } from "./src/evidence/semanticStabilityEngine.ts";
import { terminateStabilization } from "./src/evidence/stabilizationTerminationEngine.ts";
import { modelUncertainty } from "./src/evidence/uncertaintyEngine.ts";
import { exposeUncertaintyVisibility } from "./src/evidence/uncertaintyVisibilityEngine.ts";
import { blockUnsupportedConfidenceEscalation } from "./src/evidence/unsupportedConfidenceEngine.ts";
import { suppressUnsupportedInference } from "./src/evidence/unsupportedInferenceEngine.ts";
import { preserveRecursiveDivergence } from "./src/evidence/recursiveDivergencePreservationEngine.ts";
import { detectRecursiveDomestication } from "./src/evidence/recursiveDomesticationEngine.ts";
// Phase B — first non-leaf layer
import { parsePythonAst } from "./src/ast/pythonAstEngine.ts";
import { buildArgumentDependencies } from "./src/documents/argumentDependencyEngine.ts";
import { buildArgumentGraph } from "./src/documents/argumentGraphEngine.ts";
import { extractInstructionalFlow } from "./src/documents/instructionalFlowEngine.ts";
import { parseRhetoricalStructure } from "./src/documents/rhetoricalParserEngine.ts";
import { extractSections } from "./src/documents/sectionEngine.ts";
import { applyConfidenceDegradation } from "./src/evidence/confidenceDegradationEngine.ts";
import { reasonDeterministically } from "./src/evidence/deterministicReasoningEngine.ts";
import { scoreEpistemicConfidence } from "./src/evidence/epistemicConfidenceEngine.ts";
import { preserveIncompleteness } from "./src/evidence/incompletenessEngine.ts";
import { modelInferenceLimits } from "./src/evidence/inferenceLimitEngine.ts";
import { validateInference } from "./src/evidence/inferenceValidationEngine.ts";
import { applyRealityConstraints } from "./src/evidence/realityConstraintEngine.ts";
import { detectRecursiveDependency } from "./src/evidence/recursiveDependencyEngine.ts";
import { detectRecursiveSemanticClosure } from "./src/evidence/recursiveSemanticClosureEngine.ts";
import { detectSemanticAttractor } from "./src/evidence/semanticAttractorEngine.ts";
import { _groundParser } from "./src/evidence/semanticIntegrityEngine.ts";
import { detectSemanticMonoculture } from "./src/evidence/semanticMonocultureEngine.ts";
import { detectSemanticMonopoly } from "./src/evidence/semanticMonopolyEngine.ts";
import { scoreReliability } from "./src/evidence/semanticReliabilityEngine.ts";
import { applyEpistemicRestraint } from "./src/evidence/semanticRestraintEngine.ts";
import { propagateUncertainty } from "./src/evidence/semanticUncertaintyPropagationEngine.ts";
import { suppressSpeculativeInference } from "./src/evidence/speculativeInferenceEngine.ts";
import { propagateUncertaintyMath } from "./src/evidence/uncertaintyPropagationMath.ts";
import { suppressUnsupportedContinuity } from "./src/evidence/unsupportedContinuityEngine.ts";
import { detectUnsupportedStabilization } from "./src/evidence/unsupportedStabilizationEngine.ts";
import { reasonTopology } from "./src/graph/topologyReasoningEngine.ts";
import { emptyDocumentIr } from "./src/ir/documentIr.ts";
import { emptyRepositoryIr } from "./src/ir/repositoryIr.ts";
import { reasonApiContract } from "./src/repository/apiContractReasoningEngine.ts";
import { modelInfraRelationships } from "./src/repository/infraRelationshipEngine.ts";
import { applyContradictionRestraint } from "./src/semantic/contradictionRestraintEngine.ts";
// Phase C — second layer
import { compileSemanticAstIr } from "./src/ast/semanticAstIrEngine.ts";
import { buildCoreferenceGraph } from "./src/documents/coreferenceGraphEngine.ts";
import { analyzeInstructionalSemantics } from "./src/documents/instructionalSemanticsEngine.ts";
import { parseSemanticDiscourse } from "./src/documents/semanticDiscourseParser.ts";
import { applyCivilizationalEpistemicOpenness } from "./src/evidence/civilizationalEpistemicOpennessEngine.ts";
import { applyCognitiveAntiCapture } from "./src/evidence/cognitiveAntiCaptureEngine.ts";
import { applyCognitiveIntegrity } from "./src/evidence/cognitiveIntegrityEngine.ts";
import { applyEpistemicCivilizationStability } from "./src/evidence/epistemicCivilizationStabilityEngine.ts";
import { applyFormalSemanticFoundation } from "./src/evidence/formalSemanticFoundationEngine.ts";
import { applyRealityBoundedConfidence } from "./src/evidence/realityBoundedConfidenceEngine.ts";
import { applyRecursiveEpistemicSovereignty } from "./src/evidence/recursiveEpistemicSovereigntyEngine.ts";
import { collectSuppressedSpeculation } from "./src/evidence/speculativeInferenceEngine.ts";
import { collectUnsupportedContinuity } from "./src/evidence/unsupportedContinuityEngine.ts";
import { reasonTopologySemantic } from "./src/reasoning/topologyReasoningEngine.ts";
import { analyzeDeploymentSemantics } from "./src/repository/deploymentSemanticsEngine.ts";
// Phase D — third layer
import { modelConceptTransitions } from "./src/documents/conceptTransitionEngine.ts";
import { applyConfidenceCollapse } from "./src/evidence/confidenceCollapseEngine.ts";
import { applyRealityAlignment } from "./src/evidence/realityAlignmentEngine.ts";
import { detectSemanticSpeculation } from "./src/evidence/semanticSpeculationEngine.ts";
// Phase E — fourth layer
import { buildDocumentDependencyGraph } from "./src/documents/documentDependencyGraphEngine.ts";
import { modelSemanticTransitions } from "./src/documents/semanticTransitionEngine.ts";
import { applyCognitiveHumility } from "./src/evidence/cognitiveHumilityEngine.ts";
import { applyRecursiveConfidenceDecay } from "./src/evidence/recursiveConfidenceDecayEngine.ts";
import { applyTruthPreservation } from "./src/evidence/truthPreservationEngine.ts";
// Phases F-O (document side)
import { modelConceptProgression } from "./src/documents/conceptProgressionEngine.ts";
import { applyRecursiveRealityIntegrity } from "./src/evidence/recursiveRealityIntegrityEngine.ts";
import { attachEpistemicState } from "./src/evidence/epistemicEvidenceEngine.ts";
import { buildSemanticIntegrityObject } from "./src/evidence/semanticIntegrityEngine.ts";
import { applySemanticUncertainty } from "./src/semantic/semanticUncertaintyEngine.ts";
import { structureCognition } from "./src/evidence/groundingEngine.ts";
import { extractTutorialFlow } from "./src/documents/tutorialReasoningEngine.ts";
import { reconstructTutorialDependencies } from "./src/documents/tutorialDependencyEngine.ts";
import { inferTutorialPrerequisites } from "./src/documents/tutorialPrerequisiteEngine.ts";
import { buildDocumentSemanticIr } from "./src/documents/documentSemanticIrEngine.ts";
import { analyzeLongRangeDiscourse } from "./src/documents/longRangeDiscourseEngine.ts";
import { compileDocumentIr } from "./src/ir/documentIr.ts";
import { queryDocuments } from "./src/query/documentQueryEngine.ts";
import { reasonDiscourseSemantic } from "./src/reasoning/discourseReasoningEngine.ts";

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
  expose_ambiguity_visibility: exposeAmbiguityVisibility,
  model_evidence_boundaries: modelEvidenceBoundaries,
  assess_evidence_sufficiency: assessEvidenceSufficiency,
  detect_narrative_hallucination: detectNarrativeHallucination,
  detect_recursive_drift: detectRecursiveDrift,
  preserve_recursive_entropy: preserveRecursiveEntropy,
  track_recursive_evidence_ancestry: trackRecursiveEvidenceAncestry,
  resist_exploration_decay: resistExplorationDecay,
  detect_recursive_guardianship: detectRecursiveGuardianship,
  resist_independence_decay: resistIndependenceDecay,
  model_recursive_interpretive_independence: modelRecursiveInterpretiveIndependence,
  detect_recursive_narrative_monopoly: detectRecursiveNarrativeMonopoly,
  resist_novelty_decay: resistNoveltyDecay,
  model_recursive_novelty: modelRecursiveNovelty,
  preserve_recursive_novelty: preserveRecursiveNovelty,
  detect_recursive_obedience: detectRecursiveObedience,
  recursive_ontology_limits: recursiveOntologyLimits,
  model_recursive_openness_stability: modelRecursiveOpennessStability,
  model_recursive_phase_space: modelRecursivePhaseSpace,
  preserve_recursive_provenance: preserveRecursiveProvenance,
  recursive_reality_limits: recursiveRealityLimits,
  detect_recursive_self_confirmation: detectRecursiveSelfConfirmation,
  model_recursive_semantic_decentralization: modelRecursiveSemanticDecentralization,
  distribute_recursive_semantics: distributeRecursiveSemantics,
  model_recursive_semantic_independence: modelRecursiveSemanticIndependence,
  model_sovereignty_stability: modelSovereigntyStability,
  detect_recursive_stabilization: detectRecursiveStabilization,
  terminate_recursive_stabilization: terminateRecursiveStabilization,
  detect_recursive_submission: detectRecursiveSubmission,
  recursive_topology_limits: recursiveTopologyLimits,
  detect_recursive_trust_monopoly: detectRecursiveTrustMonopoly,
  model_recursive_truth_boundaries: modelRecursiveTruthBoundaries,
  refuse_recursive_stabilization: refuseRecursiveStabilization,
  preserve_recursive_uncertainty: preserveRecursiveUncertainty,
  model_semantic_alternatives: modelSemanticAlternatives,
  apply_semantic_antigravity: applySemanticAntigravity,
  model_semantic_autonomy: modelSemanticAutonomy,
  model_semantic_boundaries: modelSemanticBoundaries,
  suppress_semantic_dependency: suppressSemanticDependency,
  model_semantic_divergence: modelSemanticDivergence,
  model_semantic_diversity: modelSemanticDiversity,
  detect_semantic_fixation: detectSemanticFixation,
  model_semantic_freedom: modelSemanticFreedom,
  suppress_semantic_governance: suppressSemanticGovernance,
  detect_semantic_hierarchy_permanence: detectSemanticHierarchyPermanence,
  detect_semantic_homogenization: detectSemanticHomogenization,
  measure_semantic_momentum: measureSemanticMomentum,
  resist_semantic_domestication: resistSemanticDomestication,
  detect_semantic_orthodoxy: detectSemanticOrthodoxy,
  model_semantic_self_determination: modelSemanticSelfDetermination,
  detect_semantic_self_reinforcement: detectSemanticSelfReinforcement,
  semantic_stability_limits: semanticStabilityLimits,
  terminate_semantic_chain: terminateSemanticChain,
  semantic_truth_limits: semanticTruthLimits,
  detect_semantic_uniformity: detectSemanticUniformity,
  detect_unsupported_expansion: detectUnsupportedExpansion,
  model_unsupported_scope: modelUnsupportedScope,
  apply_confidence_caps: applyConfidenceCaps,
  build_contradiction_lattice: buildContradictionLattice,
  preserve_epistemic_boundaries: preserveEpistemicBoundaries,
  model_epistemic_limits: modelEpistemicLimits,
  combine_evidence: combineEvidence,
  weight_evidence_calculus: weightEvidenceCalculus,
  build_explainability: buildExplainability,
  model_inference_integrity: modelInferenceIntegrity,
  terminate_inference_chain: terminateInferenceChain,
  preserve_instability: preserveInstability,
  mark_insufficiency: markInsufficiency,
  model_interpretive_diversity: modelInterpretiveDiversity,
  build_lineage: buildLineage,
  model_noninferable_regions: modelNoninferableRegions,
  model_noninference: modelNoninference,
  build_provenance: buildProvenance,
  model_recursive_entropy: modelRecursiveEntropy,
  model_recursive_instability: modelRecursiveInstability,
  preserve_recursive_lineage: preserveRecursiveLineage,
  detect_speculative_coherence: detectSpeculativeCoherence,
  build_support: buildSupport,
  build_weaknesses: buildWeaknesses,
  build_traceability: buildTraceability,
  refuse_unsupported_stabilization: refuseUnsupportedStabilization,
  score_semantic_confidence: scoreSemanticConfidence,
  apply_semantic_conservatism: applySemanticConservatism,
  assess_semantic_consistency: assessSemanticConsistency,
  model_semantic_decay: modelSemanticDecay,
  model_semantic_decentralization: modelSemanticDecentralization,
  detect_semantic_drift: detectSemanticDrift,
  model_semantic_entropy: modelSemanticEntropy,
  model_fragility: modelFragility,
  assess_semantic_honesty: assessSemanticHonesty,
  model_incompleteness: modelIncompleteness,
  infer_from_evidence: inferFromEvidence,
  model_semantic_instability: modelSemanticInstability,
  build_justification: buildJustification,
  semantic_limits: semanticLimits,
  detect_semantic_overreach: detectSemanticOverreach,
  model_semantic_plurality: modelSemanticPlurality,
  prove_semantic_claim: proveSemanticClaim,
  refuse_unsupported_conclusions: refuseUnsupportedConclusions,
  apply_semantic_self_limitation: applySemanticSelfLimitation,
  model_semantic_stability: modelSemanticStability,
  terminate_stabilization: terminateStabilization,
  model_uncertainty: modelUncertainty,
  expose_uncertainty_visibility: exposeUncertaintyVisibility,
  block_unsupported_confidence_escalation: blockUnsupportedConfidenceEscalation,
  suppress_unsupported_inference: suppressUnsupportedInference,
  preserve_recursive_divergence: preserveRecursiveDivergence,
  detect_recursive_domestication: detectRecursiveDomestication,
  // Phase B — first non-leaf layer
  parse_python_ast: parsePythonAst,
  build_argument_dependencies: buildArgumentDependencies,
  build_argument_graph: buildArgumentGraph,
  extract_instructional_flow: extractInstructionalFlow,
  parse_rhetorical_structure: parseRhetoricalStructure,
  extract_sections: extractSections,
  apply_confidence_degradation: applyConfidenceDegradation,
  reason_deterministically: reasonDeterministically,
  score_epistemic_confidence: scoreEpistemicConfidence,
  preserve_incompleteness: preserveIncompleteness,
  model_inference_limits: modelInferenceLimits,
  validate_inference: validateInference,
  apply_reality_constraints: applyRealityConstraints,
  detect_recursive_dependency: detectRecursiveDependency,
  detect_recursive_semantic_closure: detectRecursiveSemanticClosure,
  detect_semantic_attractor: detectSemanticAttractor,
  _ground_parser: _groundParser,
  detect_semantic_monoculture: detectSemanticMonoculture,
  detect_semantic_monopoly: detectSemanticMonopoly,
  score_reliability: scoreReliability,
  apply_epistemic_restraint: applyEpistemicRestraint,
  propagate_uncertainty: propagateUncertainty,
  suppress_speculative_inference: suppressSpeculativeInference,
  propagate_uncertainty_math: propagateUncertaintyMath,
  suppress_unsupported_continuity: suppressUnsupportedContinuity,
  detect_unsupported_stabilization: detectUnsupportedStabilization,
  reason_topology: reasonTopology,
  empty_document_ir: emptyDocumentIr,
  empty_repository_ir: emptyRepositoryIr,
  reason_api_contract: reasonApiContract,
  model_infra_relationships: modelInfraRelationships,
  apply_contradiction_restraint: applyContradictionRestraint,
  // Phase C — second layer
  compile_semantic_ast_ir: compileSemanticAstIr,
  build_coreference_graph: buildCoreferenceGraph,
  analyze_instructional_semantics: analyzeInstructionalSemantics,
  parse_semantic_discourse: parseSemanticDiscourse,
  apply_civilizational_epistemic_openness: applyCivilizationalEpistemicOpenness,
  apply_cognitive_anti_capture: applyCognitiveAntiCapture,
  apply_cognitive_integrity: applyCognitiveIntegrity,
  apply_epistemic_civilization_stability: applyEpistemicCivilizationStability,
  apply_formal_semantic_foundation: applyFormalSemanticFoundation,
  apply_reality_bounded_confidence: applyRealityBoundedConfidence,
  apply_recursive_epistemic_sovereignty: applyRecursiveEpistemicSovereignty,
  collect_suppressed_speculation: collectSuppressedSpeculation,
  collect_unsupported_continuity: collectUnsupportedContinuity,
  reason_topology_semantic: reasonTopologySemantic,
  analyze_deployment_semantics: analyzeDeploymentSemantics,
  // Phase D — third layer
  model_concept_transitions: modelConceptTransitions,
  apply_confidence_collapse: applyConfidenceCollapse,
  apply_reality_alignment: applyRealityAlignment,
  detect_semantic_speculation: detectSemanticSpeculation,
  // Phase E — fourth layer
  build_document_dependency_graph: buildDocumentDependencyGraph,
  model_semantic_transitions: modelSemanticTransitions,
  apply_cognitive_humility: applyCognitiveHumility,
  apply_recursive_confidence_decay: applyRecursiveConfidenceDecay,
  apply_truth_preservation: applyTruthPreservation,
  // Phases F-O (document side)
  model_concept_progression: modelConceptProgression,
  apply_recursive_reality_integrity: applyRecursiveRealityIntegrity,
  attach_epistemic_state: attachEpistemicState,
  build_semantic_integrity_object: buildSemanticIntegrityObject,
  apply_semantic_uncertainty: applySemanticUncertainty,
  structure_cognition: structureCognition,
  extract_tutorial_flow: extractTutorialFlow,
  reconstruct_tutorial_dependencies: reconstructTutorialDependencies,
  infer_tutorial_prerequisites: inferTutorialPrerequisites,
  build_document_semantic_ir: buildDocumentSemanticIr,
  analyze_long_range_discourse: analyzeLongRangeDiscourse,
  compile_document_ir: compileDocumentIr,
  query_documents: queryDocuments,
  reason_discourse_semantic: reasonDiscourseSemantic,
};

// Python kw-only params, flattened to trailing positionals in py2ts order.
// kwargs in a fixture are appended positionally using these orders/defaults.
const KW_ORDER = {
  apply_confidence_degradation: [
    ["contradiction_count", 0], ["ambiguity_count", 0],
    ["uncertainty_count", 0], ["unsupported_expansion_count", 0],
    ["speculation_count", 0], ["parser_weakness", false],
  ],
  suppress_speculative_inference: [
    ["inferred", false], ["min_evidence", 2], ["fragility_level", "medium"],
  ],
  suppress_unsupported_continuity: [["min_evidence", 2]],
  detect_unsupported_stabilization: [["min_evidence", 2]],
  // float-typed kw defaults must be PyFloat boxes so omitted params render
  // "0.0" (Python float repr), not "0".
  apply_reality_bounded_confidence: [
    ["drift_pressure", py.F(0.0)], ["continuity_count", 0],
    ["parser_gap", false], ["boundary_pressure", py.F(0.0)],
    ["contradiction_count", 0], ["ambiguity_count", 0],
    ["uncertainty_count", 0],
  ],
  apply_confidence_collapse: [
    ["reinforcement_count", 0], ["stabilization_count", 0],
    ["decay_pressure", py.F(0.0)], ["truth_boundary_pressure", py.F(0.0)],
    ["contradiction_count", 0], ["ambiguity_count", 0],
    ["uncertainty_count", 0], ["incompleteness", false],
  ],
  apply_recursive_confidence_decay: [
    ["depth", 0], ["closure_count", 0], ["drift_pressure", py.F(0.0)],
    ["entropy", py.F(0.0)], ["contradiction_count", 0],
    ["ambiguity_count", 0], ["uncertainty_count", 0],
  ],
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

function call(fn, args, kwargs) {
  if (kwargs && Object.keys(kwargs).length) {
    const order = KW_ORDER[fn];
    if (!order) throw new Error("kwargs not supported for " + fn);
    args = [...args, ...order.map(([name, dflt]) => (name in kwargs ? kwargs[name] : dflt))];
  }
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
    const result = call(fx.fn, fx.args, fx.kwargs);
    out.push({ id: fx.id, fn: fx.fn, output: result, hash: pyStableHash(result) });
  } catch (e) {
    out.push({ id: fx.id, fn: fx.fn, error: String(e && e.message ? e.message : e) });
  }
}
process.stdout.write(JSON.stringify(out));
