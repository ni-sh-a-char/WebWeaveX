import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        computeGlobalRuntimeFingerprint,
        queryRuntimeGraph,
        validateReplayEquivalence;

/// Executable cross-language parity (Python ≡ JavaScript ≡ Dart) for the
/// Group-B canonical APIs. Reference outputs captured by EXECUTING Python 2.0.1
/// and corroborated by executing the JavaScript engine functions — see
/// validation/executable/. Dart output must hash-equal the executed Python output.
void main() {
  Map<String, dynamic>? asMap(dynamic v) =>
      v == null ? null : Map<String, dynamic>.from(v as Map);

  group('canonical runtime APIs — executable parity (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/canonical_runtime_api_vectors.json')
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
        switch (api) {
          case 'compute_global_runtime_fingerprint':
            actual = computeGlobalRuntimeFingerprint(
              extraction: asMap(args[0]),
              graph: asMap(args[1]),
              memory: asMap(args[2]),
              sync: asMap(args[3]),
              reconstruction: asMap(args[4]),
              kaalkaSeal: (args[5] ?? '') as String,
            );
            break;
          case 'query_runtime_graph':
            actual = queryRuntimeGraph(asMap(args[0])!, asMap(args[1])!);
            break;
          case 'validate_replay_equivalence':
            actual =
                validateReplayEquivalence(asMap(args[0])!, asMap(args[1])!);
            break;
          default:
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

  group('canonical runtime contract', () {
    test('validate_replay_equivalence yields Python-shaped checks', () {
      final env = <String, dynamic>{
        'unified_runtime_graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'a'}
          ],
          'edges': <dynamic>[],
        },
        'browser_ir': <String, dynamic>{'runtime_identity': 'id'},
      };
      final r = validateReplayEquivalence(env, Map<String, dynamic>.from(env));
      expect(r['equivalent'], isTrue);
      final checks = r['checks'] as List<dynamic>;
      expect(checks.length, equals(3));
      final first = checks.first as Map<String, dynamic>;
      expect(first.keys,
          containsAll(<String>['name', 'ok', 'original', 'replay']));
    });

    test('query_runtime_graph filters by type', () {
      final r = queryRuntimeGraph(<String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 1, 'type': 'a'},
          <String, dynamic>{'id': 2, 'type': 'b'},
        ],
      }, <String, dynamic>{
        'type': 'a'
      });
      expect(r['count'], equals(1));
      expect(r['bounded'], isTrue);
    });
  });
}
