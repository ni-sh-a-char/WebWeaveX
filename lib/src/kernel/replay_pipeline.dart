import '../replay/replay_runtime.dart';

Map<String, dynamic> runReplayPipeline(Map<String, dynamic> extraction) {
  final replayed = replayRuntimeState(extraction);
  final validation = validateFullRuntimeReplay(extraction, replayed);
  return {
    'replayed': replayed,
    'validation': validation,
    'equivalent': validation['equivalent'],
    'bounded': true,
  };
}
