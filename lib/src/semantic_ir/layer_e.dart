/// Phase E of the Category-A semantic-IR port — fourth topological layer
/// (5 portable functions; `compile_repository_ir` is parse_source-gated via
/// `build_repository_execution_ir` and deferred). Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'document_composites.dart'
    show extractInstructionalFlow, parseRhetoricalStructure;
import 'evidence_layer_b.dart'
    show applyConfidenceDegradation, detectUnsupportedStabilization;
import 'evidence_leaves.dart';
import 'evidence_leaves_2.dart';
import 'evidence_leaves_3.dart';
import 'evidence_leaves_4.dart';
import 'layer_d.dart'
    show applyConfidenceCollapse, detectSemanticSpeculation,
        modelConceptTransitions;
import 'pressure_engines.dart';
import 'py_compat.dart';

dynamic _orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;

/// Port of core.documents.document_dependency_graph_engine
/// .build_document_dependency_graph.
Map<String, dynamic> buildDocumentDependencyGraph(String text) {
  final flow = extractInstructionalFlow(text);
  final trans = modelConceptTransitions(text);
  final steps = flow['steps'] as List;
  final nodes = <Map<String, dynamic>>[
    for (var i = 0; i < steps.length; i++)
      <String, dynamic>{
        'id': pyGet(steps[i] as Map, 'title', 'step$i'),
        'kind': 'step',
      }
  ];
  return <String, dynamic>{
    'nodes': nodes,
    'edges': pyGet(trans, 'transitions', const <dynamic>[]),
    'prerequisites': pyGet(flow, 'prerequisites', const <dynamic>[]),
  };
}

/// Port of core.documents.semantic_transition_engine.model_semantic_transitions.
Map<String, dynamic> modelSemanticTransitions(String text) {
  final trans = modelConceptTransitions(text);
  final rhet = parseRhetoricalStructure(text);
  final headings = <Map<dynamic, dynamic>>[
    for (final u in pyGet(rhet, 'units', const <dynamic>[]) as List)
      if (pyGet(u as Map, 'type', null) == 'heading') u
  ];
  final transitions = List<dynamic>.from(
      pyGet(trans, 'transitions', const <dynamic>[]) as List);
  for (var i = 0; i < headings.length - 1; i++) {
    transitions.add(<String, dynamic>{
      'from': pyGet(headings[i], 'title', ''),
      'to': pyGet(headings[i + 1], 'title', ''),
      'kind': 'section_transition',
    });
  }
  return <String, dynamic>{
    'transitions': transitions,
    'count': transitions.length,
    'evidence': <String>['discourse:transitions'],
  };
}

/// Port of core.evidence.recursive_confidence_decay_engine
/// .apply_recursive_confidence_decay (kw-only args become trailing
/// positionals, py2ts order).
Map<String, dynamic> applyRecursiveConfidenceDecay(
  num score,
  Map<dynamic, dynamic> fragility, [
  int depth = 0,
  int closureCount = 0,
  num driftPressure = 0.0,
  num entropy = 0.0,
  int contradictionCount = 0,
  int ambiguityCount = 0,
  int uncertaintyCount = 0,
]) {
  final base = applyConfidenceCollapse(
      score,
      fragility,
      0,
      closureCount,
      driftPressure,
      depth * 0.05,
      contradictionCount,
      ambiguityCount,
      uncertaintyCount);
  final depthPen = pythonRound(math.min(0.35, depth * 0.08), 3);
  final entropyPen = pythonRound(math.min(0.2, entropy * 0.25), 3);
  final finalScore = pythonRound(
      math.max(0.0, (base['score'] as num) - depthPen - entropyPen), 3);
  return <String, dynamic>{
    ...base,
    'score': finalScore,
    'recursive_decay': <String, dynamic>{
      'depth_penalty': depthPen,
      'entropy_penalty': entropyPen,
      'final': finalScore,
    },
    'recursive_pressure': <String, dynamic>{
      'depth': depth,
      'closure': closureCount,
    },
    'recursive_penalties': <String, dynamic>{
      'depth': depthPen,
      'entropy': entropyPen,
    },
    'recursive_entropy': <String, dynamic>{'level': entropy},
    'recursive_instability': <String, dynamic>{'pressure': driftPressure},
    'deterministic_inputs': <dynamic>[
      ...pyGet(base, 'deterministic_inputs', const <dynamic>[]) as List,
      'depth=$depth',
      'entropy=${pyToStr(entropy)}',
    ],
  };
}

/// Port of core.evidence.cognitive_humility_engine.apply_cognitive_humility.
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyCognitiveHumility(Map<dynamic, dynamic> bundle) {
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
  // Python binds `observed` but the engine never reads it downstream.
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final noninferences = List<dynamic>.from(_orElse(
      pyGet(bundle, 'noninferences',
          pyGet(bundle, 'noninference_reasons', const <dynamic>[])),
      const <dynamic>[]) as List);
  dynamic fragility = _orElse(
      pyGet(bundle, 'fragility', pyGet(bundle, 'fragile', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  if (fragility is! Map) {
    fragility = modelFragility(evidence, ambiguities, uncertainties.length);
  }

  final speculation = detectSemanticSpeculation(evidence, inferred, reconciled);
  final suppressedSpeculation =
      pyGet(speculation, 'suppressed_speculation', const <dynamic>[]) as List;
  final scope = modelNoninferableRegions(inferred, evidence, noninferences);
  final noninferableRegions =
      pyGet(scope, 'noninferable_regions', const <dynamic>[]) as List;

  final uncVis = exposeUncertaintyVisibility(uncertainties, ambiguities, 0.5);
  final ambVis = exposeAmbiguityVisibility(ambiguities, 0.5);
  final uncPressure = computeUncertaintyPressure(uncertainties, ambiguities);
  final ambPressure = computeAmbiguityPressure(ambiguities);

  final contradicted = _orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}), <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? (pyGet(contradicted, 'pairs', const <dynamic>[]) as List).length
      : 0;
  final parserBasis = _orElse(pyGet(bundle, 'parser_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final parserWeak =
      (_orElse(pyGet(parserBasis, 'symbol_count', 0), 0) as num).toInt() < 1;

  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final rawScore = (pyGet(cb, 'score', 0.5) as num).toDouble();
  final escalation =
      blockUnsupportedConfidenceEscalation(rawScore, evidence.length);
  final degraded = applyConfidenceDegradation(
      escalation['capped_score'] as num,
      fragility,
      pairs,
      ambiguities.length,
      uncertainties.length,
      (_orElse(pyGet(bundle, 'unsupported_expansions', const <dynamic>[]),
              const <dynamic>[]) as List)
          .length,
      suppressedSpeculation.length,
      parserWeak);

  final selfLimitation = applySemanticSelfLimitation(
      evidence, suppressedSpeculation, noninferableRegions);
  final refusal =
      refuseUnsupportedConclusions(noninferableRegions, suppressedSpeculation);
  final termination = terminateInferenceChain(
      List<dynamic>.from(_orElse(
          pyGet(bundle, 'refused_inferences', const <dynamic>[]),
          const <dynamic>[]) as List),
      suppressedSpeculation);
  final limits =
      semanticLimits(evidence.length, noninferableRegions, selfLimitation);

  bundle['humility'] = <String, dynamic>{
    'self_limiting': true,
    'prefer_cannot_determine': true,
    'speculation_suppressed': suppressedSpeculation.length,
    'uncertainty_pressure': pyGet(uncPressure, 'pressure', 0),
    'ambiguity_pressure': pyGet(ambPressure, 'pressure', 0),
  };
  bundle['noninferable_regions'] = noninferableRegions;
  bundle['suppressed_speculation'] = suppressedSpeculation;
  bundle['confidence_degradation'] =
      pyGet(degraded, 'degradation', <dynamic, dynamic>{});
  bundle['uncertainty_visibility'] = uncVis;
  bundle['ambiguity_visibility'] = ambVis;
  bundle['semantic_fragility'] = fragility;
  bundle['self_limitation'] = selfLimitation;
  bundle['refusals'] = pyGet(refusal, 'refusals', const <dynamic>[]);
  bundle['terminated_inferences'] =
      pyGet(termination, 'terminated_inferences', const <dynamic>[]);
  bundle['semantic_limits'] = limits;
  bundle['termination_reasons'] =
      pyGet(refusal, 'termination_reasons', const <dynamic>[]);
  bundle['unsupported_regions'] =
      pyGet(refusal, 'unsupported_regions', const <dynamic>[]);
  bundle['inference_voids'] = pyGet(scope, 'inference_voids', const <dynamic>[]);
  bundle['epistemic_limits'] =
      pyGet(scope, 'epistemic_limits', <dynamic, dynamic>{});
  bundle['boundaries'] = <dynamic, dynamic>{
    ...pyGet(bundle, 'boundaries', <dynamic, dynamic>{}) as Map,
    ...pyGet(scope, 'semantic_boundaries', <dynamic, dynamic>{}) as Map,
  };
  bundle['confidence_basis'] = <dynamic, dynamic>{...cb, ...degraded};
  return bundle;
}

/// Port of core.evidence.truth_preservation_engine.apply_truth_preservation.
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyTruthPreservation(Map<dynamic, dynamic> bundle) {
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
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted',
          pyGet(bundle, 'contradictions', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  final unstableRegions = List<dynamic>.from(_orElse(
          pyGet(bundle, 'unstable_regions', const <dynamic>[]),
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

  final stabilization =
      detectUnsupportedStabilization(evidence, inferred, reconciled);
  final suppressedStab =
      pyGet(stabilization, 'suppressed_stabilizations', const <dynamic>[])
          as List;
  final reinforcement =
      detectSemanticSelfReinforcement(inferred, reconciled, evidence);
  final entropy = modelSemanticEntropy(ambiguities, uncertainties, contradicted);
  final evDecay = modelEvidenceDecay(evidence);
  final semDecay = modelSemanticDecay(
      evidence, inferred, pyGet(stabilization, 'count', 0) as int);
  final truthBound = modelTruthBoundaries(evidence);
  final instability =
      preserveInstability(unstableRegions, evidence, suppressedStab);
  final semInstability = modelSemanticInstability(
      instability['regions'] as List, entropy, evidence);

  // Python computes ev_pressure but never uses it; the call is pure.
  computeEvidenceDecayPressure(evidence.length);
  final truthPressure = computeTruthBoundaryPressure(
      truthBound['truth_bounded'] as bool, entropy['entropy'] as num);

  final pairs = contradicted is Map
      ? (pyGet(contradicted, 'pairs', const <dynamic>[]) as List).length
      : 0;
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  num rawScore = (pyGet(cb, 'score', 0.5) as num).toDouble();
  final echo = detectConfidenceEcho(rawScore, const <dynamic>[]);
  if (pyTruthy(pyGet(echo, 'suppress', null))) {
    rawScore = echo['collapse_to'] as num;
  }

  final collapsed = applyConfidenceCollapse(
      rawScore,
      fragility,
      pyTruthy(pyGet(reinforcement, 'reinforcement_detected', null)) ? 1 : 0,
      pyGet(stabilization, 'count', 0) as int,
      semDecay['decay_rate'] as num,
      pyGet(truthPressure, 'pressure', 0) as num,
      pairs,
      ambiguities.length,
      uncertainties.length,
      pyGet(evDecay, 'incomplete', false) as bool);

  final refusal = refuseUnsupportedStabilization(suppressedStab);
  // Python computes termination but never uses it; the call is pure.
  terminateStabilization(suppressedStab, semInstability['regions'] as List);
  final truthLimits = semanticTruthLimits(entropy, instability);

  bundle['truth_preservation'] = <String, dynamic>{
    'preserved': true,
    'prefer_truthfully_incomplete': true,
    'stabilization_suppressed': pyGet(stabilization, 'count', 0),
    'echo_suppressed': pyGet(echo, 'suppress', false),
  };
  bundle['semantic_decay'] = semDecay;
  bundle['confidence_collapse'] =
      pyGet(collapsed, 'collapse_pressure', <dynamic, dynamic>{});
  bundle['instability'] = <dynamic, dynamic>{...instability, ...semInstability};
  bundle['truth_boundaries'] = truthBound;
  bundle['unsupported_stabilization'] = suppressedStab;
  bundle['semantic_entropy'] = entropy;
  bundle['evidence_decay'] = evDecay;
  bundle['semantic_instability'] = semInstability;
  bundle['truth_pressure'] = truthPressure;
  bundle['entropy'] = entropy;
  bundle['truth_refusals'] = pyGet(refusal, 'truth_refusals', const <dynamic>[]);
  bundle['stabilization_failures'] =
      pyGet(refusal, 'stabilization_failures', const <dynamic>[]);
  bundle['truth_boundary_failures'] =
      pyGet(refusal, 'truth_boundary_failures', const <dynamic>[]);
  bundle['termination_reasons'] = (<String>{
    for (final x in pyGet(bundle, 'termination_reasons', const <dynamic>[])
        as List)
      x as String,
    for (final x
        in pyGet(refusal, 'termination_reasons', const <dynamic>[]) as List)
      x as String,
  }.toList()
    ..sort());
  bundle['semantic_limits'] = <dynamic, dynamic>{
    ...pyGet(bundle, 'semantic_limits', <dynamic, dynamic>{}) as Map,
    ...truthLimits,
  };
  bundle['confidence_basis'] = <dynamic, dynamic>{...cb, ...collapsed};
  return bundle;
}
