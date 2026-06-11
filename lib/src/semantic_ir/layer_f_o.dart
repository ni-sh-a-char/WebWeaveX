/// Phases F–O (document side) of the Category-A semantic-IR port — the final
/// topological ladder from `apply_recursive_reality_integrity` up through
/// `attach_epistemic_state` (the full epistemic chain),
/// `build_semantic_integrity_object`, `structure_cognition`, the tutorial
/// chain, `build_document_semantic_ir`, `compile_document_ir`, and the
/// document-side dispatchers `query_documents` / `reason_discourse_semantic`.
/// The repository-side F–O functions (`query_repository`,
/// `reason_runtime_semantic`, `compile_repository_ir`) remain
/// parse_source-gated. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'composites_b.dart' show applyContradictionRestraint, emptyDocumentIr;
import 'composites_c.dart'
    show analyzeInstructionalSemantics, buildCoreferenceGraph;
import 'document_composites.dart'
    show buildArgumentDependencies, extractSections, parseRhetoricalStructure;
import 'evidence_layer_b.dart';
import 'evidence_layer_c.dart';
import 'evidence_leaves.dart';
import 'evidence_leaves_2.dart';
import 'evidence_leaves_3.dart';
import 'evidence_leaves_4.dart';
import 'ir_base.dart' show emptyLineage, mergeEvidence;
import 'layer_d.dart' show applyRealityAlignment;
import 'layer_e.dart'
    show
        applyCognitiveHumility,
        applyRecursiveConfidenceDecay,
        applyTruthPreservation,
        buildDocumentDependencyGraph,
        modelSemanticTransitions;
import 'pressure_engines.dart' show computeRecursiveBoundaryPressure;
import 'py_compat.dart';

dynamic _orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;

// ---------------------------------------------------------------------------
// Phase F
// ---------------------------------------------------------------------------

/// Port of core.documents.concept_progression_engine.model_concept_progression.
Map<String, dynamic> modelConceptProgression(String text) {
  final trans = modelSemanticTransitions(text);
  final transitions = pyGet(trans, 'transitions', const <dynamic>[]) as List;
  final progression = <Map<String, dynamic>>[
    for (var i = 0; i < transitions.length; i++)
      <String, dynamic>{
        'index': i,
        'from': pyGet(transitions[i] as Map, 'from', null),
        'to': pyGet(transitions[i] as Map, 'to', null),
        'introduces': pyGet(transitions[i] as Map, 'to', null),
      }
  ];
  return <String, dynamic>{
    'progression': progression,
    'concept_count': progression.length,
    'deterministic_inputs': <String>['concepts=${progression.length}'],
  };
}

/// Private `_lineage_depth` of the recursive-reality-integrity engine.
int _lineageDepth(Map<dynamic, dynamic> bundle) {
  final lineage =
      _orElse(pyGet(bundle, 'lineage', <dynamic, dynamic>{}), <dynamic, dynamic>{})
          as Map;
  final stages = pyGet(lineage, 'stages', const <dynamic>[]);
  if (stages is List && stages.isNotEmpty) return stages.length;
  return (_orElse(pyGet(lineage, 'depth', 0), 0) as num).toInt();
}

/// Port of core.evidence.recursive_reality_integrity_engine
/// .apply_recursive_reality_integrity (+ private `_lineage_depth`).
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyRecursiveRealityIntegrity(
    Map<dynamic, dynamic> bundle) {
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
  final instabilityObj = pyGet(bundle, 'instability', <dynamic, dynamic>{});
  final unstableRegions = List<dynamic>.from(pyGet(
      bundle,
      'unstable_regions',
      instabilityObj is Map
          ? pyGet(instabilityObj, 'regions', const <dynamic>[])
          : const <dynamic>[]) as List);
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

  final depth = _lineageDepth(bundle);
  final closure =
      detectRecursiveSemanticClosure(depth, inferred, reconciled, evidence);
  final suppressed =
      pyGet(closure, 'suppressed_closures', const <dynamic>[]) as List;
  final drift = detectRecursiveDrift(depth, evidence.length, inferred.length);
  final rentropy =
      modelRecursiveEntropy(ambiguities, uncertainties, contradicted, depth);
  final rinstability =
      modelRecursiveInstability(unstableRegions, depth, evidence.length);
  final rboundaries = modelRecursiveTruthBoundaries(depth, evidence.length);
  final runcertainty = preserveRecursiveUncertainty(uncertainties, depth);
  final lineageP = preserveRecursiveLineage(
      pyGet(bundle, 'lineage', <dynamic, dynamic>{}),
      evidence,
      ambiguities,
      uncertainties,
      contradicted);
  final provenanceP = preserveRecursiveProvenance(
      pyGet(bundle, 'sources', const <dynamic>[]) as List, lineageP);
  final ancestry = trackRecursiveEvidenceAncestry(evidence, depth);
  final selfConfirm = detectRecursiveSelfConfirmation(
      depth, pyDeepEq(reconciled, inferred), evidence.length);
  final coherenceInf = detectRecursiveCoherenceInflation(
      depth, pyGet(closure, 'closure_pressure', 0) as num);
  // Python computes coherence_inf and bound_pressure but never uses them in
  // the output; the calls are pure.
  // ignore: unused_local_variable
  final _ = coherenceInf;
  computeRecursiveBoundaryPressure(
      pyGet(rboundaries, 'erosion', 0) as num, depth);

  final pairs = contradicted is Map
      ? (pyGet(contradicted, 'pairs', const <dynamic>[]) as List).length
      : 0;
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  num rawScore = (pyGet(cb, 'score', 0.5) as num).toDouble();
  final echo = detectRecursiveConfidenceEcho(rawScore, depth, const <dynamic>[]);
  if (pyTruthy(pyGet(echo, 'suppress', null))) {
    rawScore = echo['decay_to'] as num;
  }

  final decayed = applyRecursiveConfidenceDecay(
      rawScore,
      fragility,
      depth,
      pyTruthy(pyGet(closure, 'closure_detected', null)) && suppressed.isNotEmpty
          ? suppressed.length
          : 0,
      drift['drift_pressure'] as num,
      rentropy['entropy'] as num,
      pairs,
      ambiguities.length,
      uncertainties.length);

  final refusal = refuseRecursiveStabilization(suppressed);
  // Python computes termination but never uses it; the call is pure.
  terminateRecursiveStabilization(suppressed, depth);
  final limits = recursiveRealityLimits(depth, rentropy);

  bundle['recursive_reality_integrity'] = <String, dynamic>{
    'preserved': true,
    'depth': depth,
    'closure_suppressed': pyGet(closure, 'closure_detected', false),
    'echo_suppressed': pyGet(echo, 'suppress', false),
    'self_confirmation_suppressed': pyGet(selfConfirm, 'suppress', false),
  };
  bundle['recursive_entropy'] = rentropy;
  bundle['recursive_instability'] = rinstability;
  bundle['recursive_truth_boundaries'] = rboundaries;
  bundle['recursive_drift'] = drift;
  bundle['recursive_semantic_closure'] = closure;
  bundle['recursive_confidence_decay'] =
      pyGet(decayed, 'recursive_decay', <dynamic, dynamic>{});
  bundle['recursive_uncertainty'] = runcertainty;
  bundle['recursive_lineage'] = lineageP;
  bundle['recursive_provenance'] = provenanceP;
  bundle['recursive_evidence_ancestry'] = ancestry;
  bundle['recursive_truth_refusals'] =
      pyGet(refusal, 'recursive_truth_refusals', const <dynamic>[]);
  bundle['recursive_stabilization_failures'] =
      pyGet(refusal, 'recursive_stabilization_failures', const <dynamic>[]);
  bundle['recursive_limits'] = <dynamic, dynamic>{
    ...limits,
    'ontology': recursiveOntologyLimits(depth),
    'topology': recursiveTopologyLimits(depth),
  };
  bundle['recursive_termination_reasons'] = (<String>{
    for (final x in pyGet(
            bundle, 'recursive_termination_reasons', const <dynamic>[])
        as List)
      x as String,
    for (final x in pyGet(
            refusal, 'recursive_termination_reasons', const <dynamic>[])
        as List)
      x as String,
  }.toList()
    ..sort());
  bundle['recursive_boundary_failures'] =
      pyGet(refusal, 'recursive_boundary_failures', const <dynamic>[]);
  bundle['confidence_basis'] = <dynamic, dynamic>{...cb, ...decayed};
  return bundle;
}

// ---------------------------------------------------------------------------
// Phase G — attach_epistemic_state (the full epistemic chain)
// ---------------------------------------------------------------------------

/// Port of core.evidence.epistemic_evidence_engine.attach_epistemic_state.
/// Mutates `bundle` and returns the fully layered epistemic bundle.
Map<dynamic, dynamic> attachEpistemicState(Map<dynamic, dynamic> bundle) {
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  var ambiguities = List<dynamic>.from(_orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}), <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final contradicting = <String>[
    for (final p in pairs) 'contradiction:${pyToStr(p)}'
  ];
  final parserBasis = _orElse(pyGet(bundle, 'parser_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final parserDensity =
      (_orElse(pyGet(parserBasis, 'symbol_count', 0), 0) as num).toInt();

  final support = buildSupport(evidence);
  final weaknesses = buildWeaknesses(evidence, ambiguities);
  final sufficiency = assessEvidenceSufficiency(evidence);
  final reliability = scoreReliability(evidence, ambiguities, pairs.length);
  final incompleteness = preserveIncompleteness(bundle);
  final insufficiency = markInsufficiency(bundle);
  final epistemicConfidence = scoreEpistemicConfidence(
      evidence, null, contradicting, ambiguities, parserDensity);
  final lineage = pyGet(bundle, 'lineage', <dynamic, dynamic>{}) as Map;
  final how = <String, dynamic>{
    'stages': pyGet(lineage, 'stages', const <dynamic>[]),
    'depth': pyGet(lineage, 'depth', 0),
  };

  bundle['support'] = support;
  bundle['weaknesses'] = weaknesses;
  bundle['evidence_sufficiency'] = sufficiency;
  bundle['reliability'] = reliability;
  bundle['epistemic_state'] = <dynamic, dynamic>{
    ...incompleteness,
    'insufficient': insufficiency['insufficient'],
    'confidence': epistemicConfidence['score'],
  };
  bundle['confidence_basis'] = epistemicConfidence;
  bundle['how'] = how;
  bundle = propagateUncertainty(bundle);
  if (pyTruthy(insufficiency['insufficient'])) {
    ambiguities = (<String>{
      for (final a in ambiguities) a as String,
      'insufficient_evidence',
    }.toList()
      ..sort());
    bundle['ambiguities'] = ambiguities;
  }
  bundle = applyCognitiveIntegrity(bundle);
  bundle = applyContradictionRestraint(bundle);
  final chain = applyRealityAlignment(
      applyCognitiveHumility(applyEpistemicRestraint(bundle)));
  return applyCivilizationalEpistemicOpenness(
      applyRecursiveEpistemicSovereignty(applyCognitiveAntiCapture(
          applyEpistemicCivilizationStability(
              applyRecursiveRealityIntegrity(applyTruthPreservation(chain))))));
}

// ---------------------------------------------------------------------------
// Phase H — build_semantic_integrity_object
// ---------------------------------------------------------------------------

/// Port of core.evidence.semantic_integrity_engine
/// .build_semantic_integrity_object (keyword params become positionals in
/// declaration order).
Map<dynamic, dynamic> buildSemanticIntegrityObject(
    [dynamic observed,
    dynamic parsedFacts,
    dynamic inferred,
    dynamic reconciled,
    dynamic contradicted,
    dynamic derived,
    List<dynamic>? ambiguities,
    dynamic parserPayload,
    List<dynamic>? lineageStages]) {
  final obs = observed is Map ? observed : <dynamic, dynamic>{};
  final pf = parsedFacts is Map ? parsedFacts : <dynamic, dynamic>{};
  final inf = inferred is Map ? inferred : <dynamic, dynamic>{};
  final rec = reconciled is Map ? reconciled : <dynamic, dynamic>{};
  final con = contradicted is Map ? contradicted : <dynamic, dynamic>{};
  final der = derived is Map ? derived : <dynamic, dynamic>{};
  final amb = <String>{
    for (final a in ambiguities ?? const <dynamic>[])
      if (pyTruthy(a)) pyToStr(a)
  }.toList()
    ..sort();

  final prov = pyTruthy(parserPayload)
      ? groundParser(parserPayload as Map)
      : buildProvenance(<String>['no_parser']);
  final confidence = scoreSemanticConfidence(parserPayload);
  final lineage = buildLineage(pyTruthy(lineageStages)
      ? lineageStages!
      : <dynamic>[
          <String, dynamic>{
            'stage': 'semantic_integrity',
            'inputs': pyGet(prov, 'sources', const <dynamic>[]),
            'outputs': <dynamic>[],
          }
        ]);
  final explain = buildExplainability(parserPayload, confidence, prov);

  final evidenceList = pyGet(prov, 'evidence', const <dynamic>[]);
  final traceability = buildTraceability(
      evidenceList as List,
      lineage,
      <dynamic>[
        for (final s in lineageStages ?? const <dynamic>[])
          if (s is Map) pyGet(s, 'stage', '')
      ]);
  final out = <dynamic, dynamic>{
    'observed': obs,
    'parsed': pf,
    'inferred': inf,
    'reconciled': rec,
    'contradicted': con,
    'derived': der,
    'ambiguities': amb,
    'evidence': evidenceList,
    'sources': pyGet(prov, 'sources', const <dynamic>[]),
    'grounding': pyGet(prov, 'grounding', <dynamic, dynamic>{}),
    'lineage': lineage,
    'confidence_basis': confidence,
    'why': explain,
    'parser_basis': pyGet(explain, 'parser_basis', <dynamic, dynamic>{}),
    'graph_basis': pyGet(explain, 'graph_basis', <dynamic, dynamic>{}),
    'semantic_basis': pyGet(explain, 'semantic_basis', <dynamic, dynamic>{}),
    'traceability': traceability,
    'contradictions': con,
  };
  return attachEpistemicState(applyFormalSemanticFoundation(out));
}

// ---------------------------------------------------------------------------
// Phase I — structure_cognition (+ apply_semantic_uncertainty, which Python
// imports function-locally and the DAG generator could not see)
// ---------------------------------------------------------------------------

/// Port of core.semantic.semantic_uncertainty_engine.apply_semantic_uncertainty.
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applySemanticUncertainty(Map<dynamic, dynamic> bundle) {
  final evidence = _orElse(
          pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
      as List;
  final ambiguities = _orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List;
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}), <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final uncertainty =
      modelUncertainty(evidence.length, ambiguities.length, pairs.length);
  bundle['uncertainty'] = uncertainty;
  bundle = applySemanticConservatism(bundle);
  final cb = pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}) as Map;
  final capped = (pyGet(cb, 'score', 0.5) as num).toDouble();
  final uncScore = (uncertainty['confidence_score'] as num).toDouble();
  cb['score'] = pythonRound(capped < uncScore ? capped : uncScore, 3);
  bundle['confidence_basis'] = cb;
  return bundle;
}

/// Port of core.evidence.grounding_engine.structure_cognition.
Map<dynamic, dynamic> structureCognition(
    Map<dynamic, dynamic> observed,
    Map<dynamic, dynamic> inferred,
    Map<dynamic, dynamic> reconciled,
    [dynamic parsed,
    dynamic contradicted,
    List<dynamic>? ambiguities]) {
  final derived = <String, dynamic>{'structure': 'cognition_bundle'};
  if (pyTruthy(parsed) && !pyDeepEq(reconciled, observed)) {
    derived['reconciliation_applied'] = true;
  }
  final amb = List<dynamic>.from(ambiguities ?? const <dynamic>[]);
  if (pyTruthy(inferred) && !pyTruthy(observed)) {
    amb.add('inferred_without_direct_observation');
  }
  var parsedFacts = <dynamic, dynamic>{};
  if (pyTruthy(parsed)) {
    final symRaw = pyGet(parsed as Map, 'symbols', null);
    final sym = symRaw is Map ? symRaw : <dynamic, dynamic>{};
    List<dynamic> bounded(dynamic v, int cap) {
      final list =
          List<dynamic>.from(_orElse(v, const <dynamic>[]) as List);
      return list.length > cap ? list.sublist(0, cap) : list;
    }

    parsedFacts = <dynamic, dynamic>{
      'language': pyGet(parsed, 'language', 'text'),
      'classes': bounded(pyGet(sym, 'classes', const <dynamic>[]), 30),
      'functions': bounded(pyGet(sym, 'functions', const <dynamic>[]), 30),
    };
  }
  List<String> sortedKeys(Map<dynamic, dynamic> m) =>
      <String>[for (final k in m.keys) k as String]..sort();
  final bundle = buildSemanticIntegrityObject(
      observed,
      parsedFacts,
      inferred,
      reconciled,
      contradicted ?? <dynamic, dynamic>{},
      derived,
      amb,
      parsed,
      <dynamic>[
        <String, dynamic>{
          'stage': 'observe',
          'inputs': <dynamic>[],
          'outputs': sortedKeys(observed),
        },
        <String, dynamic>{
          'stage': 'infer',
          'inputs': sortedKeys(observed),
          'outputs': sortedKeys(inferred),
        },
        <String, dynamic>{
          'stage': 'reconcile',
          'inputs': sortedKeys(inferred),
          'outputs': sortedKeys(reconciled),
        },
      ]);
  return applySemanticUncertainty(applySemanticConservatism(bundle));
}

// ---------------------------------------------------------------------------
// Phases J–L — tutorial chain
// ---------------------------------------------------------------------------

final RegExp _numberedItem =
    RegExp(r'^\s*\d+\.\s+(.+)$', multiLine: true);

/// Port of core.documents.tutorial_reasoning_engine.extract_tutorial_flow.
Map<dynamic, dynamic> extractTutorialFlow(String? text) {
  final hierarchy = pyGet(extractSections(text ?? ''), 'hierarchy',
      const <dynamic>[]) as List;
  var steps = <dynamic>[
    for (final h in hierarchy)
      if (pyTruthy(pyGet(h as Map, 'title', null))) pyGet(h, 'title', '')
  ];
  var evidenceKind = 'section_hierarchy';
  if (steps.isEmpty) {
    steps = (<String>{
      for (final m in _numberedItem.allMatches(text ?? '')) m.group(1)!
    }.toList()
      ..sort());
    evidenceKind = 'numbered_list_fallback';
  }
  final observed = <String, dynamic>{'steps': steps};
  final inferred = <String, dynamic>{
    'requires_prior': <Map<String, dynamic>>[
      for (var i = 1; i < steps.length; i++)
        if (pyTruthy(steps[i]) && pyTruthy(steps[i - 1]))
          <String, dynamic>{'step': steps[i], 'requires': steps[i - 1]}
    ],
  };
  final reconciled = <String, dynamic>{
    'steps': steps,
    'flow_edges': <Map<String, dynamic>>[
      for (var i = 0; i < (steps.length - 1 > 0 ? steps.length - 1 : 0); i++)
        <String, dynamic>{'from': steps[i], 'to': steps[i + 1]}
    ],
  };
  final result = structureCognition(observed, inferred, reconciled);
  result['confidence_basis'] = <dynamic, dynamic>{
    ...pyGet(result, 'confidence_basis', <dynamic, dynamic>{}) as Map,
    'flow_evidence': evidenceKind,
  };
  return result;
}

/// Port of core.documents.tutorial_dependency_engine
/// .reconstruct_tutorial_dependencies.
Map<dynamic, dynamic> reconstructTutorialDependencies(String text) {
  final flow = extractTutorialFlow(text);
  final requires = pyGet(
      pyGet(flow, 'inferred', <dynamic, dynamic>{}) as Map,
      'requires_prior',
      const <dynamic>[]);
  final steps = pyGet(pyGet(flow, 'reconciled', <dynamic, dynamic>{}) as Map,
      'steps', const <dynamic>[]);
  final observed = <String, dynamic>{'steps': steps};
  final inferred = <String, dynamic>{
    'tutorial_dependencies': requires,
    'prerequisite_edges': requires,
  };
  final reconciled = <String, dynamic>{
    'tutorial_flow': pyGet(flow, 'reconciled', <dynamic, dynamic>{}),
    'dependencies': requires,
  };
  return structureCognition(observed, inferred, reconciled);
}

/// Port of core.documents.tutorial_prerequisite_engine
/// .infer_tutorial_prerequisites.
Map<String, dynamic> inferTutorialPrerequisites(String text) {
  final inst = analyzeInstructionalSemantics(text);
  final legacy = reconstructTutorialDependencies(text);
  final steps = pyGet(inst, 'ordering', const <dynamic>[]) as List;
  final chain = <Map<String, dynamic>>[
    for (var i = 1; i < steps.length; i++)
      <String, dynamic>{
        'prerequisite': pyGet(steps[i - 1] as Map, 'title', ''),
        'requires': pyGet(steps[i] as Map, 'title', ''),
        'evidence': 'discourse:instructional_order',
      }
  ];
  return <String, dynamic>{
    'chain': chain,
    'prerequisites': pyGet(inst, 'prerequisites', const <dynamic>[]),
    'legacy_flow': pyGet(legacy, 'reconciled', <dynamic, dynamic>{}),
    'deterministic_inputs': <String>['chain=${chain.length}'],
  };
}

// ---------------------------------------------------------------------------
// Phases M–O — document semantic IR and dispatchers
// ---------------------------------------------------------------------------

/// Port of core.documents.document_semantic_ir_engine.build_document_semantic_ir.
Map<String, dynamic> buildDocumentSemanticIr(String text) => <String, dynamic>{
      'rhetorical': parseRhetoricalStructure(text),
      'argument': buildArgumentDependencies(text),
      'progression': modelConceptProgression(text),
      'prerequisites': inferTutorialPrerequisites(text),
      'coreference': buildCoreferenceGraph(text),
      'dependency_graph': buildDocumentDependencyGraph(text),
      'evidence': <String>[
        'discourse:rhetorical',
        'discourse:argument',
        'discourse:progression',
        'discourse:prerequisites',
      ],
    };

/// Port of core.documents.long_range_discourse_engine.analyze_long_range_discourse.
Map<String, dynamic> analyzeLongRangeDiscourse(String? text,
    [int maxSpan = 5000]) {
  final src = text ?? '';
  final bounded = src.length > maxSpan ? src.substring(0, maxSpan) : src;
  final ir = buildDocumentSemanticIr(bounded);
  final edges = pyGet(pyGet(ir, 'coreference', <dynamic, dynamic>{}) as Map,
      'edges', const <dynamic>[]) as List;
  return <String, dynamic>{
    'ir': ir,
    'bounded_chars': bounded.length,
    'long_range_links': edges.length > 50 ? edges.sublist(0, 50) : edges,
    'evidence': pyGet(ir, 'evidence', const <dynamic>[]),
  };
}

/// Port of core.ir.document_ir.compile_document_ir.
Map<String, dynamic> compileDocumentIr(String text) {
  final raw = buildDocumentSemanticIr(text);
  final ir = emptyDocumentIr();
  final rhet = pyGet(raw, 'rhetorical', <dynamic, dynamic>{}) as Map;
  final arg = pyGet(raw, 'argument', <dynamic, dynamic>{}) as Map;
  ir['rhetorical_units'] = pyGet(rhet, 'units', const <dynamic>[]);
  ir['semantic_roles'] = pyGet(rhet, 'roles', const <dynamic>[]);
  ir['claims'] = pyGet(arg, 'nodes', const <dynamic>[]);
  ir['arguments'] = pyGet(arg, 'dependencies', const <dynamic>[]);
  ir['tutorial_steps'] = pyGet(
      pyGet(raw, 'prerequisites', <dynamic, dynamic>{}) as Map,
      'chain',
      const <dynamic>[]);
  ir['concept_progressions'] = pyGet(
      pyGet(raw, 'progression', <dynamic, dynamic>{}) as Map,
      'progression',
      const <dynamic>[]);
  ir['instructional_flows'] = pyGet(
      pyGet(raw, 'prerequisites', <dynamic, dynamic>{}) as Map,
      'prerequisites',
      const <dynamic>[]);
  ir['explanation_chains'] = pyGet(
      pyGet(raw, 'dependency_graph', <dynamic, dynamic>{}) as Map,
      'edges',
      const <dynamic>[]);
  ir['semantic_graph'] = pyGet(raw, 'dependency_graph', <dynamic, dynamic>{});
  // Python merge_evidence(*parts) is variadic; this call passes ONE part.
  ir['semantic_evidence'] =
      mergeEvidence(<dynamic>[pyGet(raw, 'evidence', const <dynamic>[])]);
  ir['lineage'] = emptyLineage('document_semantic_ir');
  ir['confidence'] = <String, dynamic>{
    'score': pyTruthy(ir['rhetorical_units']) ? 0.7 : 0.3,
    'basis': pyGet(raw, 'evidence', const <dynamic>[]),
    'deterministic': true,
  };
  ir['_raw'] = raw;
  return ir;
}

/// Port of core.query.document_query_engine.query_documents.
Map<String, dynamic> queryDocumentsIr(String text) {
  final ir = compileDocumentIr(text);
  return <String, dynamic>{
    'ir': ir,
    'claims': pyGet(ir, 'claims', const <dynamic>[]),
    'tutorial_steps': pyGet(ir, 'tutorial_steps', const <dynamic>[]),
    'explainable': true,
  };
}

/// Port of core.reasoning.discourse_reasoning_engine.reason_discourse_semantic.
Map<String, dynamic> reasonDiscourseSemantic(String text) {
  final ir = compileDocumentIr(text);
  final longRange = analyzeLongRangeDiscourse(text);
  return <String, dynamic>{
    'ir': ir,
    'long_range': longRange,
    'explainable': true,
  };
}
