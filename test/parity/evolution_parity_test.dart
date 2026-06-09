import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/evolution/evolution_runtime.dart';

Map<String, dynamic>? _mapOrNull(dynamic v) =>
    v == null ? null : Map<String, dynamic>.from(v as Map);

List<String>? _stringListOrNull(dynamic v) =>
    v == null ? null : (v as List).map((e) => '$e').toList();

int _int(dynamic v, [int fallback = 0]) =>
    v == null ? fallback : (v as num).toInt();

bool _bool(dynamic v, bool fallback) => v == null ? fallback : v as bool;

dynamic _dispatch(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'evolve_selector_runtime':
    case 'evolve_selector_runtime_empty':
      return evolveSelectorRuntime(
        _mapOrNull(input['selectors']),
        _mapOrNull(input['healed']),
      );
    case 'build_runtime_evolution':
    case 'build_runtime_evolution_empty':
      return buildRuntimeEvolution(
        (input['mutations'] as List)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList(),
        (input['lineage'] as List)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList(),
      );
    case 'run_evolution_runtime':
    case 'run_evolution_runtime_prior':
    case 'run_evolution_runtime_empty':
      return runEvolutionRuntime(
        adaptiveMemory: _mapOrNull(input['adaptive_memory']),
        workflowResult: _mapOrNull(input['workflow_result']),
        semanticResult: _mapOrNull(input['semantic_result']),
        syncResult: _mapOrNull(input['sync_result']),
        distributedResult: _mapOrNull(input['distributed_result']),
        failures: _stringListOrNull(input['failures']),
        memory: _mapOrNull(input['memory']),
        tick: _int(input['tick']),
      );
    case 'run_evolution_for_extraction':
    case 'run_evolution_for_extraction_disabled':
    case 'run_evolution_for_extraction_no_merge':
      return runEvolutionForExtraction(
        evolvingRuntime: _bool(input['evolving_runtime'], true),
        adaptiveMemory: _mapOrNull(input['adaptive_memory']),
        workflowResult: _mapOrNull(input['workflow_result']),
        semanticResult: _mapOrNull(input['semantic_result']),
        syncResult: _mapOrNull(input['sync_result']),
        distributedResult: _mapOrNull(input['distributed_result']),
        failures: _stringListOrNull(input['failures']),
        tick: _int(input['tick']),
        mergeGraph: _bool(input['merge_graph'], true),
      );
    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  group('evolution_runtime cross-language parity', () {
    final raw = File('validation/parity/evolution_runtime_api_vectors.json')
        .readAsStringSync();
    final vectors = (jsonDecode(raw) as List).cast<Map<String, dynamic>>();

    for (final v in vectors) {
      final api = v['api'] as String;
      final input = Map<String, dynamic>.from(v['input'] as Map);
      final expected = v['det_hash'] as String;

      test('$api matches Python deterministic hash', () {
        final result = _dispatch(api, input);
        expect(computeDeterministicHash(result), expected, reason: api);
      });
    }
  });

  group('save/load roundtrip', () {
    test('save then load recovers memory deep-equal', () {
      final dir = Directory.systemTemp.createTempSync('wwx_evo_parity_');
      final path = '${dir.path}/native.enc';
      const key = 'evolution-key';
      try {
        final memory = runEvolutionRuntime(
          adaptiveMemory: <String, dynamic>{
            'selectors': <String, dynamic>{'a': '.alpha'},
            'healed_selectors': <String, dynamic>{'.old': '.new'},
          },
          workflowResult: <String, dynamic>{
            'workflow': <String, dynamic>{
              'plan': <String, dynamic>{
                'steps': <dynamic>[
                  <String, dynamic>{'id': 's1', 'priority': 2},
                ],
              },
              'execution': <String, dynamic>{
                'executed': <dynamic>['s1']
              },
            },
          },
          tick: 1,
        )['memory'] as Map<String, dynamic>;

        final saved = saveEvolutionRuntime(path, memory, key);
        expect(saved['saved'], isTrue);
        expect(File(path).existsSync(), isTrue);

        final loaded = loadEvolutionRuntime(path, key);
        expect(loaded['available'], isTrue);
        expect(
          computeDeterministicHash(loaded['memory']),
          computeDeterministicHash(memory),
          reason: 'roundtripped memory must hash-equal original',
        );
      } finally {
        dir.deleteSync(recursive: true);
      }
    });

    test('load of missing file returns empty memory', () {
      final dir = Directory.systemTemp.createTempSync('wwx_evo_missing_');
      try {
        final loaded = loadEvolutionRuntime('${dir.path}/absent.enc', 'k');
        expect(loaded['available'], isFalse);
        final mem = loaded['memory'] as Map<String, dynamic>;
        expect(mem['evolution_histories'], isEmpty);
        expect(mem['bounded'], isTrue);
      } finally {
        dir.deleteSync(recursive: true);
      }
    });
  });
}
