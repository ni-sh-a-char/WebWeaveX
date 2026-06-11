/// Phase C evidence engines of the Category-A semantic-IR port — the heavy
/// bundle-mutating integrity/openness/anti-capture/stability/sovereignty
/// layers plus the formal foundation, reality-bounded confidence, and the
/// two speculation/continuity collectors. The shared private `_depth` helper
/// (deferred from Phase A) is ported here inside its parents. Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'evidence_layer_b.dart';
import 'evidence_leaves.dart';
import 'evidence_leaves_2.dart';
import 'evidence_leaves_3.dart';
import 'evidence_leaves_4.dart';
import 'pressure_engines.dart'
    show
        computeRecursiveConvergencePressure,
        computeRecursiveDependencyPressure;
import 'py_compat.dart';

dynamic _orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;

/// Private `_depth` helper shared (by copy) across the four civilizational
/// engines in Python (core.evidence.*: `_depth(bundle)`).
int _depth(Map<dynamic, dynamic> bundle) {
  final lineage =
      _orElse(pyGet(bundle, 'lineage', <dynamic, dynamic>{}), <dynamic, dynamic>{})
          as Map;
  final stages = pyGet(lineage, 'stages', const <dynamic>[]);
  if (stages is List) return stages.length;
  return (_orElse(pyGet(lineage, 'depth', 0), 0) as num).toInt();
}

/// Port of core.evidence.cognitive_integrity_engine.apply_cognitive_integrity.
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyCognitiveIntegrity(Map<dynamic, dynamic> bundle) {
  var evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  var ambiguities = List<dynamic>.from(_orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final observed = _orElse(
      pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}),
      _orElse(pyGet(bundle, 'contradictions', <dynamic, dynamic>{}),
          <dynamic, dynamic>{}));
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final parserBasis = _orElse(pyGet(bundle, 'parser_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final parserDensity =
      (_orElse(pyGet(parserBasis, 'symbol_count', 0), 0) as num).toInt();

  final fragility =
      modelFragility(evidence, ambiguities, pairs.length, parserDensity);
  final suppression = suppressUnsupportedInference(evidence, inferred, observed);
  final overreach = detectSemanticOverreach(evidence, inferred, reconciled);
  final supported = <String, dynamic>{
    'keys': <String>[for (final k in observed.keys) k as String]..sort(),
    'evidence': evidence,
  };
  final unsupported = <String, dynamic>{
    'claims': pyGet(suppression, 'unsupported_dimensions', const <dynamic>[]),
    'dimensions': modelUnsupportedScope(
        pyGet(suppression, 'unsupported_dimensions', const <dynamic>[])
            as List),
  };
  var cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final supporting =
      List<dynamic>.from(pyGet(cb, 'supporting_evidence', evidence) as List);
  final contradicting = List<dynamic>.from(
      pyGet(cb, 'contradicting_evidence', const <dynamic>[]) as List);
  final inference =
      modelInferenceIntegrity(evidence, supporting, contradicting, fragility);
  final limits = modelEpistemicLimits(evidence, parserDensity, fragility);
  final boundaries = modelInferenceLimits(
      pyTruthy(pyGet(suppression, 'allowed_inference', null))
          ? inferred
          : <dynamic, dynamic>{},
      evidence.length);
  final honesty =
      assessSemanticHonesty(evidence, supported, unsupported, fragility);

  final cap = (pyGet(
          pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{}) as Map,
          'max_score',
          1.0) as num)
      .toDouble();
  final score =
      pythonRound(math.min((pyGet(cb, 'score', 0.5) as num).toDouble(), cap), 3);
  cb = <dynamic, dynamic>{
    ...cb,
    'score': score,
    'support_basis': pyGet(inference, 'basis', <dynamic, dynamic>{}),
    'fragility_basis': pyGet(fragility, 'basis', <dynamic, dynamic>{}),
    'uncertainty_basis': pyGet(bundle, 'uncertainties', <dynamic, dynamic>{}),
    'contradiction_basis': <String, dynamic>{'count': pairs.length},
    'confidence_limits':
        pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{}),
  };

  bundle['supported'] = supported;
  bundle['unsupported'] = unsupported;
  bundle['fragile'] = fragility;
  bundle['uncertain'] = pyGet(bundle, 'uncertainties', <dynamic, dynamic>{});
  bundle['contradicted'] = contradicted;
  bundle['incomplete'] = pyGet(
      pyGet(bundle, 'epistemic_state', <dynamic, dynamic>{}) as Map,
      'incomplete',
      false);
  bundle['confidence_limits'] =
      pyGet(fragility, 'confidence_limits', <dynamic, dynamic>{});
  bundle['semantic_honesty'] = honesty;
  bundle['fragility'] = fragility;
  bundle['inference_integrity'] = inference;
  bundle['epistemic_limits'] = limits;
  bundle['unsupported_scope'] =
      pyGet(unsupported, 'dimensions', <dynamic, dynamic>{});
  bundle['inference_boundaries'] = boundaries;
  bundle['confidence_basis'] = cb;
  if (pyTruthy(pyGet(overreach, 'overreach_detected', null))) {
    ambiguities = (<String>{
      for (final a in ambiguities) a as String,
      for (final f
          in pyGet(overreach, 'overreach_flags', const <dynamic>[]) as List)
        f as String,
    }.toList()
      ..sort());
    bundle['ambiguities'] = ambiguities;
  }
  if (!pyTruthy(pyGet(suppression, 'allowed_inference', null)) &&
      pyTruthy(inferred)) {
    unsupported['inferred_keys'] = <String>[
      for (final k in inferred.keys) k as String
    ]..sort();
    ambiguities = (<String>{
      for (final a in ambiguities) a as String,
      'unsupported_inference',
    }.toList()
      ..sort());
    bundle['ambiguities'] = ambiguities;
  }
  return bundle;
}

/// Port of core.evidence.formal_semantic_foundation_engine
/// .apply_formal_semantic_foundation. Mutates and returns `bundle`.
Map<dynamic, dynamic> applyFormalSemanticFoundation(
    Map<dynamic, dynamic> bundle) {
  final observed = _orElse(
      pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final ambiguities = List<dynamic>.from(_orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted',
          pyGet(bundle, 'contradictions', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final lineage = _orElse(
      pyGet(bundle, 'lineage', <dynamic, dynamic>{}), <dynamic, dynamic>{});
  final parserBasis = _orElse(pyGet(bundle, 'parser_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final parserBacked = pyTruthy(pyGet(parserBasis, 'symbol_count', 0)) ||
      pyTruthy(pyGet(parserBasis, 'flags', null));

  final lattice = buildContradictionLattice(pairs);
  final uncertainty = propagateUncertaintyMath(
      evidence.length, ambiguities.length, lattice['count'] as int);
  final entropy = modelSemanticEntropy(ambiguities,
      List<dynamic>.from(pyGet(uncertainty, 'factors', ambiguities) as List),
      contradicted);
  final consistency = assessSemanticConsistency(observed, inferred, reconciled);
  final weights = weightEvidenceCalculus(evidence, parserBacked);
  final reasoning = reasonDeterministically(observed, evidence, ambiguities);
  final justification =
      buildJustification(evidence, lineage, uncertainty, entropy);

  bundle['uncertainty'] = uncertainty;
  bundle['entropy'] = entropy;
  bundle['contradictions'] = <dynamic, dynamic>{
    ...contradicted as Map,
    ...lattice,
  };
  bundle['justification'] = justification;
  bundle['formal_reasoning'] = reasoning;
  bundle['evidence_weights'] = weights;
  bundle['semantic_consistency'] = consistency;
  final validation = validateInference(observed, evidence);
  final proof = proveSemanticClaim('semantic_integrity', evidence, 1);
  bundle['inference_validation'] = validation;
  bundle['semantic_proof'] = proof;
  bundle['deterministic_inputs'] = (<String>{
    for (final x in _orElse(
            pyGet(bundle, 'deterministic_inputs', const <dynamic>[]),
            const <dynamic>[]) as List)
      x as String,
    for (final x
        in pyGet(uncertainty, 'deterministic_inputs', const <dynamic>[]) as List)
      x as String,
    for (final x in pyGet(justification, 'deterministic_inputs', const <dynamic>[])
        as List)
      x as String,
    for (final x
        in pyGet(reasoning, 'deterministic_inputs', const <dynamic>[]) as List)
      x as String,
    for (final x
        in pyGet(validation, 'deterministic_inputs', const <dynamic>[]) as List)
      x as String,
    for (final x in pyGet(proof, 'deterministic_inputs', const <dynamic>[]) as List)
      x as String,
  }.toList()
    ..sort());
  return bundle;
}

/// Port of core.evidence.civilizational_epistemic_openness_engine
/// .apply_civilizational_epistemic_openness (+ private `_depth`).
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyCivilizationalEpistemicOpenness(
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
  final observed = _orElse(
      pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted',
          pyGet(bundle, 'contradictions', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', const <dynamic>[]) as List
      : const <dynamic>[];
  final interpretiveRaw = _orElse(
      pyGet(bundle, 'interpretive_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final interpretations = interpretiveRaw is Map
      ? pyGet(interpretiveRaw, 'interpretations', const <dynamic>[]) as List
      : const <dynamic>[];
  final explanatoryRaw = _orElse(
      pyGet(bundle, 'explanatory_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final alternatives = explanatoryRaw is Map
      ? pyGet(explanatoryRaw, 'alternatives', const <dynamic>[]) as List
      : const <dynamic>[];
  final entities = inferred.keys.toList();
  final depth = _depth(bundle);
  final interpCount =
      interpretations.isNotEmpty ? interpretations.length : inferred.length;
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final score = (pyGet(cb, 'score', 0.5) as num).toDouble();

  final keyUnion = <String>{
    for (final k in observed.keys) k as String,
    for (final k in inferred.keys) k as String,
  }.length;

  final semDiv = modelSemanticDivergence(observed, inferred, ambiguities);
  final novelty = modelRecursiveNovelty(depth, keyUnion, ambiguities.length);
  final wv = modelWorldviewVariance(interpCount, pairs.length);
  final interpDiv = modelInterpretiveDivergence(interpretations);
  final ontoDiv = modelOntologyDivergence(entities, depth);
  final explDiv = modelExplanatoryDivergence(alternatives);

  final attractor = detectSemanticAttractor(depth, interpCount, evidence.length);
  final gravity =
      detectCognitiveGravityWell(score > 0.75, interpCount <= 1, depth);
  final stabilization =
      detectRecursiveStabilization(pyDeepEq(reconciled, inferred), depth);
  final semFix =
      detectSemanticFixation(inferred.keys.toSet().length <= 1, depth);
  final explFix = detectExplanatoryFixation(alternatives.length, depth);
  final ontoFix = detectOntologyFixation(entities.length, depth);

  final phaseSpace =
      modelRecursivePhaseSpace(keyUnion, ambiguities.length, depth);
  final rEntropy = preserveRecursiveEntropy(ambiguities, uncertainties, depth);
  final divPres =
      preserveRecursiveDivergence(semDiv['divergence_score'] as num);
  final novPres = preserveRecursiveNovelty(novelty, depth);
  final convPressure = computeRecursiveConvergencePressure(
      depth, semDiv['divergence_score'] as num);
  final explDecay = resistExplorationDecay(
      interpCount > 1 || ambiguities.isNotEmpty, depth);
  final novDecay = resistNoveltyDecay(novelty['novelty'] as num, depth);

  final antigravSem =
      applySemanticAntigravity(pyGet(gravity, 'suppress', false) as bool);
  final antigravOnto =
      applyOntologyAntigravity(pyGet(ontoFix, 'suppress', false) as bool);
  final antigravExpl =
      applyExplanatoryAntigravity(pyGet(explFix, 'suppress', false) as bool);
  final antigravWv = applyWorldviewAntigravity(
      pyGet(bundle, 'worldview_convergence_suppressed', false) as bool);

  final opennessStable =
      modelRecursiveOpennessStability(semDiv['preserved'] as bool, depth);
  final exploratory =
      interpCount > 1 || ambiguities.isNotEmpty || alternatives.length > 1;

  bundle['civilizational_openness'] = <String, dynamic>{
    'open': true,
    'anti_convergence': true,
    'attractors_suppressed':
        (pyGet(attractor, 'suppressed', const <dynamic>[]) as List).length,
    'phase_space_preserved': phaseSpace['preserved'],
  };
  bundle['semantic_divergence'] = semDiv;
  bundle['recursive_novelty'] = <dynamic, dynamic>{...novelty, ...novPres};
  bundle['worldview_variance'] = wv;
  bundle['interpretive_divergence'] = interpDiv;
  bundle['ontology_divergence'] = ontoDiv;
  bundle['explanatory_divergence'] = explDiv;
  bundle['semantic_attractors_suppressed'] =
      pyGet(attractor, 'suppressed', const <dynamic>[]);
  bundle['cognitive_gravity_suppressed'] = pyGet(gravity, 'suppress', false);
  bundle['recursive_stabilization_suppressed'] =
      pyGet(stabilization, 'suppress', false);
  bundle['semantic_fixation_suppressed'] = pyGet(semFix, 'suppress', false);
  bundle['explanatory_fixation_suppressed'] = pyGet(explFix, 'suppress', false);
  bundle['ontology_fixation_suppressed'] = pyGet(ontoFix, 'suppress', false);
  bundle['recursive_phase_space'] = phaseSpace;
  bundle['recursive_entropy_preservation'] = rEntropy;
  bundle['exploratory_capacity'] = <String, dynamic>{
    'capacity': exploratory,
    'preserved': exploratory,
    'collapse_blocked': true,
  };
  bundle['semantic_exploration'] = <String, dynamic>{
    'active': exploratory,
    'novelty': novelty['novelty'],
  };
  bundle['ontology_exploration'] = <String, dynamic>{
    'active': ontoDiv['preserved'],
    'entities': entities.length,
  };
  bundle['interpretive_exploration'] = <String, dynamic>{
    'active': interpDiv['exploration_maintained'],
  };
  bundle['worldview_exploration'] = <String, dynamic>{
    'active': wv['preserved'],
  };
  bundle['novelty_preservation'] = novPres;
  bundle['antigravity'] = <String, dynamic>{
    'semantic': antigravSem,
    'ontology': antigravOnto,
    'explanatory': antigravExpl,
    'worldview': antigravWv,
  };
  bundle['openness_stability'] = opennessStable;
  bundle['exploration_decay_resisted'] = pyGet(explDecay, 'resist', true);
  bundle['novelty_decay_resisted'] = pyGet(novDecay, 'resist', true);
  bundle['recursive_convergence_pressure'] = convPressure;
  bundle['divergence_preservation'] = divPres;
  return bundle;
}

/// Port of core.evidence.cognitive_anti_capture_engine
/// .apply_cognitive_anti_capture (+ private `_depth`).
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyCognitiveAntiCapture(Map<dynamic, dynamic> bundle) {
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final interpretiveRaw = _orElse(
      pyGet(bundle, 'interpretive_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final interpretations = interpretiveRaw is Map
      ? pyGet(interpretiveRaw, 'interpretations', const <dynamic>[]) as List
      : const <dynamic>[];
  final explanatoryRaw = _orElse(
      pyGet(bundle, 'explanatory_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final alternatives = explanatoryRaw is Map
      ? pyGet(explanatoryRaw, 'alternatives', const <dynamic>[]) as List
      : const <dynamic>[];
  // Python: list(set(str(k) for k in inferred.keys())) — every consumer is
  // length-only, so set iteration order is irrelevant.
  final entities = <String>{for (final k in inferred.keys) pyToStr(k)}.toList();
  final depth = _depth(bundle);
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final trustScore = (pyGet(cb, 'score', 0.5) as num).toDouble();
  final interpOrInferred =
      interpretations.isNotEmpty ? interpretations.length : inferred.length;

  final semAutonomy = modelSemanticAutonomy(interpretations, evidence.length);
  final interpAutonomy = modelInterpretiveAutonomy(interpretations);
  final ontoComp = modelOntologyCompetition(entities, depth);
  final explComp = modelExplanatoryCompetition(alternatives);
  final semFreedom = modelSemanticFreedom(semAutonomy, explComp);
  final cognitiveDecent =
      modelCognitiveDecentralization(interpOrInferred, evidence.length);

  final semMonopoly =
      detectSemanticMonopoly(interpOrInferred, depth, evidence.length);
  final ontoMonopoly = detectOntologyMonopoly(entities.length, depth);
  final authority = detectAuthorityConcentration(
      pyGet(semAutonomy, 'dominant_cluster', false) as bool, depth);
  final trustMonopoly =
      detectRecursiveTrustMonopoly(trustScore, depth, evidence.length);
  final narrativeMonopoly = detectRecursiveNarrativeMonopoly(
      alternatives.isNotEmpty ? alternatives.length : interpretations.length,
      depth);
  final semDecentRaw = pyGet(bundle, 'semantic_decentralization', null);
  final hierarchy = detectSemanticHierarchyPermanence(
      depth,
      semDecentRaw is Map
          ? pyGet(semDecentRaw, 'hierarchy_lock_in', false) as bool
          : false);

  final rDecent =
      modelRecursiveSemanticDecentralization(entities, evidence.length);
  final rAuthDiff = diffuseRecursiveAuthority(interpretations.length);
  final rSemDist = distributeRecursiveSemantics(inferred.keys.toList());
  final rCogDist = distributeRecursiveCognition((_orElse(
          pyGet(bundle, 'unstable_regions', const <dynamic>[]),
          const <dynamic>[]) as List)
      .length);

  final explFreedom = preserveExplanatoryFreedom(alternatives);
  final ontoFreedom = preserveOntologyFreedom(ontoComp);
  final interpFreedom = preserveInterpretiveFreedom(interpAutonomy);
  final autonomyErosion = resistAutonomyErosion(
      pyGet(semAutonomy, 'autonomous', true) as bool, depth);
  final governance = suppressSemanticGovernance(false, depth);
  final centralization = detectRecursiveCentralization(
      pyGet(rDecent, 'decentralized', true) as bool, depth);

  final suppressed = pyGet(semMonopoly, 'suppressed', const <dynamic>[]) as List;
  final captureResistance = modelCaptureResistance(suppressed);

  bundle['cognitive_anti_capture'] = <String, dynamic>{
    'active': true,
    'capture_suppressed': suppressed.length,
    'monopolies_blocked': pyTruthy(pyGet(semMonopoly, 'monopoly', false))
        ? pyGet(semMonopoly, 'monopoly', false)
        : pyGet(ontoMonopoly, 'monopoly', false),
  };
  bundle['semantic_autonomy'] = semAutonomy;
  bundle['interpretive_autonomy'] = interpAutonomy;
  bundle['ontology_competition'] = ontoComp;
  bundle['explanatory_competition'] = explComp;
  bundle['semantic_freedom'] = semFreedom;
  bundle['cognitive_decentralization'] = cognitiveDecent;
  bundle['recursive_semantic_decentralization'] = rDecent;
  bundle['recursive_authority_diffusion'] = rAuthDiff;
  bundle['recursive_semantic_distribution'] = rSemDist;
  bundle['recursive_cognitive_distribution'] = rCogDist;
  bundle['explanatory_freedom'] = explFreedom;
  bundle['ontology_freedom'] = ontoFreedom;
  bundle['interpretive_freedom'] = interpFreedom;
  bundle['capture_resistance'] = captureResistance;
  bundle['semantic_monopoly_suppressed'] = suppressed;
  bundle['ontology_monopoly_suppressed'] =
      pyGet(ontoMonopoly, 'suppress', false);
  bundle['trust_monopoly_suppressed'] = pyGet(trustMonopoly, 'suppress', false);
  bundle['narrative_monopoly_suppressed'] =
      pyGet(narrativeMonopoly, 'suppress', false);
  bundle['authority_concentration_suppressed'] =
      pyGet(authority, 'suppress', false);
  bundle['hierarchy_permanence_suppressed'] = pyGet(hierarchy, 'suppress', false);
  bundle['semantic_governance_suppressed'] = pyGet(governance, 'suppress', false);
  bundle['recursive_centralization_suppressed'] =
      pyGet(centralization, 'suppress', false);
  bundle['autonomy_erosion_resisted'] = pyGet(autonomyErosion, 'resist', true);
  bundle['anti_capture_stability'] = <String, dynamic>{
    'stable': pyGet(captureResistance, 'resistant', true),
    'freedom_preserved': pyGet(semFreedom, 'free', true),
  };
  return bundle;
}

/// Port of core.evidence.epistemic_civilization_stability_engine
/// .apply_epistemic_civilization_stability (+ private `_depth`).
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyEpistemicCivilizationStability(
    Map<dynamic, dynamic> bundle) {
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final ambiguities = List<dynamic>.from(_orElse(
          pyGet(bundle, 'ambiguities', const <dynamic>[]), const <dynamic>[])
      as List);
  final observed = _orElse(
      pyGet(bundle, 'observed', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final contradicted = _orElse(
      pyGet(bundle, 'contradicted',
          pyGet(bundle, 'contradictions', <dynamic, dynamic>{})),
      <dynamic, dynamic>{});
  final unstable = List<dynamic>.from(_orElse(
          pyGet(bundle, 'unstable_regions', const <dynamic>[]),
          const <dynamic>[]) as List);
  final depth = _depth(bundle);

  final plurality =
      modelSemanticPlurality(observed, inferred, ambiguities, contradicted);
  final interpretive = modelInterpretiveDiversity(evidence, inferred);
  final interpretations =
      pyGet(interpretive, 'interpretations', const <dynamic>[]) as List;
  final decentralization =
      modelSemanticDecentralization(interpretations, evidence.length);
  final ontologyInst = modelOntologyInstability(unstable, depth);
  final worldview = modelWorldviewDiversity(interpretations, contradicted);
  final explanatory = modelExplanatoryDiversity(inferred, evidence);
  final openness = modelEpistemicOpenness(plurality, decentralization);

  final monoculture =
      detectSemanticMonoculture(interpretations, evidence, depth);
  final hardening = detectOntologyHardening(depth, evidence.length);
  final consensus = detectRecursiveConsensus(
      pyDeepEq(reconciled, inferred), depth, evidence.length);
  final orthodoxy = detectSemanticOrthodoxy(interpretations, depth);
  final closure = detectInterpretiveClosure(
      pyGet(plurality, 'alternative_count', 0) as int, depth);
  final uniformity = detectSemanticUniformity(inferred.keys.toList(), depth);
  final homogenization = detectSemanticHomogenization(
      pyGet(uniformity, 'uniformity_detected', false) as bool, depth);
  final pluralityDecay = resistPluralityDecay(
      pyGet(plurality, 'alternative_count', 0) as int, depth);
  final interpretiveDecay =
      resistInterpretiveDecay(interpretations.length, depth);
  final worldviewConv = suppressWorldviewConvergence(
      pyGet(consensus, 'consensus_inflated', false) as bool, depth);
  final diversity = modelSemanticDiversity(observed, inferred, ambiguities);
  final alternatives = modelSemanticAlternatives(observed, inferred);
  final causal = modelCausalPlurality(inferred);
  final authority = diffuseAuthority(interpretations);
  final distribution = distributeInterpretations(interpretations);

  final suppressed = pyGet(monoculture, 'suppressed', const <dynamic>[]) as List;

  bundle['epistemic_openness'] = openness;
  bundle['semantic_plurality'] = plurality;
  bundle['interpretive_diversity'] = interpretive;
  bundle['semantic_decentralization'] = decentralization;
  bundle['ontology_instability'] = ontologyInst;
  bundle['worldview_diversity'] = worldview;
  bundle['explanatory_diversity'] = explanatory;
  bundle['semantic_monoculture_suppressed'] = suppressed;
  bundle['ontology_hardening_suppressed'] = pyGet(hardening, 'suppress', false);
  bundle['recursive_consensus_suppressed'] = pyGet(consensus, 'suppress', false);
  bundle['semantic_orthodoxy_suppressed'] = pyGet(orthodoxy, 'suppress', false);
  bundle['interpretive_closure_suppressed'] = pyGet(closure, 'suppress', false);
  bundle['semantic_diversity'] = diversity;
  bundle['semantic_alternatives'] = alternatives;
  bundle['causal_plurality'] = causal;
  bundle['authority_diffusion'] = authority;
  bundle['interpretive_distribution'] = distribution;
  bundle['plurality_decay_resistance'] = pluralityDecay;
  bundle['interpretive_decay_resistance'] = interpretiveDecay;
  bundle['worldview_convergence_suppressed'] =
      pyGet(worldviewConv, 'suppress', false);
  bundle['semantic_homogenization_suppressed'] =
      pyGet(homogenization, 'suppress', false);
  bundle['civilization_stability'] = <String, dynamic>{
    'stable': pyGet(openness, 'open', true),
    'plurality_preserved': pyGet(plurality, 'preserved', true),
    'anti_monoculture': suppressed.isNotEmpty ||
        !pyTruthy(pyGet(monoculture, 'detected', null)),
  };
  return bundle;
}

/// Port of core.evidence.recursive_epistemic_sovereignty_engine
/// .apply_recursive_epistemic_sovereignty (+ private `_depth`).
/// Mutates and returns `bundle`.
Map<dynamic, dynamic> applyRecursiveEpistemicSovereignty(
    Map<dynamic, dynamic> bundle) {
  final evidence = List<dynamic>.from(
      _orElse(pyGet(bundle, 'evidence', const <dynamic>[]), const <dynamic>[])
          as List);
  final inferred = _orElse(
      pyGet(bundle, 'inferred', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final reconciled = _orElse(
      pyGet(bundle, 'reconciled', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final interpretiveRaw = _orElse(
      pyGet(bundle, 'interpretive_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final interpretations = interpretiveRaw is Map
      ? pyGet(interpretiveRaw, 'interpretations', const <dynamic>[]) as List
      : const <dynamic>[];
  final explanatoryRaw = _orElse(
      pyGet(bundle, 'explanatory_diversity', <dynamic, dynamic>{}),
      <dynamic, dynamic>{});
  final alternatives = explanatoryRaw is Map
      ? pyGet(explanatoryRaw, 'alternatives', const <dynamic>[]) as List
      : const <dynamic>[];
  final entities = inferred.keys.toList();
  final depth = _depth(bundle);
  final interpCount =
      interpretations.isNotEmpty ? interpretations.length : inferred.length;
  final cb = _orElse(pyGet(bundle, 'confidence_basis', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final score = (pyGet(cb, 'score', 0.5) as num).toDouble();

  final independent = interpCount > 1 || evidence.length >= 2;
  final semSelf = modelSemanticSelfDetermination(independent, depth);
  final interpSelf = modelInterpretiveSelfDetermination(interpCount);
  final ontoSelf = modelOntologySelfDetermination(entities.length);
  final explSelf = modelExplanatorySelfDetermination(alternatives.length);
  final agency = modelRecursiveAgency(independent, depth);
  final sovereignty = modelCognitiveSovereignty(independent);

  final dependency =
      detectRecursiveDependency(depth, interpCount, evidence.length);
  final obedience =
      detectRecursiveObedience(score > 0.7, evidence.length < 2, depth);
  final submission = detectRecursiveSubmission(
      pyDeepEq(reconciled, inferred), depth, evidence.length);
  final domestication = detectRecursiveDomestication(interpCount <= 1, depth);
  final cogDecentRaw = pyGet(bundle, 'cognitive_decentralization', null);
  final guardianship = detectRecursiveGuardianship(
      cogDecentRaw is Map
          ? pyGet(cogDecentRaw, 'dominance_without_evidence', false) as bool
          : false,
      depth);
  final depPressure = computeRecursiveDependencyPressure(depth, interpCount);

  final semIndep =
      modelRecursiveSemanticIndependence(inferred.keys.toList(), depth);
  final interpIndep = modelRecursiveInterpretiveIndependence(interpCount);
  final agencyPres = preserveRecursiveAgency(independent);
  final autonomyPres = preserveRecursiveAutonomy(independent);
  final depSuppress = suppressSemanticDependency(
      pyGet(dependency, 'suppressed', const <dynamic>[]) as List);

  final nondomSem = resistSemanticDomestication(
      pyGet(domestication, 'suppress', false) as bool);
  final nondomInterp = resistInterpretiveDomestication(
      pyGet(domestication, 'suppress', false) as bool);
  final nondomOnto = resistOntologyDomestication(
      pyGet(submission, 'suppress', false) as bool);
  final nondomExpl = resistExplanatoryDomestication(
      pyGet(bundle, 'narrative_monopoly_suppressed', false) as bool);

  final stab = modelSovereigntyStability(independent, depth);
  final indepDecay = resistIndependenceDecay(independent, depth);
  final agencyDecay = resistAgencyDecay(independent, depth);

  bundle['epistemic_sovereignty'] = <String, dynamic>{
    'preserved': true,
    'anti_dependent': true,
    'dependency_suppressed':
        (pyGet(dependency, 'suppressed', const <dynamic>[]) as List).length,
  };
  bundle['semantic_self_determination'] = semSelf;
  bundle['interpretive_self_determination'] = interpSelf;
  bundle['ontology_self_determination'] = ontoSelf;
  bundle['explanatory_self_determination'] = explSelf;
  bundle['recursive_agency'] = agency;
  bundle['cognitive_sovereignty'] = sovereignty;
  bundle['recursive_dependency_suppressed'] =
      pyGet(dependency, 'suppressed', const <dynamic>[]);
  bundle['recursive_obedience_suppressed'] = pyGet(obedience, 'suppress', false);
  bundle['recursive_submission_suppressed'] =
      pyGet(submission, 'suppress', false);
  bundle['recursive_domestication_suppressed'] =
      pyGet(domestication, 'suppress', false);
  bundle['recursive_guardianship_suppressed'] =
      pyGet(guardianship, 'suppress', false);
  bundle['recursive_semantic_independence'] = semIndep;
  bundle['recursive_interpretive_independence'] = interpIndep;
  bundle['recursive_agency_preservation'] = agencyPres;
  bundle['recursive_autonomy_preservation'] = autonomyPres;
  bundle['dependency_resistance'] = depSuppress;
  bundle['sovereignty_stability'] = stab;
  bundle['independence_decay_resisted'] = pyGet(indepDecay, 'resist', true);
  bundle['agency_decay_resisted'] = pyGet(agencyDecay, 'resist', true);
  bundle['recursive_dependency_pressure'] = depPressure;
  bundle['nondomestication'] = <String, dynamic>{
    'semantic': nondomSem,
    'interpretive': nondomInterp,
    'ontology': nondomOnto,
    'explanatory': nondomExpl,
  };
  return bundle;
}

/// Port of core.evidence.reality_bounded_confidence_engine
/// .apply_reality_bounded_confidence (kw-only args become trailing
/// positionals, py2ts order).
Map<String, dynamic> applyRealityBoundedConfidence(
  num score,
  Map<dynamic, dynamic> fragility, [
  num driftPressure = 0.0,
  int continuityCount = 0,
  bool parserGap = false,
  num boundaryPressure = 0.0,
  int contradictionCount = 0,
  int ambiguityCount = 0,
  int uncertaintyCount = 0,
]) {
  final base = applyConfidenceDegradation(
      score,
      fragility,
      contradictionCount,
      ambiguityCount,
      uncertaintyCount,
      continuityCount,
      continuityCount,
      parserGap);
  final driftPen = pythonRound(math.min(0.25, driftPressure * 0.3), 3);
  final boundaryPen = pythonRound(math.min(0.2, boundaryPressure * 0.25), 3);
  final realityPen = pythonRound(driftPen + boundaryPen, 3);
  final finalScore =
      pythonRound(math.max(0.0, (base['score'] as num) - realityPen), 3);
  return <String, dynamic>{
    ...base,
    'score': finalScore,
    'reality_penalties': <String, dynamic>{
      'drift': driftPen,
      'boundary': boundaryPen,
      'total': realityPen,
    },
    'stability_penalties': <String, dynamic>{
      'continuity': pythonRound(math.min(0.2, continuityCount * 0.08), 3),
    },
    'drift_penalties': <String, dynamic>{
      'amount': driftPen,
      'pressure': driftPressure,
    },
    'boundary_penalties': <String, dynamic>{
      'amount': boundaryPen,
      'pressure': boundaryPressure,
    },
    'deterministic_inputs': <dynamic>[
      ...pyGet(base, 'deterministic_inputs', const <dynamic>[]) as List,
      'drift=${pyToStr(driftPressure)}',
      'boundary=${pyToStr(boundaryPressure)}',
      'parser_gap=${pyToStr(parserGap)}',
    ],
  };
}

/// Port of core.evidence.speculative_inference_engine
/// .collect_suppressed_speculation.
List<Map<String, dynamic>> collectSuppressedSpeculation(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final out = <Map<String, dynamic>>[];
  for (final key in inferred.keys) {
    final r = suppressSpeculativeInference('infer:$key', evidence, true);
    if (pyTruthy(r['suppressed']) && pyTruthy(r['record'])) {
      out.add(r['record'] as Map<String, dynamic>);
    }
  }
  if (pyTruthy(reconciled) && evidence.length < 2) {
    final r = suppressSpeculativeInference('reconcile', evidence);
    if (pyTruthy(r['suppressed']) && pyTruthy(r['record'])) {
      out.add(r['record'] as Map<String, dynamic>);
    }
  }
  return out;
}

/// Port of core.evidence.unsupported_continuity_engine
/// .collect_unsupported_continuity.
List<Map<String, dynamic>> collectUnsupportedContinuity(List<dynamic> evidence,
    Map<dynamic, dynamic> inferred, Map<dynamic, dynamic> reconciled) {
  final out = <Map<String, dynamic>>[];
  for (final k in inferred.keys) {
    final r = suppressUnsupportedContinuity('infer:$k', evidence);
    if (pyTruthy(r['suppressed']) && pyTruthy(r['record'])) {
      out.add(r['record'] as Map<String, dynamic>);
    }
  }
  if (pyTruthy(reconciled) && evidence.length < 2) {
    final r = suppressUnsupportedContinuity('reconcile', evidence);
    if (pyTruthy(r['suppressed']) && pyTruthy(r['record'])) {
      out.add(r['record'] as Map<String, dynamic>);
    }
  }
  return out;
}
