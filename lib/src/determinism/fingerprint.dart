import '../crypto/hashing.dart';
import '../graph/runtime_graph.dart';

/// Dart-native pipeline fingerprint (internal). The canonical Python
/// `compute_global_runtime_fingerprint` is in `parity/canonical_runtime.dart`.
String computeRuntimePipelineFingerprint(
  Map<String, dynamic> envelope,
  RuntimeGraph graph,
) {
  return computeDeterministicHash({
    'pipeline_hash': envelope['pipeline_hash'],
    'graph': graphFingerprint(graph),
    'bounded': envelope['bounded'] ?? true,
  });
}
