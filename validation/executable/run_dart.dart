// Execute the Dart implementation for each fixture; emit output + hash.
//   dart run validation/executable/run_dart.dart validation/executable/fixtures.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart'
    show
        computeDeterministicHash,
        extractKubernetesRuntime,
        extractDatabaseRuntime,
        buildRuntimeMemory,
        queryRuntimeMemory,
        computeGlobalRuntimeFingerprint,
        queryRuntimeGraph,
        validateReplayEquivalence,
        reconstructRuntime,
        getRuntimeKernel;

Map<String, dynamic>? _asMap(dynamic v) =>
    v == null ? null : Map<String, dynamic>.from(v as Map);

List<Map<String, dynamic>> _mapList(dynamic v) => v == null
    ? <Map<String, dynamic>>[]
    : <Map<String, dynamic>>[
        for (final e in v as List) Map<String, dynamic>.from(e as Map)
      ];

dynamic _call(String api, List<dynamic> args) {
  switch (api) {
    case 'extract_kubernetes_runtime':
      return extractKubernetesRuntime(_asMap(args[0]));
    case 'extract_database_runtime':
      return extractDatabaseRuntime(
        args[0] as String,
        args.length > 1 ? _asMap(args[1]) : null,
      );
    case 'build_runtime_memory':
      return buildRuntimeMemory(
        runtimeHistory: _mapList(args[0]),
        lineage: _mapList(args[1]),
        semanticRelations: _mapList(args[2]),
      );
    case 'query_runtime_memory':
      return queryRuntimeMemory(
        _asMap(args[0])!,
        args[1] as String,
        args[2] as String,
      );
    case 'compute_kaalka_hash':
      return computeDeterministicHash(args[0]);
    case 'compute_global_runtime_fingerprint':
      return computeGlobalRuntimeFingerprint(
        extraction: _asMap(args[0]),
        graph: _asMap(args[1]),
        memory: _asMap(args[2]),
        sync: _asMap(args[3]),
        reconstruction: _asMap(args[4]),
        kaalkaSeal: (args[5] ?? '') as String,
      );
    case 'query_runtime_graph':
      return queryRuntimeGraph(_asMap(args[0])!, _asMap(args[1])!);
    case 'validate_replay_equivalence':
      return validateReplayEquivalence(_asMap(args[0])!, _asMap(args[1])!);
    case 'reconstruct_runtime':
      return reconstructRuntime(
        semanticIr: _asMap(args[0]),
        workflowIr: _asMap(args[1]),
        synchronizationIr: _asMap(args[2]),
        executionIr: _asMap(args[3]),
        memoryIr: _asMap(args[4]),
        runtimeGraph: _asMap(args[5]),
        runtimeType: (args[6] ?? 'browser') as String,
        tick: (args[7] ?? 0) as int,
      );
    case 'get_runtime_kernel':
      return <String, dynamic>{
        'runtime_type':
            getRuntimeKernel(runtimeType: args[0] as String).runtimeKind,
      };
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
