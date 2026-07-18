import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/evidence_leaves.dart';

/// Phase A.3 batch 1 of the Category-A semantic-IR port — 60 core.evidence
/// trivial leaf engines. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/, 185/185 fixtures, hash + deep equality); here the
/// Dart output hash-equals the executed Python reference vectors.
void main() {
  final registry = <String, Function>{
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
  };

  group('semantic-IR Phase A.3 batch 1 — evidence leaves (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_a3_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 60 A.3 batch-1 leaf functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(60));
      expect(registry.keys.toSet(), equals(fns));
    });

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        final actual =
            Function.apply(registry[fn]!, v['args'] as List<dynamic>);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('A.3 contract spot-checks', () {
    test('confidence echo collapses to Python-rounded min(score, avg)', () {
      final r = detectConfidenceEcho(0.9, <dynamic>[0.5, 0.6]);
      expect(r['echo_detected'], isTrue);
      expect(r['collapse_to'], equals(0.55));
    });

    test('explanatory diversity grounds keys against the list repr', () {
      final r = modelExplanatoryDiversity(
          <String, dynamic>{'alpha': 1, 'beta': 2},
          <dynamic>['alpha evidence', 'z']);
      final alts = r['alternatives'] as List<dynamic>;
      expect((alts[0] as Map)['grounded'], isTrue);
      expect((alts[1] as Map)['grounded'], isFalse);
    });

    test('continuity refusal carries null boundary failures', () {
      final r = refuseUnsupportedContinuity(<dynamic>[
        {'reason': 'gap'},
        <String, dynamic>{},
      ]);
      expect(r['boundary_failures'], equals(<dynamic>['gap', null]));
      expect(r['termination_reasons'], equals(<String>['continuity_refused']));
    });
  });
}
