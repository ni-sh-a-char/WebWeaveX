import 'dart:convert';

import '../graph/runtime_graph.dart';
import 'replay_equivalence.dart';
import 'replay_fingerprint.dart';
import 'replay_graph.dart';
import 'replay_memory.dart';

Map<String, dynamic> replayRuntimeState(Map<String, dynamic> extraction) =>
    jsonDecode(jsonEncode(extraction)) as Map<String, dynamic>;

Map<String, dynamic> validateFullRuntimeReplay(
  Map<String, dynamic> original,
  Map<String, dynamic> replayed,
) {
  final graph = _graphFromEnvelope(original);
  final replayGraph = _graphFromEnvelope(replayed);
  final replay = validateReplayEquivalence(original, replayed);
  final graphResult = validateGraphReplayEquivalence(graph, replayGraph);
  final mem = original['runtime_memory'] as Map<String, dynamic>?;
  final replayMem = replayed['runtime_memory'] as Map<String, dynamic>?;
  final memory = (mem != null && replayMem != null)
      ? validateMemoryReplayEquivalence(mem, replayMem)
      : null;
  final fingerprint =
      validateFingerprintReplayEquivalence(original, replayed, graph: graph, memory: mem);
  final equivalent = replay['equivalent'] == true &&
      graphResult['equivalent'] == true &&
      fingerprint['equivalent'] == true &&
      (memory == null || memory['equivalent'] == true);
  return {
    'equivalent': equivalent,
    'replay': replay,
    'graph': graphResult,
    'memory': memory,
    'fingerprint': fingerprint,
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
