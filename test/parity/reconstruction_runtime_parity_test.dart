import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/reconstruction_runtime/reconstruction_runtime.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

Map<String, dynamic>? _mapOrNull(dynamic v) =>
    v == null ? null : Map<String, dynamic>.from(v as Map);

bool _boolOr(Map<String, dynamic> input, String key, bool fallback) =>
    input.containsKey(key) ? input[key] as bool : fallback;

dynamic _callApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'run_reconstruction_runtime':
      return runReconstructionRuntime(
        sources: _mapOrNull(input['sources']),
        stored: _mapOrNull(input['stored']),
        runtimeGraph: _mapOrNull(input['runtime_graph']),
        runtimeType: input.containsKey('runtime_type')
            ? input['runtime_type'] as String
            : 'browser',
        tick: input.containsKey('tick') ? input['tick'] as int : 0,
        fabricate: _boolOr(input, 'fabricate', false),
        clone: _boolOr(input, 'clone', false),
      );
    case 'run_reconstruction_for_extraction':
      return runReconstructionForExtraction(
        reconstructionRuntime: _boolOr(input, 'reconstruction_runtime', true),
        sources: _mapOrNull(input['sources']),
        runtimeGraph: _mapOrNull(input['runtime_graph']),
        runtimeType: input.containsKey('runtime_type')
            ? input['runtime_type'] as String
            : 'browser',
        tick: input.containsKey('tick') ? input['tick'] as int : 0,
        fabricateRuntime: _boolOr(input, 'fabricate_runtime', false),
        cloneRuntime: _boolOr(input, 'clone_runtime', false),
        mergeGraph: _boolOr(input, 'merge_graph', true),
      );
    case 'fabricate_runtime_reality':
      return fabricateRuntimeReality(
        runtime: _mapOrNull(input['runtime']),
        environment: _mapOrNull(input['environment']),
        browser: _mapOrNull(input['browser']),
        application: _mapOrNull(input['application']),
        portable: _boolOr(input, 'portable', true),
      );
    case 'clone_runtime_environment':
      return cloneRuntimeEnvironment(
        Map<String, dynamic>.from(input['source'] as Map),
        includeGraph: _boolOr(input, 'include_graph', true),
        includeQueues: _boolOr(input, 'include_queues', true),
      );
    case 'validate_reconstructed_runtime':
      return validateReconstructedRuntime(
        runtime: _mapOrNull(input['runtime']),
        replay: _mapOrNull(input['replay']),
        topology: _mapOrNull(input['topology']),
        execution: _mapOrNull(input['execution']),
        mutations: input['mutations'],
      );
    default:
      throw StateError('unknown api $api');
  }
}

void main() {
  group('reconstruction runtime API parity (Python det_hash gate)', () {
    final vectorsFile =
        File('validation/parity/reconstruction_runtime_api_vectors.json');
    final vectors =
        (jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();

    for (var i = 0; i < vectors.length; i++) {
      final v = vectors[i];
      final api = v['api'] as String;
      final input = Map<String, dynamic>.from(v['input'] as Map);
      final expected = v['det_hash'] as String;

      test('[$i] $api -> $expected', () {
        final result = _callApi(api, input);
        final actual = computeDeterministicHash(result);
        expect(actual, equals(expected),
            reason: 'parity mismatch for $api with input $input');
      });
    }
  });

  group('save/load reconstruction snapshot roundtrip', () {
    test('encrypt -> persist -> decrypt deep-equals input', () {
      final tempDir = Directory.systemTemp.createTempSync('wwx_recon_');
      final path = '${tempDir.path}${Platform.pathSeparator}snap.json';
      const key = 'parity-secret-key';

      final snapshot = <String, dynamic>{
        'state': <String, dynamic>{
          'queues': <dynamic>[
            <String, dynamic>{'order': 1, 'priority': 2},
          ],
          'deterministic_order': true,
        },
        'topology': <String, dynamic>{'reconstructed': true},
        'identities': <String, dynamic>{
          'runtime_identity': <String, dynamic>{}
        },
        'workflows': <dynamic>[
          <String, dynamic>{'id': 'w1'},
        ],
        'replay_chains': <dynamic>[
          <String, dynamic>{'step': 0, 'action_id': 'a1', 'tick': 0},
        ],
        'bounded': true,
      };

      try {
        final saved = saveReconstructionSnapshot(path, snapshot, key);
        expect(saved['saved'], isTrue);
        expect(File(path).existsSync(), isTrue);

        final loaded = loadReconstructionSnapshot(path, key);
        expect(loaded['available'], isTrue);
        final recovered = loaded['snapshot'] as Map<String, dynamic>;
        expect(recovered, equals(snapshot));
      } finally {
        tempDir.deleteSync(recursive: true);
      }
    });

    test('load missing path -> available:false with empty snapshot', () {
      final tempDir = Directory.systemTemp.createTempSync('wwx_recon_');
      final path = '${tempDir.path}${Platform.pathSeparator}missing.json';
      try {
        final loaded = loadReconstructionSnapshot(path, 'k');
        expect(loaded['available'], isFalse);
        final snap = loaded['snapshot'] as Map<String, dynamic>;
        expect(snap['state'], equals(<String, dynamic>{}));
        expect(snap['workflows'], equals(<dynamic>[]));
        expect(snap['bounded'], isTrue);
      } finally {
        tempDir.deleteSync(recursive: true);
      }
    });
  });

  group('branch coverage', () {
    test('run_reconstruction_runtime empty is deterministic', () {
      final a = runReconstructionRuntime();
      final b = runReconstructionRuntime();
      expect(computeDeterministicHash(a), equals(computeDeterministicHash(b)));
      expect(a['bounded'], isTrue);
    });

    test('run_reconstruction_for_extraction disabled returns enabled:false',
        () {
      final r = runReconstructionForExtraction(reconstructionRuntime: false);
      expect(r['enabled'], isFalse);
      expect(r['bounded'], isTrue);
    });

    test('merge_graph false produces empty unified_graph', () {
      final r = runReconstructionForExtraction(mergeGraph: false);
      expect(r['unified_graph'], equals(<String, dynamic>{}));
      expect(r['enabled'], isTrue);
    });

    test('merge_graph true produces unified_runtime_graph', () {
      final r = runReconstructionForExtraction(mergeGraph: true);
      final unified = r['unified_graph'] as Map<String, dynamic>;
      expect(unified['ir'], equals('unified_runtime_graph'));
    });

    test('fabricate+clone path populates ir graph nodes', () {
      final r = runReconstructionForExtraction(
        sources: <String, dynamic>{
          'execution_ir': <String, dynamic>{
            'actions': <dynamic>[
              <String, dynamic>{'id': 'a1'},
            ],
          },
        },
        fabricateRuntime: true,
        cloneRuntime: true,
        mergeGraph: true,
      );
      final graphIr = r['reconstruction_graph_ir'] as Map<String, dynamic>;
      final nodes = graphIr['nodes'] as List<dynamic>;
      final ids = nodes.map((dynamic n) => (n as Map)['id']).toList();
      expect(ids, contains('fabrication:reality'));
      expect(ids, contains('clone:environment'));
    });

    test('validate empty runtime -> invalid', () {
      final r = validateReconstructedRuntime();
      expect(r['valid'], isFalse);
      expect(r['integrity_score'], equals(0.0));
    });

    test('clone with include flags false drops graph and queues', () {
      final r = cloneRuntimeEnvironment(
        <String, dynamic>{
          'runtime_graph': <String, dynamic>{'nodes': <dynamic>[]},
          'queues': <dynamic>[1],
        },
        includeGraph: false,
        includeQueues: false,
      );
      expect(r['runtime_graph'], equals(<String, dynamic>{}));
      expect(r['execution_queues'], equals(<dynamic>[]));
      expect(r['cloned'], isTrue);
    });

    test('fabricate with no runtime derives base from environment', () {
      final r = fabricateRuntimeReality(
        environment: <String, dynamic>{'runtime': 'terminal'},
      );
      final runtime = r['runtime'] as Map<String, dynamic>;
      expect(runtime['runtime_type'], equals('terminal'));
      expect(r['fabricated'], isTrue);
    });
  });
}
