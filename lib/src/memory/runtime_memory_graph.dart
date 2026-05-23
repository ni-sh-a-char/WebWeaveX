import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';

Map<String, dynamic> buildRuntimeMemoryGraph(
  RuntimeGraph graph, [
  List<dynamic> history = const [],
]) {
  final normalized = normalizeRuntimeGraph(graph);
  final entities = normalized.nodes
      .map((n) => {
            'id': n.id,
            'type': n.type,
            'relations': normalized.edges
                .where((e) => e.source == n.id)
                .map((e) => e.target)
                .toList(),
          })
      .toList();
  final relations = normalized.edges
      .map((e) => {
            'from': e.source ?? e.from,
            'to': e.target ?? e.to,
            'type': e.type,
          })
      .toList();
  return {
    'entities': entities,
    'relations': relations,
    'graph_fingerprint':
        computeDeterministicHash({'entities': entities, 'relations': relations, 'history_len': history.length}),
    'bounded': true,
  };
}
