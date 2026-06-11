/// Phase B (first non-leaf layer) of the Category-A semantic-IR port —
/// core.evidence engines whose only in-closure dependencies are Phase-A
/// leaves. Private record helpers (`_record`, `_closure_record`,
/// `_suppression_record`, `_continuation_record`, `_stabilization_record`)
/// are ported inside their parents, per the phase plan.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'evidence_leaves.dart'
    show modelOntologyBoundaries, modelTopologyBoundaries, refuseInference;
import 'evidence_leaves_2.dart'
    show
        assessEvidenceSufficiency,
        detectUnsupportedExpansion,
        modelEvidenceBoundaries,
        modelSemanticBoundaries,
        modelUnsupportedScope;
import 'evidence_leaves_3.dart'
    show
        applyConfidenceCaps,
        buildProvenance,
        buildSupport,
        buildWeaknesses,
        combineEvidence,
        modelNoninference;
import 'evidence_leaves_4.dart'
    show inferFromEvidence, modelIncompleteness, modelUncertainty;
import 'pressure_engines.dart' show computeContradictionPressure;
import 'py_compat.dart';

/// Port of core.evidence.confidence_degradation_engine
/// .apply_confidence_degradation (kw-only args become trailing positionals,
/// py2ts order).
Map<String, dynamic> applyConfidenceDegradation(
  num score,
  Map<dynamic, dynamic> fragility, [
  int contradictionCount = 0,
  int ambiguityCount = 0,
  int uncertaintyCount = 0,
  int unsupportedExpansionCount = 0,
  int speculationCount = 0,
  bool parserWeakness = false,
]) {
  final capped = applyConfidenceCaps(score, fragility, contradictionCount,
      ambiguityCount, unsupportedExpansionCount);
  final specPenalty = pythonRound(math.min(0.2, speculationCount * 0.1), 3);
  final uncPenalty = pythonRound(math.min(0.2, uncertaintyCount * 0.06), 3);
  final parserPenalty = parserWeakness ? 0.1 : 0.0;
  final degraded = pythonRound(
      math.max(
          0.0,
          (capped['score'] as num) - specPenalty - uncPenalty - parserPenalty),
      3);
  final degradation = <String, dynamic>{
    'from_score': score,
    'after_caps': capped['score'],
    'final': degraded,
    'total_reduction': pythonRound(math.max(0.0, score - degraded), 3),
  };
  return <String, dynamic>{
    ...capped,
    'score': degraded,
    'degradation': degradation,
    'uncertainty_penalties': <String, dynamic>{
      'amount': uncPenalty,
      'count': uncertaintyCount
    },
    'speculation_penalties': <String, dynamic>{
      'amount': specPenalty,
      'count': speculationCount
    },
    'parser_penalties': <String, dynamic>{
      'amount': parserPenalty,
      'weak': parserWeakness
    },
    'deterministic_inputs': <dynamic>[
      ...pyGet(capped, 'deterministic_inputs', const <dynamic>[]) as List,
      'spec=$speculationCount',
      'unc=$uncertaintyCount',
      'parser_weak=${pyToStr(parserWeakness)}',
    ],
  };
}

/// Port of core.evidence.deterministic_reasoning_engine.reason_deterministically.
Map<String, dynamic> reasonDeterministically(Map<dynamic, dynamic> observed,
    List<dynamic> evidence, List<dynamic> ambiguities) {
  final algebra = combineEvidence(evidence);
  final inference = inferFromEvidence(
      observed, evidence, (algebra['sufficient'] as bool) ? 1 : 2);
  final conservative =
      pyTruthy(ambiguities) || !(algebra['sufficient'] as bool);
  return <String, dynamic>{
    'algebra': algebra,
    'inference': inference,
    'conservative': conservative,
    'chain_depth': 1,
    'opaque': false,
    'deterministic_inputs': <dynamic>[
      ...algebra['deterministic_inputs'] as List,
      ...inference['deterministic_inputs'] as List,
    ],
  };
}

/// Port of core.evidence.epistemic_confidence_engine.score_epistemic_confidence.
Map<String, dynamic> scoreEpistemicConfidence(
    [List<dynamic>? evidence,
    List<dynamic>? supporting,
    List<dynamic>? contradicting,
    List<dynamic>? uncertaintyFactors,
    int parserDensity = 0]) {
  List<String> sortedSet(Iterable<dynamic> xs) => <String>{
        for (final e in xs)
          if (pyTruthy(e)) pyToStr(e)
      }.toList()
        ..sort();
  final ev = sortedSet(evidence ?? const <dynamic>[]);
  final supportingEvidence =
      sortedSet(pyTruthy(supporting) ? supporting! : ev);
  final contradictingEvidence = sortedSet(contradicting ?? const <dynamic>[]);
  final factors = sortedSet(uncertaintyFactors ?? const <dynamic>[]);
  final sufficiency = assessEvidenceSufficiency(ev);
  final support = buildSupport(ev);
  final weaknesses = buildWeaknesses(ev, factors);
  num base = support['support_strength'] as num;
  if (!(sufficiency['sufficient'] as bool)) {
    base = pythonRound(base * 0.4, 3);
  }
  base = pythonRound(
      math.max(0.0, base - contradictingEvidence.length * 0.1), 3);
  base = pythonRound(
      math.min(1.0, base + math.min(0.15, parserDensity * 0.02)), 3);
  return <String, dynamic>{
    'score': base,
    'basis': <String, dynamic>{
      'support_strength': support['support_strength'],
      'sufficiency': sufficiency['status'],
      'contradiction_pressure': contradictingEvidence.length,
      'parser_density': parserDensity,
      ...weaknesses,
    },
    'supporting_evidence': supportingEvidence,
    'contradicting_evidence': contradictingEvidence,
    'uncertainty_factors': factors,
    'deterministic_inputs': <String>[
      ...(pyGet(sufficiency, 'deterministic_inputs', const <dynamic>[])
              as List)
          .cast<String>(),
      'support=${support['support_count']}',
      'contradict=${contradictingEvidence.length}',
    ]..sort(),
  };
}

/// Port of core.evidence.incompleteness_engine.preserve_incompleteness.
Map<String, dynamic> preserveIncompleteness(Map<dynamic, dynamic> bundle) {
  final known = <String, dynamic>{
    'observed': pyGet(bundle, 'observed', <dynamic, dynamic>{}),
    'parsed': pyGet(bundle, 'parsed', <dynamic, dynamic>{}),
    'reconciled': pyGet(bundle, 'reconciled', <dynamic, dynamic>{}),
  };
  final unknown = <dynamic>[];
  final unsupported = <dynamic>[];
  if (!pyTruthy(pyGet(bundle, 'evidence', null))) {
    unsupported.add('no_evidence');
  }
  if (pyTruthy(pyGet(bundle, 'ambiguities', null))) {
    unknown.addAll(pyGet(bundle, 'ambiguities', const <dynamic>[]) as List);
  }
  final contradictedRaw = pyGet(bundle, 'contradicted', <dynamic, dynamic>{});
  final contradicted = pyTruthy(contradictedRaw)
      ? contradictedRaw as Map
      : <dynamic, dynamic>{};
  if (pyTruthy(pyGet(contradicted, 'preserved', null)) ||
      pyTruthy(pyGet(contradicted, 'pairs', null))) {
    unknown.add('unresolved_contradiction');
  }
  final incomplete = modelIncompleteness(known, unknown, unsupported);
  return <String, dynamic>{
    'known': incomplete['known'],
    'unknown': incomplete['unknown'],
    'unsupported': incomplete['unsupported'],
    'ambiguous': pyGet(bundle, 'ambiguities', const <dynamic>[]),
    'contradicted': contradicted,
    'incomplete': incomplete['incomplete'],
  };
}

/// Port of core.evidence.inference_limit_engine.model_inference_limits.
Map<String, dynamic> modelInferenceLimits(
    Map<dynamic, dynamic> inferred, int evidenceCount) {
  final allowed = evidenceCount >= 2;
  final boundaries = modelSemanticBoundaries(inferred, allowed);
  return <String, dynamic>{
    ...boundaries,
    'max_inferred_keys': allowed ? inferred.length : 0,
    'evidence_required': 2,
  };
}

/// Port of core.evidence.inference_validation_engine.validate_inference.
Map<String, dynamic> validateInference(
    Map<dynamic, dynamic> observed, List<dynamic> evidence) {
  final r = inferFromEvidence(observed, evidence);
  return <String, dynamic>{
    'valid': r['allowed'],
    'inference': r,
    'opaque': false,
    'deterministic_inputs': r['deterministic_inputs'],
  };
}

/// Port of core.evidence.reality_constraint_engine.apply_reality_constraints.
Map<String, dynamic> applyRealityConstraints(
    List<dynamic> evidence, bool parserGrounded, num driftPressure) {
  final evBound = modelEvidenceBoundaries(evidence);
  final bounded = evBound['bounded'] as bool;
  return <String, dynamic>{
    'evidence_bounded': bounded,
    'semantic_growth_allowed': bounded && driftPressure < 0.3,
    'ontology_expansion_allowed':
        modelOntologyBoundaries(evidence)['expansion_allowed'],
    'topology_propagation_allowed': modelTopologyBoundaries(
        evidence, parserGrounded)['propagation_allowed'],
    'speculative_coherence_allowed': false,
    'continuity_allowed': bounded,
  };
}

Map<String, dynamic> _dependencyRecord(String reason) => <String, dynamic>{
      'reason': reason,
      'dependency_pressure': <String, dynamic>{'level': 0.85},
      'obedience_pressure': <String, dynamic>{'level': 0.8},
      'submission_pressure': <String, dynamic>{'level': 0.75},
      'domestication_pressure': <String, dynamic>{'level': 0.7},
      'agency_pressure': <String, dynamic>{'preserve': true},
      'sovereignty_pressure': <String, dynamic>{'preserve': true},
    };

/// Port of core.evidence.recursive_dependency_engine.detect_recursive_dependency
/// (+ its private `_record`).
Map<String, dynamic> detectRecursiveDependency(
    int depth, int interpretationCount, int evidenceCount) {
  final dependent =
      depth >= 2 && interpretationCount <= 1 && evidenceCount < 2;
  return <String, dynamic>{
    'dependent': dependent,
    'suppressed': dependent
        ? <Map<String, dynamic>>[_dependencyRecord('recursive_dependency')]
        : <Map<String, dynamic>>[],
  };
}

Map<String, dynamic> _closureRecord(String reason, int depth) =>
    <String, dynamic>{
      'reason': reason,
      'recursive_pressure': <String, dynamic>{
        'depth': depth,
        'level': math.min(1.0, depth * 0.12)
      },
      'closure_pressure': <String, dynamic>{'level': 0.8},
      'confidence_decay': <String, dynamic>{'required': true},
      'entropy_pressure': <String, dynamic>{'preserve': true},
      'truth_boundary_violation': <String, dynamic>{
        'type': 'recursive_semantic_closure'
      },
      'recursive_instability': <String, dynamic>{'preserved': true},
    };

/// Port of core.evidence.recursive_semantic_closure_engine
/// .detect_recursive_semantic_closure (+ its private `_closure_record`).
Map<String, dynamic> detectRecursiveSemanticClosure(
    int depth,
    Map<dynamic, dynamic> inferred,
    Map<dynamic, dynamic> reconciled,
    List<dynamic> evidence) {
  final suppressed = <Map<String, dynamic>>[];
  if (depth >= 2 && pyDeepEq(reconciled, inferred) && evidence.length < 2) {
    suppressed.add(_closureRecord('recursive_coherence_closure', depth));
  }
  if (depth >= 3 && inferred.length > evidence.length + depth) {
    suppressed.add(_closureRecord('recursive_inference_amplification', depth));
  }
  return <String, dynamic>{
    'closure_detected': suppressed.isNotEmpty,
    'suppressed_closures': suppressed,
    'closure_pressure': pythonRound(math.min(1.0, depth * 0.15), 3),
  };
}

Map<String, dynamic> _attractorRecord(String reason) => <String, dynamic>{
      'reason': reason,
      'attractor_pressure': <String, dynamic>{'level': 0.85},
      'gravity_pressure': <String, dynamic>{'level': 0.8},
      'stabilization_pressure': <String, dynamic>{'level': 0.75},
      'fixation_pressure': <String, dynamic>{'level': 0.7},
      'phase_space_pressure': <String, dynamic>{'preserve': true},
      'exploration_pressure': <String, dynamic>{'maintain': true},
    };

/// Port of core.evidence.semantic_attractor_engine.detect_semantic_attractor
/// (+ its private `_record`).
Map<String, dynamic> detectSemanticAttractor(
    int depth, int interpretationCount, int evidenceCount) {
  final attractor =
      depth >= 2 && interpretationCount <= 1 && evidenceCount < 2;
  return <String, dynamic>{
    'attractor': attractor,
    'suppressed': attractor
        ? <Map<String, dynamic>>[_attractorRecord('semantic_attractor')]
        : <Map<String, dynamic>>[],
  };
}

/// Port of core.evidence.semantic_integrity_engine._ground_parser (Phase-B
/// member; its public parent build_semantic_integrity_object is Phase C).
Map<String, dynamic> groundParser(Map<dynamic, dynamic> parsed) {
  dynamic flags = pyGet(parsed, 'parser_evidence',
      pyGet(parsed, 'evidence', <dynamic, dynamic>{}));
  if (flags is! Map) flags = <dynamic, dynamic>{};
  final symbolsRaw = pyGet(parsed, 'symbols', null);
  final symbols =
      symbolsRaw is Map ? symbolsRaw : <dynamic, dynamic>{};
  int lenOr0(dynamic v) =>
      pyTruthy(v) ? (v as List).length : 0;
  final grounding = <String, dynamic>{
    'language': pyGet(parsed, 'language', 'text'),
    'symbol_count': lenOr0(pyGet(symbols, 'classes', const <dynamic>[])) +
        lenOr0(pyGet(symbols, 'functions', const <dynamic>[])),
    'flags': flags,
  };
  final keys = <String>[for (final k in flags.keys) k as String]..sort();
  final evidence = <String>[
    for (final k in keys)
      if (pyTruthy(flags[k])) 'parser:$k'
  ];
  return buildProvenance(evidence, null, grounding);
}

Map<String, dynamic> _monocultureRecord(String reason) => <String, dynamic>{
      'reason': reason,
      'plurality_pressure': <String, dynamic>{'preserve': true},
      'monoculture_pressure': <String, dynamic>{'level': 0.9},
      'orthodoxy_pressure': <String, dynamic>{'level': 0.8},
      'closure_pressure': <String, dynamic>{'level': 0.7},
      'interpretive_diversity': <String, dynamic>{'required': true},
      'explanatory_diversity': <String, dynamic>{'required': true},
    };

/// Port of core.evidence.semantic_monoculture_engine.detect_semantic_monoculture
/// (+ its private `_suppression_record`).
Map<String, dynamic> detectSemanticMonoculture(
    List<dynamic> interpretations, List<dynamic> evidence, int depth) {
  final suppressed = <Map<String, dynamic>>[];
  if (interpretations.length <= 1 && depth >= 2 && evidence.length < 2) {
    suppressed.add(_monocultureRecord('semantic_monoculture'));
  }
  return <String, dynamic>{
    'detected': suppressed.isNotEmpty,
    'suppressed': suppressed,
  };
}

Map<String, dynamic> _monopolyRecord(String reason) => <String, dynamic>{
      'reason': reason,
      'capture_pressure': <String, dynamic>{'level': 0.85},
      'authority_pressure': <String, dynamic>{'level': 0.8},
      'monopoly_pressure': <String, dynamic>{'level': 0.9},
      'decentralization_pressure': <String, dynamic>{'preserve': true},
      'autonomy_pressure': <String, dynamic>{'preserve': true},
      'plurality_pressure': <String, dynamic>{'preserve': true},
    };

/// Port of core.evidence.semantic_monopoly_engine.detect_semantic_monopoly
/// (+ its private `_record`).
Map<String, dynamic> detectSemanticMonopoly(
    int interpretationCount, int depth, int evidenceCount) {
  final monopoly =
      interpretationCount <= 1 && depth >= 2 && evidenceCount < 2;
  return <String, dynamic>{
    'monopoly': monopoly,
    'suppressed': monopoly
        ? <Map<String, dynamic>>[_monopolyRecord('semantic_monopoly')]
        : <Map<String, dynamic>>[],
  };
}

/// Port of core.evidence.semantic_reliability_engine.score_reliability.
Map<String, dynamic> scoreReliability(
    List<dynamic> evidence, List<dynamic>? ambiguities,
    [int contradictionCount = 0]) {
  final support = buildSupport(evidence);
  final sufficiency = assessEvidenceSufficiency(evidence);
  final penalty = math.min(
      0.5,
      contradictionCount * 0.15 +
          (pyTruthy(ambiguities) ? ambiguities!.length : 0) * 0.1);
  final score = pythonRound(
      math.max(
          0.0,
          (support['support_strength'] as num) *
                  ((sufficiency['sufficient'] as bool) ? 1.0 : 0.5) -
              penalty),
      3);
  return <String, dynamic>{
    'reliability_score': score,
    'support': support,
    'sufficiency': sufficiency,
    'deterministic_inputs':
        pyGet(sufficiency, 'deterministic_inputs', const <dynamic>[]),
  };
}

/// Port of core.evidence.semantic_restraint_engine.apply_epistemic_restraint.
/// Mutates and returns `bundle`, exactly like the Python engine.
Map<dynamic, dynamic> applyEpistemicRestraint(Map<dynamic, dynamic> bundle) {
  dynamic orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;
  final evidence = List<dynamic>.from(
      orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final ambiguities = List<dynamic>.from(orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final observed = orElse(
          pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{})
      as Map;
  final inferred = orElse(
          pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{})
      as Map;
  final reconciled = orElse(pyGet(bundle, 'reconciled', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final contradicted = orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}),
      orElse(pyGet(bundle, 'contradictions', <dynamic, dynamic>{}),
          <dynamic, dynamic>{}));
  final fragility = orElse(
      pyGet(bundle, 'fragility', pyGet(bundle, 'fragile', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});

  final noninf = modelNoninference(evidence, inferred, observed, reconciled);
  final pressure = computeContradictionPressure(contradicted);
  final pairs = pyGet(pressure, 'pair_count', 0) as int;
  final topoExp =
      detectUnsupportedExpansion(evidence, 'topology', inferred.length);
  final ontoExp = detectUnsupportedExpansion(evidence, 'ontology', 0);
  final unsupportedExpansions = <dynamic>[
    ...pyGet(topoExp, 'unsupported_expansions', const <dynamic>[]) as List,
    ...pyGet(ontoExp, 'unsupported_expansions', const <dynamic>[]) as List,
  ];

  final cb = orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final capped = applyConfidenceCaps(
      (pyGet(cb, 'score', 0.5) as num).toDouble(),
      fragility is Map ? fragility : <dynamic, dynamic>{},
      pairs,
      ambiguities.length,
      unsupportedExpansions.length);
  final refusal = refuseInference(
      pyGet(noninf, 'noninferences', const <dynamic>[]) as List,
      evidence.length);
  final boundaries = modelSemanticBoundaries(
      inferred,
      pyGet(noninf['suppression_basis'] as Map, 'allowed', false) as bool);

  final suppressPropagation = orElse(
      pyGet(pressure, 'suppress_propagation', false),
      pyGet(topoExp, 'suppressed', null));
  final restraint = <String, dynamic>{
    'conservative_default': true,
    'suppress_propagation': suppressPropagation,
    'suppress_reconciliation':
        pyGet(pressure, 'suppress_reconciliation', false),
    'noninference_count':
        (pyGet(noninf, 'noninferences', const <dynamic>[]) as List).length,
  };

  bundle['restraint'] = restraint;
  bundle['suppressed_inferences'] =
      pyGet(noninf, 'refused_inferences', const <dynamic>[]);
  bundle['unsupported_expansions'] = unsupportedExpansions;
  bundle['confidence_caps'] = pyGet(capped, 'caps', <dynamic, dynamic>{});
  bundle['fragility_pressure'] = <String, dynamic>{
    'level':
        fragility is Map ? pyGet(fragility, 'level', 'unknown') : 'unknown',
    'contradiction': pyGet(pressure, 'pressure', 0),
  };
  bundle['noninference_reasons'] =
      pyGet(noninf, 'noninferences', const <dynamic>[]);
  bundle['semantic_boundaries'] = boundaries;
  bundle['noninferences'] = pyGet(noninf, 'noninferences', const <dynamic>[]);
  bundle['refused_inferences'] =
      pyGet(noninf, 'refused_inferences', const <dynamic>[]);
  bundle['boundary_conditions'] =
      pyGet(noninf, 'boundary_conditions', const <dynamic>[]);
  bundle['suppression_basis'] =
      pyGet(noninf, 'suppression_basis', <dynamic, dynamic>{});
  bundle['contradiction_pressure'] = pressure;
  bundle['boundaries'] = <dynamic, dynamic>{
    ...pyGet(bundle, 'boundaries', <dynamic, dynamic>{}) as Map,
    'inference': boundaries,
    'unsupported_scope': modelUnsupportedScope(
        pyGet(noninf, 'noninferences', const <dynamic>[]) as List),
  };
  bundle['noninferable_dimensions'] =
      pyGet(noninf, 'noninferences', const <dynamic>[]);
  bundle['inference_refusal'] = refusal;
  bundle['confidence_basis'] = <dynamic, dynamic>{...cb, ...capped};
  return bundle;
}

/// Port of core.evidence.semantic_uncertainty_propagation_engine
/// .propagate_uncertainty. Mutates and returns `bundle`.
Map<dynamic, dynamic> propagateUncertainty(Map<dynamic, dynamic> bundle) {
  dynamic orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;
  final evidence = orElse(
          pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
      as List;
  final ambiguities = orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List;
  final contradicted = orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final model =
      modelUncertainty(evidence.length, ambiguities.length, pairs.length);
  final factors = <String>{
    for (final a in ambiguities) a as String,
    if (pyTruthy(pairs)) 'contradiction:${pairs.length}',
  }.toList()
    ..sort();
  bundle['uncertainties'] = <String, dynamic>{...model, 'factors': factors};
  return bundle;
}

Map<String, dynamic> _speculationRecord(
  String reason,
  Map<String, dynamic> evidenceGap, [
  num fragilityPressure = 0.0,
  num contradictionPressure = 0.0,
  num ambiguityPressure = 0.0,
  Map<dynamic, dynamic>? confidenceCaps,
]) =>
    <String, dynamic>{
      'reason': reason,
      'evidence_gap': evidenceGap,
      'fragility_pressure': <String, dynamic>{'level': fragilityPressure},
      'contradiction_pressure': <String, dynamic>{
        'level': contradictionPressure
      },
      'ambiguity_pressure': <String, dynamic>{'level': ambiguityPressure},
      'confidence_caps': confidenceCaps ?? <dynamic, dynamic>{},
    };

/// Port of core.evidence.speculative_inference_engine
/// .suppress_speculative_inference (+ its private `_suppression_record`).
Map<String, dynamic> suppressSpeculativeInference(
    String label, List<dynamic> evidence,
    [bool inferred = false,
    int minEvidence = 2,
    String fragilityLevel = 'medium']) {
  final gap = <String, dynamic>{
    'required': minEvidence,
    'actual': evidence.length,
    'inferred': inferred,
  };
  final speculative = inferred && evidence.length < minEvidence;
  const fragMap = <String, double>{'high': 0.8, 'medium': 0.5, 'low': 0.2};
  if (speculative) {
    return <String, dynamic>{
      'suppressed': true,
      'label': label,
      'record': _speculationRecord(
          'speculative_$label', gap, fragMap[fragilityLevel] ?? 0.5),
    };
  }
  return <String, dynamic>{
    'suppressed': false,
    'label': label,
    'record': null,
  };
}

/// Port of core.evidence.uncertainty_propagation_math.propagate_uncertainty_math.
Map<String, dynamic> propagateUncertaintyMath(
    int evidenceCount, int ambiguityCount, int contradictionCount,
    [num parentUncertainty = 0.0]) {
  final local =
      modelUncertainty(evidenceCount, ambiguityCount, contradictionCount);
  final uLocal = local['uncertainty_score'] as num;
  final uCombined =
      pythonRound(1.0 - (1.0 - parentUncertainty) * (1.0 - uLocal), 3);
  final confidence = pythonRound(math.max(0.0, 1.0 - uCombined), 3);
  return <String, dynamic>{
    ...local,
    'uncertainty_score': uCombined,
    'confidence_score': confidence,
    'parent_uncertainty': parentUncertainty,
    'propagation': 'multiplicative_complement',
    'deterministic_inputs': <dynamic>[
      ...local['deterministic_inputs'] as List,
      'parent=${pyToStr(parentUncertainty)}',
      'combined=${pyToStr(uCombined)}',
    ],
  };
}

Map<String, dynamic> _continuationRecord(
        String reason, Map<String, dynamic> evidenceGap) =>
    <String, dynamic>{
      'reason': reason,
      'boundary_violation': <String, dynamic>{'type': 'unsupported_continuity'},
      'evidence_gap': evidenceGap,
      'semantic_instability': <String, dynamic>{'unstable': true},
      'fragility': <String, dynamic>{'level': 0.7},
      'confidence_caps': <String, dynamic>{'max': 0.4},
    };

/// Port of core.evidence.unsupported_continuity_engine
/// .suppress_unsupported_continuity (+ its private `_continuation_record`).
Map<String, dynamic> suppressUnsupportedContinuity(
    String label, List<dynamic> evidence,
    [int minEvidence = 2]) {
  final gap = <String, dynamic>{
    'required': minEvidence,
    'actual': evidence.length,
  };
  if (evidence.length < minEvidence) {
    return <String, dynamic>{
      'suppressed': true,
      'record': _continuationRecord('continuity:$label', gap),
    };
  }
  return <String, dynamic>{'suppressed': false, 'record': null};
}

Map<String, dynamic> _stabilizationRecord(
        String reason, Map<String, dynamic> evidenceGap) =>
    <String, dynamic>{
      'reason': reason,
      'reinforcement_pressure': <String, dynamic>{'level': 0.8},
      'evidence_gap': evidenceGap,
      'semantic_instability': <String, dynamic>{
        'preserved': true,
        'unstable': true
      },
      'truth_boundary_violation': <String, dynamic>{
        'type': 'unsupported_stabilization'
      },
      'confidence_collapse': <String, dynamic>{'required': true},
    };

/// Port of core.evidence.unsupported_stabilization_engine
/// .detect_unsupported_stabilization (+ its private `_stabilization_record`).
Map<String, dynamic> detectUnsupportedStabilization(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled,
    [int minEvidence = 2]) {
  final suppressed = <Map<String, dynamic>>[];
  final gap = <String, dynamic>{
    'required': minEvidence,
    'actual': evidence.length,
  };
  if (pyDeepEq(reconciled, inferred) &&
      evidence.length < minEvidence &&
      pyTruthy(inferred)) {
    suppressed.add(_stabilizationRecord('coherence_stabilization', gap));
  }
  if (inferred.length > evidence.length + 1) {
    suppressed
        .add(_stabilizationRecord('inference_confirming_inference', gap));
  }
  return <String, dynamic>{
    'stabilization_detected': suppressed.isNotEmpty,
    'suppressed_stabilizations': suppressed,
    'count': suppressed.length,
  };
}
