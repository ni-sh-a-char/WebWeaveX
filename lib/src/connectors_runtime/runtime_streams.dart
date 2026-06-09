/// Port of core/connectors/runtime_stream_connector_engine.extract_runtime_streams
/// plus the kafka/redis/websocket sub-engines it delegates to.
library;

/// Port of core/connectors/kafka_connector_engine.extract_kafka_runtime.
Map<String, dynamic> extractKafkaRuntime([Map<String, dynamic>? snapshot]) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final List<dynamic> topics =
      List<dynamic>.from(snap['topics'] as List<dynamic>? ?? <dynamic>[]);
  topics.sort((dynamic a, dynamic b) => '$a'.compareTo('$b'));
  return <String, dynamic>{
    'stream_type': 'kafka',
    'topics': topics,
    'consumers':
        List<dynamic>.from(snap['consumers'] as List<dynamic>? ?? <dynamic>[]),
    'offsets': Map<String, dynamic>.from(
        (snap['offsets'] as Map<dynamic, dynamic>?) ?? <dynamic, dynamic>{}),
    'propagation_state': '${snap['state'] ?? 'stable'}',
    'event_lineage':
        List<dynamic>.from(snap['lineage'] as List<dynamic>? ?? <dynamic>[]),
    'degraded': snap['degraded'] ?? false,
    'bounded': true,
  };
}

/// Port of core/connectors/redis_connector_engine.extract_redis_runtime.
Map<String, dynamic> extractRedisRuntime([Map<String, dynamic>? snapshot]) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final List<dynamic> keys =
      List<dynamic>.from(snap['keys'] as List<dynamic>? ?? <dynamic>[]);
  return <String, dynamic>{
    'database_type': 'redis',
    'schemas': <dynamic>[],
    'tables': keys.length > 1000 ? keys.sublist(0, 1000) : keys,
    'indexes': <dynamic>[],
    'metrics': Map<String, dynamic>.from(
        (snap['metrics'] as Map<dynamic, dynamic>?) ?? <dynamic, dynamic>{}),
    'active_connections': (snap['clients'] as num? ?? 0).toInt(),
    'replication_state': '${snap['role'] ?? 'master'}',
    'streams':
        List<dynamic>.from(snap['streams'] as List<dynamic>? ?? <dynamic>[]),
    'degraded': snap['degraded'] ?? false,
    'bounded': true,
  };
}

/// Port of core/connectors/websocket_connector_engine.extract_websocket_runtime.
Map<String, dynamic> extractWebsocketRuntime([Map<String, dynamic>? snapshot]) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  return <String, dynamic>{
    'protocol': 'websocket',
    'connections': List<dynamic>.from(
        snap['connections'] as List<dynamic>? ?? <dynamic>[]),
    'frames': (snap['frames'] as num? ?? 0).toInt(),
    'bounded': true,
  };
}

/// Port of core/connectors/runtime_stream_connector_engine.extract_runtime_streams.
Map<String, dynamic> extractRuntimeStreams({
  List<String>? streamTypes,
  Map<String, dynamic>? snapshot,
}) {
  final List<String> types =
      streamTypes ?? <String>['kafka', 'redis', 'websocket'];
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final List<Map<String, dynamic>> streams = <Map<String, dynamic>>[];

  final List<String> ordered = <String>[...types]..sort();

  for (final String streamType in ordered) {
    try {
      if (streamType == 'kafka') {
        streams
            .add(extractKafkaRuntime(snap['kafka'] as Map<String, dynamic>?));
      } else if (streamType == 'redis') {
        final Map<String, dynamic> redis =
            extractRedisRuntime(snap['redis'] as Map<String, dynamic>?);
        streams.add(<String, dynamic>{
          'stream_type': 'redis_streams',
          'topics': redis['streams'] as List<dynamic>? ?? <dynamic>[],
          'offsets': <String, dynamic>{},
          'event_lineage': <dynamic>[],
          'bounded': true,
        });
      } else if (streamType == 'websocket') {
        final Map<String, dynamic> ws =
            extractWebsocketRuntime(snap['websocket'] as Map<String, dynamic>?);
        streams.add(<String, dynamic>{
          'stream_type': 'websocket',
          'topics': ws['connections'] as List<dynamic>? ?? <dynamic>[],
          'offsets': <String, dynamic>{},
          'event_lineage': <dynamic>[],
          'bounded': true,
        });
      } else if (streamType == 'sse' || streamType == 'queue') {
        final Map<String, dynamic> section =
            (snap[streamType] as Map<dynamic, dynamic>?)
                    ?.cast<String, dynamic>() ??
                <String, dynamic>{};
        streams.add(<String, dynamic>{
          'stream_type': streamType,
          'topics': List<dynamic>.from(
              section['topics'] as List<dynamic>? ?? <dynamic>[]),
          'offsets': <String, dynamic>{},
          'event_lineage': <dynamic>[],
          'bounded': true,
        });
      }
    } catch (_) {
      streams.add(<String, dynamic>{
        'stream_type': streamType,
        'degraded': true,
        'bounded': true,
      });
    }
  }

  return <String, dynamic>{
    'streams': streams,
    'count': streams.length,
    'bounded': true,
  };
}
