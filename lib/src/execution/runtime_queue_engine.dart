/// Port of core/execution/runtime_queue_engine.
const int maxQueue = 100000;

int _asInt(dynamic v, int fallback) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? fallback;
  return fallback;
}

int _queueCompare(Map<String, dynamic> a, Map<String, dynamic> b) {
  // key = (-priority, order)
  final int pa = -_asInt(a['priority'], 0);
  final int pb = -_asInt(b['priority'], 0);
  final int c = pa.compareTo(pb);
  if (c != 0) return c;
  return _asInt(a['order'], 0).compareTo(_asInt(b['order'], 0));
}

Map<String, dynamic> enqueueRuntimeAction(
  List<Map<String, dynamic>> queue,
  Map<String, dynamic> action, {
  int priority = 0,
}) {
  final List<Map<String, dynamic>> updated = <Map<String, dynamic>>[...queue];
  updated.add(<String, dynamic>{
    'action': action,
    'priority': priority,
    'order': updated.length,
  });
  final List<Map<String, dynamic>> sorted = <Map<String, dynamic>>[...updated]
    ..sort(_queueCompare);
  final List<Map<String, dynamic>> bounded =
      sorted.length > maxQueue ? sorted.sublist(0, maxQueue) : sorted;
  return <String, dynamic>{
    'queue': bounded,
    'size': bounded.length,
    'bounded': true,
  };
}

Map<String, dynamic> dequeueRuntimeAction(List<Map<String, dynamic>> queue) {
  if (queue.isEmpty) {
    return <String, dynamic>{
      'queue': <Map<String, dynamic>>[],
      'action': null,
      'bounded': true,
    };
  }
  final List<Map<String, dynamic>> ordered = <Map<String, dynamic>>[...queue]
    ..sort(_queueCompare);
  final Map<String, dynamic> head = ordered.first;
  final List<Map<String, dynamic>> rest = ordered.sublist(1);
  return <String, dynamic>{
    'queue': rest,
    'action': head['action'],
    'bounded': true,
  };
}
