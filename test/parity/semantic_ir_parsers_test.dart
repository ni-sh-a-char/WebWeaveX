import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/parsers.dart';

/// core.parsers closure of the Category-A semantic-IR port — the
/// parse_source gate for the repository-IR dispatchers. Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 624/624 fixtures, hash + deep equality).
///
/// AST contract: the certified JS astModule.parse always raises, so
/// `python`-language fixtures use syntactically invalid source — Python's
/// native-AST enrichment of valid python is a documented Python-only
/// capability outside the 3-way parity domain.
void main() {
  final registry = <String, Function>{
    'parsers.parse_source': parseSource,
    'parsers.parse_ast': parseAst,
    'parsers.recover_syntax': recoverSyntax,
    'parsers.enforce_budget': enforceBudget,
    'parsers.resolve_symbols': resolveParserSymbols,
    'parsers.build_call_graph': buildParserCallGraph,
    'parsers.resolve_imports': resolveImports,
    'parsers.resolve_dependencies': resolveDependencies,
    'parsers.resolve_runtime': resolveRuntime,
    'parsers.resolve_frameworks': resolveFrameworks,
    'parsers.resolve_api_surface': resolveApiSurface,
    'parsers.language_capabilities': languageCapabilities,
    'parsers.build_semantic_graph': buildParserSemanticGraph,
    'parsers.normalize_parser_output': normalizeParserOutput,
    'parsers.require_parser_evidence': requireParserEvidence,
    'parsers.build_parser_cognition_evidence': buildParserCognitionEvidence,
    'parsers.analyze_repository_source': analyzeRepositorySource,
    'parsers.stream_parse': streamParse,
    'ground_parser_output': groundParserOutput,
  };

  group('semantic-IR core.parsers closure (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_parsers_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 19 parser-closure functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(19));
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

  group('parser-closure contract spot-checks', () {
    test('detect_language follows Path.suffix semantics', () {
      expect(detectLanguage(path: 'a/b.py'), equals('python'));
      expect(detectLanguage(path: '.py'), equals('text')); // dotfile: no suffix
      expect(detectLanguage(path: 'Dockerfile'), equals('text'));
      expect(detectLanguage(path: 'x.TS'), equals('typescript'));
      expect(detectLanguage(hint: 'GO'), equals('go'));
    });

    test('parse_source wires the full closure with grounding', () {
      final out = parseSource('function f() { g(); }', 'app.js');
      expect(out['language'], equals('javascript'));
      expect((out['parser_grounding'] as Map)['grounded'], isTrue);
      expect((out['grounding'] as Map).containsKey('epistemic_state'), isTrue);
      expect((out['semantic_graph'] as Map)['edges'], isNotEmpty);
    });

    test('stream_parse chunks by line count with index/count markers', () {
      final out = streamParse('a()\nb()\nc()\nd()\n', 'x.js', '', 2);
      expect(out, hasLength(2));
      expect(out[0]['chunk_index'], equals(0));
      expect(out[1]['chunk_count'], equals(2));
    });
  });
}
