import '../reconstruction/reconstruct_replay.dart';
import '../reconstruction/reconstruct_runtime.dart';

Map<String, dynamic> runReconstructionPipeline(
    Map<String, dynamic> extraction) {
  final reconstructed = reconstructRuntimeFromEnvelope(extraction: extraction);
  final replay = reconstructReplayState(extraction);
  return {
    'reconstructed': reconstructed,
    'replay': replay,
    'bounded': true,
  };
}
