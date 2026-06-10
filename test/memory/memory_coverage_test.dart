import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

/// Builds a non-trivial RuntimeGraph with multiple nodes + edges.
RuntimeGraph populatedGraph() => buildRuntimeGraph(<String, dynamic>{
      'dom': <String, dynamic>{'tag': 'div'},
      'event': <String, dynamic>{'kind': 'click'},
      'state': <String, dynamic>{'count': 1},
    });

/// Empty graph (no nodes, no edges).
RuntimeGraph emptyGraph() => buildRuntimeGraph(<String, dynamic>{});

void main() {
  group('buildRuntimeMemory', () {
    test('populated graph with history yields full envelope', () {
      final graph = populatedGraph();
      final history = <dynamic>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
      ];
      final mem = buildRuntimeMemoryFabric(graph, history);

      expect(mem['bounded'], isTrue);
      expect(mem['stable_hash'], isA<String>());
      expect((mem['stable_hash'] as String).isNotEmpty, isTrue);
      final inner = mem['memory'] as Map<String, dynamic>;
      expect(inner['graph'], isA<Map<dynamic, dynamic>>());
      expect(inner['runtime_history'], history);
    });

    test('default empty history branch', () {
      final mem = buildRuntimeMemoryFabric(populatedGraph());
      final inner = mem['memory'] as Map<String, dynamic>;
      expect(inner['runtime_history'], isEmpty);
      expect(mem['bounded'], isTrue);
    });

    test('empty graph still produces a stable hash', () {
      final mem = buildRuntimeMemoryFabric(emptyGraph());
      expect(mem['stable_hash'], isA<String>());
      final inner = mem['memory'] as Map<String, dynamic>;
      final graphJson = inner['graph'] as Map<String, dynamic>;
      expect(graphJson['nodes'], isEmpty);
      expect(graphJson['edges'], isEmpty);
    });

    test('determinism: identical inputs produce identical output', () {
      final a = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final b = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      expect(a['stable_hash'], equals(b['stable_hash']));
    });
  });

  group('stableMemoryHash', () {
    test('deterministic for same graph + history', () {
      final graph = populatedGraph();
      final h1 = stableMemoryFabricHash(graph, <dynamic>[1, 2, 3]);
      final h2 = stableMemoryFabricHash(graph, <dynamic>[1, 2, 3]);
      expect(h1, equals(h2));
    });

    test('history length changes hash', () {
      final graph = populatedGraph();
      final h1 = stableMemoryFabricHash(graph, <dynamic>[1]);
      final h2 = stableMemoryFabricHash(graph, <dynamic>[1, 2]);
      expect(h1, isNot(equals(h2)));
    });

    test('default empty history branch', () {
      final h = stableMemoryFabricHash(emptyGraph());
      expect(h, isA<String>());
      expect(h.isNotEmpty, isTrue);
    });
  });

  group('mergeRuntimeMemories', () {
    test('merges two populated memories with histories', () {
      final memA = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final memB = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 1}
      ]);
      final merged = mergeRuntimeMemories(memA, memB);

      expect(merged['bounded'], isTrue);
      final inner = merged['memory'] as Map<String, dynamic>;
      final mergedHistory = inner['runtime_history'] as List<dynamic>;
      expect(mergedHistory.length, equals(2));
    });

    test('merges when maps lack memory/graph keys (null-coalescing branches)',
        () {
      final empty = <String, dynamic>{};
      final merged = mergeRuntimeMemories(empty, empty);
      expect(merged['bounded'], isTrue);
      final inner = merged['memory'] as Map<String, dynamic>;
      // Both histories are empty (null-coalescing fallbacks engaged).
      expect(inner['runtime_history'], isEmpty);
      // buildRuntimeGraph turns the synthesized 'nodes'/'edges' keys into
      // graph nodes, so the merged graph has exactly those two nodes.
      final graphJson = inner['graph'] as Map<String, dynamic>;
      expect(graphJson['nodes'], hasLength(2));
    });

    test('merges one populated with one empty', () {
      final memA = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final merged = mergeRuntimeMemories(memA, <String, dynamic>{});
      final inner = merged['memory'] as Map<String, dynamic>;
      expect((inner['runtime_history'] as List<dynamic>).length, equals(1));
    });
  });

  group('queryRuntimeMemory', () {
    test('returns value for present key', () {
      final mem = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final history = queryRuntimeMemoryFabric(mem, 'runtime_history');
      expect(history, isA<List<dynamic>>());
      expect((history as List<dynamic>).length, equals(1));
      expect(queryRuntimeMemoryFabric(mem, 'graph'), isNotNull);
    });

    test('returns null for absent key', () {
      final mem = buildRuntimeMemoryFabric(populatedGraph());
      expect(queryRuntimeMemoryFabric(mem, 'does_not_exist'), isNull);
    });

    test('returns null when memory map is missing', () {
      expect(queryRuntimeMemoryFabric(<String, dynamic>{}, 'graph'), isNull);
    });
  });

  group('replicateRuntimeMemory', () {
    test('deep clones an equal but distinct map', () {
      final mem = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final clone = replicateRuntimeMemory(mem);
      expect(clone, equals(mem));
      expect(identical(clone, mem), isFalse);
      expect(clone['stable_hash'], equals(mem['stable_hash']));
    });
  });

  group('buildRuntimeMemoryGraph', () {
    test('populated graph yields entities + relations', () {
      final graph = populatedGraph();
      final mg = buildRuntimeMemoryGraph(graph, <dynamic>[1, 2]);

      expect(mg['bounded'], isTrue);
      expect(mg['graph_fingerprint'], isA<String>());
      final entities = mg['entities'] as List<dynamic>;
      final relations = mg['relations'] as List<dynamic>;
      expect(entities, isNotEmpty);
      // populated graph has multiple nodes => edges exist.
      expect(relations, isNotEmpty);

      final firstEntity = entities.first as Map<String, dynamic>;
      expect(firstEntity.containsKey('id'), isTrue);
      expect(firstEntity.containsKey('type'), isTrue);
      expect(firstEntity['relations'], isA<List<dynamic>>());

      final firstRelation = relations.first as Map<String, dynamic>;
      expect(firstRelation.containsKey('from'), isTrue);
      expect(firstRelation.containsKey('to'), isTrue);
    });

    test('empty graph yields empty entities/relations', () {
      final mg = buildRuntimeMemoryGraph(emptyGraph());
      expect(mg['entities'], isEmpty);
      expect(mg['relations'], isEmpty);
      expect(mg['graph_fingerprint'], isA<String>());
    });

    test('deterministic fingerprint for identical input', () {
      final f1 = buildRuntimeMemoryGraph(populatedGraph())['graph_fingerprint'];
      final f2 = buildRuntimeMemoryGraph(populatedGraph())['graph_fingerprint'];
      expect(f1, equals(f2));
    });

    test('relation source resolves from edge.source then edge.from fallback',
        () {
      // Manually build a graph whose edge uses from/to (not source/target)
      // to cover the `e.source ?? e.from` / `e.target ?? e.to` branches.
      final graph = RuntimeGraph(
        nodes: <RuntimeNode>[
          RuntimeNode(id: 'a', type: 'x'),
          RuntimeNode(id: 'b', type: 'y'),
        ],
        edges: <RuntimeEdge>[
          RuntimeEdge(from: 'a', to: 'b', type: 'link'),
        ],
      );
      final mg = buildRuntimeMemoryGraph(graph);
      final relations = mg['relations'] as List<dynamic>;
      expect(relations, hasLength(1));
      final rel = relations.first as Map<String, dynamic>;
      expect(rel['from'], equals('a'));
      expect(rel['to'], equals('b'));
    });
  });

  group('buildMemoryLineage', () {
    test('empty history yields empty lineage', () {
      final result = buildMemoryLineage(<Map<String, dynamic>>[]);
      expect(result['bounded'], isTrue);
      expect(result['lineage'], isEmpty);
    });

    test('single item: parent_id is null, valid structure', () {
      final result = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 5, 'data': 'x'}
      ]);
      final lineage = result['lineage'] as List<dynamic>;
      expect(lineage, hasLength(1));
      final entry = lineage.first as Map<String, dynamic>;
      expect(entry['parent_id'], isNull);
      expect(entry['tick'], equals(5));
      expect(entry['id'], isA<String>());
      expect(entry['stable_hash'], isA<String>());
    });

    test('chained lineage links parent ids correctly', () {
      final result = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
        <String, dynamic>{'tick': 2},
      ]);
      final lineage =
          (result['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(lineage, hasLength(3));
      expect(lineage[0]['parent_id'], isNull);
      expect(lineage[1]['parent_id'], equals(lineage[0]['id']));
      expect(lineage[2]['parent_id'], equals(lineage[1]['id']));
    });

    test('uses step key when tick absent, index when both absent', () {
      final result = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'step': 7},
        <String, dynamic>{'nothing': true},
      ]);
      final lineage =
          (result['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(lineage[0]['tick'], equals(7)); // step used
      expect(lineage[1]['tick'], equals(1)); // index fallback
    });
  });

  group('verifyMemoryLineage', () {
    test('valid lineage returns true', () {
      final built = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
        <String, dynamic>{'tick': 2},
      ]);
      final lineage =
          (built['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(verifyMemoryLineage(lineage), isTrue);
    });

    test('empty lineage is vacuously valid (true)', () {
      expect(verifyMemoryLineage(<Map<String, dynamic>>[]), isTrue);
    });

    test('single-entry lineage is valid (loop body not entered)', () {
      final built = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 0}
      ]);
      final lineage =
          (built['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(verifyMemoryLineage(lineage), isTrue);
    });

    test('tampered lineage returns false', () {
      final built = buildMemoryLineage(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
      ]);
      final lineage =
          (built['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      // Tamper: break the parent linkage.
      lineage[1]['parent_id'] = 'tampered-not-matching';
      expect(verifyMemoryLineage(lineage), isFalse);
    });
  });

  group('replayMemoryState', () {
    test('populated graph + map history produces full replay state', () {
      final graph = populatedGraph();
      final history = <dynamic>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
      ];
      final state = replayMemoryState(graph, history);

      expect(state['bounded'], isTrue);
      expect(state['replay_hash'], isA<String>());
      expect(state['stable_hash'], isA<String>());
      expect(state['lineage'], isA<List<dynamic>>());
      expect((state['lineage'] as List<dynamic>).length, equals(2));
      expect(state['memory_graph'], isA<Map<dynamic, dynamic>>());
    });

    test('non-map history items get index-based tick (cast branch)', () {
      final graph = populatedGraph();
      final history = <dynamic>['a', 'b', 'c'];
      final state = replayMemoryState(graph, history);
      final lineage =
          (state['lineage'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(lineage, hasLength(3));
      // Index-derived ticks from {'tick': history.indexOf(h)}.
      expect(lineage[0]['tick'], equals(0));
      expect(lineage[1]['tick'], equals(1));
      expect(lineage[2]['tick'], equals(2));
    });

    test('default empty history branch', () {
      final state = replayMemoryState(populatedGraph());
      expect(state['lineage'], isEmpty);
      expect(state['bounded'], isTrue);
    });

    test('replay_hash matches stableMemoryHash for same inputs', () {
      final graph = populatedGraph();
      final history = <dynamic>[
        <String, dynamic>{'tick': 0}
      ];
      final state = replayMemoryState(graph, history);
      expect(
          state['replay_hash'], equals(stableMemoryFabricHash(graph, history)));
    });
  });

  group('validateMemoryReplay', () {
    test('matching stable hashes => true', () {
      final graph = populatedGraph();
      final history = <dynamic>[
        <String, dynamic>{'tick': 0}
      ];
      final original = buildRuntimeMemoryFabric(graph, history);
      final replayed = replayMemoryState(graph, history);
      expect(validateMemoryReplay(original, replayed), isTrue);
    });

    test('mismatched stable hashes => false', () {
      final original = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0}
      ]);
      final replayed = replayMemoryState(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
      ]);
      expect(validateMemoryReplay(original, replayed), isFalse);
    });
  });

  group('queryMemoryHistory', () {
    test('returns history list when present', () {
      final mem = buildRuntimeMemoryFabric(populatedGraph(), <dynamic>[
        <String, dynamic>{'tick': 0},
        <String, dynamic>{'tick': 1},
      ]);
      final history = queryMemoryHistory(mem);
      expect(history, hasLength(2));
    });

    test('returns empty list when memory map missing', () {
      expect(queryMemoryHistory(<String, dynamic>{}), isEmpty);
    });

    test('returns empty list when runtime_history absent', () {
      final mem = <String, dynamic>{'memory': <String, dynamic>{}};
      expect(queryMemoryHistory(mem), isEmpty);
    });
  });
}
