// Execute Dart semantic-IR ported functions; emit output + hash.
//   dart run validation/semantic_ir/run_dart.dart validation/semantic_ir/fixtures.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/ast_engines.dart';
import 'package:webweavex/src/semantic_ir/document_parser.dart';
import 'package:webweavex/src/semantic_ir/evidence_leaves.dart';
import 'package:webweavex/src/semantic_ir/evidence_leaves_2.dart';
import 'package:webweavex/src/semantic_ir/graph_engines.dart';
import 'package:webweavex/src/semantic_ir/ir_base.dart';
import 'package:webweavex/src/semantic_ir/pressure_engines.dart';
import 'package:webweavex/src/semantic_ir/repository_engines.dart';

/// A.3 leaves take plain positional args — dispatch generically.
final Map<String, Function> a3Registry = <String, Function>{
  'detect_authority_concentration': detectAuthorityConcentration,
  'diffuse_authority': diffuseAuthority,
  'resist_autonomy_erosion': resistAutonomyErosion,
  'model_causal_plurality': modelCausalPlurality,
  'model_cognitive_decentralization': modelCognitiveDecentralization,
  'detect_cognitive_gravity_well': detectCognitiveGravityWell,
  'model_cognitive_sovereignty': modelCognitiveSovereignty,
  'detect_confidence_echo': detectConfidenceEcho,
  'refuse_unsupported_continuity': refuseUnsupportedContinuity,
  'model_epistemic_openness': modelEpistemicOpenness,
  'model_evidence_decay': modelEvidenceDecay,
  'apply_explanatory_antigravity': applyExplanatoryAntigravity,
  'model_explanatory_competition': modelExplanatoryCompetition,
  'model_explanatory_divergence': modelExplanatoryDivergence,
  'model_explanatory_diversity': modelExplanatoryDiversity,
  'detect_explanatory_fixation': detectExplanatoryFixation,
  'preserve_explanatory_freedom': preserveExplanatoryFreedom,
  'resist_explanatory_domestication': resistExplanatoryDomestication,
  'model_explanatory_self_determination': modelExplanatorySelfDetermination,
  'refuse_inference': refuseInference,
  'model_interpretive_autonomy': modelInterpretiveAutonomy,
  'detect_interpretive_closure': detectInterpretiveClosure,
  'resist_interpretive_decay': resistInterpretiveDecay,
  'distribute_interpretations': distributeInterpretations,
  'model_interpretive_divergence': modelInterpretiveDivergence,
  'preserve_interpretive_freedom': preserveInterpretiveFreedom,
  'resist_interpretive_domestication': resistInterpretiveDomestication,
  'model_interpretive_self_determination': modelInterpretiveSelfDetermination,
  'apply_ontology_antigravity': applyOntologyAntigravity,
  'model_ontology_boundaries': modelOntologyBoundaries,
  'model_ontology_competition': modelOntologyCompetition,
  'model_ontology_divergence': modelOntologyDivergence,
  'detect_ontology_fixation': detectOntologyFixation,
  'preserve_ontology_freedom': preserveOntologyFreedom,
  'detect_ontology_hardening': detectOntologyHardening,
  'model_ontology_instability': modelOntologyInstability,
  'ontology_limits': ontologyLimits,
  'detect_ontology_monopoly': detectOntologyMonopoly,
  'resist_ontology_domestication': resistOntologyDomestication,
  'model_ontology_self_determination': modelOntologySelfDetermination,
  'resist_plurality_decay': resistPluralityDecay,
  'resist_agency_decay': resistAgencyDecay,
  'model_recursive_agency': modelRecursiveAgency,
  'preserve_recursive_agency': preserveRecursiveAgency,
  'diffuse_recursive_authority': diffuseRecursiveAuthority,
  'preserve_recursive_autonomy': preserveRecursiveAutonomy,
  'model_capture_resistance': modelCaptureResistance,
  'detect_recursive_centralization': detectRecursiveCentralization,
  'distribute_recursive_cognition': distributeRecursiveCognition,
  'detect_recursive_coherence_inflation': detectRecursiveCoherenceInflation,
  'detect_recursive_confidence_echo': detectRecursiveConfidenceEcho,
  'detect_recursive_consensus': detectRecursiveConsensus,
  'model_stability_boundary': modelStabilityBoundary,
  'model_topology_boundaries': modelTopologyBoundaries,
  'topology_limits': topologyLimits,
  'model_truth_boundaries': modelTruthBoundaries,
  'apply_worldview_antigravity': applyWorldviewAntigravity,
  'suppress_worldview_convergence': suppressWorldviewConvergence,
  'model_worldview_diversity': modelWorldviewDiversity,
  'model_worldview_variance': modelWorldviewVariance,
  'expose_ambiguity_visibility': exposeAmbiguityVisibility,
  'model_evidence_boundaries': modelEvidenceBoundaries,
  'assess_evidence_sufficiency': assessEvidenceSufficiency,
  'detect_narrative_hallucination': detectNarrativeHallucination,
  'detect_recursive_drift': detectRecursiveDrift,
  'preserve_recursive_entropy': preserveRecursiveEntropy,
  'track_recursive_evidence_ancestry': trackRecursiveEvidenceAncestry,
  'resist_exploration_decay': resistExplorationDecay,
  'detect_recursive_guardianship': detectRecursiveGuardianship,
  'resist_independence_decay': resistIndependenceDecay,
  'model_recursive_interpretive_independence':
      modelRecursiveInterpretiveIndependence,
  'detect_recursive_narrative_monopoly': detectRecursiveNarrativeMonopoly,
  'resist_novelty_decay': resistNoveltyDecay,
  'model_recursive_novelty': modelRecursiveNovelty,
  'preserve_recursive_novelty': preserveRecursiveNovelty,
  'detect_recursive_obedience': detectRecursiveObedience,
  'recursive_ontology_limits': recursiveOntologyLimits,
  'model_recursive_openness_stability': modelRecursiveOpennessStability,
  'model_recursive_phase_space': modelRecursivePhaseSpace,
  'preserve_recursive_provenance': preserveRecursiveProvenance,
  'recursive_reality_limits': recursiveRealityLimits,
  'detect_recursive_self_confirmation': detectRecursiveSelfConfirmation,
  'model_recursive_semantic_decentralization':
      modelRecursiveSemanticDecentralization,
  'distribute_recursive_semantics': distributeRecursiveSemantics,
  'model_recursive_semantic_independence': modelRecursiveSemanticIndependence,
  'model_sovereignty_stability': modelSovereigntyStability,
  'detect_recursive_stabilization': detectRecursiveStabilization,
  'terminate_recursive_stabilization': terminateRecursiveStabilization,
  'detect_recursive_submission': detectRecursiveSubmission,
  'recursive_topology_limits': recursiveTopologyLimits,
  'detect_recursive_trust_monopoly': detectRecursiveTrustMonopoly,
  'model_recursive_truth_boundaries': modelRecursiveTruthBoundaries,
  'refuse_recursive_stabilization': refuseRecursiveStabilization,
  'preserve_recursive_uncertainty': preserveRecursiveUncertainty,
  'model_semantic_alternatives': modelSemanticAlternatives,
  'apply_semantic_antigravity': applySemanticAntigravity,
  'model_semantic_autonomy': modelSemanticAutonomy,
  'model_semantic_boundaries': modelSemanticBoundaries,
  'suppress_semantic_dependency': suppressSemanticDependency,
  'model_semantic_divergence': modelSemanticDivergence,
  'model_semantic_diversity': modelSemanticDiversity,
  'detect_semantic_fixation': detectSemanticFixation,
  'model_semantic_freedom': modelSemanticFreedom,
  'suppress_semantic_governance': suppressSemanticGovernance,
  'detect_semantic_hierarchy_permanence': detectSemanticHierarchyPermanence,
  'detect_semantic_homogenization': detectSemanticHomogenization,
  'measure_semantic_momentum': measureSemanticMomentum,
  'resist_semantic_domestication': resistSemanticDomestication,
  'detect_semantic_orthodoxy': detectSemanticOrthodoxy,
  'model_semantic_self_determination': modelSemanticSelfDetermination,
  'detect_semantic_self_reinforcement': detectSemanticSelfReinforcement,
  'semantic_stability_limits': semanticStabilityLimits,
  'terminate_semantic_chain': terminateSemanticChain,
  'semantic_truth_limits': semanticTruthLimits,
  'detect_semantic_uniformity': detectSemanticUniformity,
  'detect_unsupported_expansion': detectUnsupportedExpansion,
  'model_unsupported_scope': modelUnsupportedScope,
};

List<Map<String, dynamic>> _claims(dynamic v) => <Map<String, dynamic>>[
      for (final e in v as List) Map<String, dynamic>.from(e as Map)
    ];

dynamic _call(String fn, List<dynamic> args) {
  final a3 = a3Registry[fn];
  if (a3 != null) return Function.apply(a3, args);
  switch (fn) {
    // A.1 — document parser leaves
    case 'extract_rhetorical_structure':
      return extractRhetoricalStructure(args[0] as String?);
    case 'assign_semantic_roles':
      return assignSemanticRoles(args[0] as String?);
    case 'extract_headings':
      return extractHeadings(args[0] as String?);
    case 'reconstruct_argument_dependencies':
      return reconstructArgumentDependencies(_claims(args[0]));
    case 'resolve_coreferences':
      return resolveCoreferences(args[0] as String?);
    // A.2 — semantic pressure leaves
    case 'compute_ambiguity_pressure':
      return computeAmbiguityPressure(args[0] as List<dynamic>);
    case 'compute_contradiction_pressure':
      return computeContradictionPressure(args[0]);
    case 'compute_evidence_boundary_pressure':
      return args.length > 1
          ? computeEvidenceBoundaryPressure(args[0] as int, args[1] as int)
          : computeEvidenceBoundaryPressure(args[0] as int);
    case 'compute_evidence_decay_pressure':
      return args.length > 1
          ? computeEvidenceDecayPressure(args[0] as int, args[1] as int)
          : computeEvidenceDecayPressure(args[0] as int);
    case 'compute_recursive_boundary_pressure':
      return computeRecursiveBoundaryPressure(args[0] as num, args[1] as int);
    case 'compute_recursive_convergence_pressure':
      return computeRecursiveConvergencePressure(
          args[0] as int, args[1] as num);
    case 'compute_recursive_dependency_pressure':
      return computeRecursiveDependencyPressure(args[0] as int, args[1] as int);
    case 'compute_semantic_boundary_pressure':
      return computeSemanticBoundaryPressure(args[0] as num, args[1] as num);
    case 'compute_truth_boundary_pressure':
      return computeTruthBoundaryPressure(args[0] as bool, args[1] as num);
    case 'compute_uncertainty_pressure':
      return computeUncertaintyPressure(
          args[0] as List<dynamic>, args[1] as List<dynamic>);
    // A.2 — ir/_base leaves
    case 'empty_confidence':
      return emptyConfidence();
    case 'empty_lineage':
      return args.isNotEmpty ? emptyLineage(args[0] as String) : emptyLineage();
    case 'merge_evidence':
      return mergeEvidence(args);
    // A.2 — graph leaves
    case 'model_graph_entropy':
      return modelGraphEntropy(args[0] as Map);
    case 'detect_cycles':
      return detectCycles(args[0] as Map);
    case 'prove_topology':
      return proveTopology(args[0] as Map);
    // A.2 — repository leaves
    case 'reason_api_surface':
      return reasonApiSurface(args[0]);
    case 'reconstruct_execution_flow':
      return reconstructExecutionFlow(args[0]);
    case 'detect_infra_signals':
      return detectInfraSignals(args[0] as List<dynamic>?);
    case 'resolve_runtime_dependencies':
      return args.length > 1
          ? resolveRuntimeDependencies(args[0], args[1] as String)
          : resolveRuntimeDependencies(args[0]);
    case 'infer_service_interactions':
      return inferServiceInteractions(args[0], args[1] as List<dynamic>);
    // A.2 — ast leaves
    case 'build_control_flow_graph':
      return buildControlFlowGraph(args[0] as Map);
    case 'reconstruct_execution_paths':
      return reconstructExecutionPaths(args[0] as Map);
    case 'resolve_symbols':
      return resolveSymbols(args[0] as Map);
    default:
      throw StateError('unknown fn $fn');
  }
}

void main(List<String> argv) {
  final fixtures =
      jsonDecode(File(argv[0]).readAsStringSync()) as List<dynamic>;
  final out = <Map<String, dynamic>>[];
  for (final f in fixtures) {
    final fx = Map<String, dynamic>.from(f as Map);
    final fn = fx['fn'] as String;
    try {
      final result = _call(fn, fx['args'] as List<dynamic>);
      out.add(<String, dynamic>{
        'id': fx['id'],
        'fn': fn,
        'output': result,
        'hash': computeDeterministicHash(result),
      });
    } catch (e) {
      out.add(
          <String, dynamic>{'id': fx['id'], 'fn': fn, 'error': e.toString()});
    }
  }
  stdout.write(jsonEncode(out));
}
