import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/semantic/semantic_runtime.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

List<Map<String, dynamic>>? _interactions(dynamic v) {
  if (v == null) return null;
  return (v as List<dynamic>)
      .map((e) => Map<String, dynamic>.from(e as Map<dynamic, dynamic>))
      .toList();
}

List<String>? _repoFiles(dynamic v) {
  if (v == null) return null;
  return (v as List<dynamic>).map((e) => '$e').toList();
}

dynamic _callApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'run_semantic_runtime':
      return runSemanticRuntime(
        url: (input['url'] as String?) ?? '',
        html: (input['html'] as String?) ?? '',
        text: (input['text'] as String?) ?? '',
        interactions: _interactions(input['interactions']),
        applicationResult: input['application_result'] as Map<String, dynamic>?,
        causalityResult: input['causality_result'] as Map<String, dynamic>?,
        nativeCognition: input['native_cognition'] as Map<String, dynamic>?,
        repositoryFiles: _repoFiles(input['repository_files']),
        runtimeGraph: input['runtime_graph'] as Map<String, dynamic>?,
        memory: input['memory'] as Map<String, dynamic>?,
        objective: (input['objective'] as String?) ?? '',
      );
    case 'run_semantic_for_extraction':
      return runSemanticForExtraction(
        semanticRuntime: input.containsKey('semantic_runtime')
            ? input['semantic_runtime'] as bool
            : true,
        memoryPath: (input['memory_path'] as String?) ?? '',
        memoryKey: (input['memory_key'] as String?) ?? '',
        url: (input['url'] as String?) ?? '',
        html: (input['html'] as String?) ?? '',
        interactions: _interactions(input['interactions']),
        applicationResult: input['application_result'] as Map<String, dynamic>?,
        causalityResult: input['causality_result'] as Map<String, dynamic>?,
        nativeCognition: input['native_cognition'] as Map<String, dynamic>?,
        runtimeGraph: input['runtime_graph'] as Map<String, dynamic>?,
        objective: (input['objective'] as String?) ?? '',
        mergeGraph: input.containsKey('merge_graph')
            ? input['merge_graph'] as bool
            : true,
      );
    case 'replay_semantic_runtime':
      return replaySemanticRuntime(
          Map<String, dynamic>.from(input['memory'] as Map<dynamic, dynamic>));
    default:
      throw StateError('unknown api $api');
  }
}

void main() {
  final vectorsFile = File('validation/parity/semantic_api_vectors.json');

  group('semantic runtime family — Python parity', () {
    late List<dynamic> vectors;

    setUpAll(() {
      vectors = jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;
    });

    test('vector file loads', () {
      expect(vectors, isNotEmpty);
    });

    test('hash parity for run_* / replay_* APIs', () {
      for (final raw in vectors) {
        final v = raw as Map<String, dynamic>;
        final api = v['api'] as String;
        if (api == 'save_load_roundtrip') continue;
        final input =
            Map<String, dynamic>.from(v['input'] as Map<dynamic, dynamic>);
        final expected = v['det_hash'] as String;
        final result = _callApi(api, input);
        final actual = computeDeterministicHash(result);
        expect(actual, equals(expected),
            reason: 'NO-MATCH for $api with input $input');
      }
    });
  });

  group('semantic memory — save/load roundtrip', () {
    test('save then load deep-equals the input memory', () {
      final vectors =
          jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;
      var roundtripCases = 0;
      for (final raw in vectors) {
        final v = raw as Map<String, dynamic>;
        if (v['api'] != 'save_load_roundtrip') continue;
        roundtripCases++;
        final input =
            Map<String, dynamic>.from(v['input'] as Map<dynamic, dynamic>);
        final memory =
            Map<String, dynamic>.from(input['memory'] as Map<dynamic, dynamic>);
        final key = input['key'] as String;

        final tmp = File(
            '${Directory.systemTemp.path}/wwx_sem_mem_${DateTime.now().microsecondsSinceEpoch}_$roundtripCases.kaalka');
        try {
          final saved = saveSemanticMemory(tmp.path, memory, key);
          expect(saved['saved'], isTrue);
          expect(tmp.existsSync(), isTrue);

          final loaded = loadSemanticMemory(tmp.path, key);
          expect(loaded['available'], isTrue);
          expect(loaded['algorithm'], equals('kaalka'));
          expect(loaded['memory'], equals(memory));
        } finally {
          if (tmp.existsSync()) tmp.deleteSync();
        }
      }
      expect(roundtripCases, greaterThan(0));
    });

    test('load of a missing file returns empty memory envelope', () {
      final missing = File(
          '${Directory.systemTemp.path}/wwx_sem_missing_${DateTime.now().microsecondsSinceEpoch}.kaalka');
      if (missing.existsSync()) missing.deleteSync();
      final loaded = loadSemanticMemory(missing.path, 'any-key');
      expect(loaded['available'], isFalse);
      expect(loaded['bounded'], isTrue);
      final mem = loaded['memory'] as Map<String, dynamic>;
      expect(mem['ontology'], equals(<String, dynamic>{}));
      expect(mem['semantic_graph'], equals(<String, dynamic>{}));
      expect(mem['entity_mappings'], equals(<String, dynamic>{}));
      expect(mem['semantic_workflows'], equals(<String, dynamic>{}));
      expect(mem['runtime_semantics'], equals(<String, dynamic>{}));
      expect(mem['bounded'], isTrue);
    });
  });

  group('branch coverage', () {
    test('run_semantic_for_extraction disabled short-circuits', () {
      final out = runSemanticForExtraction(semanticRuntime: false);
      expect(out['enabled'], isFalse);
      expect(out['bounded'], isTrue);
    });

    test('run_semantic_for_extraction merge_graph=false leaves empty graph',
        () {
      final out = runSemanticForExtraction(mergeGraph: false, objective: 'x');
      expect(out['enabled'], isTrue);
      expect(out['unified_graph'], equals(<String, dynamic>{}));
      expect(out['memory_persisted'], isFalse);
    });

    test('run_semantic_for_extraction with memory_path persists + reloads', () {
      final tmp = File(
          '${Directory.systemTemp.path}/wwx_sem_ext_${DateTime.now().microsecondsSinceEpoch}.kaalka');
      try {
        final out = runSemanticForExtraction(
          memoryPath: tmp.path,
          memoryKey: 'k',
          objective: 'persist',
        );
        expect(out['memory_persisted'], isTrue);
        expect(tmp.existsSync(), isTrue);
        // second run loads the persisted memory (available branch)
        final out2 = runSemanticForExtraction(
          memoryPath: tmp.path,
          memoryKey: 'k',
          objective: 'persist',
        );
        expect(out2['enabled'], isTrue);
      } finally {
        if (tmp.existsSync()) tmp.deleteSync();
      }
    });

    test('run_semantic_runtime with seeded memory triggers diff branch', () {
      final out = runSemanticRuntime(
        text: 'api service user',
        objective: 'go',
        memory: <String, dynamic>{
          'entities': <String, dynamic>{
            'entities': <dynamic>[
              <String, dynamic>{'id': 'entity:old:0'}
            ]
          },
          'domain': <String, dynamic>{'domain': 'finance'},
          'ontology': <String, dynamic>{'primary_domain': 'finance'},
          'workflow': <String, dynamic>{'objective': 'old'},
        },
      );
      final diff = out['diff'] as Map<String, dynamic>;
      expect(diff, isNotEmpty);
      expect(diff['bounded'], isTrue);
      // hash is stable across two identical invocations
      final a = computeDeterministicHash(out);
      final b = computeDeterministicHash(runSemanticRuntime(
        text: 'api service user',
        objective: 'go',
        memory: <String, dynamic>{
          'entities': <String, dynamic>{
            'entities': <dynamic>[
              <String, dynamic>{'id': 'entity:old:0'}
            ]
          },
          'domain': <String, dynamic>{'domain': 'finance'},
          'ontology': <String, dynamic>{'primary_domain': 'finance'},
          'workflow': <String, dynamic>{'objective': 'old'},
        },
      ));
      expect(a, equals(b));
    });

    test('replay with empty vs populated memory differ', () {
      final empty = replaySemanticRuntime(<String, dynamic>{});
      expect(empty['replayed'], isTrue);
      expect(empty['semantic_graph'], equals(<String, dynamic>{}));
      final populated = replaySemanticRuntime(<String, dynamic>{
        'semantic_graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n:1'}
          ]
        },
      });
      expect(
          populated['semantic_graph'],
          equals(<String, dynamic>{
            'nodes': <dynamic>[
              <String, dynamic>{'id': 'n:1'}
            ]
          }));
    });
  });
}
