import '../determinism/fingerprint.dart';
import '../graph/runtime_graph.dart';
import 'replay_graph.dart';

Map<String, dynamic> validateFingerprintReplayEquivalence(
  Map<String, dynamic> original,
  Map<String, dynamic> replayed, {
  RuntimeGraph? graph,
  Map<String, dynamic>? memory,
}) {
  final g = graph ?? _graphFromEnvelope(original);
  final rg = _graphFromEnvelope(replayed);
  final origFp = computeGlobalRuntimeFingerprint(original, g);
  final replayFp = computeGlobalRuntimeFingerprint(replayed, rg);
  final graphHashMatch = graphReplayHash(g) == graphReplayHash(rg);
  return {
    'equivalent': origFp == replayFp && graphHashMatch,
    'global_fingerprint_match': origFp == replayFp,
    'graph_hash_match': graphHashMatch,
    'bounded': true,
  };
}

RuntimeGraph _graphFromEnvelope(Map<String, dynamic> envelope) {
  final g = envelope['unified_runtime_graph'] ?? envelope['graph'];
  if (g is RuntimeGraph) return g;
  if (g is Map<String, dynamic>) {
    return buildRuntimeGraph({'graph': g});
  }
  return RuntimeGraph(nodes: [], edges: []);
}
