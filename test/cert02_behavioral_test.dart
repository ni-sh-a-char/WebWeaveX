import 'dart:convert';
import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('Replay validation', () {
    test('replay equivalence after serialization round-trip', () {
      final original = {
        'unified_runtime_graph': {
          'nodes': [{'id': 'n1', 'type': 'file', 'name': 'test.dart'}],
          'edges': [{'source': 'n1', 'target': 'n1', 'type': 'self'}]
        }
      };
      final serialized = jsonEncode(original);
      final deserialized = jsonDecode(serialized) as Map<String, dynamic>;
      final result = validateReplayEquivalence(original, deserialized);
      expect(result['equivalent'], isTrue);
    });

    test('replay equivalence after stableSerialize round-trip', () {
      final original = {
        'unified_runtime_graph': {
          'nodes': [{'id': 'n1', 'type': 'file'}],
          'edges': []
        }
      };
      final serialized = stableSerialize(original);
      final deserialized = jsonDecode(serialized) as Map<String, dynamic>;
      final result = validateReplayEquivalence(original, deserialized);
      expect(result['equivalent'], isTrue);
    });

    test('replay detects differing graphs', () {
      final a = {'unified_runtime_graph': {'nodes': [{'id': 'n1'}], 'edges': []}};
      final b = {'unified_runtime_graph': {'nodes': [{'id': 'n2'}], 'edges': []}};
      final result = validateReplayEquivalence(a, b);
      expect(result['equivalent'], isFalse);
    });
  });

  group('Memory validation', () {
    test('runtime memory fabric construction', () {
      final graph = RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'test.dart')],
        edges: [],
      );
      final fabric = buildRuntimeMemoryFabric(graph);
      expect(fabric, isA<Map<String, dynamic>>());
      expect(fabric.containsKey('memory'), isTrue);
      expect(fabric.containsKey('stable_hash'), isTrue);
    });

    test('memory fabric deterministic across rebuilds', () {
      final graph = RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'a.dart')],
        edges: [],
      );
      final f1 = buildRuntimeMemoryFabric(graph);
      final f2 = buildRuntimeMemoryFabric(graph);
      expect(f1['stable_hash'], equals(f2['stable_hash']));
    });

    test('memory merge produces deterministic result', () {
      final m1 = buildRuntimeMemoryFabric(RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'a.dart')],
        edges: [],
      ));
      final m2 = buildRuntimeMemoryFabric(RuntimeGraph(
        nodes: [RuntimeNode(id: 'n2', type: 'file', name: 'b.dart')],
        edges: [],
      ));
      final merged1 = mergeRuntimeMemories(m1, m2);
      final merged2 = mergeRuntimeMemories(m1, m2);
      expect(stableSerialize(merged1), equals(stableSerialize(merged2)));
    });
  });

  group('Knowledge graph validation', () {
    test('graph construction from nodes and edges', () {
      final graph = RuntimeGraph(
        nodes: [
          RuntimeNode(id: 'n1', type: 'file', name: 'test.dart'),
          RuntimeNode(id: 'n2', type: 'module', name: 'core'),
          RuntimeNode(id: 'n3', type: 'file', name: 'utils.dart'),
        ],
        edges: [
          RuntimeEdge(source: 'n1', target: 'n2', type: 'imports'),
          RuntimeEdge(source: 'n3', target: 'n2', type: 'imports'),
        ],
      );
      expect(graph.nodes.length, equals(3));
      expect(graph.edges.length, equals(2));
    });

    test('graph fingerprint is deterministic', () {
      final g1 = RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'a.dart')],
        edges: [],
      );
      final g2 = RuntimeGraph(
        nodes: [RuntimeNode(id: 'n1', type: 'file', name: 'a.dart')],
        edges: [],
      );
      expect(graphFingerprint(g1), equals(graphFingerprint(g2)));
    });

    test('graph query returns correct nodes', () {
      final graph = {
        'nodes': [
          {'id': 'n1', 'type': 'file'},
          {'id': 'n2', 'type': 'module'},
        ],
        'edges': [],
      };
      final result = queryRuntimeGraph(graph, {
        'query_type': 'by_type',
        'type': 'file'
      });
      expect(result, isA<Map>());
      expect(result.containsKey('results'), isTrue);
    });
  });
}
