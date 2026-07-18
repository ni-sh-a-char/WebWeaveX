import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/composites_c.dart';
import 'package:webweavex/src/semantic_ir/evidence_layer_c.dart';

/// Phase C of the Category-A semantic-IR port — the second topological layer
/// (15 functions over proven A/B dependencies; the shared private `_depth`
/// helper proves inside its four parents). Proven Python ≡ JavaScript ≡ Dart
/// by execution (validation/semantic_ir/, 531/531 fixtures, hash + deep
/// equality). The 2 parse_source-gated engines (analyze_runtime_execution,
/// reason_runtime_flow) are deferred to the parser-subsystem phase.
void main() {
  final registry = <String, Function>{
    'compile_semantic_ast_ir': compileSemanticAstIr,
    'build_coreference_graph': buildCoreferenceGraph,
    'analyze_instructional_semantics': analyzeInstructionalSemantics,
    'parse_semantic_discourse': parseSemanticDiscourse,
    'apply_civilizational_epistemic_openness':
        applyCivilizationalEpistemicOpenness,
    'apply_cognitive_anti_capture': applyCognitiveAntiCapture,
    'apply_cognitive_integrity': applyCognitiveIntegrity,
    'apply_epistemic_civilization_stability':
        applyEpistemicCivilizationStability,
    'apply_formal_semantic_foundation': applyFormalSemanticFoundation,
    'apply_reality_bounded_confidence': applyRealityBoundedConfidence,
    'apply_recursive_epistemic_sovereignty': applyRecursiveEpistemicSovereignty,
    'collect_suppressed_speculation': collectSuppressedSpeculation,
    'collect_unsupported_continuity': collectUnsupportedContinuity,
    'reason_topology_semantic': reasonTopologySemantic,
    'analyze_deployment_semantics': analyzeDeploymentSemantics,
  };

  const kwOrder = <String, List<List<dynamic>>>{
    'apply_reality_bounded_confidence': <List<dynamic>>[
      <dynamic>['drift_pressure', 0.0],
      <dynamic>['continuity_count', 0],
      <dynamic>['parser_gap', false],
      <dynamic>['boundary_pressure', 0.0],
      <dynamic>['contradiction_count', 0],
      <dynamic>['ambiguity_count', 0],
      <dynamic>['uncertainty_count', 0],
    ],
  };

  group('semantic-IR Phase C — second layer (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_c_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 15 Phase C functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(15));
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

  group('Phase C contract spot-checks', () {
    test('reality-bounded confidence stacks drift and boundary penalties', () {
      final r = applyRealityBoundedConfidence(
          0.9, <String, dynamic>{}, 0.6, 2, true, 0.4, 1, 1, 2);
      final reality = r['reality_penalties'] as Map;
      // drift = min(0.25, 0.18) = 0.18; boundary = min(0.2, 0.1) = 0.1
      expect(reality['drift'], equals(0.18));
      expect(reality['boundary'], equals(0.1));
      expect(reality['total'], equals(0.28));
    });

    test('cognitive integrity marks unsupported inference into ambiguities',
        () {
      final out = applyCognitiveIntegrity(<String, dynamic>{
        'evidence': <String>['e1'],
        'inferred': <String, dynamic>{'i1': 1, 'i2': 2, 'i3': 3},
        'observed': <String, dynamic>{},
      });
      expect((out['ambiguities'] as List).contains('unsupported_inference'),
          isTrue);
      expect((out['unsupported'] as Map).containsKey('inferred_keys'), isTrue);
    });

    test('_depth falls back to lineage.depth when stages is not a list', () {
      final out = applyRecursiveEpistemicSovereignty(<String, dynamic>{
        'lineage': <String, dynamic>{'depth': 2, 'stages': 'notalist'},
        'evidence': <String>['e1'],
        'inferred': <String, dynamic>{'a': 1},
        'reconciled': <String, dynamic>{'a': 1},
      });
      // depth 2 + reconciled == inferred -> recursive submission suppressed
      expect(out['recursive_submission_suppressed'], isTrue);
    });

    test(
        'speculation collector gathers one record per inferred key; the '
        'reconcile probe is not speculative (inferred=False default)', () {
      final recs = collectSuppressedSpeculation(<String>['e1'],
          <String, dynamic>{'i1': 1, 'i2': 2}, <String, dynamic>{'r': 1});
      expect(recs, hasLength(2));
      expect(recs.first['reason'], equals('speculative_infer:i1'));
      // continuity collector HAS a reconcile record (no inferred gate)
      final cont = collectUnsupportedContinuity(<String>['e1'],
          <String, dynamic>{'i1': 1}, <String, dynamic>{'r': 1});
      expect(cont, hasLength(2));
      expect(cont.last['reason'], equals('continuity:reconcile'));
    });
  });
}
