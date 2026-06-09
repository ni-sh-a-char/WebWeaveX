/// Port of core/execution/runtime_replay_engine.replay_runtime_execution.
int _asInt(dynamic v, int fallback) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? fallback;
  return fallback;
}

Map<String, dynamic> replayRuntimeExecution(
  List<Map<String, dynamic>> actions, {
  List<Map<String, dynamic>>? transactions,
  List<Map<String, dynamic>>? mutations,
  int tick = 0,
}) {
  final List<Map<String, dynamic>> orderedActions = <Map<String, dynamic>>[
    ...actions
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));

  final List<Map<String, dynamic>> orderedTx = <Map<String, dynamic>>[
    ...(transactions ?? <Map<String, dynamic>>[])
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      '${a['transaction_id'] ?? ''}'.compareTo('${b['transaction_id'] ?? ''}'));

  final List<Map<String, dynamic>> orderedMutations = <Map<String, dynamic>>[
    ...(mutations ?? <Map<String, dynamic>>[])
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) {
      final int t = _asInt(a['tick'], 0).compareTo(_asInt(b['tick'], 0));
      if (t != 0) return t;
      return _asInt(a['ordered_index'], 0)
          .compareTo(_asInt(b['ordered_index'], 0));
    });

  return <String, dynamic>{
    'actions': orderedActions,
    'transactions': orderedTx,
    'mutations': orderedMutations,
    'tick': tick,
    'replayed': true,
    'identical': true,
    'bounded': true,
  };
}
