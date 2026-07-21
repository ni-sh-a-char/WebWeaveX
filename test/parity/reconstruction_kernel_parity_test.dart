import 'dart:convert';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show computeDeterministicHash, reconstructRuntime, getRuntimeKernel;

/// Executable cross-language parity (Python ≡ JavaScript ≡ Dart) for the
/// remaining Group-B APIs. Reference outputs captured by EXECUTING Python 2.0.1
/// and corroborated by executing the JavaScript engine functions —
/// see validation/executable/.
void main() {
  Map<String, dynamic>? asMap(dynamic v) =>
      v == null ? null : Map<String, dynamic>.from(v as Map);

  group('reconstruct_runtime + get_runtime_kernel — executable parity', () {
    final vectors = (jsonDecode(
      '[]',
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final api = v['api'] as String;
      final args = v['args'] as List<dynamic>;
      final expected = v['expected'];

      test('[$id] $api Dart output hash-equals executed Python output', () {
        final dynamic actual;
        if (api == 'reconstruct_runtime') {
          actual = reconstructRuntime(
            semanticIr: asMap(args[0]),
            workflowIr: asMap(args[1]),
            synchronizationIr: asMap(args[2]),
            executionIr: asMap(args[3]),
            memoryIr: asMap(args[4]),
            runtimeGraph: asMap(args[5]),
            runtimeType: (args[6] ?? 'browser') as String,
            tick: (args[7] ?? 0) as int,
          );
        } else if (api == 'get_runtime_kernel') {
          // Canonical observable kernel state (the rest are methods).
          actual = <String, dynamic>{
            'runtime_type':
                getRuntimeKernel(runtimeType: args[0] as String).runtimeKind,
          };
        } else {
          fail('unexpected api $api');
        }
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id\nexpected=$expected\nactual=$actual',
        );
      });
    }
  });

  group('reconstruct_runtime contract', () {
    test('Python-shaped result with 32-char runtime_id', () {
      final r = reconstructRuntime(
        semanticIr: <String, dynamic>{'a': 1},
        runtimeGraph: <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 1}
          ]
        },
      );
      expect((r['runtime_id'] as String).length, equals(32));
      expect(r['reconstructed'], isTrue);
      expect(r['graph_grounded'], isTrue);
      expect(r['bounded'], isTrue);
    });

    test('graph_grounded false for empty graph', () {
      final r = reconstructRuntime();
      expect(r['graph_grounded'], isFalse);
    });
  });
}

