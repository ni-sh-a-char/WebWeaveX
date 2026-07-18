import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/evidence_leaves_3.dart';

/// Phase A.3 batch 3 of the Category-A semantic-IR port — 24 core.evidence
/// medium leaf engines (confidence caps, lattices, evidence algebra,
/// explainability, lineage/provenance/traceability, noninference, instability).
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 349/349 fixtures, hash + deep equality); here the Dart output hash-equals
/// the executed Python reference vectors.
void main() {
  final registry = <String, Function>{
    'apply_confidence_caps': applyConfidenceCaps,
    'build_contradiction_lattice': buildContradictionLattice,
    'preserve_epistemic_boundaries': preserveEpistemicBoundaries,
    'model_epistemic_limits': modelEpistemicLimits,
    'combine_evidence': combineEvidence,
    'weight_evidence_calculus': weightEvidenceCalculus,
    'build_explainability': buildExplainability,
    'model_inference_integrity': modelInferenceIntegrity,
    'terminate_inference_chain': terminateInferenceChain,
    'preserve_instability': preserveInstability,
    'mark_insufficiency': markInsufficiency,
    'model_interpretive_diversity': modelInterpretiveDiversity,
    'build_lineage': buildLineage,
    'model_noninferable_regions': modelNoninferableRegions,
    'model_noninference': modelNoninference,
    'build_provenance': buildProvenance,
    'model_recursive_entropy': modelRecursiveEntropy,
    'model_recursive_instability': modelRecursiveInstability,
    'preserve_recursive_lineage': preserveRecursiveLineage,
    'detect_speculative_coherence': detectSpeculativeCoherence,
    'build_support': buildSupport,
    'build_weaknesses': buildWeaknesses,
    'build_traceability': buildTraceability,
    'refuse_unsupported_stabilization': refuseUnsupportedStabilization,
  };

  group('semantic-IR Phase A.3 batch 3 — evidence leaves (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_a3c_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 24 A.3 batch-3 leaf functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(24));
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

  group('A.3 batch 3 contract spot-checks', () {
    test('confidence caps stack penalties and floor at 0.0', () {
      final r = applyConfidenceCaps(
          0.3, <String, dynamic>{'level': 'medium'}, 5, 5, 5);
      expect(r['score'], equals(0.0));
      expect((r['contradiction_penalties'] as Map)['amount'], equals(0.35));
    });

    test('empty evidence algebra keeps Python int-zero weight sum', () {
      final r = combineEvidence(<dynamic>[]);
      expect(r['weight_sum'], equals(0));
      expect(jsonEncode(r['weight_sum']), equals('0'));
    });

    test('contradiction lattice sorts stringified pairs lexicographically', () {
      final r = buildContradictionLattice(<dynamic>[
        ['z', 'y'],
        ['a', 'b'],
        ['a', 'b', 'extra'],
        'junk',
        ['solo'],
      ]);
      expect(
          r['pairs'],
          equals([
            ['a', 'b'],
            ['a', 'b'],
            ['z', 'y']
          ]));
    });

    test('inference chain stop_at is the pre-sort first element', () {
      final r = terminateInferenceChain(<dynamic>[
        'r1'
      ], <dynamic>[
        {'reason': 'spec1'},
        <String, dynamic>{},
        'junk',
      ]);
      expect(r['stop_at'], equals('r1'));
      expect(
          r['terminated_inferences'], equals(['r1', 'spec1', 'speculative']));
    });
  });
}
