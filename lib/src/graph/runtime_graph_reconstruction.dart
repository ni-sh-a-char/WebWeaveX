import '../reconstruction/reconstruct_graph.dart';
import 'runtime_graph.dart';

Map<String, dynamic> reconstructGraphFromIr(Map<String, dynamic> sources) {
  final graph = reconstructGraphFromSources(sources);
  return {
    'graph': graph.toJson(),
    'fingerprint': graphFingerprint(graph),
    'bounded': true,
  };
}

RuntimeGraph rebuildGraphFromPartial(RuntimeGraph partial) {
  final normalized = normalizeRuntimeGraph(partial);
  final nodes = <RuntimeNode>[];
  for (var i = 0; i < normalized.nodes.length; i++) {
    final n = normalized.nodes[i];
    nodes.add(RuntimeNode(
      id: n.id ?? 'rebuilt:$i',
      type: n.type,
      payload: n.payload,
    ));
  }
  return normalizeRuntimeGraph(
      RuntimeGraph(nodes: nodes, edges: normalized.edges));
}
