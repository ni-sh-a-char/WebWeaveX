import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/layer_repo.dart';

/// Repository-IR closure of the Category-A semantic-IR port — the 11
/// formerly parse_source-gated engines, including the dispatchers
/// compile_repository_ir / query_repository / reason_runtime_semantic.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 644/644 fixtures, hash + deep equality).
void main() {
  final registry = <String, Function>{
    'build_repository_semantic_ir': buildRepositorySemanticIr,
    'model_execution_dependencies': modelExecutionDependencies,
    'analyze_runtime_semantics': analyzeRuntimeSemantics,
    'build_service_runtime_graph': buildServiceRuntimeGraph,
    'analyze_runtime_execution': analyzeRuntimeExecution,
    'reason_runtime_flow': reasonRuntimeFlow,
    'build_repository_execution_ir': buildRepositoryExecutionIr,
    'model_runtime_state': modelRuntimeState,
    'compile_repository_ir': compileRepositoryIr,
    'query_repository': queryRepositoryIr,
    'reason_runtime_semantic': reasonRuntimeSemantic,
  };

  group('semantic-IR repository closure (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_repo_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 11 repository-IR functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(11));
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

  group('repository-IR contract spot-checks', () {
    test(
        'compile_repository_ir scores 0.8 when runtime deps make it '
        'parser-first (executed-Python semantics), 0.4 otherwise', () {
      const pkg = '{"dependencies": {"react": "18"}}';
      final parserFirst = compileRepositoryIr(pkg, 'package.json');
      final empty = compileRepositoryIr('');
      expect((parserFirst['confidence'] as Map)['score'], equals(0.8));
      expect((empty['confidence'] as Map)['score'], equals(0.4));
    });

    test(
        'dispatcher semantic_ast falls back when the scanner validity gate '
        'fires (JSX/Vue leading <)', () {
      final ir = compileRepositoryIr('<template>x</template>', 'App.jsx');
      expect((ir['semantic_ast'] as Map)['semantic_grounded'], isFalse);
    });

    test(
        'runtime state is active only when dependency-backed '
        '(executed-Python semantics)', () {
      final active = modelRuntimeState(
          '{"dependencies": {"react": "18"}}', 'package.json');
      final unknown = modelRuntimeState('', '');
      expect(active['state'], equals('active'));
      expect((unknown['transitions'] as List).single,
          equals(<String, String>{'from': 'init', 'to': 'text'}));
    });
  });
}
