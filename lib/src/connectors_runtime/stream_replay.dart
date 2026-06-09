/// Port of core/streaming/stream_replay_engine: replay_stream_events and
/// build_stream_timeline.
library;

const int maxReplayEvents = 10000;

int _asInt(dynamic value) {
  if (value is int) return value;
  if (value is num) return value.toInt();
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}

/// Port of core/streaming/stream_replay_engine.replay_stream_events.
///
/// The `page` side-effect path (appending to `page._test_replay_log`) is a
/// live-object hook with no deterministic-output contribution; the snapshot
/// path (page == null) is ported. The returned dict is identical regardless.
Map<String, dynamic> replayStreamEvents(
  Object? page,
  List<Map<String, dynamic>> streamLog,
) {
  final List<Map<String, dynamic>> replayed = <Map<String, dynamic>>[];

  final int limit =
      streamLog.length > maxReplayEvents ? maxReplayEvents : streamLog.length;

  for (int index = 0; index < limit; index++) {
    final Map<String, dynamic> event = streamLog[index];
    replayed.add(<String, dynamic>{
      'step': index,
      'event': Map<String, dynamic>.from(event),
      'replayed': true,
    });
  }

  return <String, dynamic>{
    'replay': replayed,
    'bounded': true,
  };
}

/// Port of core/streaming/stream_replay_engine.build_stream_timeline.
Map<String, dynamic> buildStreamTimeline(
  List<Map<String, dynamic>> events,
) {
  // Python sorted() is stable; Dart List.sort is not — append the original
  // index as a final tiebreak to preserve insertion order for equal keys.
  final List<MapEntry<int, Map<String, dynamic>>> indexed =
      <MapEntry<int, Map<String, dynamic>>>[];
  for (int i = 0; i < events.length; i++) {
    indexed.add(MapEntry<int, Map<String, dynamic>>(i, events[i]));
  }

  indexed.sort((MapEntry<int, Map<String, dynamic>> a,
      MapEntry<int, Map<String, dynamic>> b) {
    final int tsCmp = _asInt(a.value['timestamp'] ?? 0)
        .compareTo(_asInt(b.value['timestamp'] ?? 0));
    if (tsCmp != 0) return tsCmp;
    final int idCmp =
        '${a.value['id'] ?? ''}'.compareTo('${b.value['id'] ?? ''}');
    if (idCmp != 0) return idCmp;
    final int srcCmp =
        '${a.value['source'] ?? ''}'.compareTo('${b.value['source'] ?? ''}');
    if (srcCmp != 0) return srcCmp;
    return a.key.compareTo(b.key);
  });

  final List<Map<String, dynamic>> ordered = <Map<String, dynamic>>[
    for (final MapEntry<int, Map<String, dynamic>> e in indexed) e.value
  ];

  final List<Map<String, dynamic>> edges = <Map<String, dynamic>>[];
  String previousId = '';

  for (final Map<String, dynamic> event in ordered) {
    final String eventId = '${event['id'] ?? ''}';
    if (previousId.isNotEmpty) {
      edges.add(<String, dynamic>{
        'from': previousId,
        'to': eventId,
        'relation': 'stream_next',
      });
    }
    previousId = eventId;
  }

  return <String, dynamic>{
    'events': ordered,
    'edges': edges,
    'bounded': true,
  };
}
