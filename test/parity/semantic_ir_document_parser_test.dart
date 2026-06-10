import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/document_parser.dart';

/// Phase A of the Category-A semantic-IR port — document-parser leaf functions.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/);
/// here Dart output hash-equals the executed Python reference.
void main() {
  List<Map<String, dynamic>> claims(dynamic v) => <Map<String, dynamic>>[
        for (final e in v as List) Map<String, dynamic>.from(e as Map)
      ];

  dynamic call(String fn, List<dynamic> args) {
    switch (fn) {
      case 'extract_rhetorical_structure':
        return extractRhetoricalStructure(args[0] as String?);
      case 'assign_semantic_roles':
        return assignSemanticRoles(args[0] as String?);
      case 'extract_headings':
        return extractHeadings(args[0] as String?);
      case 'reconstruct_argument_dependencies':
        return reconstructArgumentDependencies(claims(args[0]));
      case 'resolve_coreferences':
        return resolveCoreferences(args[0] as String?);
      default:
        throw StateError('unknown $fn');
    }
  }

  group('semantic-IR Phase A — document parser (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_document_parser_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        final actual = call(fn, v['args'] as List<dynamic>);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('document parser contract spot-checks', () {
    test('rhetorical units classify headings/lists/fences', () {
      final r = extractRhetoricalStructure('# H\n- x\n```\ny\n```');
      final units = r['units'] as List<dynamic>;
      expect((units[0] as Map)['type'], equals('heading'));
      expect((units[0] as Map)['level'], equals(1));
      expect((units[1] as Map)['type'], equals('list_item'));
      expect((units[2] as Map)['type'], equals('code_fence'));
    });

    test('headings sorted by (level, title)', () {
      final r = extractHeadings('## B\n# A');
      final h = r['headings'] as List<dynamic>;
      expect((h.first as Map)['title'], equals('A'));
    });
  });
}
