import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('buildRuntimeGraph', () {
    test('empty sources yields empty graph, no edges', () {
      final g = buildRuntimeGraph(<String, dynamic>{});
      expect(g.nodes, isEmpty);
      expect(g.edges, isEmpty);
      expect(g.bounded, isTrue);
    });

    test('single source yields one node and no edges', () {
      final g = buildRuntimeGraph(<String, dynamic>{'alpha': 1});
      expect(g.nodes.length, 1);
      expect(g.edges, isEmpty);
      expect(g.nodes.first.type, 'alpha');
      expect(g.nodes.first.payload, 1);
    });

    test('multiple sources create runtime_link edges from first node', () {
      final g = buildRuntimeGraph(<String, dynamic>{
        'alpha': <String, dynamic>{'k': 1},
        'beta': <String, dynamic>{'k': 2},
        'gamma': <String, dynamic>{'k': 3},
      });
      expect(g.nodes.length, 3);
      expect(g.edges.length, 2);
      for (final e in g.edges) {
        expect(e.type, 'runtime_link');
      }
    });

    test('is deterministic across builds (order independent)', () {
      final a = buildRuntimeGraph(<String, dynamic>{'b': 2, 'a': 1, 'c': 3});
      final b = buildRuntimeGraph(<String, dynamic>{'c': 3, 'a': 1, 'b': 2});
      expect(graphFingerprint(a), graphFingerprint(b));
    });
  });

  group('normalizeRuntimeGraph', () {
    test('sorts nodes and edges deterministically and sets bounded', () {
      final unsorted = RuntimeGraph(
        nodes: <RuntimeNode>[
          RuntimeNode(id: 'z', type: 't', name: 'n'),
          RuntimeNode(id: 'a', type: 't', name: 'n'),
        ],
        edges: <RuntimeEdge>[
          RuntimeEdge(source: 'z', target: 'a', type: 'e'),
          RuntimeEdge(source: 'a', target: 'z', type: 'e'),
        ],
        bounded: false,
      );
      final n = normalizeRuntimeGraph(unsorted);
      expect(n.nodes.first.id, 'a');
      expect(n.edges.first.source, 'a');
      expect(n.bounded, isTrue);
    });

    test('handles edges defined via from/to fallback keys', () {
      final g = RuntimeGraph(
        nodes: <RuntimeNode>[],
        edges: <RuntimeEdge>[
          RuntimeEdge(from: 'b', to: 'c', type: 'e'),
          RuntimeEdge(from: 'a', to: 'c', type: 'e'),
        ],
      );
      final n = normalizeRuntimeGraph(g);
      expect(n.edges.first.from, 'a');
    });

    test('handles nodes with all-null sortable fields', () {
      final g = RuntimeGraph(
        nodes: <RuntimeNode>[RuntimeNode(), RuntimeNode()],
        edges: <RuntimeEdge>[],
      );
      final n = normalizeRuntimeGraph(g);
      expect(n.nodes.length, 2);
    });
  });

  group('queryRuntimeGraph', () {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'alpha': <String, dynamic>{'k': 1},
      'beta': <String, dynamic>{'k': 2},
    });

    test('null nodeType returns normalized full graph', () {
      final q = queryRuntimeGraph(graph);
      expect(q.nodes.length, 2);
    });

    test('present nodeType filters to matching nodes', () {
      final q = queryRuntimeGraph(graph, nodeType: 'alpha');
      expect(q.nodes.length, 1);
      expect(q.nodes.first.type, 'alpha');
    });

    test('absent nodeType yields empty nodes but keeps edges', () {
      final q = queryRuntimeGraph(graph, nodeType: 'missing');
      expect(q.nodes, isEmpty);
      expect(q.edges, isNotEmpty);
    });
  });

  group('fingerprints and validation', () {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'alpha': <String, dynamic>{'k': 1},
      'beta': <String, dynamic>{'k': 2},
    });

    test('graphFingerprint is deterministic', () {
      expect(graphFingerprint(graph), graphFingerprint(graph));
    });

    test('computeRuntimeFingerprint aliases graphFingerprint', () {
      expect(computeRuntimeFingerprint(graph), graphFingerprint(graph));
    });

    test('validateRuntimeGraph returns full contract report', () {
      final r = validateRuntimeGraph(graph);
      expect(r['valid'], isTrue);
      expect(r['bounded'], isTrue);
      expect(r['node_count'], 2);
      expect(r['edge_count'], 1);
      expect(r['fingerprint'], graphFingerprint(graph));
    });

    test('toJson round-trips node/edge/graph shapes', () {
      final node = RuntimeNode(
        id: 'i',
        type: 't',
        name: 'n',
        payload: <String, dynamic>{'x': 1},
      );
      expect(node.toJson()['id'], 'i');
      final edge = RuntimeEdge(
        source: 's',
        target: 't',
        type: 'e',
        from: 'f',
        to: 'to',
      );
      final ej = edge.toJson();
      expect(ej['from'], 'f');
      expect(ej['to'], 'to');
      final gj = graph.toJson();
      expect(gj['bounded'], isTrue);
      expect(gj['nodes'], isA<List<dynamic>>());
    });
  });

  group('runtime_graph_replay', () {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'alpha': <String, dynamic>{'k': 1},
      'beta': <String, dynamic>{'k': 2},
    });

    test('replayGraphLineage exposes replayed graph and lineage hash', () {
      final r = replayGraphLineage(graph);
      expect(r['bounded'], isTrue);
      expect(r['lineage_hash'], isA<String>());
      expect((r['replayed'] as Map<String, dynamic>)['nodes'], isNotEmpty);
    });

    test('mergeGraphReplay combines and normalizes two graphs', () {
      final base = buildRuntimeGraph(<String, dynamic>{'a': 1});
      final overlay = buildRuntimeGraph(<String, dynamic>{'b': 2});
      final merged = mergeGraphReplay(base, overlay);
      expect(merged.nodes.length, 2);
      expect(merged.bounded, isTrue);
    });

    test('graphReplayHash is deterministic', () {
      expect(graphReplayHash(graph), graphReplayHash(graph));
    });

    test('replayRuntimeGraph reconstructs equivalent graph', () {
      final replayed = replayRuntimeGraph(graph);
      final r = validateGraphReplayEquivalence(graph, replayed);
      expect(r['equivalent'], isTrue);
      expect(r['graph_hash'], r['replay_hash']);
    });

    test('validateGraphReplayEquivalence detects mismatch', () {
      final other = buildRuntimeGraph(<String, dynamic>{'z': 99});
      final r = validateGraphReplayEquivalence(graph, other);
      expect(r['equivalent'], isFalse);
    });
  });

  group('runtime_graph_reconstruction', () {
    test('reconstructGraphFromIr builds graph with fingerprint', () {
      final r = reconstructGraphFromIr(<String, dynamic>{
        'alpha': <String, dynamic>{'k': 1},
        'beta': <String, dynamic>{'k': 2},
      });
      expect(r['bounded'], isTrue);
      expect(r['fingerprint'], isA<String>());
      expect((r['graph'] as Map<String, dynamic>)['nodes'], isNotEmpty);
    });

    test('rebuildGraphFromPartial preserves ids and normalizes', () {
      final partial = buildRuntimeGraph(<String, dynamic>{
        'alpha': <String, dynamic>{'k': 1},
        'beta': <String, dynamic>{'k': 2},
      });
      final rebuilt = rebuildGraphFromPartial(partial);
      expect(rebuilt.nodes.length, partial.nodes.length);
      expect(rebuilt.bounded, isTrue);
    });

    test('rebuildGraphFromPartial assigns ids when missing', () {
      final partial = RuntimeGraph(
        nodes: <RuntimeNode>[
          RuntimeNode(type: 't1'),
          RuntimeNode(type: 't2'),
        ],
        edges: <RuntimeEdge>[],
      );
      final rebuilt = rebuildGraphFromPartial(partial);
      expect(rebuilt.nodes.every((n) => n.id != null), isTrue);
    });
  });
}
