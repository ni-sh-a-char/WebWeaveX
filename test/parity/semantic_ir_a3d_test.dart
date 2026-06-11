import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/evidence_leaves_4.dart';

/// Phase A.3 batch 4 of the Category-A semantic-IR port — the final 27
/// core.evidence public leaves (semantic_* heavy cluster). With this batch,
/// every public Phase-A leaf is executable-proven: 197 proven + 14 private
/// helpers (prove through parents) + 1 reclassified = 212 plan rows.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 405/405 fixtures, hash + deep equality).
void main() {
  final registry = <String, Function>{
    'score_semantic_confidence': scoreSemanticConfidence,
    'apply_semantic_conservatism': applySemanticConservatism,
    'assess_semantic_consistency': assessSemanticConsistency,
    'model_semantic_decay': modelSemanticDecay,
    'model_semantic_decentralization': modelSemanticDecentralization,
    'detect_semantic_drift': detectSemanticDrift,
    'model_semantic_entropy': modelSemanticEntropy,
    'model_fragility': modelFragility,
    'assess_semantic_honesty': assessSemanticHonesty,
    'model_incompleteness': modelIncompleteness,
    'infer_from_evidence': inferFromEvidence,
    'model_semantic_instability': modelSemanticInstability,
    'build_justification': buildJustification,
    'semantic_limits': semanticLimits,
    'detect_semantic_overreach': detectSemanticOverreach,
    'model_semantic_plurality': modelSemanticPlurality,
    'prove_semantic_claim': proveSemanticClaim,
    'refuse_unsupported_conclusions': refuseUnsupportedConclusions,
    'apply_semantic_self_limitation': applySemanticSelfLimitation,
    'model_semantic_stability': modelSemanticStability,
    'terminate_stabilization': terminateStabilization,
    'model_uncertainty': modelUncertainty,
    'expose_uncertainty_visibility': exposeUncertaintyVisibility,
    'block_unsupported_confidence_escalation':
        blockUnsupportedConfidenceEscalation,
    'suppress_unsupported_inference': suppressUnsupportedInference,
    'preserve_recursive_divergence': preserveRecursiveDivergence,
    'detect_recursive_domestication': detectRecursiveDomestication,
  };

  group(
      'semantic-IR Phase A.3 batch 4 — final evidence leaves (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_a3d_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 27 A.3 batch-4 leaf functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(27));
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

  group('A.3 batch 4 contract spot-checks', () {
    test('semantic confidence accumulates in Python flag-sorted order', () {
      final r = scoreSemanticConfidence(
        <String, dynamic>{
          'evidence': {'b': true, 'a': false, 'c': 1}
        },
        <String, dynamic>{
          'nodes': [
            {'id': 'n'}
          ],
          'edges': [
            {'e': 1},
            {'e': 2}
          ],
        },
        <dynamic>['x1', 'x2'],
      );
      // 0.2 + 0.12*2 (b, c truthy) + min(0.25, 0.02) + 0.05*2 = 0.56
      expect(r['score'], equals(0.56));
      expect((r['basis'] as Map)['parser_density'], equals(2));
    });

    test('conservatism caps score and merges deterministic inputs', () {
      final r = applySemanticConservatism(<String, dynamic>{
        'evidence': ['e1'],
        'contradicted': {'preserved': true},
        'confidence_basis': {'score': 0.9},
      });
      final conf = r['confidence_basis'] as Map;
      // min(0.9, 0.35) then min(0.35, 0.45) -> 0.35
      expect(conf['score'], equals(0.35));
      expect(r['ambiguities'],
          equals(['unresolved_contradiction', 'weak_evidence']));
    });

    test('semantic instability keeps Python int truth_pressure for int math',
        () {
      final r = modelSemanticInstability(
          <dynamic>[], <String, dynamic>{}, <dynamic>['e1', 'e2']);
      expect(r['truth_pressure'], equals(0));
      expect(jsonEncode(r['truth_pressure']), equals('0'));
    });

    test('justification falls back to uncertainty factors', () {
      final r = buildJustification(<dynamic>[], <String, dynamic>{},
          <String, dynamic>{'factors': <dynamic>['f1']}, <String, dynamic>{});
      expect(r['uncertainty_basis'], equals(['f1']));
      expect(r['entropy'], equals(0));
    });
  });
}
