/// Phase D of the Category-A semantic-IR port — third topological layer
/// (4 portable functions; `build_repository_execution_ir` and
/// `model_runtime_state` are parse_source-gated and deferred to the
/// parser-subsystem phase). Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'composites_c.dart' show parseSemanticDiscourse;
import 'evidence_layer_b.dart' show applyRealityConstraints;
import 'evidence_layer_c.dart'
    show
        applyRealityBoundedConfidence,
        collectSuppressedSpeculation,
        collectUnsupportedContinuity;
import 'evidence_leaves.dart';
import 'evidence_leaves_2.dart';
import 'evidence_leaves_3.dart'
    show detectSpeculativeCoherence, preserveEpistemicBoundaries;
import 'evidence_leaves_4.dart'
    show detectSemanticDrift, modelSemanticStability;
import 'pressure_engines.dart'
    show computeEvidenceBoundaryPressure, computeSemanticBoundaryPressure;
import 'py_compat.dart';

dynamic _orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;

/// Port of core.documents.concept_transition_engine.model_concept_transitions.
Map<String, dynamic> modelConceptTransitions(String text) {
  final d = parseSemanticDiscourse(text);
  final transitions = <Map<String, dynamic>>[
    for (final e in pyGet(d, 'transitions', const <dynamic>[]) as List)
      if (e is Map &&
          pyTruthy(pyGet(e, 'from', null)) &&
          pyTruthy(pyGet(e, 'to', null)))
        <String, dynamic>{'from': e['from'], 'to': e['to'], 'kind': 'discourse'}
  ];
  return <String, dynamic>{
    'transitions': transitions,
    'count': transitions.length,
  };
}

/// Port of core.evidence.semantic_speculation_engine.detect_semantic_speculation.
Map<String, dynamic> detectSemanticSpeculation(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final suppressed =
      collectSuppressedSpeculation(evidence, inferred, reconciled);
  return <String, dynamic>{
    'speculative': suppressed.isNotEmpty,
    'suppressed_speculation': suppressed,
    'density':
        pythonRound(suppressed.length / math.max(1, inferred.length + 1), 3),
  };
}

/// Port of core.evidence.confidence_collapse_engine.apply_confidence_collapse
/// (kw-only args become trailing positionals, py2ts order).
Map<String, dynamic> applyConfidenceCollapse(
  num score,
  Map<dynamic, dynamic> fragility, [
  int reinforcementCount = 0,
  int stabilizationCount = 0,
  num decayPressure = 0.0,
  num truthBoundaryPressure = 0.0,
  int contradictionCount = 0,
  int ambiguityCount = 0,
  int uncertaintyCount = 0,
  bool incompleteness = false,
]) {
  final base = applyRealityBoundedConfidence(
      score,
      fragility,
      decayPressure,
      stabilizationCount,
      false,
      truthBoundaryPressure,
      contradictionCount,
      ambiguityCount,
      uncertaintyCount);
  final reinfPen = pythonRound(math.min(0.3, reinforcementCount * 0.12), 3);
  final stabPen = pythonRound(math.min(0.25, stabilizationCount * 0.1), 3);
  final incomPen = incompleteness ? 0.08 : 0.0;
  final collapse = pythonRound(reinfPen + stabPen + incomPen, 3);
  final finalScore =
      pythonRound(math.max(0.0, (base['score'] as num) - collapse), 3);
  return <String, dynamic>{
    ...base,
    'score': finalScore,
    'collapse_pressure': <String, dynamic>{
      'reinforcement': reinfPen,
      'stabilization': stabPen,
      'incompleteness': incomPen,
      'total': collapse,
    },
    'truth_penalties': <String, dynamic>{
      'boundary': truthBoundaryPressure,
      'decay': decayPressure,
    },
    'instability_penalties': <String, dynamic>{'amount': stabPen},
    'reinforcement_penalties': <String, dynamic>{
      'amount': reinfPen,
      'count': reinforcementCount,
    },
    'deterministic_inputs': <dynamic>[
      ...pyGet(base, 'deterministic_inputs', const <dynamic>[]) as List,
      'reinf=$reinforcementCount',
      'stab=$stabilizationCount',
      'incomplete=${pyToStr(incompleteness)}',
    ],
  };
}

/// Port of core.evidence.reality_alignment_engine.apply_reality_alignment.
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyRealityAlignment(Map<dynamic, dynamic> bundle) {
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final ambiguities = List<dynamic>.from(_orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final uncertaintiesRaw = _orElse(
      pyGet(bundle, 'uncertainties',
          pyGet(bundle, 'uncertain', const <dynamic>[])),
      const <dynamic>[]);
  final uncertainties = uncertaintiesRaw is Map
      ? uncertaintiesRaw.keys.toList()
      : List<dynamic>.from(uncertaintiesRaw as List);
  final observed = _orElse(
          pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{})
      as Map;
  final inferred = _orElse(
          pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{})
      as Map;
  final reconciled = _orElse(pyGet(bundle, 'reconciled', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final noninferable = List<dynamic>.from(_orElse(
      pyGet(bundle, 'noninferable_regions', const <dynamic>[]),
      const <dynamic>[]) as List);
  dynamic fragility = _orElse(
      pyGet(bundle, 'fragility',
          pyGet(bundle, 'semantic_fragility', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  if (fragility is! Map) {
    fragility = <String, dynamic>{
      'level': 'medium',
      'confidence_limits': <String, dynamic>{'max_score': 0.7},
    };
  }

  final parserBasis = _orElse(
      pyGet(bundle, 'parser_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final parserGrounded =
      (_orElse(pyGet(parserBasis, 'symbol_count', 0), 0) as num).toInt() > 0 ||
          pyTruthy(pyGet(bundle, 'grounding', null));

  final drift = detectSemanticDrift(observed, inferred, reconciled, evidence);
  final unsupportedContinuity =
      collectUnsupportedContinuity(evidence, inferred, reconciled);
  final momentum = measureSemanticMomentum(inferred.length, evidence.length);
  final coherence = detectSpeculativeCoherence(evidence, inferred, reconciled);
  final narrative =
      detectNarrativeHallucination(inferred, evidence, parserGrounded);

  final evBound = modelEvidenceBoundaries(evidence);
  final ontoBound = modelOntologyBoundaries(
      evidence, pyTruthy(inferred) && !pyTruthy(evidence));
  final topoBound = modelTopologyBoundaries(evidence, parserGrounded);
  final semBound =
      modelSemanticBoundaries(inferred, evBound['bounded'] as bool);

  final stability = modelSemanticStability(evidence,
      drift['drift_pressure'] as num, unsupportedContinuity, parserGrounded);
  final constraints = applyRealityConstraints(
      evidence, parserGrounded, drift['drift_pressure'] as num);
  final epistemicBound = preserveEpistemicBoundaries(
      evidence, noninferable, stability['unstable_regions'] as List);
  final stabBound =
      modelStabilityBoundary(stability['unstable_regions'] as List);
  // Python computes ev_pressure but never uses it; the call is pure.
  computeEvidenceBoundaryPressure(evidence.length);
  final boundPressure = computeSemanticBoundaryPressure(
      pyTruthy(pyGet(stabBound, 'broken', false)) ? 1.0 : 0.0,
      drift['drift_pressure'] as num);

  final contradicted = _orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? (pyGet(contradicted, 'pairs', const <dynamic>[]) as List).length
      : 0;
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final boundedConf = applyRealityBoundedConfidence(
      (pyGet(cb, 'score', 0.5) as num).toDouble(),
      fragility,
      drift['drift_pressure'] as num,
      unsupportedContinuity.length,
      !parserGrounded,
      pyGet(boundPressure, 'pressure', 0) as num,
      pairs,
      ambiguities.length,
      uncertainties.length);

  final continuityRefusal = refuseUnsupportedContinuity(unsupportedContinuity);
  // Python computes termination but never uses it; the call is pure.
  terminateSemanticChain(
      stability['unstable_regions'] as List,
      pyGet(continuityRefusal, 'continuity_refusals', const <dynamic>[])
          as List);
  final stabLimits = semanticStabilityLimits(stability);

  bundle['reality_alignment'] = <String, dynamic>{
    'aligned': (stability['stable'] as bool) && (evBound['bounded'] as bool),
    'parser_grounded': parserGrounded,
    'drift_suppressed': drift['suppress_continuation'],
    'continuity_suppressed': unsupportedContinuity.isNotEmpty,
    'narrative_suppressed': pyGet(narrative, 'suppressed', false),
  };
  bundle['semantic_boundaries'] = semBound;
  bundle['ontology_boundaries'] = ontoBound;
  bundle['topology_boundaries'] = topoBound;
  bundle['evidence_boundaries'] = evBound;
  bundle['semantic_stability'] = stability;
  bundle['drift_pressure'] = drift;
  bundle['unsupported_continuity'] = unsupportedContinuity;
  bundle['reality_constraints'] = constraints;
  bundle['unstable_regions'] = stability['unstable_regions'];
  bundle['boundary_pressure'] = boundPressure;
  bundle['continuity_refusals'] =
      pyGet(continuityRefusal, 'continuity_refusals', const <dynamic>[]);
  bundle['stability_failures'] = stability['unstable_regions'];
  bundle['boundary_failures'] =
      pyGet(continuityRefusal, 'boundary_failures', const <dynamic>[]);
  bundle['semantic_limits'] = <dynamic, dynamic>{
    ...pyGet(bundle, 'semantic_limits', <dynamic, dynamic>{}) as Map,
    ...stabLimits,
    'ontology': ontologyLimits(ontoBound),
    'topology': topologyLimits(topoBound),
  };
  bundle['termination_reasons'] = (<String>{
    for (final x
        in pyGet(bundle, 'termination_reasons', const <dynamic>[]) as List)
      x as String,
    for (final x
        in pyGet(continuityRefusal, 'termination_reasons', const <dynamic>[])
            as List)
      x as String,
  }.toList()
    ..sort());
  bundle['epistemic_boundaries'] = epistemicBound;
  bundle['speculative_coherence'] = coherence;
  bundle['narrative_hallucination'] = narrative;
  bundle['semantic_momentum'] = momentum;
  bundle['confidence_basis'] = <dynamic, dynamic>{...cb, ...boundedConf};
  return bundle;
}
