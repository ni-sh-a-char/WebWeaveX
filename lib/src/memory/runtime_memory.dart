import 'dart:convert';

import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';

/// Graph-based runtime-memory fabric (internal helper; not the canonical Python
/// `build_runtime_memory`). The public, Python-aligned `buildRuntimeMemory`
/// (runtime_history / lineage / semantic_relations) lives in
/// `runtime_memory_family/runtime_memory_engines.dart`.
Map<String, dynamic> buildRuntimeMemoryFabric(RuntimeGraph graph,
    [List<dynamic> history = const []]) {
  final normalized = normalizeRuntimeGraph(graph);
  return {
    'memory': {'graph': normalized.toJson(), 'runtime_history': history},
    'stable_hash': stableMemoryFabricHash(normalized, history),
    'bounded': true,
  };
}

String stableMemoryFabricHash(RuntimeGraph graph,
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
  return buildRuntimeMemoryFabric(merged, [...ha, ...hb]);
}

/// Key lookup against the graph-based fabric (internal; not the canonical Python
/// `query_runtime_memory`, which takes `(memory, query_type, term)`).
dynamic queryRuntimeMemoryFabric(Map<String, dynamic> mem, String key) {
  final m = mem['memory'] as Map<String, dynamic>?;
  return m?[key];
}

Map<String, dynamic> replicateRuntimeMemory(Map<String, dynamic> mem) =>
    jsonDecode(jsonEncode(mem)) as Map<String, dynamic>;
