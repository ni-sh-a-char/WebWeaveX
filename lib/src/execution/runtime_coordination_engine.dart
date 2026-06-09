/// Port of core/execution/runtime_coordination_engine.coordinate_runtime_execution.
int _asInt(dynamic v, int fallback) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? fallback;
  return fallback;
}

Map<String, dynamic> coordinateRuntimeExecution(
  List<Map<String, dynamic>> queue,
  Map<String, dynamic> federation, {
  Map<String, dynamic>? workflow,
  Map<String, dynamic>? syncState,
}) {
  final List<Map<String, dynamic>> routes = <Map<String, dynamic>>[
    ...((federation['execution_routes'] as List<dynamic>?) ?? <dynamic>[])
        .cast<Map<String, dynamic>>()
  ];
  final List<Map<String, dynamic>> orderedQueue = <Map<String, dynamic>>[
    ...queue
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) {
      final int p =
          (-_asInt(a['priority'], 0)).compareTo(-_asInt(b['priority'], 0));
      if (p != 0) return p;
      return _asInt(a['order'], 0).compareTo(_asInt(b['order'], 0));
    });

  final List<dynamic> rollbackOrder = routes.reversed
      .map((Map<String, dynamic> route) => route['worker_id'])
      .toList();

  return <String, dynamic>{
    'queue_size': orderedQueue.length,
    'routes': routes,
    'workflow_bound': workflow != null && workflow.isNotEmpty,
    'sync_bound': syncState != null && syncState.isNotEmpty,
    'rollback_order': rollbackOrder,
    'coordinated': true,
    'deterministic': true,
    'bounded': true,
  };
}
