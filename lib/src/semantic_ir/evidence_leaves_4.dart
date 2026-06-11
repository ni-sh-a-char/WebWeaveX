/// Phase A.3 batch 4 (final core.evidence public leaves) of the Category-A
/// semantic-IR port — the 25 semantic_* heavy engines (confidence scoring,
/// conservatism, drift, fragility, stability, uncertainty, refusal),
/// proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.evidence.recursive_divergence_preservation_engine.preserve_recursive_divergence.
Map<String, dynamic> preserveRecursiveDivergence(num divergenceScore) =>
    <String, dynamic>{
      'preserved': divergenceScore > 0,
      'collapse_blocked': true,
    };

/// Port of core.evidence.recursive_domestication_engine.detect_recursive_domestication.
Map<String, dynamic> detectRecursiveDomestication(bool passive, int depth) {
  final domesticated = passive && depth >= 3;
  return <String, dynamic>{
    'domesticated': domesticated,
    'suppress': domesticated,
  };
}

/// Port of core.evidence.semantic_confidence_engine.score_semantic_confidence.
/// Float accumulation happens in Python's exact order: 0.2 base, +0.12 per
/// truthy parser flag (flags sorted by key), +min(0.25, edges*0.01), +0.05
/// per extra evidence item.
Map<String, dynamic> scoreSemanticConfidence(
    [dynamic parsed, dynamic graph, List<dynamic>? extraEvidence]) {
  final inputs = <String>[];
  final evidence = <String>[];
  var score = 0.2;
  if (parsed is Map) {
    final flags = pyGet(parsed, 'evidence', <dynamic, dynamic>{});
    if (flags is Map) {
      final keys = <String>[for (final k in flags.keys) k as String]..sort();
      for (final key in keys) {
        final val = flags[key];
        inputs.add('parser.$key=${pyTruthy(val) ? 'True' : 'False'}');
        if (pyTruthy(val)) {
          evidence.add('parser:$key');
          score += 0.12;
        }
      }
    }
  }
  var graphEdgeCount = 0;
  if (graph is Map) {
    dynamic nodes = pyGet(graph, 'nodes', <dynamic>[]);
    if (!pyTruthy(nodes)) nodes = <dynamic>[];
    dynamic edges = pyGet(graph, 'edges', <dynamic>[]);
    if (!pyTruthy(edges)) edges = <dynamic>[];
    inputs.add('graph.nodes=${(nodes as List).length}');
    inputs.add('graph.edges=${(edges as List).length}');
    if (pyTruthy(edges)) {
      evidence.add('graph:edges');
      score += math.min(0.25, edges.length * 0.01);
    }
  }
  for (final e in extraEvidence ?? const <dynamic>[]) {
    evidence.add(pyToStr(e));
    score += 0.05;
  }
  final finalScore = pythonRound(math.min(1.0, math.max(0.0, score)), 3);
  if (pyTruthy(graph)) {
    dynamic ge = pyGet(graph as Map, 'edges', <dynamic>[]);
    if (!pyTruthy(ge)) ge = <dynamic>[];
    graphEdgeCount = (ge as List).length;
  }
  return <String, dynamic>{
    'score': finalScore,
    'basis': <String, dynamic>{
      'parser_density':
          evidence.where((e) => e.startsWith('parser:')).length,
      'graph_edges': graphEdgeCount,
    },
    'evidence': evidence.toSet().toList()..sort(),
    'deterministic_inputs': inputs.toList()..sort(),
  };
}

/// Port of core.evidence.semantic_conservatism_engine.apply_semantic_conservatism.
/// Python mutates and returns the bundle — here a copy is mutated.
Map<String, dynamic> applySemanticConservatism(Map<dynamic, dynamic> bundle,
    [int minEvidence = 2]) {
  final out = <String, dynamic>{
    for (final e in bundle.entries) e.key as String: e.value
  };
  dynamic evidence = pyGet(out, 'evidence', <dynamic>[]);
  if (!pyTruthy(evidence)) evidence = <dynamic>[];
  dynamic ambSrc = pyGet(out, 'ambiguities', <dynamic>[]);
  if (!pyTruthy(ambSrc)) ambSrc = <dynamic>[];
  final ambiguities = List<dynamic>.from(ambSrc as List);
  dynamic contradicted = pyGet(out, 'contradicted', <dynamic, dynamic>{});
  if (!pyTruthy(contradicted)) contradicted = <dynamic, dynamic>{};
  if ((evidence as List).length < minEvidence) {
    ambiguities.add('weak_evidence');
  }
  final preserved = pyGet(contradicted as Map, 'preserved', null);
  if (pyTruthy(preserved) || pyTruthy(pyGet(contradicted, 'pairs', null))) {
    ambiguities.add('unresolved_contradiction');
  }
  dynamic confSrc = pyGet(out, 'confidence_basis', <dynamic, dynamic>{});
  if (!pyTruthy(confSrc)) confSrc = <dynamic, dynamic>{};
  final confidence = <String, dynamic>{
    for (final e in (confSrc as Map).entries) e.key as String: e.value
  };
  var score = (pyGet(confidence, 'score', 0.5) as num).toDouble();
  if (evidence.length < minEvidence) {
    score = pythonRound(math.min(score, 0.35), 3);
  }
  if (pyTruthy(preserved)) {
    score = pythonRound(math.min(score, 0.45), 3);
  }
  confidence['score'] = score;
  confidence['conservative'] = true;
  dynamic detSrc = pyGet(confidence, 'deterministic_inputs', <dynamic>[]);
  if (!pyTruthy(detSrc)) detSrc = <dynamic>[];
  confidence['deterministic_inputs'] = <String>{
    for (final d in detSrc as List) d as String,
    'evidence_count=${evidence.length}',
  }.toList()
    ..sort();
  out['ambiguities'] = <String>{
    for (final a in ambiguities)
      if (pyTruthy(a)) pyToStr(a)
  }.toList()
    ..sort();
  out['confidence_basis'] = confidence;
  final semanticBasis = pyGet(out, 'semantic_basis', null);
  if (pyTruthy(semanticBasis)) {
    out['semantic_basis'] = <String, dynamic>{
      for (final e in (semanticBasis as Map).entries) e.key as String: e.value,
      'conservative_score': score,
    };
  }
  return out;
}

/// Port of core.evidence.semantic_consistency_engine.assess_semantic_consistency.
Map<String, dynamic> assessSemanticConsistency(Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final ko = observed.keys.toSet();
  final ki = inferred.keys.toSet();
  final kr = reconciled.keys.toSet();
  final overlapOi = ko.intersection(ki).length;
  final overlapOr = ko.intersection(kr).length;
  final total = math.max(1, ko.union(ki).union(kr).length);
  final score = pythonRound((overlapOi + overlapOr) / (2 * total), 3);
  final consistent = score >= 0.5 || !pyTruthy(inferred);
  return <String, dynamic>{
    'consistent': consistent,
    'consistency_score': score,
    'overlap_observed_inferred': overlapOi,
    'overlap_observed_reconciled': overlapOr,
    'deterministic_inputs': <String>[
      'score=${pyFloatStr(score)}',
      'keys_total=$total'
    ],
  };
}

/// Port of core.evidence.semantic_decay_engine.model_semantic_decay.
Map<String, dynamic> modelSemanticDecay(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, int stabilizationCount) {
  final decayRate = pythonRound(
      math.min(
          1.0,
          (inferred.length / math.max(1, evidence.length + 1)) * 0.2 +
              stabilizationCount * 0.15),
      3);
  return <String, dynamic>{
    'decaying': decayRate > 0,
    'decay_rate': decayRate,
    'destabilize_unsupported': evidence.length < 2,
    'prefer_incomplete': true,
  };
}

/// Port of core.evidence.semantic_decentralization_engine.model_semantic_decentralization.
Map<String, dynamic> modelSemanticDecentralization(
    List<dynamic> interpretations, int evidenceCount) {
  final dominant = interpretations.length == 1 && evidenceCount < 2;
  return <String, dynamic>{
    'decentralized': !dominant,
    'authority_diffused': interpretations.length > 1 || evidenceCount >= 2,
    'hierarchy_lock_in': false,
    'single_interpretation_dominance': dominant,
  };
}

/// Port of core.evidence.semantic_drift_engine.detect_semantic_drift.
Map<String, dynamic> detectSemanticDrift(
    Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred,
    Map<dynamic, dynamic> reconciled,
    List<dynamic> evidence) {
  final driftKeys = <String>[];
  if (pyTruthy(inferred) && !pyTruthy(observed)) {
    driftKeys.add('inferred_without_observation');
  }
  if (!pyDeepEq(reconciled, observed) && evidence.length < 2) {
    driftKeys.add('reconcile_drift');
  }
  for (final k in inferred.keys) {
    if (!observed.containsKey(k) && !reconciled.containsKey(k)) {
      driftKeys.add('drift:$k');
    }
  }
  final pressure = pythonRound(math.min(1.0, driftKeys.length * 0.2), 3);
  return <String, dynamic>{
    'drift_detected': pyTruthy(driftKeys),
    'drift_keys': driftKeys.toSet().toList()..sort(),
    'drift_pressure': pressure,
    'suppress_continuation': pressure >= 0.2,
  };
}

/// Port of core.evidence.semantic_entropy_engine.model_semantic_entropy.
Map<String, dynamic> modelSemanticEntropy(List<dynamic> ambiguities,
    List<dynamic> uncertainties, dynamic contradicted) {
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  final entropy = pythonRound(
      math.min(
          1.0,
          ambiguities.length * 0.1 +
              uncertainties.length * 0.08 +
              (pairs as List).length * 0.15),
      3);
  return <String, dynamic>{
    'entropy': entropy,
    'visible': entropy > 0,
    'suppress_stabilization': entropy >= 0.2,
    'suppress_coherence': entropy >= 0.15,
    'preserved': true,
  };
}

/// Port of core.evidence.semantic_fragility_engine.model_fragility.
Map<String, dynamic> modelFragility(
    List<dynamic> evidence, List<dynamic> ambiguities,
    [int contradictionCount = 0, int parserDensity = 0]) {
  final missing = <String>[];
  if (evidence.length < 2) missing.add('low_evidence_density');
  if (parserDensity == 0) missing.add('no_parser_grounding');
  final pressure = contradictionCount != 0
      ? <String>['contradiction:$contradictionCount']
      : <String>[];
  String level;
  num cap;
  if (evidence.length >= 3 && ambiguities.isEmpty && contradictionCount == 0) {
    level = 'low';
    cap = 0.85;
  } else if (evidence.isNotEmpty) {
    level = 'medium';
    cap = 0.55;
  } else {
    level = 'high';
    cap = 0.35;
  }
  if (pyTruthy(ambiguities)) {
    level = level == 'medium' ? 'high' : level;
    cap = pythonRound(math.min(cap.toDouble(), 0.45), 3);
  }
  return <String, dynamic>{
    'level': level,
    'basis': <String, dynamic>{
      'evidence_count': evidence.length,
      'ambiguity_count': ambiguities.length,
      'parser_density': parserDensity,
    },
    'missing_support': missing.toSet().toList()..sort(),
    'contradiction_pressure': pressure,
    'confidence_limits': <String, dynamic>{'max_score': cap},
  };
}

/// Port of core.evidence.semantic_honesty_engine.assess_semantic_honesty.
Map<String, dynamic> assessSemanticHonesty(
    List<dynamic> evidence,
    Map<dynamic, dynamic> supported,
    Map<dynamic, dynamic> unsupported,
    Map<dynamic, dynamic> fragile) {
  final honest = !pyTruthy(pyGet(unsupported, 'claims', null)) &&
      pyGet(fragile, 'level', null) != 'high';
  dynamic supportedKeys = pyGet(supported, 'keys', <dynamic>[]);
  if (!pyTruthy(supportedKeys)) supportedKeys = <dynamic>[];
  dynamic unsupportedClaims = pyGet(unsupported, 'claims', <dynamic>[]);
  if (!pyTruthy(unsupportedClaims)) unsupportedClaims = <dynamic>[];
  return <String, dynamic>{
    'honest': honest,
    'prefers_insufficient_over_certainty': true,
    'supported_claims': (supportedKeys as List).length,
    'unsupported_claims': (unsupportedClaims as List).length,
    'message': honest ? 'sufficient_honesty' : 'semantic_honesty_warning',
    'deterministic_inputs': <String>[
      'evidence=${evidence.length}',
      'fragility=${pyToStr(pyGet(fragile, 'level', 'unknown'))}',
    ],
  };
}

/// Port of core.evidence.semantic_incompleteness_engine.model_incompleteness.
Map<String, dynamic> modelIncompleteness(Map<dynamic, dynamic> known,
    List<dynamic>? unknown, List<dynamic>? unsupported) {
  List<String> sortedSet(List<dynamic>? xs) =>
      <String>{for (final x in (pyTruthy(xs) ? xs! : const <dynamic>[])) x as String}
          .toList()
        ..sort();
  return <String, dynamic>{
    'known': known,
    'unknown': sortedSet(unknown),
    'unsupported': sortedSet(unsupported),
    'incomplete': pyTruthy(unknown) || pyTruthy(unsupported),
    'preserved': true,
  };
}

/// Port of core.evidence.semantic_inference_calculus.infer_from_evidence.
Map<String, dynamic> inferFromEvidence(
    dynamic observed, List<dynamic> evidence,
    [int minEvidence = 1]) {
  final ev = <String>{
    for (final e in evidence)
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  final allowed = ev.length >= minEvidence;
  final src = pyTruthy(observed) ? observed as Map : const <dynamic, dynamic>{};
  final inferred = allowed
      ? <String, dynamic>{
          for (final e in src.entries) e.key as String: e.value
        }
      : <String, dynamic>{};
  return <String, dynamic>{
    'inferred': inferred,
    'allowed': allowed,
    'evidence_count': ev.length,
    'rule': 'inference_requires_evidence',
    'deterministic_inputs': <String>[
      'evidence_count=${ev.length}',
      'min=$minEvidence'
    ],
  };
}

/// Port of core.evidence.semantic_instability_engine.model_semantic_instability.
Map<String, dynamic> modelSemanticInstability(List<dynamic> unstableRegions,
    Map<dynamic, dynamic> entropy, List<dynamic> evidence) {
  final regions = List<dynamic>.from(unstableRegions);
  final entropyVal = pyGet(entropy, 'entropy', 0) as num;
  if (entropyVal >= 0.2) regions.add('semantic:entropy_instability');
  // Python: round(int + int, 3) stays int — preserve numeric type.
  final num rawPressure =
      entropyVal + (evidence.length < 2 ? 0.3 : 0);
  final num truthPressure =
      rawPressure is int ? rawPressure : pythonRound(rawPressure, 3);
  return <String, dynamic>{
    'unstable': pyTruthy(regions) || evidence.length < 2,
    'regions': <String>{for (final r in regions) r as String}.toList()..sort(),
    'truth_pressure': truthPressure,
    'preserved': true,
  };
}

/// Port of core.evidence.semantic_justification_engine.build_justification.
Map<String, dynamic> buildJustification(List<dynamic> evidence,
    dynamic lineage, Map<dynamic, dynamic> uncertainty, Map<dynamic, dynamic> entropy) {
  final stages =
      lineage is Map ? pyGet(lineage, 'stages', <dynamic>[]) : <dynamic>[];
  final steps = <dynamic>[
    for (final s in stages as List)
      if (s is Map) pyGet(s, 'stage', _pyStrOfMap(s))
  ];
  dynamic detSrc = pyGet(uncertainty, 'deterministic_inputs', <dynamic>[]);
  if (!pyTruthy(detSrc)) detSrc = <dynamic>[];
  final detInputs = <String>{
    'evidence_count=${evidence.length}',
    'stage_count=${steps.length}',
    for (final d in detSrc as List) d as String,
  }.toList()
    ..sort();
  return <String, dynamic>{
    'evidence': (<String>{
      for (final e in evidence)
        if (pyTruthy(e)) pyToStr(e)
    }.toList()
      ..sort()),
    'lineage_stages': steps,
    'uncertainty_basis': pyGet(uncertainty, 'deterministic_inputs',
        pyGet(uncertainty, 'factors', <dynamic>[])),
    'entropy': pyGet(entropy, 'entropy', 0),
    'explainable': true,
    'opaque': false,
    'deterministic_inputs': detInputs,
  };
}

String _pyStrOfMap(Map<dynamic, dynamic> m) => pyToStr(m);

/// Port of core.evidence.semantic_limit_engine.semantic_limits.
Map<String, dynamic> semanticLimits(int evidenceCount,
    List<dynamic> noninferableRegions, Map<dynamic, dynamic> selfLimitation) {
  return <String, dynamic>{
    'max_confidence_without_evidence': 0.45,
    'min_evidence_for_inference': 2,
    'noninferable_count': noninferableRegions.length,
    'expansion_allowed': pyGet(selfLimitation, 'expansion_allowed', false),
    'reconciliation_allowed':
        pyGet(selfLimitation, 'reconciliation_allowed', false),
  };
}

/// Port of core.evidence.semantic_overreach_engine.detect_semantic_overreach.
Map<String, dynamic> detectSemanticOverreach(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final overreach = <String>[];
  if (!pyDeepEq(reconciled, inferred) && evidence.length < 2) {
    overreach.add('reconciled_beyond_evidence');
  }
  if (inferred.isNotEmpty && evidence.length < 2) {
    overreach.add('inference_expansion');
  }
  if (pyTruthy(inferred) && evidence.isEmpty) {
    overreach.add('pure_heuristic_inference');
  }
  return <String, dynamic>{
    'overreach_detected': pyTruthy(overreach),
    'overreach_flags': overreach.toSet().toList()..sort(),
    'deterministic_inputs': <String>[
      'inferred_keys=${inferred.length}',
      'evidence=${evidence.length}'
    ],
  };
}

/// Port of core.evidence.semantic_plurality_engine.model_semantic_plurality.
Map<String, dynamic> modelSemanticPlurality(
    Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred,
    List<dynamic> ambiguities,
    dynamic contradicted) {
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  final altCount = observed.keys.toSet().union(inferred.keys.toSet()).length +
      ambiguities.length +
      (pairs as List).length;
  return <String, dynamic>{
    'preserved': true,
    'alternative_count': altCount,
    'unresolved': pyTruthy(ambiguities) || pyTruthy(pairs),
    'monoculture_risk': altCount < 2 && !pyTruthy(pairs),
  };
}

/// Port of core.evidence.semantic_proof_engine.prove_semantic_claim.
Map<String, dynamic> proveSemanticClaim(String claim, List<dynamic> evidence,
    [int minEvidence = 1]) {
  final ev = <String>{
    for (final e in evidence)
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  final proved = ev.length >= minEvidence;
  return <String, dynamic>{
    'claim': claim,
    'proved': proved,
    'evidence': ev,
    'steps': <Map<String, dynamic>>[
      <String, dynamic>{'rule': 'evidence_threshold', 'met': proved}
    ],
    'deterministic_inputs': <String>[
      'evidence=${ev.length}',
      'min=$minEvidence'
    ],
  };
}

/// Port of core.evidence.semantic_refusal_engine.refuse_unsupported_conclusions.
Map<String, dynamic> refuseUnsupportedConclusions(
    List<dynamic> noninferableRegions, List<dynamic> suppressedSpeculation) {
  final refusals = <Map<String, dynamic>>[
    for (final region in noninferableRegions)
      <String, dynamic>{'target': region, 'message': 'cannot_determine'},
    for (final spec in suppressedSpeculation)
      <String, dynamic>{
        'target': pyGet(spec as Map, 'reason', 'speculation'),
        'message': 'cannot_determine',
      },
  ];
  final reasons = <String>{for (final r in refusals) r['message'] as String}
      .toList()
    ..sort();
  return <String, dynamic>{
    'refusals': refusals,
    'terminated_inferences': <dynamic>[for (final r in refusals) r['target']],
    'termination_reasons': reasons,
    'unsupported_regions': noninferableRegions,
  };
}

/// Port of core.evidence.semantic_self_limitation_engine.apply_semantic_self_limitation.
Map<String, dynamic> applySemanticSelfLimitation(List<dynamic> evidence,
    List<dynamic> suppressedSpeculation, List<dynamic> noninferableRegions) {
  final limited = evidence.length < 2 ||
      pyTruthy(suppressedSpeculation) ||
      pyTruthy(noninferableRegions);
  final reasons = <String>{
    if (evidence.length < 2) 'insufficient_evidence',
    if (pyTruthy(suppressedSpeculation)) 'speculative_suppression',
    if (pyTruthy(noninferableRegions)) 'noninferable_regions',
  }.toList()
    ..sort();
  return <String, dynamic>{
    'active': limited,
    'prefer_cannot_determine': true,
    'propagation_allowed': !limited,
    'reconciliation_allowed': evidence.length >= 2,
    'expansion_allowed':
        evidence.length >= 2 && !pyTruthy(noninferableRegions),
    'limit_reasons': reasons,
  };
}

/// Port of core.evidence.semantic_stability_engine.model_semantic_stability.
Map<String, dynamic> modelSemanticStability(List<dynamic> evidence,
    num driftPressure, List<dynamic> unsupportedContinuity, bool parserGrounded) {
  final unstable = <String>[];
  if (driftPressure >= 0.2) unstable.add('semantic:drift');
  if (pyTruthy(unsupportedContinuity)) unstable.add('semantic:continuity');
  if (!parserGrounded) unstable.add('semantic:parser_gap');
  if (evidence.length < 2) unstable.add('semantic:insufficient_evidence');
  final stable = unstable.isEmpty;
  return <String, dynamic>{
    'stable': stable,
    'level': stable ? 'high' : (unstable.length >= 2 ? 'low' : 'medium'),
    'unstable_regions': unstable.toSet().toList()..sort(),
    'boundary_pressure':
        pythonRound(math.min(1.0, unstable.length * 0.25), 3),
    'stability_limits': <String, dynamic>{
      'max_confidence': stable ? 0.85 : 0.5
    },
  };
}

/// Port of core.evidence.stabilization_termination_engine.terminate_stabilization.
Map<String, dynamic> terminateStabilization(
    List<dynamic> suppressed, List<dynamic> unstableRegions) {
  final terminated = <dynamic>[
    for (final s in suppressed) pyGet(s as Map, 'reason', ''),
    ...unstableRegions,
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

/// Port of core.evidence.uncertainty_engine.model_uncertainty.
Map<String, dynamic> modelUncertainty(
    int evidenceCount, int ambiguityCount, int contradictionCount) {
  var uncertainty = pythonRound(
      math.min(
          1.0, 0.2 + ambiguityCount * 0.15 + contradictionCount * 0.2),
      3);
  if (evidenceCount < 2) {
    uncertainty = pythonRound(math.min(1.0, uncertainty + 0.3), 3);
  }
  final confidence = pythonRound(math.max(0.0, 1.0 - uncertainty), 3);
  return <String, dynamic>{
    'uncertainty_score': uncertainty,
    'confidence_score': confidence,
    'evidence_count': evidenceCount,
    'ambiguity_count': ambiguityCount,
    'contradiction_count': contradictionCount,
    'deterministic_inputs': <String>[
      'evidence=$evidenceCount',
      'ambiguity=$ambiguityCount',
      'contradiction=$contradictionCount',
    ],
  };
}

/// Port of core.evidence.uncertainty_visibility_engine.expose_uncertainty_visibility.
Map<String, dynamic> exposeUncertaintyVisibility(List<dynamic> uncertainties,
    List<dynamic> ambiguities, num confidenceScore) {
  final pressure = pythonRound(
      math.min(
          1.0, uncertainties.length * 0.15 + ambiguities.length * 0.1),
      3);
  return <String, dynamic>{
    'visible': pyTruthy(uncertainties) || pyTruthy(ambiguities),
    'count': uncertainties.length,
    'items': (<String>{for (final u in uncertainties) pyToStr(u)}.toList()
      ..sort()),
    'pressure': pressure,
    'suppress_propagation': pressure >= 0.3,
    'confidence_impact': pythonRound(math.min(0.35, pressure * 0.4), 3),
    'preserved': true,
  };
}

/// Port of core.evidence.unsupported_confidence_engine.block_unsupported_confidence_escalation.
Map<String, dynamic> blockUnsupportedConfidenceEscalation(
    num score, int evidenceCount,
    {int minEvidence = 2, double maxWithoutEvidence = 0.45}) {
  if (evidenceCount >= minEvidence) {
    return <String, dynamic>{
      'escalation_blocked': false,
      'capped_score': score,
      'reason': null,
    };
  }
  final capped = math.min(score.toDouble(), maxWithoutEvidence);
  return <String, dynamic>{
    'escalation_blocked': score > capped,
    'capped_score': pythonRound(capped, 3),
    'reason': 'unsupported_confidence_escalation',
    'evidence_count': evidenceCount,
  };
}

/// Port of core.evidence.unsupported_inference_engine.suppress_unsupported_inference.
Map<String, dynamic> suppressUnsupportedInference(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> observed,
    [int minEvidence = 2]) {
  final unsupportedDims = <String>[];
  var suppressed = <String>[];
  if (evidence.length < minEvidence && pyTruthy(inferred)) {
    unsupportedDims.add('inferred_without_evidence');
    suppressed = <String>[for (final k in inferred.keys) k as String]..sort();
  }
  if (pyTruthy(inferred) && !pyTruthy(observed)) {
    unsupportedDims.add('inferred_without_observation');
  }
  return <String, dynamic>{
    'suppressed': pyTruthy(suppressed),
    'unsupported_dimensions': unsupportedDims.toSet().toList()..sort(),
    'suppressed_keys': suppressed,
    'allowed_inference': evidence.length >= minEvidence,
  };
}
