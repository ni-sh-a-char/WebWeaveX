import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('Long-run stability', () {
    test('10000 sequential graph builds', () {
      final sw = Stopwatch()..start();
      for (var i = 0; i < 10000; i++) {
        final g = buildRuntimeGraph({'step': i, 'data': 'item_$i'});
        expect(g, isNotNull);
      }
      sw.stop();
      expect(sw.elapsedMilliseconds, lessThan(30000));
    });

    test('10000 replay operations', () {
      final graph = buildRuntimeGraph({'step': 1});
      final env = {'unified_runtime_graph': graph.toJson()};
      for (var i = 0; i < 10000; i++) {
        final r = validateReplayEquivalence(env, env);
        expect(r['equivalent'], isTrue);
      }
    });

    test('10000 canonical serializations identical', () {
      final data = {'z': 1, 'a': 2, 'n': {'b': 3}};
      final expected = stableSerialize(data);
      for (var i = 0; i < 10000; i++) {
        expect(stableSerialize(data), equals(expected));
      }
    });

    test('10000 fingerprints identical', () {
      final g = buildRuntimeGraph({'key': 'val'});
      final fp = graphFingerprint(g);
      for (var i = 0; i < 10000; i++) {
        expect(graphFingerprint(g), equals(fp));
      }
    });
  });

  group('Large-scale', () {
    test('graph with 1000 nodes', () {
      final graph = buildRuntimeGraph({
        'nodes': List.generate(1000, (i) => {'id': 'n$i', 'type': 'file'}),
        'edges': List.generate(999, (i) => {'source': 'n$i', 'target': 'n${i+1}'}),
      });
      final fp = graphFingerprint(graph);
      expect(fp.length, equals(64));
    });
  });

  group('Error resilience', () {
    test('stableSerialize with null values', () {
      expect(stableSerialize({'key': null}), isA<String>());
    });

    test('stableSerialize with empty structures', () {
      expect(stableSerialize({'a': {}, 'b': [], 'c': ''}), isA<String>());
    });

    test('graphFingerprint on empty graph', () {
      expect(graphFingerprint(buildRuntimeGraph({})).length, equals(64));
    });

    test('validateReplayEquivalence on empty envelopes', () {
      expect(validateReplayEquivalence({}, {}), isA<Map>());
    });

    test('normalizeRuntimeValue on empty string', () {
      expect(normalizeRuntimeValue(''), equals(''));
    });

    test('queryRuntimeGraph on malformed query', () {
      expect(queryRuntimeGraph({'nodes': [], 'edges': []}, {}), isA<Map>());
    });
  });

  group('Determinism stress', () {
    test('5000 iterations bit-identical for complex data', () {
      final data = {'v': '3.0.0', 'n': {'a': 1, 'b': [1, 2, 3]}, 'l': [{'x': 1}]};
      final expected = stableSerialize(data);
      for (var i = 0; i < 5000; i++) {
        expect(stableSerialize(data), equals(expected));
      }
    });

    test('fingerprint chain deterministic', () {
      final g1 = buildRuntimeGraph({'a': 1});
      final g2 = buildRuntimeGraph({'a': 1});
      expect(graphFingerprint(g1), equals(graphFingerprint(g2)));
    });

    test('memory fabric deterministic', () {
      final g = buildRuntimeGraph({'k': 'v'});
      final f1 = buildRuntimeMemoryFabric(g);
      final f2 = buildRuntimeMemoryFabric(g);
      expect(f1['stable_hash'], equals(f2['stable_hash']));
    });
  });
}
