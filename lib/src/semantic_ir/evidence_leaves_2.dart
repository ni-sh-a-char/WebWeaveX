/// Phase A.3 batch 2 (core.evidence leaves) of the Category-A semantic-IR
/// port — 57 leaf engines (recursive/semantic/unsupported families, incl.
/// sorted/set/round sites), proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.evidence.ambiguity_visibility_engine.expose_ambiguity_visibility.
/// `confidence_score` is accepted but unused — exactly as in Python.
Map<String, dynamic> exposeAmbiguityVisibility(
    List<dynamic> ambiguities, num confidenceScore) {
  final pressure = pythonRound(math.min(1.0, ambiguities.length * 0.12), 3);
  final items = <String>{for (final a in ambiguities) pyToStr(a)}.toList()
    ..sort();
  return <String, dynamic>{
    'visible': pyTruthy(ambiguities),
    'count': ambiguities.length,
    'items': items,
    'pressure': pressure,
    'suppress_expansion': pressure >= 0.25,
    'confidence_impact': pythonRound(math.min(0.3, pressure * 0.35), 3),
    'preserved': true,
  };
}

/// Port of core.evidence.evidence_boundary_engine.model_evidence_boundaries.
Map<String, dynamic> modelEvidenceBoundaries(List<dynamic> evidence,
    {int minEvidence = 2}) {
  final bounded = evidence.length >= minEvidence;
  return <String, dynamic>{
    'bounded': bounded,
    'evidence_count': evidence.length,
    'min_required': minEvidence,
    'violation': !bounded,
    'where_evidence_stops': evidence.length,
  };
}

/// Port of core.evidence.evidence_sufficiency_engine.assess_evidence_sufficiency.
Map<String, dynamic> assessEvidenceSufficiency(List<dynamic>? evidence,
    [int required = 2]) {
  final count = (evidence ?? const <dynamic>[]).length;
  final sufficient = count >= required;
  return <String, dynamic>{
    'sufficient': sufficient,
    'evidence_count': count,
    'required': required,
    'status': sufficient ? 'sufficient' : 'insufficient_evidence',
    'deterministic_inputs': <String>['count=$count', 'required=$required'],
  };
}

/// Port of core.evidence.narrative_hallucination_engine.detect_narrative_hallucination.
Map<String, dynamic> detectNarrativeHallucination(
    Map<dynamic, dynamic> inferred,
    List<dynamic> evidence,
    bool parserGrounded) {
  final hallucinated =
      pyTruthy(inferred) && !parserGrounded && evidence.isEmpty;
  return <String, dynamic>{
    'hallucination_risk': hallucinated,
    'suppressed': hallucinated,
    'reason': hallucinated ? 'narrative_without_parser' : null,
  };
}

/// Port of core.evidence.recursive_drift_engine.detect_recursive_drift.
Map<String, dynamic> detectRecursiveDrift(
    int depth, int evidenceCount, int inferredCount) {
  final drift = pythonRound(
      math.min(
          1.0, depth * 0.1 + math.max(0, inferredCount - evidenceCount) * 0.15),
      3);
  return <String, dynamic>{
    'drift_detected': drift >= 0.2,
    'drift_pressure': drift,
    'suppress_normalization': drift >= 0.15,
  };
}

/// Port of core.evidence.recursive_entropy_preservation_engine.preserve_recursive_entropy.
Map<String, dynamic> preserveRecursiveEntropy(
    List<dynamic> ambiguities, List<dynamic> uncertainties, int depth) {
  final entropy = pythonRound(
      math.min(
          1.0,
          ambiguities.length * 0.1 +
              uncertainties.length * 0.08 +
              depth * 0.02),
      3);
  return <String, dynamic>{
    'entropy': entropy,
    'preserved': true,
    'collapse_blocked': true,
  };
}

/// Port of core.evidence.recursive_evidence_ancestry_engine.track_recursive_evidence_ancestry.
Map<String, dynamic> trackRecursiveEvidenceAncestry(
    List<dynamic> evidence, int depth) {
  final detached = depth > 3 && evidence.length < 2;
  return <String, dynamic>{
    'ancestry': List<dynamic>.from(evidence),
    'depth': depth,
    'detached': detached,
    'suppress_stabilization': detached,
  };
}

/// Port of core.evidence.recursive_exploration_decay_engine.resist_exploration_decay.
Map<String, dynamic> resistExplorationDecay(bool exploratory, int depth) {
  final decay = depth >= 5 && !exploratory;
  return <String, dynamic>{'decay_risk': decay, 'resist': true};
}

/// Port of core.evidence.recursive_guardianship_engine.detect_recursive_guardianship.
Map<String, dynamic> detectRecursiveGuardianship(bool centrality, int depth) {
  final guardianship = centrality && depth >= 2;
  return <String, dynamic>{
    'guardianship': guardianship,
    'suppress': guardianship,
    'paternalism_blocked': true,
  };
}

/// Port of core.evidence.recursive_independence_decay_engine.resist_independence_decay.
Map<String, dynamic> resistIndependenceDecay(bool independent, int depth) {
  final decay = depth >= 5 && !independent;
  return <String, dynamic>{'decay_risk': decay, 'resist': true};
}

/// Port of core.evidence.recursive_interpretive_independence_engine.model_recursive_interpretive_independence.
Map<String, dynamic> modelRecursiveInterpretiveIndependence(int count) =>
    <String, dynamic>{
      'independent': count > 1,
      'collapse_blocked': true,
    };

/// Port of core.evidence.recursive_narrative_monopoly_engine.detect_recursive_narrative_monopoly.
Map<String, dynamic> detectRecursiveNarrativeMonopoly(
    int narrativeCount, int depth) {
  final monopoly = narrativeCount <= 1 && depth >= 2;
  return <String, dynamic>{
    'monopoly': monopoly,
    'suppress': monopoly,
    'lock_in_blocked': true,
  };
}

/// Port of core.evidence.recursive_novelty_decay_engine.resist_novelty_decay.
Map<String, dynamic> resistNoveltyDecay(num novelty, int depth) {
  final decay = depth >= 4 && novelty < 0.2;
  return <String, dynamic>{
    'decay_risk': decay,
    'resist': true,
    'exhaustion_blocked': decay,
  };
}

/// Port of core.evidence.recursive_novelty_engine.model_recursive_novelty.
Map<String, dynamic> modelRecursiveNovelty(
    int depth, int keyCount, int ambiguityCount) {
  final novelty = pythonRound(
      math.min(
          1.0,
          keyCount * 0.12 +
              ambiguityCount * 0.08 +
              math.max(0, 3 - depth) * 0.05),
      3);
  return <String, dynamic>{
    'novelty': novelty,
    'preserved': novelty > 0.1,
    'exhaustion_blocked': true,
  };
}

/// Port of core.evidence.recursive_novelty_preservation_engine.preserve_recursive_novelty.
Map<String, dynamic> preserveRecursiveNovelty(
    Map<dynamic, dynamic> novelty, int depth) {
  final decayRisk = depth >= 5 && (pyGet(novelty, 'novelty', 0) as num) < 0.15;
  return <String, dynamic>{
    'preserved': true,
    'decay_risk': decayRisk,
    'decay_suppressed': decayRisk,
  };
}

/// Port of core.evidence.recursive_obedience_engine.detect_recursive_obedience.
Map<String, dynamic> detectRecursiveObedience(
    bool highConfidence, bool lowEvidence, int depth) {
  final obedience = highConfidence && lowEvidence && depth >= 2;
  return <String, dynamic>{'obedience': obedience, 'suppress': obedience};
}

/// Port of core.evidence.recursive_ontology_limit_engine.recursive_ontology_limits.
Map<String, dynamic> recursiveOntologyLimits(int depth) => <String, dynamic>{
      'lock_in_allowed': false,
      'max_recursive_depth': 3,
      'depth': depth,
    };

/// Port of core.evidence.recursive_openness_stability_engine.model_recursive_openness_stability.
Map<String, dynamic> modelRecursiveOpennessStability(bool isOpen, int depth) =>
    <String, dynamic>{
      'stable': isOpen,
      'long_horizon': true,
      'convergence_collapse_blocked': depth >= 3,
      'novelty_exhaustion_blocked': true,
    };

/// Port of core.evidence.recursive_phase_space_engine.model_recursive_phase_space.
Map<String, dynamic> modelRecursivePhaseSpace(
    int keyCount, int ambiguityCount, int depth) {
  final volume =
      pythonRound(math.min(1.0, keyCount * 0.1 + ambiguityCount * 0.08), 3);
  final reduction = depth >= 4 && keyCount <= 1;
  return <String, dynamic>{
    'volume': volume,
    'reduction_blocked': reduction,
    'preserved': volume > 0,
  };
}

/// Port of core.evidence.recursive_provenance_engine.preserve_recursive_provenance.
Map<String, dynamic> preserveRecursiveProvenance(
    List<dynamic> sources, Map<dynamic, dynamic> lineage) {
  return <String, dynamic>{
    'sources': List<dynamic>.from(sources),
    'lineage_depth': pyGet(lineage, 'depth', 0),
    'complete': pyTruthy(sources),
  };
}

/// Port of core.evidence.recursive_reality_limit_engine.recursive_reality_limits.
Map<String, dynamic> recursiveRealityLimits(
    int depth, Map<dynamic, dynamic> entropy) {
  return <String, dynamic>{
    'max_depth_without_evidence': 2,
    'closure_allowed': false,
    'stabilization_allowed':
        pyGet(entropy, 'suppress_recursive_stabilization', false) != true,
    'current_depth': depth,
  };
}

/// Port of core.evidence.recursive_self_confirmation_engine.detect_recursive_self_confirmation.
Map<String, dynamic> detectRecursiveSelfConfirmation(
    int depth, bool reconciledEqInferred, int evidenceCount) {
  final confirm = depth >= 2 && reconciledEqInferred && evidenceCount < 2;
  return <String, dynamic>{
    'detected': confirm,
    'suppress': confirm,
    'recursive_pressure': confirm ? pythonRound(depth * 0.1, 3) : 0.0,
  };
}

/// Port of core.evidence.recursive_semantic_decentralization_engine.model_recursive_semantic_decentralization.
Map<String, dynamic> modelRecursiveSemanticDecentralization(
    List<dynamic> clusters, int evidenceCount) {
  final dominated = clusters.length <= 1 && evidenceCount < 3;
  return <String, dynamic>{
    'decentralized': !dominated,
    'cluster_count': clusters.length,
    'dominance_blocked': dominated,
  };
}

/// Port of core.evidence.recursive_semantic_distribution_engine.distribute_recursive_semantics.
Map<String, dynamic> distributeRecursiveSemantics(List<dynamic> keys) {
  final unique = <dynamic>{...keys};
  return <String, dynamic>{
    'distributed': unique.length > 1,
    'key_count': unique.length,
  };
}

/// Port of core.evidence.recursive_semantic_independence_engine.model_recursive_semantic_independence.
Map<String, dynamic> modelRecursiveSemanticIndependence(
        List<dynamic> keys, int depth) =>
    <String, dynamic>{
      'independent': <dynamic>{...keys}.length > 1 || depth < 2,
      'reliance_blocked': true,
    };

/// Port of core.evidence.recursive_sovereignty_stability_engine.model_sovereignty_stability.
Map<String, dynamic> modelSovereigntyStability(bool sovereign, int depth) =>
    <String, dynamic>{
      'stable': sovereign,
      'long_horizon': true,
      'dependence_loops_blocked': depth >= 2,
      'obedience_loops_blocked': true,
    };

/// Port of core.evidence.recursive_stabilization_engine.detect_recursive_stabilization.
Map<String, dynamic> detectRecursiveStabilization(
    bool reconciledEqInferred, int depth) {
  final stabilized = reconciledEqInferred && depth >= 2;
  return <String, dynamic>{
    'stabilized': stabilized,
    'suppress': stabilized,
    'basin_blocked': stabilized,
  };
}

/// Port of core.evidence.recursive_stabilization_termination_engine.terminate_recursive_stabilization.
Map<String, dynamic> terminateRecursiveStabilization(
    List<dynamic> suppressed, int depth) {
  final terminated = <String>[
    for (final s in suppressed) pyGet(s as Map, 'reason', '') as String,
    if (depth >= 4) 'depth_${depth}_limit',
  ];
  final unique = <String>{
    for (final t in terminated)
      if (pyTruthy(t)) t
  }.toList()
    ..sort();
  return <String, dynamic>{
    'terminated': unique,
    'chain_stopped': pyTruthy(terminated),
  };
}

/// Port of core.evidence.recursive_submission_engine.detect_recursive_submission.
Map<String, dynamic> detectRecursiveSubmission(
    bool reconciledEqInferred, int depth, int evidenceCount) {
  final submission = reconciledEqInferred && depth >= 2 && evidenceCount < 2;
  return <String, dynamic>{'submission': submission, 'suppress': submission};
}

/// Port of core.evidence.recursive_topology_limit_engine.recursive_topology_limits.
Map<String, dynamic> recursiveTopologyLimits(int depth) => <String, dynamic>{
      'normalization_allowed': false,
      'max_recursive_depth': 3,
      'depth': depth,
    };

/// Port of core.evidence.recursive_trust_monopoly_engine.detect_recursive_trust_monopoly.
Map<String, dynamic> detectRecursiveTrustMonopoly(
    num trustScore, int depth, int evidenceCount) {
  final monopoly = trustScore > 0.85 && depth >= 2 && evidenceCount < 2;
  return <String, dynamic>{
    'monopoly': monopoly,
    'suppress': monopoly,
    'absolutism_blocked': true,
  };
}

/// Port of core.evidence.recursive_truth_boundary_engine.model_recursive_truth_boundaries.
Map<String, dynamic> modelRecursiveTruthBoundaries(int depth, int evidenceCount,
    {int minEvidence = 2}) {
  final erosion = pythonRound(math.min(1.0, depth * 0.08), 3);
  final bounded = evidenceCount >= minEvidence && erosion < 0.5;
  return <String, dynamic>{
    'bounded': bounded,
    'depth': depth,
    'erosion': erosion,
    'closure_allowed': false,
    'recursive_lock_in_allowed': false,
  };
}

/// Port of core.evidence.recursive_truth_refusal_engine.refuse_recursive_stabilization.
Map<String, dynamic> refuseRecursiveStabilization(List<dynamic> suppressed) {
  final refusals = <Map<String, dynamic>>[
    for (final s in suppressed)
      <String, dynamic>{
        'target': pyGet(s as Map, 'reason', 'closure'),
        'message': 'recursive_truthfully_incomplete',
      }
  ];
  final reasons = <String>{for (final r in refusals) r['message'] as String}
      .toList()
    ..sort();
  return <String, dynamic>{
    'recursive_truth_refusals': refusals,
    'recursive_stabilization_failures': <dynamic>[
      for (final s in suppressed) pyGet(s as Map, 'reason', null)
    ],
    'recursive_boundary_failures': <dynamic>[
      for (final s in suppressed)
        pyGet(
            (pyGet(s as Map, 'truth_boundary_violation', <dynamic, dynamic>{})
                as Map),
            'type',
            null)
    ],
    'recursive_termination_reasons': reasons,
  };
}

/// Port of core.evidence.recursive_uncertainty_preservation_engine.preserve_recursive_uncertainty.
Map<String, dynamic> preserveRecursiveUncertainty(
    List<dynamic> uncertainties, int depth) {
  final items = <String>{for (final u in uncertainties) pyToStr(u)}.toList()
    ..sort();
  return <String, dynamic>{
    'preserved': true,
    'items': items,
    'depth': depth,
    'collapse_suppressed': true,
  };
}

/// Port of core.evidence.semantic_alternative_engine.model_semantic_alternatives.
Map<String, dynamic> modelSemanticAlternatives(
    Map<dynamic, dynamic> observed, Map<dynamic, dynamic> inferred) {
  final keys = <dynamic>{...observed.keys, ...inferred.keys}.toList()
    ..sort((a, b) => (a as String).compareTo(b as String));
  final alts = <Map<String, dynamic>>[
    for (final k in keys)
      <String, dynamic>{
        'key': k,
        'source': observed.containsKey(k) ? 'observed' : 'inferred',
      }
  ];
  return <String, dynamic>{
    'alternatives': alts.take(15).toList(),
    'preserved': alts.length > 1 || alts.isEmpty,
  };
}

/// Port of core.evidence.semantic_antigravity_engine.apply_semantic_antigravity.
Map<String, dynamic> applySemanticAntigravity(bool gravitySuppressed) =>
    <String, dynamic>{
      'active': true,
      'gravity_well_suppressed': gravitySuppressed,
      'basin_escape': true,
    };

/// Port of core.evidence.semantic_autonomy_engine.model_semantic_autonomy.
Map<String, dynamic> modelSemanticAutonomy(
        List<dynamic> interpretations, int evidenceCount) =>
    <String, dynamic>{
      'autonomous': interpretations.length > 1 || evidenceCount >= 2,
      'capture_resistant': true,
      'dominant_cluster': interpretations.length <= 1 && evidenceCount < 2,
    };

/// Port of core.evidence.semantic_boundary_engine.model_semantic_boundaries.
Map<String, dynamic> modelSemanticBoundaries(
    Map<dynamic, dynamic> inferred, bool allowed) {
  List<String> sortedKeys() =>
      <String>[for (final k in inferred.keys) k as String]..sort();
  return <String, dynamic>{
    'inference_allowed': allowed,
    'bounded_inferences': allowed ? sortedKeys() : <String>[],
    'blocked_inferences': !allowed ? sortedKeys() : <String>[],
    'where_inference_stops': allowed ? <String>[] : sortedKeys(),
    'reality_bounded': allowed,
  };
}

/// Port of core.evidence.semantic_dependency_suppression_engine.suppress_semantic_dependency.
Map<String, dynamic> suppressSemanticDependency(List<dynamic> suppressed) =>
    <String, dynamic>{
      'suppressed': suppressed.length,
      'active': pyTruthy(suppressed),
      'loops_blocked': true,
    };

/// Port of core.evidence.semantic_divergence_engine.model_semantic_divergence.
Map<String, dynamic> modelSemanticDivergence(Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred, List<dynamic> ambiguities) {
  final keys = <dynamic>{...observed.keys, ...inferred.keys};
  final score = pythonRound(
      math.min(1.0, keys.length * 0.15 + ambiguities.length * 0.1), 3);
  return <String, dynamic>{
    'divergence_score': score,
    'preserved': score > 0 || pyTruthy(ambiguities),
    'phase_space_maintained': keys.length > 1,
  };
}

/// Port of core.evidence.semantic_diversity_engine.model_semantic_diversity.
Map<String, dynamic> modelSemanticDiversity(Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred, List<dynamic> ambiguities) {
  final score = pythonRound(
      math.min(
          1.0, (observed.length + inferred.length + ambiguities.length) * 0.1),
      3);
  return <String, dynamic>{
    'diversity_score': score,
    'preserved': score > 0 || pyTruthy(ambiguities),
  };
}

/// Port of core.evidence.semantic_fixation_engine.detect_semantic_fixation.
Map<String, dynamic> detectSemanticFixation(bool keyUniformity, int depth) {
  final fixation = keyUniformity && depth >= 2;
  return <String, dynamic>{
    'fixation': fixation,
    'suppress': fixation,
    'inevitability_blocked': fixation,
  };
}

/// Port of core.evidence.semantic_freedom_engine.model_semantic_freedom.
Map<String, dynamic> modelSemanticFreedom(
    Map<dynamic, dynamic> autonomy, Map<dynamic, dynamic> competition) {
  return <String, dynamic>{
    'free': pyGet(autonomy, 'autonomous', true) == true &&
        pyGet(competition, 'competitive', true) == true,
    'governance_suppressed': true,
    'hierarchy_permanence_blocked': true,
  };
}

/// Port of core.evidence.semantic_governance_engine.suppress_semantic_governance.
Map<String, dynamic> suppressSemanticGovernance(
        bool governanceDetected, int depth) =>
    <String, dynamic>{
      'governance': governanceDetected && depth >= 2,
      'suppress': true,
      'centralized_governance_blocked': true,
    };

/// Port of core.evidence.semantic_hierarchy_engine.detect_semantic_hierarchy_permanence.
Map<String, dynamic> detectSemanticHierarchyPermanence(
    int depth, bool hierarchyLocked) {
  final permanent = hierarchyLocked && depth >= 3;
  return <String, dynamic>{
    'permanent': permanent,
    'suppress': permanent,
    'aristocracy_blocked': true,
  };
}

/// Port of core.evidence.semantic_homogenization_engine.detect_semantic_homogenization.
Map<String, dynamic> detectSemanticHomogenization(bool uniformity, int depth) {
  final homogenized = uniformity && depth >= 2;
  return <String, dynamic>{
    'homogenized': homogenized,
    'suppress': homogenized,
    'flattening_prevented': true,
  };
}

/// Port of core.evidence.semantic_momentum_engine.measure_semantic_momentum.
Map<String, dynamic> measureSemanticMomentum(
    int inferredCount, int evidenceCount) {
  final ratio = inferredCount / math.max(1, evidenceCount);
  final pressure =
      pythonRound(math.min(1.0, math.max(0.0, ratio - 1.0) * 0.3), 3);
  return <String, dynamic>{
    'momentum': pressure,
    'halt_expansion': pressure >= 0.25,
    'inferred_count': inferredCount,
    'evidence_count': evidenceCount,
  };
}

/// Port of core.evidence.semantic_nondomestication_engine.resist_semantic_domestication.
Map<String, dynamic> resistSemanticDomestication(bool domestication) =>
    <String, dynamic>{
      'resisted': true,
      'domestication_suppressed': domestication,
    };

/// Port of core.evidence.semantic_orthodoxy_engine.detect_semantic_orthodoxy.
Map<String, dynamic> detectSemanticOrthodoxy(
    List<dynamic> interpretations, int depth) {
  final orthodox = interpretations.length <= 1 && depth >= 3;
  return <String, dynamic>{
    'orthodoxy_detected': orthodox,
    'suppress': orthodox,
    'orthodoxy_pressure': <String, dynamic>{'level': orthodox ? 0.85 : 0.0},
  };
}

/// Port of core.evidence.semantic_self_determination_engine.model_semantic_self_determination.
Map<String, dynamic> modelSemanticSelfDetermination(
        bool independent, int depth) =>
    <String, dynamic>{
      'self_determined': independent,
      'dependency_blocked': true,
      'obedience_blocked': true,
      'depth': depth,
    };

/// Port of core.evidence.semantic_self_reinforcement_engine.detect_semantic_self_reinforcement.
/// Python compares `reconciled == inferred` structurally — [pyDeepEq].
Map<String, dynamic> detectSemanticSelfReinforcement(
    Map<dynamic, dynamic> inferred,
    Map<dynamic, dynamic> reconciled,
    List<dynamic> evidence) {
  final echo = pyDeepEq(reconciled, inferred) &&
      inferred.length > 1 &&
      evidence.length < 2;
  return <String, dynamic>{
    'reinforcement_detected': echo,
    'suppress': echo,
    'pressure': echo ? 0.8 : 0.0,
  };
}

/// Port of core.evidence.semantic_stability_limit_engine.semantic_stability_limits.
Map<String, dynamic> semanticStabilityLimits(Map<dynamic, dynamic> stability) {
  final limits =
      pyGet(stability, 'stability_limits', <dynamic, dynamic>{}) as Map;
  return <String, dynamic>{
    'max_confidence': pyGet(limits, 'max_confidence', 0.5),
    'expansion_allowed': pyGet(stability, 'stable', false),
  };
}

/// Port of core.evidence.semantic_termination_engine.terminate_semantic_chain.
Map<String, dynamic> terminateSemanticChain(
    List<dynamic> unstableRegions, List<dynamic> continuityRefusals) {
  final terminated = <dynamic>[
    ...unstableRegions,
    for (final r in continuityRefusals) pyGet(r as Map, 'target', ''),
  ];
  final unique = <String>{
    for (final t in terminated)
      if (pyTruthy(t)) t as String
  }.toList()
    ..sort();
  return <String, dynamic>{
    'terminated': unique,
    'chain_stopped': pyTruthy(terminated),
  };
}

/// Port of core.evidence.semantic_truth_limit_engine.semantic_truth_limits.
Map<String, dynamic> semanticTruthLimits(
    Map<dynamic, dynamic> entropy, Map<dynamic, dynamic> instability) {
  return <String, dynamic>{
    'stabilization_allowed':
        pyGet(entropy, 'suppress_stabilization', false) != true,
    'coherence_allowed': pyGet(entropy, 'suppress_coherence', false) != true,
    'instability_preserved': pyGet(instability, 'preserved', true),
  };
}

/// Port of core.evidence.semantic_uniformity_engine.detect_semantic_uniformity.
Map<String, dynamic> detectSemanticUniformity(List<dynamic> keys, int depth) {
  final uniform = <dynamic>{...keys}.length <= 1 && depth >= 2;
  return <String, dynamic>{
    'uniformity_detected': uniform,
    'suppress': uniform,
  };
}

/// Port of core.evidence.unsupported_expansion_engine.detect_unsupported_expansion.
Map<String, dynamic> detectUnsupportedExpansion(
    List<dynamic> evidence, String expansionType, int count) {
  final suppressed = count > 0 && evidence.length < 2;
  return <String, dynamic>{
    'expansion_type': expansionType,
    'count': count,
    'suppressed': suppressed,
    'unsupported_expansions': suppressed
        ? <String>[for (var i = 0; i < count; i++) '$expansionType:$i']
        : <String>[],
    'reason': suppressed ? 'insufficient_evidence' : 'allowed',
  };
}

/// Port of core.evidence.unsupported_scope_engine.model_unsupported_scope.
Map<String, dynamic> modelUnsupportedScope(List<dynamic>? dimensions) {
  final dims = <String>{
    for (final d in dimensions ?? const <dynamic>[])
      if (pyTruthy(d)) pyToStr(d)
  }.toList()
    ..sort();
  return <String, dynamic>{
    'dimensions': dims,
    'scope_unsupported': pyTruthy(dims),
    'count': dims.length,
  };
}
