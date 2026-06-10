import '../graph/runtime_graph.dart';
import '../memory/runtime_memory.dart';

Map<String, dynamic> replayRuntimeMemory(RuntimeGraph graph,
    [List<dynamic> history = const []]) {
  return buildRuntimeMemoryFabric(graph, history);
}

Map<String, dynamic> validateMemoryReplayEquivalence(
  Map<String, dynamic> original,
  Map<String, dynamic> replayed,
) {
  return {
    'equivalent': original['stable_hash'] == replayed['stable_hash'],
    'stable_hash_match': original['stable_hash'] == replayed['stable_hash'],
    'bounded': true,
  };
}

String memoryReplayHash(RuntimeGraph graph,
        [List<dynamic> history = const []]) =>
    stableMemoryFabricHash(graph, history);
