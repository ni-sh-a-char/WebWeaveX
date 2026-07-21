import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('Adversarial - empty inputs', () {
    test('stableSerialize with empty map', () {
      expect(stableSerialize({}), isA<String>());
    });
    test('stableSerialize with empty list', () {
      expect(stableSerialize([]), isA<String>());
    });
    test('stableSerialize with deeply nested empty', () {
      expect(
          stableSerialize({
            'a': {
              'b': {'c': {}}
            }
          }),
          isA<String>());
    });
    test('normalizeRuntimeValue with empty', () {
      expect(normalizeRuntimeValue(''), equals(''));
    });
    test('graphFingerprint with empty graph', () {
      final g = buildRuntimeGraph({});
      expect(graphFingerprint(g).length, equals(64));
    });
  });

  group('Adversarial - large inputs', () {
    test('stableSerialize with 1000 keys', () {
      final data = Map.fromEntries(
        List.generate(1000, (i) => MapEntry('key_$i', i)),
      );
      final result = stableSerialize(data);
      expect(result, isA<String>());
      expect(result.length, greaterThan(100));
    });
    test('stableSerialize with deeply nested (50 levels)', () {
      dynamic nested = 'leaf';
      for (var i = 0; i < 50; i++) {
        nested = {'level_$i': nested};
      }
      expect(stableSerialize(nested), isA<String>());
    });
    test('buildRuntimeGraph with 5000 nodes', () {
      final graph = buildRuntimeGraph({
        'nodes': List.generate(5000, (i) => {'id': 'n$i', 'type': 't'}),
      });
      expect(graph, isNotNull);
    });
  });

  group('Adversarial - repeated execution', () {
    test('10000 serialize-deserialize cycles', () {
      final data = {'key': 'value', 'num': 42};
      for (var i = 0; i < 10000; i++) {
        final s = stableSerialize(data);
        expect(s, isA<String>());
      }
    });
    test('10000 replay cycles', () {
      final g = buildRuntimeGraph({'step': 1});
      final env = {'unified_runtime_graph': g.toJson()};
      for (var i = 0; i < 10000; i++) {
        final r = validateReplayEquivalence(env, env);
        expect(r['equivalent'], isTrue);
      }
    });
  });

  group('Adversarial - edge cases', () {
    test('stableSerialize with unicode keys', () {
      expect(stableSerialize({'\u00e9': 1, 'a': 2}), isA<String>());
    });
    test('stableSerialize with boolean and null values', () {
      expect(stableSerialize({'b': true, 'n': null, 's': ''}), isA<String>());
    });
    test('graphFingerprint is deterministic', () {
      final g = buildRuntimeGraph({'x': 1});
      final fp1 = graphFingerprint(g);
      final fp2 = graphFingerprint(g);
      expect(fp1, equals(fp2));
    });
    test('validateReplayEquivalence with corrupted envelope', () {
      final result = validateReplayEquivalence(
        {'garbage': true},
        {
          'more_garbage': [1, 2, 3]
        },
      );
      expect(result, isA<Map>());
    });
    test('encryptValue with empty string key', () {
      final e = encryptValue({'data': 1}, '');
      expect(e, isA<String>());
      final d = decryptValue(e, '');
      expect(d['data'], equals(1));
    });
    test('queryRuntimeGraph with null-like values', () {
      final result = queryRuntimeGraph(
        {
          'nodes': [
            {'id': 'n1', 'type': null}
          ],
          'edges': []
        },
        {'query_type': 'by_type', 'type': 'file'},
      );
      expect(result, isA<Map>());
    });
  });
}
