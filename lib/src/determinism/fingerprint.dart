import '../crypto/hashing.dart';
import '../graph/runtime_graph.dart';

String computeGlobalRuntimeFingerprint(
  Map<String, dynamic> envelope,
  RuntimeGraph graph,
) {
  return computeDeterministicHash({
    'pipeline_hash': envelope['pipeline_hash'],
    'graph': graphFingerprint(graph),
    'bounded': envelope['bounded'] ?? true,
  });
}
