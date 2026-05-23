import '../replay/replay_runtime.dart';
import 'reconstruct_browser.dart';
import 'reconstruct_graph.dart';
import 'reconstruct_memory.dart';

Map<String, dynamic> reconstructReplayState(Map<String, dynamic> extraction) {
  final replayed = replayRuntimeState(extraction);
  final graph = reconstructRuntimeGraph(extraction);
  final memory = reconstructMemoryFromEnvelope(extraction);
  final browser = reconstructBrowserState(extraction);
  final validation = validateFullRuntimeReplay(extraction, replayed);
  return {
    'replayed': replayed,
    'graph': graph.toJson(),
    'memory': memory,
    'browser': browser,
    'validation': validation,
    'bounded': true,
  };
}
