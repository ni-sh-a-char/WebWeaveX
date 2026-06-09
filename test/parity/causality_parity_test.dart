import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/causality/causality.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

dynamic _callApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'run_causality_runtime':
      return runCausalityRuntime(
        interactions: input['interactions'] as List<dynamic>?,
        nativeCognition: input['native_cognition'] as Map<String, dynamic>?,
        browserEvents: _eventsOrNull(input['browser_events']),
        applicationResult: input['application_result'] as Map<String, dynamic>?,
        distributedResult: input['distributed_result'] as Map<String, dynamic>?,
        memory: input['memory'] as Map<String, dynamic>?,
      );
    case 'run_causality_for_extraction':
      return runCausalityForExtraction(
        causalityRuntime: input.containsKey('causality_runtime')
            ? input['causality_runtime'] as bool
            : true,
        mergeGraph: input.containsKey('merge_graph')
            ? input['merge_graph'] as bool
            : true,
        interactions: input['interactions'] as List<dynamic>?,
        nativeCognition: input['native_cognition'] as Map<String, dynamic>?,
        browserEvents: _eventsOrNull(input['browser_events']),
        applicationResult: input['application_result'] as Map<String, dynamic>?,
        distributedResult: input['distributed_result'] as Map<String, dynamic>?,
      );
    case 'replay_causal_runtime':
      return replayCausalRuntime(input['memory'] as Map<String, dynamic>);
    default:
      throw StateError('unknown api $api');
  }
}

List<Map<String, dynamic>>? _eventsOrNull(dynamic v) {
  if (v == null) return null;
  return List<Map<String, dynamic>>.from(
    (v as List<dynamic>).map((e) => Map<String, dynamic>.from(e as Map)),
  );
}

void main() {
  group('causality API parity (Python det_hash gate)', () {
    final vectorsFile = File('validation/parity/causality_api_vectors.json');
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

  group('save/load causal memory roundtrip', () {
    test('encrypt -> persist -> decrypt deep-equals input', () {
      final tempDir = Directory.systemTemp.createTempSync('wwx_causal_');
      final path = '${tempDir.path}${Platform.pathSeparator}mem.json';
      const key = 'parity-secret-key';

      final memory = <String, dynamic>{
        'event_chains': <String, dynamic>{
          'chain': <dynamic>[
            <String, dynamic>{'id': 'browser:evt:0', 'step': 0, 'depth': 0},
          ],
          'length': 1,
        },
        'runtime_propagation': <String, dynamic>{
          'order': <dynamic>['a', 'b']
        },
        'causal_graphs': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[]
        },
        'distributed_workflows': <String, dynamic>{},
        'synchronization_state': <String, dynamic>{'count': 2},
        'bounded': true,
      };

      try {
        final saved = saveCausalMemory(path, memory, key);
        expect(saved['saved'], isTrue);
        expect(File(path).existsSync(), isTrue);

        final loaded = loadCausalMemory(path, key);
        expect(loaded['available'], isTrue);
        final recovered = loaded['memory'] as Map<String, dynamic>;

        expect(recovered, equals(memory));
      } finally {
        tempDir.deleteSync(recursive: true);
      }
    });

    test('load missing path -> available:false with empty memory', () {
      final tempDir = Directory.systemTemp.createTempSync('wwx_causal_');
      final path = '${tempDir.path}${Platform.pathSeparator}missing.json';
      try {
        final loaded = loadCausalMemory(path, 'k');
        expect(loaded['available'], isFalse);
        final mem = loaded['memory'] as Map<String, dynamic>;
        expect(mem['event_chains'], equals(<String, dynamic>{}));
        expect(mem['bounded'], isTrue);
      } finally {
        tempDir.deleteSync(recursive: true);
      }
    });
  });

  group('branch coverage', () {
    test('run_causality_runtime with empty inputs is deterministic', () {
      final a = runCausalityRuntime();
      final b = runCausalityRuntime();
      expect(computeDeterministicHash(a), equals(computeDeterministicHash(b)));
      expect(a['bounded'], isTrue);
    });

    test('run_causality_for_extraction disabled returns enabled:false', () {
      final r = runCausalityForExtraction(causalityRuntime: false);
      expect(r['enabled'], isFalse);
      expect(r['bounded'], isTrue);
    });

    test('merge_graph true produces unified_runtime_graph', () {
      final r = runCausalityForExtraction(
        interactions: <dynamic>[
          <String, dynamic>{'action': 'click', 'selector': '#a'},
        ],
        mergeGraph: true,
      );
      final unified = r['unified_graph'] as Map<String, dynamic>;
      expect(unified['ir'], equals('unified_runtime_graph'));
    });

    test('replay of empty memory yields replayed:true', () {
      final r = replayCausalRuntime(<String, dynamic>{});
      expect(r['replayed'], isTrue);
      expect(r['event_propagation'], equals(<String, dynamic>{}));
    });
  });
}
