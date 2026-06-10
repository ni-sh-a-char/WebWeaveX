import '../crypto/kaalka_runtime.dart';
import '../graph/runtime_graph.dart';
import 'reconstruct_browser.dart';
import 'reconstruct_graph.dart';
import 'reconstruct_memory.dart';
import 'reconstruct_replay.dart';

Map<String, dynamic> reconstructRuntimeFromEnvelope(
    {required Map<String, dynamic> extraction}) {
  final graph = reconstructRuntimeGraph(extraction);
  final memory = reconstructMemoryFromEnvelope(extraction);
  final browser = reconstructBrowserState(extraction);
  return {
    'runtime_id': computeDeterministicHash({
      'graph': graph.toJson(),
      'nodes': graph.nodes.length,
    }).substring(0, 32),
    'graph': graph.toJson(),
    'memory': memory,
    'browser': browser,
    'bounded': true,
    'reconstructed': true,
  };
}

Map<String, dynamic> replayRuntime(Map<String, dynamic> envelope) =>
    reconstructReplayState(envelope)['replayed'] as Map<String, dynamic>;

Map<String, dynamic> rebuildExecutionGraph(RuntimeGraph graph) => {
      'nodes': graph.nodes.length,
      'edges': graph.edges.length,
      'fingerprint': graphFingerprint(graph),
      'bounded': true,
    };
