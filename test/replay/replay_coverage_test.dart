import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

Map<String, dynamic> _graphMap() => <String, dynamic>{
      'nodes': <dynamic>[
        <String, dynamic>{'id': 'n1', 'type': 'alpha', 'payload': 1},
        <String, dynamic>{'id': 'n2', 'type': 'beta', 'payload': 2},
      ],
      'edges': <dynamic>[
        <String, dynamic>{
          'source': 'n1',
          'target': 'n2',
          'type': 'runtime_link'
        },
      ],
    };

Map<String, dynamic> _envelope() => <String, dynamic>{
      'pipeline_hash': 'ph-123',
      'graph': _graphMap(),
      'dom_snapshot': '<div data-reactid="x">hello</div>',
      'browser_ir': <String, dynamic>{
        'runtime_identity': 'identity-abc',
        'dom_html': '<div>body</div>',
      },
    };

void main() {
  group('replay_dom', () {
    test('replayDomSnapshot stabilizes html and hashes it', () {
      final r = replayDomSnapshot('<div data-reactid="a">x</div>');
      expect(r['bounded'], isTrue);
      expect(r['stabilized'], isA<String>());
      expect(r['hash'], isA<String>());
    });

    test('validateDomReplayEquivalence true for stabilization-equivalent html',
        () {
      final a = '<div data-reactid="1">x</div>';
      final b = '<div data-reactid="2">x</div>';
      expect(validateDomReplayEquivalence(a, b), isTrue);
    });

    test('validateDomReplayEquivalence false for differing html', () {
      expect(validateDomReplayEquivalence('<p>a</p>', '<p>b</p>'), isFalse);
    });
  });

  group('replay_memory', () {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'alpha': <String, dynamic>{'k': 1},
      'beta': <String, dynamic>{'k': 2},
    });

    test('replayRuntimeMemory builds bounded memory with stable hash', () {
      final m = replayRuntimeMemory(graph);
      expect(m['bounded'], isTrue);
      expect(m['stable_hash'], isA<String>());
    });

    test('replayRuntimeMemory with history', () {
      final m = replayRuntimeMemory(graph, <dynamic>['ev1', 'ev2']);
      expect(m['stable_hash'], isA<String>());
    });

    test('memoryReplayHash is deterministic', () {
      expect(memoryReplayHash(graph), memoryReplayHash(graph));
    });

    test('validateMemoryReplayEquivalence true for matching hashes', () {
      final a = replayRuntimeMemory(graph);
      final b = replayRuntimeMemory(graph);
      final r = validateMemoryReplayEquivalence(a, b);
      expect(r['equivalent'], isTrue);
      expect(r['stable_hash_match'], isTrue);
    });

    test('validateMemoryReplayEquivalence false for differing hashes', () {
      final a = replayRuntimeMemory(graph);
      final b = replayRuntimeMemory(
        buildRuntimeGraph(<String, dynamic>{'other': 9}),
      );
      final r = validateMemoryReplayEquivalence(a, b);
      expect(r['equivalent'], isFalse);
    });
  });

  group('replay_graph', () {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'alpha': <String, dynamic>{'k': 1},
      'beta': <String, dynamic>{'k': 2},
    });

    test('graphReplayHash deterministic', () {
      expect(graphReplayHash(graph), graphReplayHash(graph));
    });

    test('replayRuntimeGraph + validateGraphReplayEquivalence equivalent', () {
      final replayed = replayRuntimeGraph(graph);
      final r = validateGraphReplayEquivalence(graph, replayed);
      expect(r['equivalent'], isTrue);
    });

    test('validateGraphReplayEquivalence not equivalent for different graph',
        () {
      final r = validateGraphReplayEquivalence(
        graph,
        buildRuntimeGraph(<String, dynamic>{'z': 1}),
      );
      expect(r['equivalent'], isFalse);
    });
  });

  group('replay_fingerprint', () {
    test('equivalent for identical envelopes', () {
      final r = validateFingerprintReplayEquivalence(_envelope(), _envelope());
      expect(r['equivalent'], isTrue);
      expect(r['global_fingerprint_match'], isTrue);
      expect(r['graph_hash_match'], isTrue);
    });

    test('not equivalent for differing pipeline_hash/graph', () {
      final a = _envelope();
      final b = _envelope()
        ..['pipeline_hash'] = 'different'
        ..['graph'] = <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'x', 'type': 'zeta', 'payload': 9},
          ],
          'edges': <dynamic>[],
        };
      final r = validateFingerprintReplayEquivalence(a, b);
      expect(r['equivalent'], isFalse);
    });

    test('accepts explicit graph and memory args', () {
      final g = buildRuntimeGraph(<String, dynamic>{'a': 1});
      final r = validateFingerprintReplayEquivalence(
        _envelope(),
        _envelope(),
        graph: g,
        memory: <String, dynamic>{'stable_hash': 'h'},
      );
      expect(r, isA<Map<String, dynamic>>());
    });

    test('handles RuntimeGraph-typed envelope graph and missing graph', () {
      final withGraph = <String, dynamic>{
        'pipeline_hash': 'p',
        'unified_runtime_graph': buildRuntimeGraph(<String, dynamic>{'a': 1}),
      };
      final empty = <String, dynamic>{'pipeline_hash': 'p'};
      final r1 = validateFingerprintReplayEquivalence(withGraph, withGraph);
      final r2 = validateFingerprintReplayEquivalence(empty, empty);
      expect(r1['graph_hash_match'], isTrue);
      expect(r2['graph_hash_match'], isTrue);
    });
  });

  group('replay_equivalence', () {
    test('equivalent for identical envelopes', () {
      final r = validateReplayEquivalenceExtended(_envelope(), _envelope());
      expect(r['equivalent'], isTrue);
      final checks = r['checks'] as List<dynamic>;
      expect(checks.every((c) => (c as Map)['ok'] == true), isTrue);
    });

    test('not equivalent when graph differs', () {
      final a = _envelope();
      final b = _envelope()
        ..['graph'] = <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'q', 'type': 'q', 'payload': 0},
          ],
          'edges': <dynamic>[],
        };
      final r = validateReplayEquivalenceExtended(a, b);
      expect(r['equivalent'], isFalse);
    });

    test('not equivalent when browser identity differs', () {
      final a = _envelope();
      final b = _envelope()
        ..['browser_ir'] = <String, dynamic>{
          'runtime_identity': 'other-identity',
          'dom_html': '<div>body</div>',
        };
      final r = validateReplayEquivalenceExtended(a, b);
      expect(r['equivalent'], isFalse);
    });

    test('not equivalent when dom snapshot differs materially', () {
      final a = _envelope();
      final b = _envelope()..['dom_snapshot'] = '<div>totally different</div>';
      final r = validateReplayEquivalenceExtended(a, b);
      expect(r['equivalent'], isFalse);
    });

    test('includes memory check when both envelopes carry runtime_memory', () {
      final a = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'mh'};
      final b = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'mh'};
      final r = validateReplayEquivalenceExtended(a, b);
      final checks = r['checks'] as List<dynamic>;
      expect(
        checks.any((c) => (c as Map)['name'] == 'memory_stable_hash'),
        isTrue,
      );
      expect(r['equivalent'], isTrue);
    });

    test('handles envelopes with no dom snapshot (skips dom check)', () {
      final a = <String, dynamic>{
        'pipeline_hash': 'p',
        'graph': _graphMap(),
        'browser_ir': <String, dynamic>{'runtime_identity': 'id'},
      };
      final r = validateReplayEquivalenceExtended(a, a);
      final checks = r['checks'] as List<dynamic>;
      expect(
        checks.any((c) => (c as Map)['name'] == 'dom_stabilized_hash'),
        isFalse,
      );
      expect(r['equivalent'], isTrue);
    });

    test('uses RuntimeGraph-typed graph and dom_html/browser_ir fallbacks', () {
      final env = <String, dynamic>{
        'pipeline_hash': 'p',
        'unified_runtime_graph': buildRuntimeGraph(<String, dynamic>{'a': 1}),
        'dom_html': '<div>x</div>',
      };
      final r = validateReplayEquivalenceExtended(env, env);
      expect(r['equivalent'], isTrue);
    });

    test('empty graph fallback when graph key absent', () {
      final env = <String, dynamic>{'pipeline_hash': 'p'};
      final r = validateReplayEquivalenceExtended(env, env);
      expect(r['equivalent'], isTrue);
    });
  });

  group('replay_runtime', () {
    test('replayRuntimeState deep-copies extraction', () {
      final src = <String, dynamic>{
        'a': <String, dynamic>{'b': 1},
      };
      final copy = replayRuntimeState(src);
      expect(copy, equals(src));
      expect(identical(copy, src), isFalse);
    });

    test('validateFullRuntimeReplay equivalent for identical envelopes', () {
      final r = validateFullRuntimeReplay(_envelope(), _envelope());
      expect(r['equivalent'], isTrue);
      expect(r['bounded'], isTrue);
      expect(r['replay'], isA<Map<String, dynamic>>());
      expect(r['graph'], isA<Map<String, dynamic>>());
      expect(r['fingerprint'], isA<Map<String, dynamic>>());
    });

    test('validateFullRuntimeReplay includes memory when present', () {
      final a = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'mh'};
      final b = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'mh'};
      final r = validateFullRuntimeReplay(a, b);
      expect(r['memory'], isA<Map<String, dynamic>>());
      expect(r['equivalent'], isTrue);
    });

    test('validateFullRuntimeReplay null memory when absent', () {
      final r = validateFullRuntimeReplay(_envelope(), _envelope());
      expect(r['memory'], isNull);
    });

    test('validateFullRuntimeReplay not equivalent for differing envelopes',
        () {
      final a = _envelope();
      final b = _envelope()..['pipeline_hash'] = 'changed';
      final r = validateFullRuntimeReplay(a, b);
      expect(r['equivalent'], isFalse);
    });

    test('validateFullRuntimeReplay not equivalent when memory differs', () {
      final a = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'h1'};
      final b = _envelope()
        ..['runtime_memory'] = <String, dynamic>{'stable_hash': 'h2'};
      final r = validateFullRuntimeReplay(a, b);
      expect(r['equivalent'], isFalse);
    });
  });
}
