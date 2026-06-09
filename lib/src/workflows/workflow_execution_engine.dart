// Port of core/workflows/workflow_execution_engine.py

Map<String, dynamic> executeWorkflowPlan(
  Map<String, dynamic> plan, {
  int tick = 0,
}) {
  final List<Map<String, dynamic>> executed = <Map<String, dynamic>>[];

  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];

  int index = 0;
  for (final dynamic stepRaw in steps.take(10000)) {
    final Map<String, dynamic> step = stepRaw is Map
        ? Map<String, dynamic>.from(stepRaw)
        : <String, dynamic>{};
    executed.add(<String, dynamic>{
      'step_id': '${step['id'] ?? 'step:$index'}',
      'action': '${step['action'] ?? ''}',
      'runtime': '${step['runtime'] ?? 'browser'}',
      'completed': true,
      'tick': tick + index,
      'replay_index': index,
    });
    index++;
  }

  return <String, dynamic>{
    'objective': plan['objective'] ?? '',
    'executed': executed,
    'completed_count': executed.length,
    'bounded': true,
  };
}
