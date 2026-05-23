import 'dart:convert';

import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';

Map<String, dynamic> buildRuntimeMemory(RuntimeGraph graph,
    [List<dynamic> history = const []]) {
  final normalized = normalizeRuntimeGraph(graph);
  return {
    'memory': {'graph': normalized.toJson(), 'runtime_history': history},
    'stable_hash': stableMemoryHash(normalized, history),
    'bounded': true,
  };
}

String stableMemoryHash(RuntimeGraph graph,
    [List<dynamic> history = const []]) {
  return computeDeterministicHash({
    'graph': normalizeRuntimeGraph(graph).toJson(),
    'history_len': history.length,
  });
}

Map<String, dynamic> mergeRuntimeMemories(
  Map<String, dynamic> a,
  Map<String, dynamic> b,
) {
  final ga = ((a['memory'] as Map?)?['graph'] as Map?) ?? {};
  final gb = ((b['memory'] as Map?)?['graph'] as Map?) ?? {};
  final merged = buildRuntimeGraph({
    'nodes': [
      ...((ga['nodes'] as List?) ?? []),
      ...((gb['nodes'] as List?) ?? []),
    ],
    'edges': [
      ...((ga['edges'] as List?) ?? []),
      ...((gb['edges'] as List?) ?? []),
    ],
  });
  final ha = ((a['memory'] as Map?)?['runtime_history'] as List?) ?? [];
  final hb = ((b['memory'] as Map?)?['runtime_history'] as List?) ?? [];
  return buildRuntimeMemory(merged, [...ha, ...hb]);
}

dynamic queryRuntimeMemory(Map<String, dynamic> mem, String key) {
  final m = mem['memory'] as Map<String, dynamic>?;
  return m?[key];
}

Map<String, dynamic> replicateRuntimeMemory(Map<String, dynamic> mem) =>
    jsonDecode(jsonEncode(mem)) as Map<String, dynamic>;
