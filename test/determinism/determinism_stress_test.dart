import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('Determinism 1000-iteration validation', () {
    test('stableSerialize is identical across 1000 iterations', () {
      final data = {
        'z': 1,
        'a': 2,
        'm': {'b': 3, 'a': 1}
      };
      final expected = stableSerialize(data);
      for (var i = 0; i < 1000; i++) {
        expect(stableSerialize(data), equals(expected));
      }
    });

    test('normalizeRuntimeValue is deterministic across 1000 iterations', () {
      final values = ['Hello World', 'test', '  spaced  ', 'CamelCase'];
      for (final v in values) {
        final expected = normalizeRuntimeValue(v);
        for (var i = 0; i < 1000; i++) {
          expect(normalizeRuntimeValue(v), equals(expected));
        }
      }
    });

    test('graphFingerprint is stable across 1000 iterations', () {
      final graph = RuntimeGraph(
        nodes: [
          RuntimeNode(id: 'n1', type: 'file', name: 'test.dart'),
          RuntimeNode(id: 'n2', type: 'module', name: 'core')
        ],
        edges: [RuntimeEdge(source: 'n1', target: 'n2', type: 'imports')],
      );
      final expected = graphFingerprint(graph);
      for (var i = 0; i < 1000; i++) {
        expect(graphFingerprint(graph), equals(expected));
      }
    });

    test('computeRuntimePipelineFingerprint is stable across 1000 iterations',
        () {
      final graph = RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'test.dart')],
        edges: [],
      );
      final envelope = {'pipeline_hash': 'abc', 'bounded': true};
      final expected = computeRuntimePipelineFingerprint(envelope, graph);
      for (var i = 0; i < 1000; i++) {
        expect(computeRuntimePipelineFingerprint(envelope, graph),
            equals(expected));
      }
    });

    test('stableSerialize produces sorted keys', () {
      final data = {'z': 1, 'a': 2, 'm': 3, 'b': 4};
      final result = stableSerialize(data);
      final aIndex = result.indexOf('"a"');
      final bIndex = result.indexOf('"b"');
      final mIndex = result.indexOf('"m"');
      final zIndex = result.indexOf('"z"');
      expect(aIndex, lessThan(bIndex));
      expect(bIndex, lessThan(mIndex));
      expect(mIndex, lessThan(zIndex));
    });

    test('validateReplayEquivalence is deterministic', () {
      final original = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n1', 'type': 'file', 'name': 'a.dart'}
          ],
          'edges': []
        }
      };
      final replayed = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n1', 'type': 'file', 'name': 'a.dart'}
          ],
          'edges': []
        }
      };
      final expected = validateReplayEquivalence(original, replayed);
      for (var i = 0; i < 1000; i++) {
        expect(validateReplayEquivalence(original, replayed), equals(expected));
      }
    });

    test('computeGlobalRuntimeFingerprint is deterministic', () {
      final envelope = {
        'unified_runtime_graph': {
          'nodes': [
            {'id': 'n1', 'type': 'file'}
          ],
          'edges': []
        },
        'pipeline_hash': 'test_hash'
      };
      final expected = computeGlobalRuntimeFingerprint(extraction: envelope);
      for (var i = 0; i < 1000; i++) {
        expect(computeGlobalRuntimeFingerprint(extraction: envelope),
            equals(expected));
      }
    });
  });
}
