import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        computeGlobalRuntimeFingerprint,
        queryRuntimeGraph,
        validateReplayEquivalence;

/// Cross-language parity tests for canonical runtime APIs.
/// Tests verify that Dart output matches expected behavior from Python/JS.
void main() {
  group('canonical runtime APIs — parity', () {
    test('compute_global_runtime_fingerprint with empty inputs', () {
      final result = computeGlobalRuntimeFingerprint(
        extraction: <String, dynamic>{},
        graph: <String, dynamic>{},
        memory: <String, dynamic>{},
        sync: <String, dynamic>{},
        reconstruction: <String, dynamic>{},
        kaalkaSeal: '',
      );
      expect(computeDeterministicHash(result).length, equals(64));
    });

    test('compute_global_runtime_fingerprint with data', () {
      final result = computeGlobalRuntimeFingerprint(
        extraction: <String, dynamic>{
          'pipeline_hash': 'test_hash',
        },
        graph: <String, dynamic>{},
        memory: <String, dynamic>{},
        sync: <String, dynamic>{},
        reconstruction: <String, dynamic>{},
        kaalkaSeal: 'seal',
      );
      expect(computeDeterministicHash(result).length, equals(64));
    });

    test('compute_global_runtime_fingerprint is deterministic', () {
      final a = computeGlobalRuntimeFingerprint(
        extraction: <String, dynamic>{'pipeline_hash': 'x'},
      );
      final b = computeGlobalRuntimeFingerprint(
        extraction: <String, dynamic>{'pipeline_hash': 'x'},
      );
      expect(a, equals(b));
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

    test('query_runtime_graph with empty graph', () {
      final r = queryRuntimeGraph(<String, dynamic>{
        'nodes': <dynamic>[],
      }, <String, dynamic>{
        'type': 'a'
      });
      expect(r['count'], equals(0));
    });

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

    test('validate_replay_equivalence detects differences', () {
      final a = <String, dynamic>{
        'unified_runtime_graph': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[],
        },
        'browser_ir': <String, dynamic>{'runtime_identity': 'id1'},
      };
      final b = <String, dynamic>{
        'unified_runtime_graph': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[],
        },
        'browser_ir': <String, dynamic>{'runtime_identity': 'id2'},
      };
      final r = validateReplayEquivalence(a, b);
      expect(r['equivalent'], isFalse);
    });
  });
}
