import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  // A populated extraction envelope with an embedded graph map, browser IR,
  // runtime session and runtime_memory history. Used across many tests.
  Map<String, dynamic> populatedEnvelope() {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'browser': <String, dynamic>{'url': 'x', 'dom_hash': 'h'},
      'network': <dynamic>[
        <String, dynamic>{'url': 'x', 'method': 'GET'},
      ],
    });
    return <String, dynamic>{
      'bounded': true,
      'unified_runtime_graph': graph.toJson(),
      'graph': graph.toJson(),
      'runtime': <String, dynamic>{
        'available': true,
        'session': <String, dynamic>{'token': 'abc'},
      },
      'browser_ir': <String, dynamic>{
        'runtime_identity': 'ident-123',
        'storage': <String, dynamic>{'k': 'v'},
      },
      'runtime_memory': <String, dynamic>{
        'runtime_history': <dynamic>[
          <String, dynamic>{'step': 0},
          <String, dynamic>{'step': 1},
        ],
      },
    };
  }

  group('reconstructRuntimeGraph', () {
    test('returns empty graph when no graph key present', () {
      final g = reconstructRuntimeGraph(<String, dynamic>{});
      expect(g.nodes, isEmpty);
      expect(g.edges, isEmpty);
    });

    test('normalizes a passed-in RuntimeGraph instance', () {
      final raw = RuntimeGraph(
        nodes: <RuntimeNode>[
          RuntimeNode(id: 'b', type: 't'),
          RuntimeNode(id: 'a', type: 't'),
        ],
        edges: <RuntimeEdge>[],
        bounded: false,
      );
      final out = reconstructRuntimeGraph(
          <String, dynamic>{'unified_runtime_graph': raw});
      expect(out.bounded, isTrue);
      // normalized => sorted by id, so 'a' first.
      expect(out.nodes.first.id, 'a');
    });

    test('builds graph from a Map under graph key', () {
      final out = reconstructRuntimeGraph(<String, dynamic>{
        'graph': <String, dynamic>{'nodes': <dynamic>[], 'edges': <dynamic>[]},
      });
      expect(out.nodes, isNotEmpty);
    });

    test('builds graph from unified_runtime_graph map', () {
      final out = reconstructRuntimeGraph(<String, dynamic>{
        'unified_runtime_graph': <String, dynamic>{'a': 1},
      });
      expect(out.nodes, isNotEmpty);
    });
  });

  group('reconstructGraphFromSources', () {
    test('produces a graph from multiple sources with edges', () {
      final g = reconstructGraphFromSources(<String, dynamic>{
        'alpha': <String, dynamic>{'v': 1},
        'beta': <String, dynamic>{'v': 2},
      });
      expect(g.nodes.length, 2);
      expect(g.edges.length, 1);
    });

    test('single source has no edges', () {
      final g = reconstructGraphFromSources(<String, dynamic>{'only': 'value'});
      expect(g.nodes.length, 1);
      expect(g.edges, isEmpty);
    });
  });

  group('graphReconstructionFingerprint', () {
    test('is deterministic and non-empty', () {
      final g = reconstructGraphFromSources(<String, dynamic>{'a': 1});
      final f1 = graphReconstructionFingerprint(g);
      final f2 = graphReconstructionFingerprint(g);
      expect(f1, isNotEmpty);
      expect(f1, equals(f2));
    });
  });

  group('reconstructBrowserState', () {
    test('uses identity and IR storage from a populated envelope', () {
      final out = reconstructBrowserState(populatedEnvelope());
      expect(out['runtime_identity'], 'ident-123');
      expect(out['storage'], <String, dynamic>{'k': 'v'});
      expect(out['session'], <String, dynamic>{'token': 'abc'});
      expect(out['bounded'], isTrue);
      expect(out['tabs'], hasLength(1));
      expect(out['navigation_history'], hasLength(1));
    });

    test('falls back to empty maps for an empty extraction', () {
      final out = reconstructBrowserState(<String, dynamic>{});
      expect(out['runtime_identity'], '');
      expect(out['session'], <String, dynamic>{});
      expect(out['storage'], <String, dynamic>{});
      expect(out['bounded'], isTrue);
    });
  });

  group('reconstructMemoryGraph', () {
    test('builds memory graph + fabric with default empty history', () {
      final g = reconstructGraphFromSources(<String, dynamic>{
        'a': 1,
        'b': 2,
      });
      final out = reconstructMemoryGraph(g);
      expect(out['memory_graph'], isA<Map<String, dynamic>>());
      expect(out['memory'], isA<Map<String, dynamic>>());
      expect(out['stable_hash'], isNotEmpty);
      expect(out['bounded'], isTrue);
    });

    test('honors explicit history list', () {
      final g = reconstructGraphFromSources(<String, dynamic>{'a': 1});
      final out = reconstructMemoryGraph(g, <dynamic>[
        <String, dynamic>{'e': 0}
      ]);
      final mg = out['memory_graph'] as Map<String, dynamic>;
      expect(mg['entities'], isA<List<dynamic>>());
      expect(mg['relations'], isA<List<dynamic>>());
    });
  });

  group('reconstructMemoryFromEnvelope', () {
    test('reads runtime_history from envelope', () {
      final out = reconstructMemoryFromEnvelope(populatedEnvelope());
      expect(out['memory_graph'], isA<Map<String, dynamic>>());
      expect(out['stable_hash'], isNotEmpty);
    });

    test('handles envelope without runtime_memory', () {
      final out = reconstructMemoryFromEnvelope(<String, dynamic>{});
      expect(out['bounded'], isTrue);
    });
  });

  group('reconstructReplayState', () {
    test('produces replay + graph + memory + browser + validation', () {
      final out = reconstructReplayState(populatedEnvelope());
      expect(out['replayed'], isA<Map<String, dynamic>>());
      expect(out['graph'], isA<Map<String, dynamic>>());
      expect(out['memory'], isA<Map<String, dynamic>>());
      expect(out['browser'], isA<Map<String, dynamic>>());
      expect(out['validation'], isA<Map<String, dynamic>>());
      expect(out['bounded'], isTrue);
    });

    test('replay validation marks identical state equivalent', () {
      final out = reconstructReplayState(populatedEnvelope());
      final validation = out['validation'] as Map<String, dynamic>;
      expect(validation['equivalent'], isTrue);
    });

    test('works on an empty extraction', () {
      final out = reconstructReplayState(<String, dynamic>{});
      expect(out['bounded'], isTrue);
    });
  });

  group('reconstructRuntime', () {
    test('produces runtime_id of length 32 and embedded sections', () {
      final out = reconstructRuntime(extraction: populatedEnvelope());
      expect((out['runtime_id'] as String).length, 32);
      expect(out['graph'], isA<Map<String, dynamic>>());
      expect(out['memory'], isA<Map<String, dynamic>>());
      expect(out['browser'], isA<Map<String, dynamic>>());
      expect(out['reconstructed'], isTrue);
      expect(out['bounded'], isTrue);
    });

    test('is deterministic for the same input', () {
      final a = reconstructRuntime(extraction: populatedEnvelope());
      final b = reconstructRuntime(extraction: populatedEnvelope());
      expect(a['runtime_id'], b['runtime_id']);
    });
  });

  group('replayRuntime', () {
    test('returns the replayed map', () {
      final out = replayRuntime(populatedEnvelope());
      expect(out, isA<Map<String, dynamic>>());
      expect(out['bounded'], isTrue);
    });
  });

  group('rebuildExecutionGraph', () {
    test('counts nodes and edges and fingerprints', () {
      final g = reconstructGraphFromSources(<String, dynamic>{
        'a': 1,
        'b': 2,
        'c': 3,
      });
      final out = rebuildExecutionGraph(g);
      expect(out['nodes'], 3);
      expect(out['edges'], 2);
      expect(out['fingerprint'], isNotEmpty);
      expect(out['bounded'], isTrue);
    });

    test('empty graph reports zero counts', () {
      final out = rebuildExecutionGraph(
          RuntimeGraph(nodes: <RuntimeNode>[], edges: <RuntimeEdge>[]));
      expect(out['nodes'], 0);
      expect(out['edges'], 0);
    });
  });
}
