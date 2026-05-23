import '../graph/runtime_graph.dart';
import '../memory/runtime_memory.dart';
import '../memory/runtime_memory_graph.dart';
import 'reconstruct_graph.dart';

Map<String, dynamic> reconstructMemoryGraph(
  RuntimeGraph graph, [
  List<dynamic> history = const [],
]) {
  final memoryGraph = buildRuntimeMemoryGraph(graph, history);
  final fabric = buildRuntimeMemory(graph, history);
  return {
    'memory_graph': memoryGraph,
    'memory': fabric['memory'],
    'stable_hash': fabric['stable_hash'],
    'bounded': true,
  };
}

Map<String, dynamic> reconstructMemoryFromEnvelope(Map<String, dynamic> envelope) {
  final graph = reconstructRuntimeGraph(envelope);
  final history =
      ((envelope['runtime_memory'] as Map?)?['runtime_history'] as List?) ?? [];
  return reconstructMemoryGraph(graph, history);
}
