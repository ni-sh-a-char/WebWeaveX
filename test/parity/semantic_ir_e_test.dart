import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/layer_e.dart';

/// Phase E of the Category-A semantic-IR port — fourth topological layer
/// (5 portable functions; compile_repository_ir is parse_source-gated and
/// deferred). Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/, 555/555 fixtures, hash + deep equality).
void main() {
  final registry = <String, Function>{
    'build_document_dependency_graph': buildDocumentDependencyGraph,
    'model_semantic_transitions': modelSemanticTransitions,
    'apply_cognitive_humility': applyCognitiveHumility,
    'apply_recursive_confidence_decay': applyRecursiveConfidenceDecay,
    'apply_truth_preservation': applyTruthPreservation,
  };

  const kwOrder = <String, List<List<dynamic>>>{
    'apply_recursive_confidence_decay': <List<dynamic>>[
      <dynamic>['depth', 0],
      <dynamic>['closure_count', 0],
      <dynamic>['drift_pressure', 0.0],
      <dynamic>['entropy', 0.0],
      <dynamic>['contradiction_count', 0],
      <dynamic>['ambiguity_count', 0],
      <dynamic>['uncertainty_count', 0],
    ],
  };

  group('semantic-IR Phase E — fourth layer (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_e_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 5 Phase E functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(5));
      expect(registry.keys.toSet(), equals(fns));
    });

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        var args = List<dynamic>.from(v['args'] as List);
        final kwargs = v['kwargs'] as Map<String, dynamic>?;
        if (kwargs != null && kwargs.isNotEmpty) {
          final order = kwOrder[fn]!;
          args = <dynamic>[
            ...args,
            for (final spec in order)
              kwargs.containsKey(spec[0]) ? kwargs[spec[0]] : spec[1],
          ];
        }
        final actual = Function.apply(registry[fn]!, args);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('Phase E contract spot-checks', () {
    test('recursive decay stacks depth and entropy penalties', () {
      final r = applyRecursiveConfidenceDecay(
          0.95, <String, dynamic>{}, 3, 2, 0.3, 0.5, 1, 1, 1);
      final decay = r['recursive_decay'] as Map;
      // depth = min(0.35, 0.24) = 0.24; entropy = min(0.2, 0.125) = 0.125
      expect(decay['depth_penalty'], equals(0.24));
      expect(decay['entropy_penalty'], equals(0.125));
    });

    test('humility coerces non-dict fragility via model_fragility', () {
      final out = applyCognitiveHumility(<String, dynamic>{
        'evidence': <String>['e1'],
        'ambiguities': <String>['a1'],
        'fragility': 'notadict',
      });
      expect((out['semantic_fragility'] as Map).containsKey('level'), isTrue);
      expect((out['humility'] as Map)['self_limiting'], isTrue);
    });

    test(
        'truth preservation: echo probe runs with empty prior scores, so no '
        'suppression (matches executed Python)', () {
      final out = applyTruthPreservation(<String, dynamic>{
        'evidence': <String>['e1', 'e2'],
        'inferred': <String, dynamic>{'a': 1},
        'reconciled': <String, dynamic>{'b': 2},
        'confidence_basis': <String, dynamic>{'score': 0.99},
      });
      expect((out['truth_preservation'] as Map)['echo_suppressed'], isFalse);
      expect((out['confidence_basis'] as Map).containsKey('collapse_pressure'),
          isTrue);
    });
  });
}
