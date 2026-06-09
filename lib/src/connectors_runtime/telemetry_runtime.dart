/// Port of core/connectors/telemetry_connector_engine.extract_telemetry_runtime.
library;

List<dynamic> _capped(List<dynamic>? source, int limit) {
  final List<dynamic> list = List<dynamic>.from(source ?? <dynamic>[]);
  return list.length > limit ? list.sublist(0, limit) : list;
}

/// Port of core/connectors/telemetry_connector_engine.extract_telemetry_runtime.
Map<String, dynamic> extractTelemetryRuntime({
  List<String>? backends,
  Map<String, dynamic>? snapshot,
}) {
  final List<String> backendList =
      backends ?? <String>['opentelemetry', 'prometheus', 'jaeger'];
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};

  final List<String> sortedBackends = <String>[...backendList]..sort();

  return <String, dynamic>{
    'backends': sortedBackends,
    'metrics':
        List<dynamic>.from(snap['metrics'] as List<dynamic>? ?? <dynamic>[]),
    'traces':
        List<dynamic>.from(snap['traces'] as List<dynamic>? ?? <dynamic>[]),
    'spans': _capped(snap['spans'] as List<dynamic>?, 10000),
    'logs': _capped(snap['logs'] as List<dynamic>?, 10000),
    'distributed_correlations': List<dynamic>.from(
        snap['correlations'] as List<dynamic>? ?? <dynamic>[]),
    'degraded': snap['degraded'] ?? false,
    'bounded': true,
  };
}
