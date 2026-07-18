/// Phase A.3 batch 3 (core.evidence leaves) of the Category-A semantic-IR
/// port — 24 medium engines (confidence caps, lattices, evidence algebra,
/// explainability, lineage/provenance/traceability, noninference, instability),
/// proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.evidence.confidence_cap_engine.apply_confidence_caps.
Map<String, dynamic> applyConfidenceCaps(
  num score,
  Map<dynamic, dynamic> fragility, [
  int contradictionCount = 0,
  int ambiguityCount = 0,
  int unsupportedExpansionCount = 0,
]) {
  final limits =
      pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{}) as Map;
  final cap = (pyGet(limits, 'max_score', 0.85) as num).toDouble();
  const fragPenalties = <String, double>{
    'high': 0.25,
    'medium': 0.12,
    'low': 0.0
  };
  final level = pyGet(fragility, 'level', 'medium');
  final fragPenalty = level is String ? (fragPenalties[level] ?? 0.12) : 0.12;
  final contradictPenalty =
      pythonRound(math.min(0.35, contradictionCount * 0.12), 3);
  final ambigPenalty = pythonRound(math.min(0.25, ambiguityCount * 0.08), 3);
  final expandPenalty =
      pythonRound(math.min(0.2, unsupportedExpansionCount * 0.1), 3);
  final finalScore = pythonRound(
      math.max(
          0.0,
          math.min(score.toDouble(), cap) -
              fragPenalty -
              contradictPenalty -
              ambigPenalty -
              expandPenalty),
      3);
  return <String, dynamic>{
    'score': finalScore,
    'caps': <String, dynamic>{'fragility_max': cap},
    'fragility_penalties': <String, dynamic>{
      'amount': fragPenalty,
      'level': pyGet(fragility, 'level', null),
    },
    'contradiction_penalties': <String, dynamic>{
      'amount': contradictPenalty,
      'count': contradictionCount,
    },
    'ambiguity_penalties': <String, dynamic>{
      'amount': ambigPenalty,
      'count': ambiguityCount,
    },
    'unsupported_expansion_penalties': <String, dynamic>{
      'amount': expandPenalty,
      'count': unsupportedExpansionCount,
    },
    'deterministic_inputs': <String>[
      'cap=${pyFloatStr(cap)}',
      'contradict=$contradictionCount',
      'ambig=$ambiguityCount',
      'expand=$unsupportedExpansionCount',
    ],
  };
}

/// Port of core.evidence.contradiction_lattice_engine.build_contradiction_lattice.
Map<String, dynamic> buildContradictionLattice(List<dynamic>? pairs) {
  final normalized = <List<String>>[
    for (final p in pairs ?? const <dynamic>[])
      if (p is List && p.length >= 2) <String>[pyToStr(p[0]), pyToStr(p[1])]
  ];
  normalized.sort((a, b) {
    final c = a[0].compareTo(b[0]);
    return c != 0 ? c : a[1].compareTo(b[1]);
  });
  final count = normalized.length;
  final pressure = pythonRound(math.min(1.0, count * 0.25), 3);
  return <String, dynamic>{
    'pairs': normalized,
    'count': count,
    'pressure': pressure,
    'rigor': 'lattice_enumeration',
    'deterministic_inputs': <String>[
      'pair_count=$count',
      'pressure=${pyFloatStr(pressure)}'
    ],
  };
}

/// Port of core.evidence.epistemic_boundary_engine.preserve_epistemic_boundaries.
Map<String, dynamic> preserveEpistemicBoundaries(List<dynamic> evidence,
    List<dynamic> noninferableRegions, List<dynamic> unstableRegions) {
  return <String, dynamic>{
    'visible': true,
    'where_inference_stops': noninferableRegions,
    'where_cognition_stops': unstableRegions,
    'where_reconstruction_stops': unstableRegions,
    'suppress_stabilization': pyTruthy(unstableRegions),
    'suppress_coherence': evidence.length < 2,
  };
}

/// Port of core.evidence.epistemic_limit_engine.model_epistemic_limits.
Map<String, dynamic> modelEpistemicLimits(List<dynamic> evidence,
    int parserDensity, Map<dynamic, dynamic> fragility) {
  final cannotConclude = <String>[];
  if (evidence.length < 2) cannotConclude.add('definitive_semantic_conclusion');
  if (parserDensity == 0) cannotConclude.add('parser_grounded_conclusion');
  if (pyGet(fragility, 'level', null) == 'high') {
    cannotConclude.add('high_confidence_claim');
  }
  final unique = cannotConclude.toSet().toList()..sort();
  final limits =
      pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{}) as Map;
  return <String, dynamic>{
    'cannot_conclude': unique,
    'exceeds_evidence': evidence.isEmpty,
    'exceeds_parser_grounding': parserDensity == 0,
    'exceeds_corroboration': evidence.length < 2,
    'max_confidence': pyGet(limits, 'max_score', 0.5),
  };
}

/// Port of core.evidence.evidence_algebra_engine.combine_evidence.
Map<String, dynamic> combineEvidence(List<dynamic> evidence,
    [Map<dynamic, dynamic>? weights]) {
  final w = weights ?? const <dynamic, dynamic>{};
  final items = <String>{
    for (final e in evidence)
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  // Python: round(sum(...), 3) — an empty sum is int 0 and stays int.
  final num total = items.isEmpty
      ? 0
      : pythonRound(
          items.fold<double>(
              0.0, (acc, e) => acc + (pyGet(w, e, 1.0) as num).toDouble()),
          3);
  return <String, dynamic>{
    'items': items,
    'count': items.length,
    'weight_sum': total,
    'sufficient': items.length >= 2,
    'deterministic_inputs': <String>[
      'count=${items.length}',
      'weight_sum=${total is int ? total.toString() : pyFloatStr(total as double)}',
    ],
  };
}

/// Port of core.evidence.evidence_weighting_calculus.weight_evidence_calculus.
Map<String, dynamic> weightEvidenceCalculus(List<dynamic> evidence,
    [bool parserBacked = false]) {
  final items = <String>{
    for (final e in evidence)
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  final weights = <String, double>{};
  for (final e in items) {
    if (e.startsWith('parser:')) {
      weights[e] = 1.0;
    } else if (parserBacked) {
      weights[e] = 0.85;
    } else {
      weights[e] = 0.6;
    }
  }
  final num total = weights.isEmpty
      ? 0
      : pythonRound(weights.values.fold<double>(0.0, (a, b) => a + b), 3);
  return <String, dynamic>{
    'weights': weights,
    'total': total,
    'parser_backed': parserBacked,
    'deterministic_inputs': <String>[
      'items=${items.length}',
      'total=${total is int ? total.toString() : pyFloatStr(total as double)}',
    ],
  };
}

/// Port of core.evidence.explainability_engine.build_explainability.
Map<String, dynamic> buildExplainability(dynamic parserPayload,
    Map<dynamic, dynamic> confidence, Map<dynamic, dynamic> provenance) {
  dynamic flags = <dynamic, dynamic>{};
  if (parserPayload is Map) {
    flags = pyGet(parserPayload, 'parser_evidence',
        pyGet(parserPayload, 'evidence', <dynamic, dynamic>{}));
    if (flags is! Map) flags = <dynamic, dynamic>{};
  }
  final grounding = pyGet(provenance, 'grounding', <dynamic, dynamic>{}) as Map;
  final parserBasis = <String, dynamic>{
    'language': pyTruthy(parserPayload)
        ? pyGet(parserPayload as Map, 'language', 'text')
        : 'unknown',
    'flags': flags,
    'symbol_count': pyGet(grounding, 'symbol_count', 0),
  };
  var graphBasis = <String, dynamic>{};
  if (pyTruthy(parserPayload) &&
      pyGet(parserPayload as Map, 'semantic_graph', null) is Map) {
    final g = parserPayload['semantic_graph'] as Map;
    dynamic nodes = pyGet(g, 'nodes', <dynamic>[]);
    if (!pyTruthy(nodes)) nodes = <dynamic>[];
    dynamic edges = pyGet(g, 'edges', <dynamic>[]);
    if (!pyTruthy(edges)) edges = <dynamic>[];
    graphBasis = <String, dynamic>{
      'nodes': (nodes as List).length,
      'edges': (edges as List).length,
    };
  }
  final semanticBasis = <String, dynamic>{
    'confidence_score': pyGet(confidence, 'score', 0.0),
    'deterministic_inputs':
        pyGet(confidence, 'deterministic_inputs', <dynamic>[]),
  };
  dynamic summarySrc = pyGet(provenance, 'evidence', <dynamic>[]);
  if (!pyTruthy(summarySrc)) summarySrc = <dynamic>[];
  final summary = <String>[for (final e in summarySrc as List) e as String]
    ..sort();
  return <String, dynamic>{
    'parser_basis': parserBasis,
    'graph_basis': graphBasis,
    'semantic_basis': semanticBasis,
    'summary': summary,
  };
}

/// Port of core.evidence.inference_integrity_engine.model_inference_integrity.
Map<String, dynamic> modelInferenceIntegrity(
  List<dynamic> evidence,
  List<dynamic>? supporting,
  List<dynamic>? contradicting,
  Map<dynamic, dynamic> fragility, [
  List<dynamic>? missingEvidence,
]) {
  final caps =
      pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{}) as Map;
  List<String> sortedSet(List<dynamic> xs) =>
      <String>{for (final x in xs) x as String}.toList()..sort();
  final supportingSrc = pyTruthy(supporting) ? supporting! : evidence;
  final contradictingSrc =
      pyTruthy(contradicting) ? contradicting! : const <dynamic>[];
  final missingSrc = pyTruthy(missingEvidence)
      ? missingEvidence!
      : pyGet(fragility, 'missing_support', <dynamic>[]) as List;
  return <String, dynamic>{
    'basis': pyGet(fragility, 'basis', <dynamic, dynamic>{}),
    'supporting_evidence': sortedSet(supportingSrc),
    'contradicting_evidence': sortedSet(contradictingSrc),
    'missing_evidence': sortedSet(missingSrc),
    'uncertainty_factors':
        pyGet(fragility, 'contradiction_pressure', <dynamic>[]),
    'confidence_caps': <dynamic>[pyGet(caps, 'max_score', 1.0)],
    'unsupported_dimensions': pyGet(fragility, 'missing_support', <dynamic>[]),
    'fragility': fragility,
  };
}

/// Port of core.evidence.inference_termination_engine.terminate_inference_chain.
Map<String, dynamic> terminateInferenceChain(
    List<dynamic> refusedInferences, List<dynamic> suppressedSpeculation) {
  final terminated = <dynamic>[
    ...refusedInferences,
    for (final s in suppressedSpeculation)
      if (s is Map) pyGet(s, 'reason', 'speculative'),
  ];
  final unique = <String>{for (final t in terminated) t as String}.toList()
    ..sort();
  return <String, dynamic>{
    'terminated_inferences': unique,
    'chain_stopped': pyTruthy(terminated),
    'stop_at': terminated.isNotEmpty ? terminated[0] : null,
  };
}

/// Port of core.evidence.instability_preservation_engine.preserve_instability.
Map<String, dynamic> preserveInstability(List<dynamic> unstableRegions,
    List<dynamic> evidence, List<dynamic> stabilizationSuppressed) {
  final regions = List<dynamic>.from(unstableRegions);
  if (evidence.length < 2) regions.add('semantic:weak_evidence_instability');
  if (pyTruthy(stabilizationSuppressed)) {
    regions.add('semantic:stabilization_blocked');
  }
  final unique = <String>{for (final r in regions) r as String}.toList()
    ..sort();
  return <String, dynamic>{
    'preserved': true,
    'unstable': pyTruthy(regions),
    'regions': unique,
    'do_not_stabilize': true,
  };
}

/// Port of core.evidence.insufficiency_engine.mark_insufficiency.
Map<String, dynamic> markInsufficiency(Map<dynamic, dynamic> bundle,
    [int minEvidence = 2]) {
  dynamic evidence = pyGet(bundle, 'evidence', <dynamic>[]);
  if (!pyTruthy(evidence)) evidence = <dynamic>[];
  final insufficient = (evidence as List).length < minEvidence;
  final flags = <String>[];
  if (insufficient) flags.add('insufficient_evidence');
  if (pyTruthy(pyGet(bundle, 'ambiguities', null)))
    flags.add('ambiguous_claim');
  final unique = flags.toSet().toList()..sort();
  return <String, dynamic>{
    'insufficient': insufficient,
    'flags': unique,
    'evidence_count': evidence.length,
    'required': minEvidence,
    'message': insufficient ? 'insufficient evidence' : 'evidence_ok',
  };
}

/// Port of core.evidence.interpretive_diversity_engine.model_interpretive_diversity.
Map<String, dynamic> modelInterpretiveDiversity(
    List<dynamic> evidence, Map<dynamic, dynamic> inferred) {
  final interpretations = <Map<String, dynamic>>[];
  if (pyTruthy(evidence)) {
    interpretations.add(<String, dynamic>{
      'id': 'evidence_backed',
      'evidence': List<dynamic>.from(evidence),
      'limitations': <dynamic>[],
    });
  }
  for (final k in inferred.keys) {
    interpretations.add(<String, dynamic>{
      'id': 'infer:$k',
      'interpretation': <String, dynamic>{k as String: inferred[k]},
      'evidence': List<dynamic>.from(evidence),
      'limitations': evidence.contains(k) ? <dynamic>[] : <dynamic>['inferred'],
      'contradictions': <dynamic>[],
      'ambiguities': <dynamic>[],
      'plurality': <String, dynamic>{
        'rank': evidence.length < 2 ? 'secondary' : 'primary'
      },
      'confidence': <String, dynamic>{'capped': evidence.length < 2},
    });
  }
  return <String, dynamic>{
    'preserved': true,
    'count': interpretations.length,
    'interpretations': interpretations.take(10).toList(),
  };
}

/// Port of core.evidence.lineage_engine.build_lineage.
Map<String, dynamic> buildLineage(List<dynamic>? stages) {
  final chain = <Map<String, dynamic>>[];
  final src = stages ?? const <dynamic>[];
  for (var idx = 0; idx < src.length; idx++) {
    final stage = src[idx];
    if (stage is! Map) continue;
    List<String> sortedList(dynamic v) => v is List
        ? (<String>[for (final x in v) x as String]..sort())
        : <String>[];
    chain.add(<String, dynamic>{
      'step': idx,
      'stage': pyGet(stage, 'stage', 'step_$idx'),
      'inputs': sortedList(pyGet(stage, 'inputs', null)),
      'outputs': sortedList(pyGet(stage, 'outputs', null)),
    });
  }
  return <String, dynamic>{'stages': chain, 'depth': chain.length};
}

/// Port of core.evidence.noninferable_scope_engine.model_noninferable_regions.
Map<String, dynamic> modelNoninferableRegions(Map<dynamic, dynamic> inferred,
    List<dynamic> evidence, List<dynamic> noninferences,
    {int minEvidence = 2}) {
  final regions = <dynamic>[...noninferences];
  if (evidence.length < minEvidence && pyTruthy(inferred)) {
    regions.add('semantic:insufficient_evidence');
  }
  if (pyTruthy(inferred) && !pyTruthy(evidence)) {
    regions.add('semantic:ungrounded_inference');
  }
  final voids = <String>{for (final r in regions) r as String}.toList()..sort();
  return <String, dynamic>{
    'noninferable_regions': voids,
    'inference_voids': voids,
    'semantic_boundaries': <String, dynamic>{
      'min_evidence': minEvidence,
      'blocked': voids.isNotEmpty,
    },
    'unsupported_scope': <String, dynamic>{
      'regions': voids,
      'count': voids.length,
    },
    'epistemic_limits': <String, dynamic>{
      'cannot_determine': voids.isNotEmpty,
      'reason': voids.isNotEmpty ? 'insufficient_evidence' : null,
    },
  };
}

/// Port of core.evidence.noninference_engine.model_noninference.
Map<String, dynamic> modelNoninference(
    List<dynamic> evidence,
    Map<dynamic, dynamic> inferred,
    Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> reconciled,
    [int minEvidence = 2]) {
  final refused = <String>[];
  final noninferences = <String>[];
  if (evidence.length < minEvidence && pyTruthy(inferred)) {
    final inferKeys = <String>[for (final k in inferred.keys) 'infer:$k']
      ..sort();
    refused.addAll(inferKeys);
    noninferences.add('entity_link_without_evidence');
  }
  if (!pyDeepEq(reconciled, observed) && evidence.length < minEvidence) {
    noninferences.add('reconcile_without_evidence');
    refused.add('reconcile:unsupported');
  }
  if (pyTruthy(inferred) && !pyTruthy(observed)) {
    noninferences.add('inferred_without_observation');
  }
  return <String, dynamic>{
    'noninferences': noninferences.toSet().toList()..sort(),
    'refused_inferences': refused.toSet().toList()..sort(),
    'boundary_conditions': <String>['min_evidence=$minEvidence'],
    'suppression_basis': <String, dynamic>{
      'evidence_count': evidence.length,
      'allowed': evidence.length >= minEvidence,
    },
  };
}

/// Port of core.evidence.provenance_engine.build_provenance.
Map<String, dynamic> buildProvenance(List<dynamic>? evidence,
    [List<dynamic>? sources,
    dynamic grounding,
    dynamic lineage,
    dynamic confidenceBasis]) {
  List<String> sortedSet(List<dynamic> xs) => <String>{
        for (final x in xs)
          if (pyTruthy(x)) pyToStr(x)
      }.toList()
        ..sort();
  final ev = sortedSet(evidence ?? const <dynamic>[]);
  final srcInput = pyTruthy(sources)
      ? sources!
      : (pyTruthy(evidence) ? evidence! : const <dynamic>[]);
  final src = sortedSet(srcInput);
  return <String, dynamic>{
    'evidence': ev,
    'sources': src,
    'grounding': grounding is Map ? grounding : <dynamic, dynamic>{},
    'lineage': lineage is Map ? lineage : <dynamic, dynamic>{},
    'confidence_basis':
        confidenceBasis is Map ? confidenceBasis : <dynamic, dynamic>{},
  };
}

/// Port of core.evidence.recursive_entropy_engine.model_recursive_entropy.
Map<String, dynamic> modelRecursiveEntropy(List<dynamic> ambiguities,
    List<dynamic> uncertainties, dynamic contradicted, int depth) {
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  final base = ambiguities.length * 0.1 +
      uncertainties.length * 0.08 +
      (pairs as List).length * 0.15;
  final entropy = pythonRound(math.min(1.0, base + depth * 0.05), 3);
  return <String, dynamic>{
    'entropy': entropy,
    'depth': depth,
    'preserved': true,
    'suppress_recursive_stabilization': entropy >= 0.15,
    'suppress_recursive_closure': entropy >= 0.2,
  };
}

/// Port of core.evidence.recursive_instability_engine.model_recursive_instability.
Map<String, dynamic> modelRecursiveInstability(
    List<dynamic> unstableRegions, int depth, int evidenceCount) {
  final regions = List<dynamic>.from(unstableRegions);
  if (depth > 2) regions.add('recursive:depth_${depth}_instability');
  if (evidenceCount < 2) regions.add('recursive:weak_evidence');
  final unique = <String>{for (final r in regions) r as String}.toList()
    ..sort();
  return <String, dynamic>{
    'preserved': true,
    'unstable': pyTruthy(regions),
    'regions': unique,
    'depth': depth,
  };
}

/// Port of core.evidence.recursive_lineage_engine.preserve_recursive_lineage.
Map<String, dynamic> preserveRecursiveLineage(
    dynamic lineage,
    List<dynamic> evidence,
    List<dynamic> ambiguities,
    List<dynamic> uncertainties,
    dynamic contradicted) {
  final stages =
      lineage is Map ? pyGet(lineage, 'stages', <dynamic>[]) : <dynamic>[];
  final int depth;
  if (stages is List) {
    depth = stages.length;
  } else {
    final d = pyGet(lineage as Map, 'depth', 0);
    depth = pyTruthy(d) ? (d as num).toInt() : 0;
  }
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  return <String, dynamic>{
    'depth': depth,
    'evidence_ancestry': List<dynamic>.from(evidence),
    'ambiguity_ancestry': List<dynamic>.from(ambiguities),
    'uncertainty_ancestry': List<dynamic>.from(uncertainties),
    'contradiction_ancestry': List<dynamic>.from(pairs as List),
    'entropy_ancestry_preserved': true,
    'instability_ancestry_preserved': true,
    'decay_prevented': true,
  };
}

/// Port of core.evidence.speculative_coherence_engine.detect_speculative_coherence.
Map<String, dynamic> detectSpeculativeCoherence(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final speculative = !pyDeepEq(reconciled, inferred) &&
      evidence.length < 2 &&
      pyTruthy(inferred);
  return <String, dynamic>{
    'speculative': speculative,
    'suppress_coherence': speculative,
    'density': speculative ? 1.0 : 0.0,
  };
}

/// Port of core.evidence.semantic_support_engine.build_support.
Map<String, dynamic> buildSupport(List<dynamic>? evidence,
    [List<dynamic>? extra]) {
  final combined = <dynamic>[
    ...evidence ?? const <dynamic>[],
    ...extra ?? const <dynamic>[]
  ];
  final items = <String>{
    for (final e in combined)
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  return <String, dynamic>{
    'supporting_evidence': items,
    'support_count': items.length,
    'support_strength':
        pythonRound(math.min(1.0, 0.15 + items.length * 0.1), 3),
  };
}

/// Port of core.evidence.semantic_weakness_engine.build_weaknesses.
Map<String, dynamic> buildWeaknesses(
    List<dynamic> evidence, List<dynamic>? ambiguities,
    [int minEvidence = 2]) {
  final weaknesses = <String>[];
  if (evidence.length < minEvidence) weaknesses.add('insufficient_evidence');
  for (final a in ambiguities ?? const <dynamic>[]) {
    weaknesses.add('ambiguity:$a');
  }
  final unique = weaknesses.toSet().toList()..sort();
  return <String, dynamic>{
    'weaknesses': unique,
    'weak_evidence': evidence.length < minEvidence,
    'weakness_count': weaknesses.length,
  };
}

/// Port of core.evidence.traceability_engine.build_traceability.
Map<String, dynamic> buildTraceability(
    [List<dynamic>? evidence, dynamic lineage, List<dynamic>? stages]) {
  final ev = <String>{
    for (final e in evidence ?? const <dynamic>[])
      if (pyTruthy(e)) pyToStr(e)
  }.toList()
    ..sort();
  final chain = <String>{
    for (final s in stages ?? const <dynamic>[]) s as String
  }.toList()
    ..sort();
  return <String, dynamic>{
    'evidence_chain': ev,
    'lineage_ref': pyTruthy(lineage) ? lineage : <dynamic, dynamic>{},
    'stages': chain,
    'deterministic': true,
    'reconstructible': pyTruthy(ev),
  };
}

/// Port of core.evidence.truth_refusal_engine.refuse_unsupported_stabilization.
Map<String, dynamic> refuseUnsupportedStabilization(List<dynamic> suppressed) {
  final refusals = <Map<String, dynamic>>[
    for (final s in suppressed)
      <String, dynamic>{
        'target': pyGet(s as Map, 'reason', 'stabilization'),
        'message': 'truthfully_incomplete',
      }
  ];
  final reasons = <String>{for (final r in refusals) r['message'] as String}
      .toList()
    ..sort();
  return <String, dynamic>{
    'truth_refusals': refusals,
    'stabilization_failures': <dynamic>[
      for (final s in suppressed) pyGet(s as Map, 'reason', null)
    ],
    'truth_boundary_failures': <dynamic>[
      for (final s in suppressed)
        pyGet(
            (pyGet(s as Map, 'truth_boundary_violation', <dynamic, dynamic>{})
                as Map),
            'type',
            null)
    ],
    'termination_reasons': reasons,
  };
}
