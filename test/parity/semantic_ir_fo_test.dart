import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/layer_f_o.dart';

/// Phases F–O (document side) of the Category-A semantic-IR port — the final
/// ladder closing compile_document_ir / query_documents /
/// reason_discourse_semantic end-to-end through the full epistemic chain
/// (attach_epistemic_state over every civilizational engine). Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 581/581 fixtures, hash + deep equality). Repository-side F–O
/// (query_repository, reason_runtime_semantic, compile_repository_ir)
/// remains parse_source-gated.
void main() {
  final registry = <String, Function>{
    'model_concept_progression': modelConceptProgression,
    'apply_recursive_reality_integrity': applyRecursiveRealityIntegrity,
    'attach_epistemic_state': attachEpistemicState,
    'build_semantic_integrity_object': buildSemanticIntegrityObject,
    'apply_semantic_uncertainty': applySemanticUncertainty,
    'structure_cognition': structureCognition,
    'extract_tutorial_flow': extractTutorialFlow,
    'reconstruct_tutorial_dependencies': reconstructTutorialDependencies,
    'infer_tutorial_prerequisites': inferTutorialPrerequisites,
    'build_document_semantic_ir': buildDocumentSemanticIr,
    'analyze_long_range_discourse': analyzeLongRangeDiscourse,
    'compile_document_ir': compileDocumentIr,
    'query_documents': queryDocumentsIr,
    'reason_discourse_semantic': reasonDiscourseSemantic,
  };

  group('semantic-IR Phases F–O — document dispatchers (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_fo_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 14 F–O document-side functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(14));
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

  group('F–O contract spot-checks', () {
    test('compile_document_ir scores 0.7 with rhetorical units, 0.3 without',
        () {
      final withUnits = compileDocumentIr('# Heading\nbody\n');
      final without = compileDocumentIr('');
      expect((withUnits['confidence'] as Map)['score'], equals(0.7));
      expect((without['confidence'] as Map)['score'], equals(0.3));
      expect(withUnits.containsKey('_raw'), isTrue);
    });

    test('tutorial flow falls back to sorted numbered-list steps', () {
      final flow = extractTutorialFlow('intro\n1. zebra step\n2. alpha step\n');
      final cb = flow['confidence_basis'] as Map;
      expect(cb['flow_evidence'], equals('numbered_list_fallback'));
      expect((flow['observed'] as Map)['steps'],
          equals(<String>['alpha step', 'zebra step']));
    });

    test('attach_epistemic_state layers the full epistemic chain', () {
      final out = attachEpistemicState(<String, dynamic>{
        'evidence': <String>['e1'],
        'observed': <String, dynamic>{'o': 1},
        'inferred': <String, dynamic>{'i': 1},
      });
      // every chained engine left its marker
      for (final key in <String>[
        'epistemic_state',
        'humility',
        'reality_alignment',
        'truth_preservation',
        'recursive_reality_integrity',
        'civilizational_openness',
        'cognitive_anti_capture',
        'epistemic_sovereignty',
      ]) {
        expect(out.containsKey(key), isTrue, reason: 'missing $key');
      }
    });
  });
}
