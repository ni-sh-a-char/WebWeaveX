// Port of core/workflows/workflow_scheduler_engine.py

Map<String, dynamic> scheduleWorkflowExecution(
  List<Map<String, dynamic>> plans, {
  int tick = 0,
}) {
  int toIntValue(dynamic p) {
    if (p is int) {
      return p;
    }
    if (p is num) {
      return p.toInt();
    }
    return int.tryParse('$p') ?? 0;
  }

  // Sort key mirrors Python: priority, fallback objective_priority, then 0.
  int sortPriorityOf(Map<String, dynamic> item) =>
      toIntValue(item['priority'] ?? item['objective_priority'] ?? 0);

  // Output priority mirrors Python: priority only, fallback 0.
  int outPriorityOf(Map<String, dynamic> item) =>
      toIntValue(item['priority'] ?? 0);

  final List<Map<String, dynamic>> ordered =
      List<Map<String, dynamic>>.from(plans);
  ordered.sort((Map<String, dynamic> a, Map<String, dynamic> b) {
    final int pa = sortPriorityOf(a);
    final int pb = sortPriorityOf(b);
    if (pa != pb) {
      return pa.compareTo(pb);
    }
    return '${a['objective'] ?? ''}'.compareTo('${b['objective'] ?? ''}');
  });

  final List<Map<String, dynamic>> schedule = <Map<String, dynamic>>[];
  int index = 0;
  for (final Map<String, dynamic> plan in ordered.take(10000)) {
    schedule.add(<String, dynamic>{
      'objective': plan['objective'] ?? '',
      'priority': outPriorityOf(plan),
      'tick': tick + index,
      'pacing': index,
      'retries': 0,
      'distributed_order': index,
    });
    index++;
  }

  return <String, dynamic>{
    'schedule': schedule,
    'count': schedule.length,
    'bounded': true,
  };
}
