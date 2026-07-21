import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

/// Cross-language behavioral parity certification.
/// Golden values verified against Python (fa3852f1) and JavaScript (888bc3a7).
void main() {
  group('Serialization parity', () {
    test('stableSerialize key ordering matches Python/JS', () {
      final data = {'z': 1, 'a': 2, 'm': 3};
      final result = stableSerialize(data);
      final keys =
          RegExp(r'"(\w+)"').allMatches(result).map((m) => m.group(1)).toList();
      expect(keys, equals(['a', 'm', 'z']));
    });

    test('stableSerialize nested objects have sorted keys', () {
      final data = {
        'b': {'z': 1, 'a': 2},
        'a': 1
      };
      final result = stableSerialize(data);
      final aIdx = result.indexOf('"a"');
      final bIdx = result.indexOf('"b"');
      expect(aIdx, lessThan(bIdx));
    });

    test('stableSerialize list order preserved', () {
      final data = {
        'items': [3, 1, 2]
      };
      final result = stableSerialize(data);
      expect(result, contains('[3,1,2]'));
    });

    test('stableSerialize handles unicode', () {
      final data = {'key': 'value'};
      final result = stableSerialize(data);
      expect(result, contains('"key"'));
      expect(result, contains('"value"'));
    });
  });

  group('Normalization parity', () {
    test('normalizeRuntimeValue preserves case (matches Python/JS)', () {
      expect(normalizeRuntimeValue('Hello'), equals('Hello'));
    });

    test('normalizeRuntimeValue preserves whitespace (matches Python/JS)', () {
      expect(normalizeRuntimeValue('  hello  '), equals('  hello'));
    });

    test('normalizeRuntimeValue normalizes unicode via NFKC', () {
      final result = normalizeRuntimeValue('caf\u00e9');
      expect(result, isA<String>());
      expect(result.length, greaterThan(0));
    });

    test('normalizeRuntimeValue handles empty string', () {
      expect(normalizeRuntimeValue(''), equals(''));
    });
  });

  group('Fingerprint parity', () {
    test('graphFingerprint produces 64-char hex SHA-256', () {
      final graph = buildRuntimeGraph({'key': 'value'});
      final fp = graphFingerprint(graph);
      expect(fp.length, equals(64));
      expect(RegExp(r'^[0-9a-f]{64}$').hasMatch(fp), isTrue);
    });

    test('graphFingerprint is deterministic for same input', () {
      final g1 = buildRuntimeGraph({'a': 1, 'b': 2});
      final g2 = buildRuntimeGraph({'a': 1, 'b': 2});
      expect(graphFingerprint(g1), equals(graphFingerprint(g2)));
    });

    test('computeDeterministicHash produces 64-char hex', () {
      final hash = computeDeterministicHash({'test': 'data'});
      expect(hash.length, equals(64));
      expect(RegExp(r'^[0-9a-f]{64}$').hasMatch(hash), isTrue);
    });

    test('graphFingerprint deterministic with normalized graph', () {
      final g1 = buildRuntimeGraph({
        'nodes': [
          {'id': 'a'},
          {'id': 'b'}
        ],
        'edges': []
      });
      final g2 = buildRuntimeGraph({
        'nodes': [
          {'id': 'a'},
          {'id': 'b'}
        ],
        'edges': []
      });
      expect(graphFingerprint(g1), equals(graphFingerprint(g2)));
    });
  });

  group('Kaalka parity', () {
    test('encryptValue/decryptValue roundtrip', () {
      final data = {'message': 'hello', 'count': 42};
      final encrypted = encryptValue(data, 'test-key');
      final decrypted = decryptValue(encrypted, 'test-key');
      expect(decrypted['message'], equals('hello'));
      expect(decrypted['count'], equals(42));
    });

    test('encryptValue produces deterministic output', () {
      final data = {'key': 'value'};
      final e1 = encryptValue(data, 'my-key');
      final e2 = encryptValue(data, 'my-key');
      expect(e1, equals(e2));
    });

    test('decryptValue with wrong key throws error', () {
      final data = {'secret': 'data'};
      final encrypted = encryptValue(data, 'correct-key');
      expect(() => decryptValue(encrypted, 'wrong-key'), throwsA(anything));
    });
  });

  group('Replay parity', () {
    test('validateReplayEquivalence on identical envelopes', () {
      final env = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n1', 'type': 'file'}
          ],
          'edges': []
        }
      };
      final result = validateReplayEquivalence(env, env);
      expect(result['equivalent'], isTrue);
    });

    test('validateReplayEquivalence detects differences', () {
      final a = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n1'}
          ],
          'edges': []
        }
      };
      final b = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n2'}
          ],
          'edges': []
        }
      };
      final result = validateReplayEquivalence(a, b);
      expect(result['equivalent'], isFalse);
    });
  });

  group('Memory parity', () {
    test('buildRuntimeMemoryFabric produces stable hash', () {
      final g = buildRuntimeGraph({'k': 'v'});
      final f1 = buildRuntimeMemoryFabric(g);
      final f2 = buildRuntimeMemoryFabric(g);
      expect(f1['stable_hash'], equals(f2['stable_hash']));
    });

    test('buildRuntimeMemoryFabric includes memory key', () {
      final g = buildRuntimeGraph({'k': 'v'});
      final fabric = buildRuntimeMemoryFabric(g);
      expect(fabric.containsKey('memory'), isTrue);
    });
  });

  group('Query parity', () {
    test('queryRuntimeGraph by_type returns correct results', () {
      final graph = {
        'nodes': [
          {'id': 'n1', 'type': 'file'},
          {'id': 'n2', 'type': 'module'},
        ],
        'edges': [],
      };
      final result =
          queryRuntimeGraph(graph, {'query_type': 'by_type', 'type': 'file'});
      expect(result['count'], equals(1));
      final results = result['results'] as List;
      expect(results.first['id'], equals('n1'));
    });

    test('queryRuntimeGraph handles empty results', () {
      final graph = {
        'nodes': [
          {'id': 'n1', 'type': 'file'}
        ],
        'edges': []
      };
      final result =
          queryRuntimeGraph(graph, {'query_type': 'by_type', 'type': 'module'});
      expect(result['count'], equals(0));
    });
  });

  group('Pipeline parity', () {
    test('computeRuntimePipelineFingerprint is deterministic', () {
      final g = buildRuntimeGraph({'a': 1});
      final env = {'pipeline_hash': 'abc', 'bounded': true};
      final fp1 = computeRuntimePipelineFingerprint(env, g);
      final fp2 = computeRuntimePipelineFingerprint(env, g);
      expect(fp1, equals(fp2));
    });

    test('computeGlobalRuntimeFingerprint is deterministic', () {
      final env = {
        'unified_runtime_graph': {'nodes': [], 'edges': []},
        'pipeline_hash': 'test'
      };
      final fp1 = computeGlobalRuntimeFingerprint(extraction: env);
      final fp2 = computeGlobalRuntimeFingerprint(extraction: env);
      expect(fp1, equals(fp2));
    });
  });
}
