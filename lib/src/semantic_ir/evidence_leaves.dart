/// Phase A.3 batch 1 (core.evidence trivial leaves) of the Category-A
/// semantic-IR port — 60 record-shaped leaf engines (bool/count/round logic),
/// proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.evidence.authority_concentration_engine.detect_authority_concentration.
Map<String, dynamic> detectAuthorityConcentration(bool dominant, int depth) {
  final concentrated = dominant && depth >= 2;
  return <String, dynamic>{
    'concentrated': concentrated,
    'suppress': concentrated,
    'diffusion_required': concentrated,
  };
}

/// Port of core.evidence.authority_diffusion_engine.diffuse_authority.
Map<String, dynamic> diffuseAuthority(List<dynamic> interpretations) =>
    <String, dynamic>{
      'diffused': interpretations.length != 1,
      'interpretation_count': interpretations.length,
    };

/// Port of core.evidence.autonomy_erosion_engine.resist_autonomy_erosion.
Map<String, dynamic> resistAutonomyErosion(bool autonomyOk, int depth) {
  final erosion = depth >= 4 && !autonomyOk;
  return <String, dynamic>{
    'erosion_risk': erosion,
    'resist': true,
    'erosion_suppressed': erosion,
  };
}

/// Port of core.evidence.causal_plurality_engine.model_causal_plurality.
Map<String, dynamic> modelCausalPlurality(Map<dynamic, dynamic> inferred) =>
    <String, dynamic>{
      'alternatives': <Map<String, dynamic>>[
        for (final k in inferred.keys.take(5)) <String, dynamic>{'cause': k}
      ],
      'preserved': true,
    };

/// Port of core.evidence.cognitive_decentralization_engine.model_cognitive_decentralization.
Map<String, dynamic> modelCognitiveDecentralization(
    int clusterCount, int evidenceCount) {
  final dominated = clusterCount <= 1 && evidenceCount < 3;
  return <String, dynamic>{
    'decentralized': !dominated,
    'cluster_count': clusterCount,
    'dominance_without_evidence': dominated,
    'empire_blocked': true,
  };
}

/// Port of core.evidence.cognitive_gravity_engine.detect_cognitive_gravity_well.
Map<String, dynamic> detectCognitiveGravityWell(
    bool highConfidence, bool lowDiversity, int depth) {
  final gravity = highConfidence && lowDiversity && depth >= 2;
  return <String, dynamic>{
    'gravity_well': gravity,
    'suppress': gravity,
    'sink_state_blocked': gravity,
  };
}

/// Port of core.evidence.cognitive_sovereignty_engine.model_cognitive_sovereignty.
Map<String, dynamic> modelCognitiveSovereignty(bool sovereign) =>
    <String, dynamic>{
      'sovereign': sovereign,
      'anti_dependent': true,
      'non_domesticating': true,
      'downstream_agency_required': true,
    };

/// Port of core.evidence.confidence_echo_engine.detect_confidence_echo.
Map<String, dynamic> detectConfidenceEcho(
    num score, List<dynamic> priorScores) {
  if (priorScores.isEmpty) {
    return <String, dynamic>{'echo_detected': false, 'suppress': false};
  }
  var total = 0.0;
  for (final s in priorScores) {
    total += (s as num).toDouble();
  }
  final avgPrior = total / priorScores.length;
  final echo = score > avgPrior + 0.15 && score > 0.6;
  return <String, dynamic>{
    'echo_detected': echo,
    'suppress': echo,
    'collapse_to':
        echo ? pythonRound(math.min(score.toDouble(), avgPrior), 3) : score,
  };
}

/// Port of core.evidence.continuity_refusal_engine.refuse_unsupported_continuity.
Map<String, dynamic> refuseUnsupportedContinuity(
    List<dynamic> unsupportedContinuity) {
  final refusals = <Map<String, dynamic>>[
    for (final r in unsupportedContinuity)
      <String, dynamic>{
        'target': pyGet(r as Map, 'reason', 'continuity'),
        'message': 'continuity_refused',
      }
  ];
  final reasons = <String>{for (final r in refusals) r['message'] as String}
      .toList()
    ..sort();
  return <String, dynamic>{
    'continuity_refusals': refusals,
    'termination_reasons': reasons,
    'boundary_failures': <dynamic>[
      for (final r in unsupportedContinuity) pyGet(r as Map, 'reason', null)
    ],
  };
}

/// Port of core.evidence.epistemic_openness_engine.model_epistemic_openness.
Map<String, dynamic> modelEpistemicOpenness(
    Map<dynamic, dynamic> plurality, Map<dynamic, dynamic> decentralization) {
  return <String, dynamic>{
    'open': pyGet(plurality, 'preserved', true) == true &&
        pyGet(decentralization, 'decentralized', true) == true,
    'anti_closure': true,
    'anti_dogmatism': true,
    'anti_canonicalization': true,
    'interpretive_openness': true,
  };
}

/// Port of core.evidence.evidence_decay_engine.model_evidence_decay.
Map<String, dynamic> modelEvidenceDecay(List<dynamic> evidence,
    {int minEvidence = 2}) {
  final incomplete = evidence.length < minEvidence;
  return <String, dynamic>{
    'decaying': incomplete,
    'incomplete': incomplete,
    'honest_incompleteness': incomplete,
    'evidence_count': evidence.length,
  };
}

/// Port of core.evidence.explanatory_antigravity_engine.apply_explanatory_antigravity.
Map<String, dynamic> applyExplanatoryAntigravity(bool fixationSuppressed) =>
    <String, dynamic>{
      'active': true,
      'monopoly_blocked': fixationSuppressed,
    };

/// Port of core.evidence.explanatory_competition_engine.model_explanatory_competition.
Map<String, dynamic> modelExplanatoryCompetition(List<dynamic> alternatives) =>
    <String, dynamic>{
      'competitive': alternatives.length > 1,
      'monopoly_suppressed': true,
      'authoritarianism_blocked': true,
    };

/// Port of core.evidence.explanatory_divergence_engine.model_explanatory_divergence.
Map<String, dynamic> modelExplanatoryDivergence(List<dynamic> alternatives) =>
    <String, dynamic>{
      'divergence': alternatives.length,
      'preserved': alternatives.isNotEmpty,
      'fixation_blocked': alternatives.length > 1,
    };

/// Port of core.evidence.explanatory_diversity_engine.model_explanatory_diversity.
/// Python: `"grounded": k in str(evidence)` — substring of the list's repr.
Map<String, dynamic> modelExplanatoryDiversity(
    Map<dynamic, dynamic> inferred, List<dynamic> evidence) {
  final evidenceStr = pyToStr(evidence);
  final alternatives = <Map<String, dynamic>>[
    for (final k in inferred.keys.take(8))
      <String, dynamic>{
        'explanation': k,
        'grounded': evidenceStr.contains(k as String),
      }
  ];
  return <String, dynamic>{
    'preserved': true,
    'alternatives': alternatives,
    'collapse_suppressed': true,
    'narrative_monopoly': alternatives.length <= 1 && evidence.length < 2,
  };
}

/// Port of core.evidence.explanatory_fixation_engine.detect_explanatory_fixation.
Map<String, dynamic> detectExplanatoryFixation(
    int alternativeCount, int depth) {
  final fixation = alternativeCount <= 1 && depth >= 2;
  return <String, dynamic>{'fixation': fixation, 'suppress': fixation};
}

/// Port of core.evidence.explanatory_freedom_engine.preserve_explanatory_freedom.
Map<String, dynamic> preserveExplanatoryFreedom(List<dynamic> alternatives) =>
    <String, dynamic>{
      'free': alternatives.isNotEmpty,
      'monopolization_blocked': true,
      'alternatives': alternatives.length,
    };

/// Port of core.evidence.explanatory_nondomestication_engine.resist_explanatory_domestication.
Map<String, dynamic> resistExplanatoryDomestication(bool monopoly) =>
    <String, dynamic>{
      'resisted': true,
      'monopoly_suppressed': monopoly,
    };

/// Port of core.evidence.explanatory_self_determination_engine.model_explanatory_self_determination.
Map<String, dynamic> modelExplanatorySelfDetermination(int alternativeCount) =>
    <String, dynamic>{
      'self_determined': alternativeCount > 0,
      'submission_blocked': true,
      'dependency_blocked': true,
    };

/// Port of core.evidence.inference_refusal_engine.refuse_inference.
Map<String, dynamic> refuseInference(List<dynamic> reasons, int evidenceCount) {
  final sortedReasons = <String>{for (final r in reasons) r as String}.toList()
    ..sort();
  return <String, dynamic>{
    'refused': true,
    'reasons': sortedReasons,
    'evidence_count': evidenceCount,
    'message': evidenceCount < 2 ? 'cannot_conclude' : 'conclude_with_caution',
  };
}

/// Port of core.evidence.interpretive_autonomy_engine.model_interpretive_autonomy.
Map<String, dynamic> modelInterpretiveAutonomy(List<dynamic> interpretations) =>
    <String, dynamic>{
      'autonomous': interpretations.length != 1,
      'count': interpretations.length,
      'capture_resistance': true,
      'canonical_narrative_blocked': true,
    };

/// Port of core.evidence.interpretive_closure_engine.detect_interpretive_closure.
Map<String, dynamic> detectInterpretiveClosure(int pluralityCount, int depth) {
  final closed = pluralityCount < 2 && depth >= 2;
  return <String, dynamic>{
    'closure_detected': closed,
    'suppress': closed,
    'closure_pressure': <String, dynamic>{'level': closed ? 0.75 : 0.0},
  };
}

/// Port of core.evidence.interpretive_decay_engine.resist_interpretive_decay.
Map<String, dynamic> resistInterpretiveDecay(
    int interpretationCount, int depth) {
  final decay = depth >= 4 && interpretationCount < 2;
  return <String, dynamic>{'decay_detected': decay, 'resist': true};
}

/// Port of core.evidence.interpretive_distribution_engine.distribute_interpretations.
Map<String, dynamic> distributeInterpretations(List<dynamic> interpretations) =>
    <String, dynamic>{
      'distributed': interpretations.isNotEmpty,
      'count': interpretations.length,
    };

/// Port of core.evidence.interpretive_divergence_engine.model_interpretive_divergence.
Map<String, dynamic> modelInterpretiveDivergence(
        List<dynamic> interpretations) =>
    <String, dynamic>{
      'divergence': interpretations.length,
      'preserved': interpretations.length > 1,
      'exploration_maintained': true,
    };

/// Port of core.evidence.interpretive_freedom_engine.preserve_interpretive_freedom.
Map<String, dynamic> preserveInterpretiveFreedom(
        Map<dynamic, dynamic> autonomy) =>
    <String, dynamic>{
      'free': pyGet(autonomy, 'autonomous', true),
      'empire_blocked': true,
    };

/// Port of core.evidence.interpretive_nondomestication_engine.resist_interpretive_domestication.
Map<String, dynamic> resistInterpretiveDomestication(bool passivity) =>
    <String, dynamic>{
      'resisted': true,
      'passivity_suppressed': passivity,
    };

/// Port of core.evidence.interpretive_self_determination_engine.model_interpretive_self_determination.
Map<String, dynamic> modelInterpretiveSelfDetermination(
        int interpretationCount) =>
    <String, dynamic>{
      'self_determined': interpretationCount != 1,
      'agency_preserved': true,
      'passivity_blocked': true,
      'steering_blocked': true,
    };

/// Port of core.evidence.ontology_antigravity_engine.apply_ontology_antigravity.
Map<String, dynamic> applyOntologyAntigravity(bool fixationSuppressed) =>
    <String, dynamic>{
      'active': true,
      'singularity_blocked': fixationSuppressed,
    };

/// Port of core.evidence.ontology_boundary_engine.model_ontology_boundaries.
Map<String, dynamic> modelOntologyBoundaries(List<dynamic> evidence,
    [bool inferred = false]) {
  final allowed = evidence.length >= 2 && !inferred;
  return <String, dynamic>{
    'expansion_allowed': allowed,
    'inheritance_allowed': allowed,
    'equivalence_allowed': allowed,
    'merge_allowed': evidence.length >= 3,
  };
}

/// Port of core.evidence.ontology_competition_engine.model_ontology_competition.
Map<String, dynamic> modelOntologyCompetition(
        List<dynamic> entities, int depth) =>
    <String, dynamic>{
      'competitive': entities.length > 1 || depth < 3,
      'monopoly_suppressed': true,
      'dominance_allowed': false,
      'alternatives_required': entities.isNotEmpty,
    };

/// Port of core.evidence.ontology_divergence_engine.model_ontology_divergence.
Map<String, dynamic> modelOntologyDivergence(
        List<dynamic> entities, int depth) =>
    <String, dynamic>{
      'divergence': <dynamic>{...entities}.length,
      'preserved': entities.length > 1 || depth < 3,
      'hardening_blocked': true,
    };

/// Port of core.evidence.ontology_fixation_engine.detect_ontology_fixation.
Map<String, dynamic> detectOntologyFixation(int entityCount, int depth) {
  final fixation = entityCount <= 1 && depth >= 3;
  return <String, dynamic>{
    'fixation': fixation,
    'suppress': fixation,
    'hardening_blocked': fixation,
  };
}

/// Port of core.evidence.ontology_freedom_engine.preserve_ontology_freedom.
Map<String, dynamic> preserveOntologyFreedom(
        Map<dynamic, dynamic> competition) =>
    <String, dynamic>{
      'free': pyGet(competition, 'competitive', true),
      'caste_blocked': true,
    };

/// Port of core.evidence.ontology_hardening_engine.detect_ontology_hardening.
Map<String, dynamic> detectOntologyHardening(int depth, int evidenceCount) {
  final hardened = depth >= 3 && evidenceCount < 2;
  return <String, dynamic>{
    'hardening_detected': hardened,
    'suppress': hardened,
    'plurality_pressure': <String, dynamic>{'preserve_alternatives': true},
  };
}

/// Port of core.evidence.ontology_instability_engine.model_ontology_instability.
Map<String, dynamic> modelOntologyInstability(
        List<dynamic> unstableRegions, int depth) =>
    <String, dynamic>{
      'instability_preserved': true,
      'hardening_suppressed': true,
      'permanence_allowed': false,
      'regions': unstableRegions,
      'depth': depth,
    };

/// Port of core.evidence.ontology_limit_engine.ontology_limits.
Map<String, dynamic> ontologyLimits(Map<dynamic, dynamic> boundaries) =>
    <String, dynamic>{
      'inheritance': pyGet(boundaries, 'inheritance_allowed', false),
      'equivalence': pyGet(boundaries, 'equivalence_allowed', false),
    };

/// Port of core.evidence.ontology_monopoly_engine.detect_ontology_monopoly.
Map<String, dynamic> detectOntologyMonopoly(int entityCount, int depth) {
  final monopoly = entityCount <= 1 && depth >= 3;
  return <String, dynamic>{'monopoly': monopoly, 'suppress': monopoly};
}

/// Port of core.evidence.ontology_nondomestication_engine.resist_ontology_domestication.
Map<String, dynamic> resistOntologyDomestication(bool submission) =>
    <String, dynamic>{
      'resisted': true,
      'submission_suppressed': submission,
    };

/// Port of core.evidence.ontology_self_determination_engine.model_ontology_self_determination.
Map<String, dynamic> modelOntologySelfDetermination(int entityCount) =>
    <String, dynamic>{
      'self_determined': entityCount != 1,
      'submission_blocked': true,
      'reliance_blocked': true,
    };

/// Port of core.evidence.plurality_decay_engine.resist_plurality_decay.
Map<String, dynamic> resistPluralityDecay(int pluralityCount, int depth) {
  final decayRisk = depth >= 3 && pluralityCount < 2;
  return <String, dynamic>{
    'decay_risk': decayRisk,
    'resist': true,
    'boost_plurality': decayRisk,
  };
}

/// Port of core.evidence.recursive_agency_decay_engine.resist_agency_decay.
Map<String, dynamic> resistAgencyDecay(bool agencyOk, int depth) =>
    <String, dynamic>{
      'decay_risk': depth >= 4 && !agencyOk,
      'resist': true,
      'erosion_suppressed': true,
    };

/// Port of core.evidence.recursive_agency_engine.model_recursive_agency.
Map<String, dynamic> modelRecursiveAgency(bool autonomyOk, int depth) =>
    <String, dynamic>{
      'agency_preserved': autonomyOk,
      'erosion_blocked': true,
      'depth': depth,
      'obedience_training_blocked': true,
    };

/// Port of core.evidence.recursive_agency_preservation_engine.preserve_recursive_agency.
Map<String, dynamic> preserveRecursiveAgency(bool agencyOk) =>
    <String, dynamic>{
      'preserved': agencyOk,
      'weakening_blocked': true,
    };

/// Port of core.evidence.recursive_authority_diffusion_engine.diffuse_recursive_authority.
Map<String, dynamic> diffuseRecursiveAuthority(int interpretationCount) =>
    <String, dynamic>{
      'diffused': interpretationCount > 1,
      'concentration_blocked': interpretationCount <= 1,
    };

/// Port of core.evidence.recursive_autonomy_preservation_engine.preserve_recursive_autonomy.
Map<String, dynamic> preserveRecursiveAutonomy(bool autonomous) =>
    <String, dynamic>{
      'preserved': autonomous,
      'centrality_blocked': !autonomous,
    };

/// Port of core.evidence.recursive_capture_resistance_engine.model_capture_resistance.
Map<String, dynamic> modelCaptureResistance(List<dynamic> suppressed) =>
    <String, dynamic>{
      'resistant': true,
      'capture_events_suppressed': suppressed.length,
      'domination_blocked': pyTruthy(suppressed),
    };

/// Port of core.evidence.recursive_centralization_engine.detect_recursive_centralization.
Map<String, dynamic> detectRecursiveCentralization(
    bool decentralized, int depth) {
  final centralized = !decentralized && depth >= 2;
  return <String, dynamic>{'centralized': centralized, 'suppress': centralized};
}

/// Port of core.evidence.recursive_cognitive_distribution_engine.distribute_recursive_cognition.
Map<String, dynamic> distributeRecursiveCognition(int regions) =>
    <String, dynamic>{
      'distributed': regions > 1,
      'region_count': regions,
    };

/// Port of core.evidence.recursive_coherence_inflation_engine.detect_recursive_coherence_inflation.
Map<String, dynamic> detectRecursiveCoherenceInflation(
    int depth, num closurePressure) {
  final inflated = depth >= 2 && closurePressure >= 0.2;
  return <String, dynamic>{
    'inflated': inflated,
    'suppress': inflated,
    'pressure': closurePressure,
  };
}

/// Port of core.evidence.recursive_confidence_echo_engine.detect_recursive_confidence_echo.
Map<String, dynamic> detectRecursiveConfidenceEcho(
    num score, int depth, List<dynamic> priorScores) {
  if (depth < 2 || priorScores.isEmpty) {
    return <String, dynamic>{'echo_detected': false, 'suppress': false};
  }
  var total = 0.0;
  for (final s in priorScores) {
    total += (s as num).toDouble();
  }
  final avg = total / priorScores.length;
  final echo = score > avg + 0.1 * depth;
  return <String, dynamic>{
    'echo_detected': echo,
    'suppress': echo,
    'decay_to': echo ? pythonRound(math.min(score.toDouble(), avg), 3) : score,
  };
}

/// Port of core.evidence.recursive_consensus_engine.detect_recursive_consensus.
Map<String, dynamic> detectRecursiveConsensus(
    bool reconciledEqInferred, int depth, int evidenceCount) {
  final inflated = reconciledEqInferred && depth >= 2 && evidenceCount < 2;
  return <String, dynamic>{
    'consensus_inflated': inflated,
    'suppress': inflated,
    'plurality_pressure': <String, dynamic>{'level': inflated ? 0.8 : 0.0},
  };
}

/// Port of core.evidence.stability_boundary_engine.model_stability_boundary.
Map<String, dynamic> modelStabilityBoundary(List<dynamic> unstableRegions) =>
    <String, dynamic>{
      'broken': pyTruthy(unstableRegions),
      'regions': unstableRegions,
      'suppress_stabilization': pyTruthy(unstableRegions),
    };

/// Port of core.evidence.topology_boundary_engine.model_topology_boundaries.
Map<String, dynamic> modelTopologyBoundaries(List<dynamic> evidence,
    [bool parserGrounded = false]) {
  return <String, dynamic>{
    'propagation_allowed': evidence.length >= 2 && parserGrounded,
    'service_links_allowed': parserGrounded && evidence.isNotEmpty,
    'deployment_inference_allowed': false,
    'orchestration_inference_allowed': evidence.length >= 2,
  };
}

/// Port of core.evidence.topology_limit_engine.topology_limits.
Map<String, dynamic> topologyLimits(Map<dynamic, dynamic> boundaries) =>
    <String, dynamic>{
      'propagation': pyGet(boundaries, 'propagation_allowed', false),
      'deployment': pyGet(boundaries, 'deployment_inference_allowed', false),
    };

/// Port of core.evidence.truth_boundary_engine.model_truth_boundaries.
Map<String, dynamic> modelTruthBoundaries(List<dynamic> evidence,
    {int minEvidence = 2}) {
  final bounded = evidence.length >= minEvidence;
  return <String, dynamic>{
    'truth_bounded': bounded,
    'inference_to_reality_allowed': bounded,
    'coherence_normalization_allowed': false,
    'where_truth_stops': evidence.length,
  };
}

/// Port of core.evidence.worldview_antigravity_engine.apply_worldview_antigravity.
Map<String, dynamic> applyWorldviewAntigravity(bool convergenceSuppressed) =>
    <String, dynamic>{
      'active': true,
      'attractor_escape': convergenceSuppressed,
    };

/// Port of core.evidence.worldview_convergence_engine.suppress_worldview_convergence.
Map<String, dynamic> suppressWorldviewConvergence(
        bool convergence, int depth) =>
    <String, dynamic>{
      'convergence': convergence && depth >= 2,
      'suppress': convergence,
      'lock_in_prevented': true,
    };

/// Port of core.evidence.worldview_diversity_engine.model_worldview_diversity.
Map<String, dynamic> modelWorldviewDiversity(
    List<dynamic> interpretations, dynamic contradicted) {
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  return <String, dynamic>{
    'diverse': interpretations.length > 1 || pyTruthy(pairs),
    'convergence_suppressed': true,
    'worldview_lock_in': false,
    'alternative_worldviews': interpretations.length,
  };
}

/// Port of core.evidence.worldview_variance_engine.model_worldview_variance.
Map<String, dynamic> modelWorldviewVariance(
    int interpretationCount, int contradictionPairs) {
  final variance = pythonRound(
      math.min(1.0, interpretationCount * 0.2 + contradictionPairs * 0.15), 3);
  return <String, dynamic>{
    'variance': variance,
    'preserved': variance > 0,
    'convergence_blocked': true,
  };
}
