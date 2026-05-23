import '../replay/replay_graph.dart';
import 'runtime_graph.dart';

Map<String, dynamic> replayGraphLineage(RuntimeGraph graph) {
  final replayed = replayRuntimeGraph(graph);
  return {
    'replayed': replayed.toJson(),
    'lineage_hash': graphReplayHash(replayed),
    'bounded': true,
  };
}

RuntimeGraph mergeGraphReplay(RuntimeGraph base, RuntimeGraph overlay) {
  final b = normalizeRuntimeGraph(base);
  final o = normalizeRuntimeGraph(overlay);
  return normalizeRuntimeGraph(RuntimeGraph(
    nodes: [...b.nodes, ...o.nodes],
    edges: [...b.edges, ...o.edges],
  ));
}
