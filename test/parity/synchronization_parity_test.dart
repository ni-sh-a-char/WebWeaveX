import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/synchronization/synchronization.dart';

/// Coerce a decoded-JSON value to `Map<String, dynamic>?`.
Map<String, dynamic>? _map(dynamic v) =>
    v == null ? null : Map<String, dynamic>.from(v as Map);

List<dynamic>? _list(dynamic v) =>
    v == null ? null : List<dynamic>.from(v as List);

int _int(dynamic v, [int fallback = 0]) => v is int ? v : fallback;

bool _bool(dynamic v, bool fallback) => v is bool ? v : fallback;

/// Dispatch a vector input to its Dart API, returning the result to hash.
Map<String, dynamic> _runVector(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'build_runtime_delta':
      return buildRuntimeDelta(
        _map(input['previous']),
        _map(input['current']),
        tick: _int(input['tick']),
      );
    case 'replay_synchronized_runtime':
      return replaySynchronizedRuntime(_map(input['memory']) ?? {});
    case 'run_synchronized_runtime':
      return runSynchronizedRuntime(
        tick: _int(input['tick']),
        browser: _map(input['browser']),
        native: _map(input['native']),
        semanticResult: _map(input['semantic_result']),
        workflowResult: _map(input['workflow_result']),
        causalityResult: _map(input['causality_result']),
        distributedResult: _map(input['distributed_result']),
        session: _map(input['session']),
        identity: _map(input['identity']),
        memory: _map(input['memory']),
        workers: _list(input['workers']),
      );
    case 'run_sync_for_extraction':
      return runSyncForExtraction(
        synchronizedRuntime: _bool(input['synchronized_runtime'], true),
        memoryPath: (input['memory_path'] as String?) ?? '',
        memoryKey: (input['memory_key'] as String?) ?? '',
        tick: _int(input['tick']),
        browser: _map(input['browser']),
        native: _map(input['native']),
        semanticResult: _map(input['semantic_result']),
        workflowResult: _map(input['workflow_result']),
        causalityResult: _map(input['causality_result']),
        distributedResult: _map(input['distributed_result']),
        session: _map(input['session']),
        identity: _map(input['identity']),
        mergeGraph: _bool(input['merge_graph'], true),
      );
    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  final vectorsFile = File(
    '${Directory.current.path}/validation/parity/synchronization_api_vectors.json',
  );
  final vectors = (jsonDecode(vectorsFile.readAsStringSync()) as List)
      .cast<Map<String, dynamic>>();

  group('synchronization cross-language parity (deterministic hash)', () {
    for (var i = 0; i < vectors.length; i++) {
      final vector = vectors[i];
      final api = vector['api'] as String;
      final input = Map<String, dynamic>.from(vector['input'] as Map);
      final expected = vector['det_hash'] as String;

      test('[$i] $api → hash matches Python', () {
        final result = _runVector(api, input);
        final actual = computeDeterministicHash(result);
        expect(
          actual,
          expected,
          reason: 'API $api (vector $i) produced a non-matching hash.\n'
              '  python: $expected\n'
              '  dart  : $actual',
        );
      });
    }
  });

  group('build_runtime_delta branch coverage', () {
    test('null defaults yield no changes', () {
      final delta = buildRuntimeDelta(null, null);
      expect(delta['changes'], isEmpty);
      expect(delta['timestamp'], 0);
      expect(delta['bounded'], true);
    });

    test('change classifications', () {
      final delta = buildRuntimeDelta(
        <String, dynamic>{
          'semantic': 1,
          'workflow': 1,
          'dom': 1,
          'ui': 1,
          'state': 1,
          'other': 1,
        },
        <String, dynamic>{
          'semantic': 2,
          'workflow': 2,
          'dom': 2,
          'ui': 2,
          'state': 2,
          'other': 2,
        },
      );
      final kinds = <String, String>{
        for (final c in (delta['changes'] as List).cast<Map>())
          c['field'] as String: c['kind'] as String,
      };
      expect(kinds['semantic'], 'semantic_change');
      expect(kinds['workflow'], 'workflow_change');
      expect(kinds['dom'], 'ui_mutation');
      expect(kinds['ui'], 'ui_mutation');
      expect(kinds['state'], 'application_state_mutation');
      expect(kinds['other'], 'runtime_transition');
    });
  });

  group('replay_synchronized_runtime branches', () {
    test('empty memory uses defaults', () {
      final replay = replaySynchronizedRuntime(<String, dynamic>{});
      expect(replay['synchronized_histories'], <String, dynamic>{});
      expect(replay['runtime_deltas'], <dynamic>[]);
      expect(replay['replayed'], true);
    });
  });

  group('save/load sync memory roundtrip (temp file)', () {
    test('roundtrip deep-equals original memory', () {
      final dir = Directory.systemTemp.createTempSync('wwx_sync_mem_');
      final path = '${dir.path}/native.kaalka';
      const key = 'webweavex-parity-key';

      final memory = <String, dynamic>{
        'deltas': <dynamic>[
          <String, dynamic>{
            'delta_id': 'd1',
            'timestamp': 1,
            'changes': <dynamic>[
              <String, dynamic>{
                'field': 'semantic',
                'from': null,
                'to': <String, dynamic>{'x': 1},
                'kind': 'semantic_change',
              },
            ],
            'bounded': true,
          },
        ],
        'history': <String, dynamic>{'length': 1},
        'timeline': <String, dynamic>{
          'timeline': <dynamic>[
            <String, dynamic>{'tick': 1, 'delta_id': 'd1', 'change_count': 1},
          ],
        },
        'convergence': <String, dynamic>{'converged': true},
        'realities': <dynamic>[
          <String, dynamic>{'reality_id': 'primary', 'tick': 1},
        ],
        'continuity': <String, dynamic>{'continuous': true},
        'state_graph': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[],
        },
        'bounded': true,
      };

      try {
        final saved = saveSyncMemory(path, memory, key);
        expect(saved['saved'], true);
        expect(saved['algorithm'], 'kaalka');
        expect(File(path).existsSync(), true);

        final loaded = loadSyncMemory(path, key);
        expect(loaded['available'], true);
        expect(loaded['algorithm'], 'kaalka');
        expect(
          _canonical(loaded['memory']),
          _canonical(memory),
          reason: 'loaded memory must deep-equal the saved memory',
        );
      } finally {
        if (dir.existsSync()) dir.deleteSync(recursive: true);
      }
    });

    test('load missing file returns unavailable empty memory', () {
      final dir = Directory.systemTemp.createTempSync('wwx_sync_mem_miss_');
      final path = '${dir.path}/absent.kaalka';
      try {
        final loaded = loadSyncMemory(path, 'k');
        expect(loaded['available'], false);
        final mem = loaded['memory'] as Map<String, dynamic>;
        expect(mem['deltas'], <dynamic>[]);
        expect(mem['bounded'], true);
      } finally {
        if (dir.existsSync()) dir.deleteSync(recursive: true);
      }
    });

    test('save then load equals a fresh save (deterministic ciphertext)', () {
      final dir = Directory.systemTemp.createTempSync('wwx_sync_mem_det_');
      final pathA = '${dir.path}/a.kaalka';
      final pathB = '${dir.path}/b.kaalka';
      const key = 'k2';
      final memory = <String, dynamic>{'deltas': <dynamic>[], 'bounded': true};
      try {
        saveSyncMemory(pathA, memory, key);
        saveSyncMemory(pathB, memory, key);
        expect(
          File(pathA).readAsStringSync(),
          File(pathB).readAsStringSync(),
          reason: 'encryption must be deterministic for identical input',
        );
      } finally {
        if (dir.existsSync()) dir.deleteSync(recursive: true);
      }
    });
  });

  group('run_sync_for_extraction branches', () {
    test('disabled short-circuits', () {
      final result = runSyncForExtraction(synchronizedRuntime: false);
      expect(result['enabled'], false);
      expect(result['bounded'], true);
      expect(result.containsKey('synchronization'), false);
    });

    test('mergeGraph=false yields empty unified graph', () {
      final result = runSyncForExtraction(
        synchronizedRuntime: true,
        browser: <String, dynamic>{
          'dom': <String, dynamic>{'t': 'q'}
        },
        mergeGraph: false,
      );
      expect(result['enabled'], true);
      expect(result['unified_graph'], <String, dynamic>{});
      expect(result['memory_persisted'], false);
    });
  });
}

/// Canonicalize a JSON value for order-insensitive deep comparison.
dynamic _canonical(dynamic v) {
  if (v is Map) {
    final keys = v.keys.map((k) => k.toString()).toList()..sort();
    return <String, dynamic>{
      for (final k in keys) k: _canonical(v[k]),
    };
  }
  if (v is List) {
    return v.map(_canonical).toList();
  }
  return v;
}
