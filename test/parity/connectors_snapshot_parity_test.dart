import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        extractKubernetesRuntime,
        extractDatabaseRuntime;

/// Executable cross-language parity for the snapshot extractors.
/// Reference outputs were captured by EXECUTING Python 2.0.1 (and corroborated
/// by executing the JavaScript reference) on the same fixtures —
/// see validation/executable/. Dart output must hash-equal the executed Python
/// output: `computeDeterministicHash(dartOut) == computeDeterministicHash(pyOut)`.
void main() {
  Map<String, dynamic>? asMap(dynamic v) =>
      v == null ? null : Map<String, dynamic>.from(v as Map);

  group('connectors snapshot extractors — executable parity (vs Python 2.0.1)',
      () {
    final vectors = (jsonDecode(
      File('validation/parity/connectors_snapshot_api_vectors.json')
          .readAsStringSync(),
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
        if (api == 'extract_kubernetes_runtime') {
          actual = extractKubernetesRuntime(asMap(args[0]));
        } else if (api == 'extract_database_runtime') {
          actual = extractDatabaseRuntime(
            args[0] as String,
            args.length > 1 ? asMap(args[1]) : null,
          );
        } else {
          fail('unexpected api $api');
        }
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id\nexpected=$expected\nactual=$actual',
        );
        expect((actual as Map)['bounded'], isTrue);
      });
    }
  });

  group('snapshot extractor branch coverage', () {
    test('database dispatch covers all engines + degraded', () {
      for (final t in ['postgresql', 'mysql', 'sqlite', 'redis', 'mongodb']) {
        final r = extractDatabaseRuntime(t);
        expect(r['bounded'], isTrue);
        expect(r['database_type'], equals(t == 'mongodb' ? 'mongodb' : t));
      }
      expect(extractDatabaseRuntime('mongodb')['degraded'], isTrue);
    });

    test('kubernetes sorts namespaces and pods deterministically', () {
      final r = extractKubernetesRuntime(<String, dynamic>{
        'namespaces': <dynamic>['z', 'a'],
        'pods': <dynamic>[
          <String, dynamic>{'name': 'b'},
          <String, dynamic>{'name': 'a'},
        ],
      });
      expect(r['namespaces'], equals(<dynamic>['a', 'z']));
      expect((r['pods'] as List).first, equals(<String, dynamic>{'name': 'a'}));
      expect(r['deployments'], equals(<dynamic>[]));
    });
  });
}
