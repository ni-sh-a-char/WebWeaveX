import 'dart:convert';

import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';

String graphReplayHash(RuntimeGraph graph) {
  final n = normalizeRuntimeGraph(graph);
  return computeDeterministicHash(jsonEncode({
    'nodes': n.nodes.map((e) => e.toJson()).toList(),
    'edges': n.edges.map((e) => e.toJson()).toList(),
  }));
}

RuntimeGraph replayRuntimeGraph(RuntimeGraph graph) {
  final raw = jsonDecode(jsonEncode(graph.toJson())) as Map<String, dynamic>;
  final nodes = (raw['nodes'] as List)
      .map((n) => RuntimeNode(
            id: (n as Map)['id'] as String?,
            type: n['type'] as String?,
            payload: n['payload'],
          ))
      .toList();
  final edges = (raw['edges'] as List)
      .map((e) => RuntimeEdge(
            source: (e as Map)['source'] as String?,
            target: e['target'] as String?,
            type: e['type'] as String?,
          ))
      .toList();
  return normalizeRuntimeGraph(RuntimeGraph(nodes: nodes, edges: edges));
}

Map<String, dynamic> validateGraphReplayEquivalence(
  RuntimeGraph original,
  RuntimeGraph replayed,
) {
  final a = graphReplayHash(original);
  final b = graphReplayHash(replayed);
  return {
    'equivalent': a == b,
    'graph_hash': a,
    'replay_hash': b,
    'bounded': true,
  };
}
