import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        executeRuntimeObjective,
        saveApplicationMemory,
        loadApplicationMemory,
        saveNativeRuntime,
        loadNativeRuntime;

/// Group D — application/native runtime APIs.
/// `execute_runtime_objective`: executable parity (Python ≡ JS ≡ Dart).
/// save/load pairs: proven by Kaalka save → load → deep-equality roundtrip.
void main() {
  Map<String, dynamic>? asMap(dynamic v) =>
      v == null ? null : Map<String, dynamic>.from(v as Map);

  group('execute_runtime_objective — executable parity (Python ≡ JS ≡ Dart)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/application_runtime_api_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final args = v['args'] as List<dynamic>;
      final expected = v['expected'];
      test('[$id] Dart output hash-equals executed Python output', () {
        final actual = executeRuntimeObjective(
          args[0] as String,
          asMap(args[1]) ?? <String, dynamic>{},
          asMap(args[2]) ?? <String, dynamic>{},
          asMap(args[3]) ?? <String, dynamic>{},
          adaptiveRuntime: asMap(args[4]),
        );
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('application/native memory persistence — save→load roundtrip', () {
    test('save_application_memory → load_application_memory deep-equals', () {
      final dir = Directory.systemTemp.createTempSync('wwx_app_');
      final path = '${dir.path}${Platform.pathSeparator}app.enc';
      const key = 'app-key';
      final memory = <String, dynamic>{
        'workflows': <String, dynamic>{'w1': 1},
        'forms': <String, dynamic>{},
        'bounded': true,
      };
      try {
        final saved = saveApplicationMemory(path, memory, key);
        expect(saved['saved'], isTrue);
        expect(saved['algorithm'], equals('kaalka'));
        final loaded = loadApplicationMemory(path, key);
        expect(loaded['available'], isTrue);
        expect(
          computeDeterministicHash(loaded['memory']),
          equals(computeDeterministicHash(memory)),
        );
      } finally {
        dir.deleteSync(recursive: true);
      }
    });

    test('load_application_memory missing → available:false, empty memory', () {
      final dir = Directory.systemTemp.createTempSync('wwx_app_');
      try {
        final loaded = loadApplicationMemory('${dir.path}/absent.enc', 'k');
        expect(loaded['available'], isFalse);
        expect((loaded['memory'] as Map)['bounded'], isTrue);
        expect((loaded['memory'] as Map)['workflows'],
            equals(<String, dynamic>{}));
      } finally {
        dir.deleteSync(recursive: true);
      }
    });

    test('save_native_runtime → load_native_runtime deep-equals', () {
      final dir = Directory.systemTemp.createTempSync('wwx_nat_');
      final path = '${dir.path}${Platform.pathSeparator}native.enc';
      const key = 'nat-key';
      final runtime = <String, dynamic>{
        'windows': <String, dynamic>{'main': true},
        'bounded': true,
      };
      try {
        expect(saveNativeRuntime(path, runtime, key)['saved'], isTrue);
        final loaded = loadNativeRuntime(path, key);
        expect(loaded['available'], isTrue);
        expect(
          computeDeterministicHash(loaded['runtime']),
          equals(computeDeterministicHash(runtime)),
        );
      } finally {
        dir.deleteSync(recursive: true);
      }
    });

    test('load_native_runtime missing → available:false, empty runtime', () {
      final dir = Directory.systemTemp.createTempSync('wwx_nat_');
      try {
        final loaded = loadNativeRuntime('${dir.path}/absent.enc', 'k');
        expect(loaded['available'], isFalse);
        expect((loaded['runtime'] as Map)['accessibility_trees'],
            equals(<String, dynamic>{}));
      } finally {
        dir.deleteSync(recursive: true);
      }
    });
  });
}
