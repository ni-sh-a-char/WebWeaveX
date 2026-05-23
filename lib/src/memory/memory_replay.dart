import '../graph/runtime_graph.dart';
import 'memory_lineage.dart';
import 'runtime_memory.dart';
import 'runtime_memory_graph.dart';

Map<String, dynamic> replayMemoryState(
  RuntimeGraph graph, [
  List<dynamic> history = const [],
]) {
  final mem = buildRuntimeMemory(graph, history);
  final histMaps = history
      .map((h) => h is Map<String, dynamic> ? h : {'tick': history.indexOf(h)})
      .cast<Map<String, dynamic>>()
      .toList();
  final lineage = buildMemoryLineage(histMaps);
  final memoryGraph = buildRuntimeMemoryGraph(graph, history);
  return {
    ...mem,
    'lineage': lineage['lineage'],
    'memory_graph': memoryGraph,
    'replay_hash': stableMemoryHash(graph, history),
    'bounded': true,
  };
}

bool validateMemoryReplay(
  Map<String, dynamic> original,
  Map<String, dynamic> replayed,
) =>
    original['stable_hash'] == replayed['stable_hash'];
