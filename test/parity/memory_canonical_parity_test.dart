import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show computeDeterministicHash, buildRuntimeMemory, queryRuntimeMemory;

/// Executable cross-language parity for the canonical Python-aligned
/// `build_runtime_memory(runtime_history, lineage, semantic_relations)` and
/// `query_runtime_memory(memory, query_type, term)`. Reference outputs were
/// captured by EXECUTING Python 2.0.1 (and corroborated by executing the
/// JavaScript engine implementation) — see validation/executable/. All three
/// languages produced identical hashes.
void main() {
  List<Map<String, dynamic>> mapList(dynamic v) => v == null
      ? <Map<String, dynamic>>[]
      : <Map<String, dynamic>>[
          for (final e in v as List) Map<String, dynamic>.from(e as Map)
        ];

  group('canonical memory APIs — executable parity (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/memory_canonical_api_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final api = v['api'] as String;
      final args = v['args'] as List<dynamic>;
      final expected = v['expected'];

      test('[$id] $api Dart output hash-equals executed Python output', () {
        final dynamic actual;
        if (api == 'build_runtime_memory') {
          actual = buildRuntimeMemory(
            runtimeHistory: mapList(args[0]),
            lineage: mapList(args[1]),
            semanticRelations: mapList(args[2]),
          );
        } else if (api == 'query_runtime_memory') {
          actual = queryRuntimeMemory(
            Map<String, dynamic>.from(args[0] as Map),
            args[1] as String,
            args[2] as String,
          );
        } else {
          fail('unexpected api $api');
        }
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id\nexpected=$expected\nactual=$actual',
        );
      });
    }
  });

  group('canonical memory contract', () {
    test('build_runtime_memory yields Python-shaped keys', () {
      final r = buildRuntimeMemory(
        runtimeHistory: <Map<String, dynamic>>[
          <String, dynamic>{'tick': 1, 'kind': 'workflow'},
        ],
      );
      expect(
          r.keys,
          containsAll(<String>[
            'memory_id',
            'runtime_history',
            'workflow_history',
            'synchronization_history',
            'evolution_history',
            'lineage',
            'semantic_relations',
            'stable_hash',
            'bounded',
          ]));
      expect((r['memory_id'] as String).length, equals(32));
    });

    test('query_runtime_memory returns Python-shaped result', () {
      final mem = <String, dynamic>{
        'semantic_relations': <dynamic>[
          <String, dynamic>{'from': 'a', 'to': 'b'},
        ],
      };
      final r = queryRuntimeMemory(mem, 'semantic', 'a');
      expect(r['query_type'], equals('semantic'));
      expect(r['count'], equals(1));
      expect(r['bounded'], isTrue);
    });
  });
}
