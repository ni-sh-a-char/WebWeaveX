// Execute the Dart implementation for each fixture; emit output + hash.
//   dart run validation/executable/run_dart.dart validation/executable/fixtures.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        extractKubernetesRuntime,
        extractDatabaseRuntime;

Map<String, dynamic>? _asMap(dynamic v) =>
    v == null ? null : Map<String, dynamic>.from(v as Map);

dynamic _call(String api, List<dynamic> args) {
  switch (api) {
    case 'extract_kubernetes_runtime':
      return extractKubernetesRuntime(_asMap(args[0]));
    case 'extract_database_runtime':
      return extractDatabaseRuntime(
        args[0] as String,
        args.length > 1 ? _asMap(args[1]) : null,
      );
    case 'compute_kaalka_hash':
      return computeDeterministicHash(args[0]);
    default:
      throw StateError('unknown/contract-divergent api $api');
  }
}

void main(List<String> argv) {
  final fixtures =
      jsonDecode(File(argv[0]).readAsStringSync()) as List<dynamic>;
  final out = <Map<String, dynamic>>[];
  for (final f in fixtures) {
    final fx = Map<String, dynamic>.from(f as Map);
    final api = fx['api'] as String;
    final args = fx['args'] as List<dynamic>;
    try {
      final result = _call(api, args);
      out.add(<String, dynamic>{
        'id': fx['id'],
        'api': api,
        'output': result,
        'hash': api == 'compute_kaalka_hash'
            ? result
            : computeDeterministicHash(result),
      });
    } catch (e) {
      out.add(<String, dynamic>{
        'id': fx['id'],
        'api': api,
        'error': e.toString(),
      });
    }
  }
  stdout.write(jsonEncode(out));
}
