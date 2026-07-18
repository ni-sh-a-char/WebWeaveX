import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/layer_d.dart';

/// Phase D of the Category-A semantic-IR port — third topological layer
/// (4 portable functions; build_repository_execution_ir and
/// model_runtime_state are parse_source-gated and deferred). Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 542/542 fixtures, hash + deep equality).
void main() {
  final registry = <String, Function>{
    'model_concept_transitions': modelConceptTransitions,
    'apply_confidence_collapse': applyConfidenceCollapse,
    'apply_reality_alignment': applyRealityAlignment,
    'detect_semantic_speculation': detectSemanticSpeculation,
  };

  const kwOrder = <String, List<List<dynamic>>>{
    'apply_confidence_collapse': <List<dynamic>>[
      <dynamic>['reinforcement_count', 0],
      <dynamic>['stabilization_count', 0],
      <dynamic>['decay_pressure', 0.0],
      <dynamic>['truth_boundary_pressure', 0.0],
      <dynamic>['contradiction_count', 0],
      <dynamic>['ambiguity_count', 0],
      <dynamic>['uncertainty_count', 0],
      <dynamic>['incompleteness', false],
    ],
  };

  group('semantic-IR Phase D — third layer (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_d_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 4 Phase D functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(4));
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

  group('Phase D contract spot-checks', () {
    test('confidence collapse stacks reinforcement/stabilization penalties',
        () {
      final r = applyConfidenceCollapse(
          0.9, <String, dynamic>{}, 2, 1, 0.4, 0.3, 1, 1, 2, true);
      final collapse = r['collapse_pressure'] as Map;
      // reinf = min(0.3, 0.24) = 0.24; stab = min(0.25, 0.1) = 0.1; incom 0.08
      expect(collapse['reinforcement'], equals(0.24));
      expect(collapse['stabilization'], equals(0.1));
      expect(collapse['incompleteness'], equals(0.08));
      expect(collapse['total'], equals(0.42));
    });

    test('reality alignment coerces non-dict fragility to the medium default',
        () {
      final out = applyRealityAlignment(<String, dynamic>{
        'evidence': <dynamic>[],
        'inferred': <String, dynamic>{'a': 1},
        'fragility': 'notadict',
        'confidence_basis': <String, dynamic>{'score': 0.4},
      });
      final cb = out['confidence_basis'] as Map;
      // medium default caps max_score at 0.7 -> degraded path applies
      expect((out['reality_alignment'] as Map)['parser_grounded'], isFalse);
      expect(cb.containsKey('reality_penalties'), isTrue);
    });

    test('speculation density divides by inferred size + 1', () {
      final r = detectSemanticSpeculation(<String>['e1'],
          <String, dynamic>{'i1': 1, 'i2': 2}, <String, dynamic>{});
      // 2 suppressed / max(1, 3) = 0.667
      expect(r['density'], equals(0.667));
      expect(r['speculative'], isTrue);
    });
  });
}
