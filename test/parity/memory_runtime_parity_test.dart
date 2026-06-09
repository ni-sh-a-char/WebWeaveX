import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/runtime_memory_family/runtime_memory_engines.dart';
import 'package:webweavex/src/runtime_memory_family/runtime_memory_runtime.dart';

List<Map<String, dynamic>>? _nodes(dynamic v) {
  if (v is List) {
    return v.map((dynamic e) => (e as Map).cast<String, dynamic>()).toList();
  }
  return null;
}

dynamic _runVector(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'run_runtime_memory':
      return runRuntimeMemory(
        sources: (input['sources'] as Map?)?.cast<String, dynamic>(),
        stored: (input['stored'] as Map?)?.cast<String, dynamic>(),
        nodes: _nodes(input['nodes']),
        tick: input['tick'] as int? ?? 0,
      );

    case 'run_memory_for_extraction':
      return runMemoryForExtraction(
        federatedMemory: input['federated_memory'] as bool? ?? true,
        memoryPath: input['memory_path'] as String? ?? '',
        memoryKey: input['memory_key'] as String? ?? '',
        sources: (input['sources'] as Map?)?.cast<String, dynamic>(),
        nodes: _nodes(input['nodes']),
        tick: input['tick'] as int? ?? 0,
        mergeGraph: input['merge_graph'] as bool? ?? true,
      );

    case 'search_runtime_memory':
      return searchRuntimeMemory(
        (input['index'] as Map).cast<String, dynamic>(),
        input['term'] as String,
        input['search_type'] as String? ?? 'structural',
      );

    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  final File vectorsFile = File('validation/parity/memory_api_vectors.json');
  final List<dynamic> vectors =
      jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;

  group('runtime-memory family cross-language hash parity', () {
    for (final dynamic vDyn in vectors) {
      final Map<String, dynamic> v = (vDyn as Map).cast<String, dynamic>();
      final String api = v['api'] as String;
      final String expected = v['det_hash'] as String;
      final Map<String, dynamic> input =
          (v['input'] as Map).cast<String, dynamic>();

      test(
          '$api :: ${jsonEncode(input).substring(0, jsonEncode(input).length > 80 ? 80 : jsonEncode(input).length)}',
          () {
        final dynamic result = _runVector(api, input);
        final String dartHash = computeDeterministicHash(result);
        expect(dartHash, equals(expected),
            reason: 'Dart hash must equal Python det_hash for $api');
      });
    }
  });

  group('save/load temp-file roundtrip parity', () {
    test('save then load deep-equals the input memory', () {
      final Map<String, dynamic> memory = <String, dynamic>{
        'runtime': <String, dynamic>{
          'memory_id': 'abc123',
          'runtime_history': <Map<String, dynamic>>[
            <String, dynamic>{
              'tick': 1,
              'kind': 'workflow',
              'source': 'workflow'
            },
            <String, dynamic>{'tick': 2, 'kind': 'sync', 'source': 'sync'},
          ],
          'bounded': true,
        },
        'knowledge': <String, dynamic>{'entities': <dynamic>[]},
        'semantic': <String, dynamic>{'domain': 'web'},
        'index': <String, dynamic>{'entity_index': <String, dynamic>{}},
        'graph': <String, dynamic>{
          'nodes': <Map<String, dynamic>>[
            <String, dynamic>{'id': 'n1', 'type': 'node'}
          ]
        },
        'lineage': <String, dynamic>{'lineage': <dynamic>[]},
        'bounded': true,
      };

      final Directory tmp =
          Directory.systemTemp.createTempSync('wwx_mem_parity_');
      final String path = '${tmp.path}/memory.kaalka';
      const String key = 'roundtrip-key';
      try {
        final Map<String, dynamic> saved = saveRuntimeMemory(path, memory, key);
        expect(saved['saved'], isTrue);
        expect(File(path).existsSync(), isTrue);

        final Map<String, dynamic> loaded = loadRuntimeMemory(path, key);
        expect(loaded['available'], isTrue);
        expect(loaded['memory'], equals(memory));
      } finally {
        tmp.deleteSync(recursive: true);
      }
    });

    test('load of a missing path returns the empty store', () {
      final Map<String, dynamic> loaded = loadRuntimeMemory(
          '${Directory.systemTemp.path}/wwx_does_not_exist_xyz.kaalka', 'k');
      expect(loaded['available'], isFalse);
      expect((loaded['memory'] as Map)['bounded'], isTrue);
      expect((loaded['memory'] as Map).containsKey('runtime'), isTrue);
    });
  });

  group('branch coverage', () {
    test('run_memory_for_extraction disabled short-circuits', () {
      final Map<String, dynamic> r =
          runMemoryForExtraction(federatedMemory: false);
      expect(r['enabled'], isFalse);
      expect(r['bounded'], isTrue);
    });

    test('run_memory_for_extraction persists when path+key given', () {
      final Directory tmp =
          Directory.systemTemp.createTempSync('wwx_mem_persist_');
      final String path = '${tmp.path}/store.kaalka';
      try {
        final Map<String, dynamic> r = runMemoryForExtraction(
          federatedMemory: true,
          memoryPath: path,
          memoryKey: 'k',
          sources: <String, dynamic>{
            'workflow': <String, dynamic>{'objective': 'x'}
          },
          tick: 1,
        );
        expect(r['memory_persisted'], isTrue);
        expect(File(path).existsSync(), isTrue);
        // Reload through extraction (stored branch) — must stay deterministic.
        final Map<String, dynamic> r2 = runMemoryForExtraction(
          federatedMemory: true,
          memoryPath: path,
          memoryKey: 'k',
          sources: <String, dynamic>{
            'workflow': <String, dynamic>{'objective': 'x'}
          },
          tick: 2,
        );
        expect(r2['enabled'], isTrue);
      } finally {
        tmp.deleteSync(recursive: true);
      }
    });

    test('search semantic/lineage/graph branches return matches', () {
      final Map<String, dynamic> index = <String, dynamic>{
        'entity_index': <String, dynamic>{
          'alpha': <String, dynamic>{'id': 'alpha'}
        },
        'workflow_index': <String, dynamic>{
          'flow': <String, dynamic>{'id': 'flow'}
        },
        'graph_index': <String, dynamic>{
          '0': <String, dynamic>{'nodes': <dynamic>[]}
        },
        'connector_index': <String, dynamic>{},
      };
      expect(
          (searchRuntimeMemory(index, 'alpha', 'semantic')['matches'] as List)
              .length,
          equals(1));
      expect(
          (searchRuntimeMemory(index, 'flow', 'lineage')['matches'] as List)
              .length,
          equals(1));
      expect(
          (searchRuntimeMemory(index, '', 'graph')['matches'] as List).length,
          equals(1));
      expect(
          searchRuntimeMemory(index, 'nope', 'structural')['count'], equals(0));
    });

    test('run_runtime_memory with defaults yields bounded payload', () {
      final Map<String, dynamic> r = runRuntimeMemory();
      expect(r['bounded'], isTrue);
      expect((r['runtime'] as Map)['memory_id'], isNotNull);
      expect(r.containsKey('memory_ir'), isTrue);
    });
  });

  group('engine branch coverage', () {
    test('converge with empty replicas', () {
      final Map<String, dynamic> r =
          convergeRuntimeMemory(<Map<String, dynamic>>[]);
      expect(r['converged'], isTrue);
      expect(r['memory_id'], equals(''));
    });

    test('converge with conflicting memory ids', () {
      final Map<String, dynamic> r =
          convergeRuntimeMemory(<Map<String, dynamic>>[
        <String, dynamic>{'memory_id': 'a'},
        <String, dynamic>{'memory_id': 'b'},
      ]);
      expect(r['converged'], isFalse);
      expect(r['conflict'], isTrue);
    });

    test('distributed memory sums num conflicts and detects unsynced', () {
      final Map<String, dynamic> r =
          buildDistributedMemory(<Map<String, dynamic>>[
        <String, dynamic>{
          'node_id': 'a',
          'synced': false,
          'conflicts_resolved': 2.0
        },
        <String, dynamic>{'node_id': 'b', 'conflicts_resolved': '3'},
      ]);
      expect(r['synchronized'], isFalse);
      expect(r['conflicts_resolved'], equals(5));
      expect(r['converged'], isTrue);
    });

    test('build_runtime_memory uses step fallback for tick', () {
      final Map<String, dynamic> r = buildRuntimeMemory(
        runtimeHistory: <Map<String, dynamic>>[
          <String, dynamic>{'step': 2, 'kind': 'workflow'},
          <String, dynamic>{'step': 1, 'kind': 'sync'},
        ],
      );
      final List<dynamic> hist = r['runtime_history'] as List<dynamic>;
      expect((hist.first as Map)['kind'], equals('sync'));
    });

    test('knowledge memory carries topology operations', () {
      final Map<String, dynamic> r = buildKnowledgeMemory(
        relations: <Map<String, dynamic>>[
          <String, dynamic>{'from': 'a', 'to': 'b', 'relation': 'x'}
        ],
        topology: <String, dynamic>{
          'operations': <dynamic>['op1'],
          'distributed': <String, dynamic>{'n': 1},
        },
      );
      expect((r['operational_structures'] as List).length, equals(1));
      expect((r['distributed_topology'] as Map)['n'], equals(1));
    });

    test('semantic memory falls back to entity type as label', () {
      final Map<String, dynamic> r = buildSemanticMemory(<String, dynamic>{
        'semantic': <String, dynamic>{
          'entities': <String, dynamic>{
            'entities': <Map<String, dynamic>>[
              <String, dynamic>{'type': 'TypeOnly'}
            ]
          }
        }
      }, <Map<String, dynamic>>[
        <String, dynamic>{'kind': 'workflow', 'objective': 'obj'}
      ]);
      expect((r['recurring_concepts'] as List), contains('TypeOnly'));
      expect((r['recurring_workflows'] as List), contains('obj'));
    });

    test('graph and index use label when id absent', () {
      final Map<String, dynamic> g = buildRuntimeMemoryGraph(
        <Map<String, dynamic>>[
          <String, dynamic>{'label': 'L1', 'type': 'kind'}
        ],
        <Map<String, dynamic>>[],
      );
      expect((g['nodes'] as List).first,
          equals(<String, dynamic>{'id': 'L1', 'type': 'kind'}));

      final Map<String, dynamic> idx = buildRuntimeIndex(
        entities: <Map<String, dynamic>>[
          <String, dynamic>{'label': 'L1'}
        ],
        workflows: <Map<String, dynamic>>[
          <String, dynamic>{'objective': 'op'}
        ],
        graphs: <Map<String, dynamic>>[],
        streams: <Map<String, dynamic>>[],
        connectors: <Map<String, dynamic>>[],
      );
      expect((idx['entity_index'] as Map).containsKey('L1'), isTrue);
      expect((idx['workflow_index'] as Map).containsKey('op'), isTrue);
    });

    test('graph with no nodes yields memory:root', () {
      final Map<String, dynamic> g = buildRuntimeMemoryGraph(
          <Map<String, dynamic>>[], <Map<String, dynamic>>[]);
      expect((g['nodes'] as List).first,
          equals(<String, dynamic>{'id': 'memory:root', 'type': 'memory'}));
    });

    test('query lineage/topology/sync/default branches', () {
      final Map<String, dynamic> mem = <String, dynamic>{
        'lineage': <Map<String, dynamic>>[
          <String, dynamic>{'id': 'wf:0'}
        ],
        'runtime_history': <Map<String, dynamic>>[
          <String, dynamic>{'runtime': 'browser', 'tick': 1}
        ],
        'synchronization_history': <Map<String, dynamic>>[
          <String, dynamic>{'kind': 'sync'}
        ],
      };
      expect(queryRuntimeMemory(mem, 'lineage', 'wf')['count'], equals(1));
      expect(
          queryRuntimeMemory(mem, 'topology', 'browser')['count'], equals(1));
      expect(queryRuntimeMemory(mem, 'sync', '')['count'], equals(1));
      expect(queryRuntimeMemory(mem, 'other', 'browser')['count'], equals(1));
    });

    test('merge falls back to runtime_id ordering', () {
      final Map<String, dynamic> m =
          mergeRuntimeMemories(<Map<String, dynamic>>[
        <String, dynamic>{
          'runtime_id': 'z',
          'runtime_history': <Map<String, dynamic>>[
            <String, dynamic>{'tick': 1, 'kind': 'a', 'source': 's'}
          ]
        },
        <String, dynamic>{
          'runtime_id': 'a',
          'runtime_history': <Map<String, dynamic>>[]
        },
      ]);
      expect(m['bounded'], isTrue);
    });

    test('runtime_memory_ir_to_graph injects root node when empty', () {
      final Map<String, dynamic> g = runtimeMemoryIrToGraph(<String, dynamic>{
        'memory_graphs': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[]
        }
      });
      expect((g['nodes'] as List).first,
          equals(<String, dynamic>{'id': 'memory:root', 'type': 'memory'}));
    });

    test('build_runtime_graph_from_irs dedups nodes and edges', () {
      final Map<String, dynamic> g =
          buildRuntimeGraphFromIrs(<Map<String, dynamic>>[
        <String, dynamic>{
          'ir': 'x',
          'nodes': <Map<String, dynamic>>[
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': ''},
          ],
          'edges': <Map<String, dynamic>>[
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': '', 'to': 'b'},
          ],
        }
      ]);
      expect((g['nodes'] as List).length, equals(1));
      expect((g['edges'] as List).length, equals(1));
    });

    test('pythonRepr renders bool/null/list/map', () {
      expect(pythonReprScalar(true), equals('True'));
      expect(pythonReprScalar(null), equals('None'));
      expect(pythonRepr(<dynamic>[1, 'a']), equals("[1, 'a']"));
      expect(pythonRepr(<String, dynamic>{'k': false}), equals("{'k': False}"));
    });

    test('stableMemoryHash is deterministic', () {
      final Map<String, dynamic> m = <String, dynamic>{
        'memory_id': 'x',
        'runtime_history': <Map<String, dynamic>>[
          <String, dynamic>{'tick': 1, 'kind': 'a', 'source': 's'}
        ],
        'lineage': <Map<String, dynamic>>[],
        'semantic_relations': <Map<String, dynamic>>[],
      };
      expect(stableMemoryHash(m), equals(stableMemoryHash(m)));
    });
  });
}
