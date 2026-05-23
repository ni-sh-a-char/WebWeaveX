import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';

Map<String, dynamic> reconstructRuntime(
    {required Map<String, dynamic> extraction}) {
  final graphRaw = extraction['unified_runtime_graph'] ?? extraction['graph'];
  final graph = graphRaw is RuntimeGraph
      ? graphRaw
      : buildRuntimeGraph({'extraction': graphRaw});
  return {
    'runtime_id': computeDeterministicHash(graph.toJson()).substring(0, 16),
    'graph': graph.toJson(),
    'bounded': true,
    'reconstructed': true,
  };
}

Map<String, dynamic> replayRuntime(Map<String, dynamic> envelope) =>
    reconstructRuntime(extraction: envelope);

Map<String, dynamic> rebuildExecutionGraph(RuntimeGraph graph) => {
      'nodes': graph.nodes.length,
      'edges': graph.edges.length,
      'fingerprint': graphFingerprint(graph),
      'bounded': true,
    };
