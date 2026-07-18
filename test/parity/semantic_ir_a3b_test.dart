import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/evidence_leaves_2.dart';
import 'package:webweavex/src/semantic_ir/py_compat.dart' show pyDeepEq;

/// Phase A.3 batch 2 of the Category-A semantic-IR port — 57 core.evidence
/// leaf engines (recursive/semantic/unsupported families). Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/, 298/298
/// fixtures, hash + deep equality); here the Dart output hash-equals the
/// executed Python reference vectors.
void main() {
  final registry = <String, Function>{
    'expose_ambiguity_visibility': exposeAmbiguityVisibility,
    'model_evidence_boundaries': modelEvidenceBoundaries,
    'assess_evidence_sufficiency': assessEvidenceSufficiency,
    'detect_narrative_hallucination': detectNarrativeHallucination,
    'detect_recursive_drift': detectRecursiveDrift,
    'preserve_recursive_entropy': preserveRecursiveEntropy,
    'track_recursive_evidence_ancestry': trackRecursiveEvidenceAncestry,
    'resist_exploration_decay': resistExplorationDecay,
    'detect_recursive_guardianship': detectRecursiveGuardianship,
    'resist_independence_decay': resistIndependenceDecay,
    'model_recursive_interpretive_independence':
        modelRecursiveInterpretiveIndependence,
    'detect_recursive_narrative_monopoly': detectRecursiveNarrativeMonopoly,
    'resist_novelty_decay': resistNoveltyDecay,
    'model_recursive_novelty': modelRecursiveNovelty,
    'preserve_recursive_novelty': preserveRecursiveNovelty,
    'detect_recursive_obedience': detectRecursiveObedience,
    'recursive_ontology_limits': recursiveOntologyLimits,
    'model_recursive_openness_stability': modelRecursiveOpennessStability,
    'model_recursive_phase_space': modelRecursivePhaseSpace,
    'preserve_recursive_provenance': preserveRecursiveProvenance,
    'recursive_reality_limits': recursiveRealityLimits,
    'detect_recursive_self_confirmation': detectRecursiveSelfConfirmation,
    'model_recursive_semantic_decentralization':
        modelRecursiveSemanticDecentralization,
    'distribute_recursive_semantics': distributeRecursiveSemantics,
    'model_recursive_semantic_independence': modelRecursiveSemanticIndependence,
    'model_sovereignty_stability': modelSovereigntyStability,
    'detect_recursive_stabilization': detectRecursiveStabilization,
    'terminate_recursive_stabilization': terminateRecursiveStabilization,
    'detect_recursive_submission': detectRecursiveSubmission,
    'recursive_topology_limits': recursiveTopologyLimits,
    'detect_recursive_trust_monopoly': detectRecursiveTrustMonopoly,
    'model_recursive_truth_boundaries': modelRecursiveTruthBoundaries,
    'refuse_recursive_stabilization': refuseRecursiveStabilization,
    'preserve_recursive_uncertainty': preserveRecursiveUncertainty,
    'model_semantic_alternatives': modelSemanticAlternatives,
    'apply_semantic_antigravity': applySemanticAntigravity,
    'model_semantic_autonomy': modelSemanticAutonomy,
    'model_semantic_boundaries': modelSemanticBoundaries,
    'suppress_semantic_dependency': suppressSemanticDependency,
    'model_semantic_divergence': modelSemanticDivergence,
    'model_semantic_diversity': modelSemanticDiversity,
    'detect_semantic_fixation': detectSemanticFixation,
    'model_semantic_freedom': modelSemanticFreedom,
    'suppress_semantic_governance': suppressSemanticGovernance,
    'detect_semantic_hierarchy_permanence': detectSemanticHierarchyPermanence,
    'detect_semantic_homogenization': detectSemanticHomogenization,
    'measure_semantic_momentum': measureSemanticMomentum,
    'resist_semantic_domestication': resistSemanticDomestication,
    'detect_semantic_orthodoxy': detectSemanticOrthodoxy,
    'model_semantic_self_determination': modelSemanticSelfDetermination,
    'detect_semantic_self_reinforcement': detectSemanticSelfReinforcement,
    'semantic_stability_limits': semanticStabilityLimits,
    'terminate_semantic_chain': terminateSemanticChain,
    'semantic_truth_limits': semanticTruthLimits,
    'detect_semantic_uniformity': detectSemanticUniformity,
    'detect_unsupported_expansion': detectUnsupportedExpansion,
    'model_unsupported_scope': modelUnsupportedScope,
  };

  group('semantic-IR Phase A.3 batch 2 — evidence leaves (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_a3b_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 57 A.3 batch-2 leaf functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(57));
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

  group('A.3 batch 2 contract spot-checks', () {
    test('pyDeepEq mirrors Python == (numeric cross-type, nested)', () {
      expect(pyDeepEq({'a': 1}, {'a': 1.0}), isTrue);
      expect(
          pyDeepEq({
            'a': [1, 2]
          }, {
            'a': [1, 2]
          }),
          isTrue);
      expect(pyDeepEq({'a': 1}, {'a': 2}), isFalse);
    });

    test('semantic alternatives sort union keys and prefer observed source',
        () {
      final r = modelSemanticAlternatives(
          <String, dynamic>{'b': 1, 'a': 2}, <String, dynamic>{'c': 3, 'a': 9});
      final alts = r['alternatives'] as List<dynamic>;
      expect(
          alts.map((a) => (a as Map)['key']).toList(), equals(['a', 'b', 'c']));
      expect((alts[0] as Map)['source'], equals('observed'));
      expect((alts[2] as Map)['source'], equals('inferred'));
    });

    test('semantic momentum uses true division like Python', () {
      final r = measureSemanticMomentum(5, 2);
      // ratio 2.5 -> pressure round(min(1.0, 1.5*0.3), 3) == 0.45
      expect(r['momentum'], equals(0.45));
      expect(r['halt_expansion'], isTrue);
    });
  });
}
