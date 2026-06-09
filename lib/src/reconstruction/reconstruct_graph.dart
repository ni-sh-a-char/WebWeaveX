import '../graph/runtime_graph.dart';

RuntimeGraph reconstructRuntimeGraph(Map<String, dynamic> extraction) {
  final graphRaw = extraction['unified_runtime_graph'] ?? extraction['graph'];
  if (graphRaw is RuntimeGraph) return normalizeRuntimeGraph(graphRaw);
  if (graphRaw is Map<String, dynamic>) {
    return buildRuntimeGraph({'extraction': graphRaw});
  }
  return RuntimeGraph(nodes: [], edges: []);
}

RuntimeGraph reconstructGraphFromSources(Map<String, dynamic> sources) {
  return buildRuntimeGraph(sources);
}

String graphReconstructionFingerprint(RuntimeGraph graph) =>
    graphFingerprint(graph);
