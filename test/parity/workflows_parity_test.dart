import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/kaalka_runtime.dart';
import 'package:webweavex/src/workflows/workflows.dart';

Map<String, dynamic>? _asMap(dynamic v) =>
    v is Map ? Map<String, dynamic>.from(v) : null;

List<String>? _asStringList(dynamic v) =>
    v is List ? v.map<String>((dynamic e) => '$e').toList() : null;

/// Dispatch a vector input to the corresponding Dart workflow API.
dynamic _runApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'build_runtime_objective':
      return buildRuntimeObjective(
        input['objective'] as String,
        (input['priority'] as int?) ?? 0,
      );
    case 'build_workflow_plan':
      return buildWorkflowPlan(
        input['objective'] as String,
        semanticRuntime: _asMap(input['semantic_runtime']),
        causality: _asMap(input['causality']),
        applicationRuntime: _asMap(input['application_runtime']),
      );
    case 'run_autonomous_workflow':
      return runAutonomousWorkflow(
        objective: (input['objective'] as String?) ?? 'extract_dashboard',
        priority: (input['priority'] as int?) ?? 0,
        semanticRuntime: _asMap(input['semantic_runtime']),
        causalityResult: _asMap(input['causality_result']),
        applicationResult: _asMap(input['application_result']),
        distributedResult: _asMap(input['distributed_result']),
        nativeCognition: _asMap(input['native_cognition']),
        url: (input['url'] as String?) ?? '',
        memory: _asMap(input['memory']),
        tick: (input['tick'] as int?) ?? 0,
        failures: _asStringList(input['failures']),
      );
    case 'run_workflow_for_extraction':
      return runWorkflowForExtraction(
        autonomousWorkflow: (input['autonomous_workflow'] as bool?) ?? true,
        objective: (input['objective'] as String?) ?? 'extract_dashboard',
        memoryPath: (input['memory_path'] as String?) ?? '',
        memoryKey: (input['memory_key'] as String?) ?? '',
        url: (input['url'] as String?) ?? '',
        semanticRuntime: _asMap(input['semantic_runtime']),
        causalityResult: _asMap(input['causality_result']),
        applicationResult: _asMap(input['application_result']),
        distributedResult: _asMap(input['distributed_result']),
        nativeCognition: _asMap(input['native_cognition']),
        mergeGraph: (input['merge_graph'] as bool?) ?? true,
        tick: (input['tick'] as int?) ?? 0,
      );
    case 'replay_workflow_runtime':
      return replayWorkflowRuntime(
          _asMap(input['memory']) ?? <String, dynamic>{});
    default:
      throw StateError('Unknown api: $api');
  }
}

void main() {
  final File vectorsFile = File('validation/parity/workflows_api_vectors.json');
  final List<dynamic> vectors =
      jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;

  group('workflows family cross-language parity (hash)', () {
    for (var i = 0; i < vectors.length; i++) {
      final Map<String, dynamic> vec =
          Map<String, dynamic>.from(vectors[i] as Map);
      final String api = vec['api'] as String;
      final Map<String, dynamic> input =
          Map<String, dynamic>.from(vec['input'] as Map);
      final String expected = vec['det_hash'] as String;

      test('[$i] $api', () {
        final dynamic result = _runApi(api, input);
        final String actual = computeDeterministicHash(result);
        expect(
          actual,
          equals(expected),
          reason: 'API $api vector $i: Dart hash != Python hash',
        );
      });
    }
  });

  group('save/load workflow memory roundtrip', () {
    test('roundtrips a memory dict via temp file (deep-equal)', () {
      final Directory tmp = Directory.systemTemp.createTempSync('wwx_wf_mem_');
      final String path = '${tmp.path}/workflow_memory.kaalka';
      const String key = 'workflow-secret-key';

      final Map<String, dynamic> memory = <String, dynamic>{
        'objectives': <String, dynamic>{'objective': 'extract_dashboard'},
        'workflow_states': <String, dynamic>{'current_step': 1},
        'execution_graphs': <String, dynamic>{
          'executed': <dynamic>[
            <String, dynamic>{'step_id': 'step:0', 'completed': true}
          ]
        },
        'semantic_checkpoints': <dynamic>[
          <String, dynamic>{'aligned': true}
        ],
        'runtime_transitions': <dynamic>[
          <String, dynamic>{'from': 'step:0', 'to': 'step:1'}
        ],
        'bounded': true,
      };

      try {
        final Map<String, dynamic> saved =
            saveWorkflowMemory(path, memory, key);
        expect(saved['saved'], isTrue);
        expect(saved['algorithm'], equals('kaalka'));
        expect(File(path).existsSync(), isTrue);

        final Map<String, dynamic> loaded = loadWorkflowMemory(path, key);
        expect(loaded['available'], isTrue);
        expect(loaded['algorithm'], equals('kaalka'));

        // Deep-equal via stable serialization (order-independent).
        expect(
          computeDeterministicHash(loaded['memory']),
          equals(computeDeterministicHash(memory)),
        );
      } finally {
        if (tmp.existsSync()) {
          tmp.deleteSync(recursive: true);
        }
      }
    });

    test('load on missing path returns empty bounded memory', () {
      final Directory tmp =
          Directory.systemTemp.createTempSync('wwx_wf_mem_miss_');
      final String path = '${tmp.path}/does_not_exist.kaalka';
      try {
        final Map<String, dynamic> loaded = loadWorkflowMemory(path, 'any-key');
        expect(loaded['available'], isFalse);
        expect(loaded['bounded'], isTrue);
        final Map<String, dynamic> mem =
            Map<String, dynamic>.from(loaded['memory'] as Map);
        expect(mem['objectives'], equals(<String, dynamic>{}));
        expect(mem['semantic_checkpoints'], equals(<dynamic>[]));
      } finally {
        if (tmp.existsSync()) {
          tmp.deleteSync(recursive: true);
        }
      }
    });
  });
}
