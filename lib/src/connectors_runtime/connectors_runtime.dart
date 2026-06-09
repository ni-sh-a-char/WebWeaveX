/// Connectors / streaming / interaction runtime family — native Dart port of
/// the Python `webweavex` public APIs with proven cross-language determinism
/// parity (computeDeterministicHash(dartOutput) == Python compute_deterministic_hash).
///
/// Parity-proven (see test/parity/connectors_runtime_parity_test.dart and
/// validation/parity/connectors_runtime_api_vectors.json):
///   - extractApiRuntime       (extract_api_runtime)
///   - extractRuntimeStreams   (extract_runtime_streams)
///   - extractTelemetryRuntime (extract_telemetry_runtime)
///   - replayStreamEvents      (replay_stream_events)
///   - buildStreamTimeline     (build_stream_timeline)
///   - buildInteractionGraph   (build_interaction_graph)
library;

export 'api_connector.dart' show extractApiRuntime;
export 'runtime_streams.dart' show extractRuntimeStreams;
export 'telemetry_runtime.dart' show extractTelemetryRuntime;
export 'stream_replay.dart' show replayStreamEvents, buildStreamTimeline;
export 'interaction_graph.dart' show buildInteractionGraph;
