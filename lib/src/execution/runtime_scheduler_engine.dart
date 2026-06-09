/// Port of core/execution/runtime_scheduler_engine.schedule_runtime_execution.
Map<String, dynamic> scheduleRuntimeExecution(
  List<Map<String, dynamic>> actions, {
  Map<String, int>? priorities,
  int cooldownTicks = 0,
  String workerId = 'worker:0',
  int tick = 0,
}) {
  final Map<String, int> prio = priorities ?? <String, int>{};
  final List<Map<String, dynamic>> scheduled = <Map<String, dynamic>>[];

  final List<Map<String, dynamic>> bounded =
      actions.length > 10000 ? actions.sublist(0, 10000) : actions;
  final int cooldown = cooldownTicks > 0 ? cooldownTicks : 0;

  for (int index = 0; index < bounded.length; index++) {
    final Map<String, dynamic> action = bounded[index];
    final String actionId = '${action['id'] ?? 'action:$index'}';
    final int priority = prio[actionId] ?? 0;
    scheduled.add(<String, dynamic>{
      'action': action,
      'priority': priority,
      'worker_id': workerId,
      'tick': tick + (index * cooldown),
      'retry': 0,
      'paced': true,
    });
  }

  scheduled.sort((Map<String, dynamic> a, Map<String, dynamic> b) {
    // key = (-priority, tick, str(action.id))
    final int p = (-(a['priority'] as int)).compareTo(-(b['priority'] as int));
    if (p != 0) return p;
    final int t = (a['tick'] as int).compareTo(b['tick'] as int);
    if (t != 0) return t;
    final String ia = '${(a['action'] as Map<String, dynamic>)['id'] ?? ''}';
    final String ib = '${(b['action'] as Map<String, dynamic>)['id'] ?? ''}';
    return ia.compareTo(ib);
  });

  return <String, dynamic>{
    'scheduled': scheduled,
    'worker_id': workerId,
    'cooldown_ticks': cooldownTicks,
    'deterministic': true,
    'bounded': true,
  };
}
