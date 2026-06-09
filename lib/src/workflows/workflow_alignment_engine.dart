// Port of core/workflows/workflow_alignment_engine.py

Map<String, dynamic> alignWorkflowRuntime(
  Map<String, dynamic> plan,
  Map<String, dynamic> state,
  Map<String, dynamic> execution,
) {
  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];
  final int completedCount = execution['completed_count'] is int
      ? execution['completed_count'] as int
      : 0;

  return <String, dynamic>{
    'objective': plan['objective'] ?? '',
    'steps_aligned': steps.length == completedCount,
    'state_step': state['current_step'] ?? 0,
    'aligned': true,
    'bounded': true,
  };
}
