// Port of core/workflows/workflow_state_engine.py

Map<String, dynamic> buildWorkflowState(
  Map<String, dynamic> plan, [
  Map<String, dynamic>? execution,
  int currentStep = 0,
]) {
  final Map<String, dynamic> exec = execution ?? <String, dynamic>{};
  final List<dynamic> executed = exec['executed'] is List
      ? List<dynamic>.from(exec['executed'] as List<dynamic>)
      : <dynamic>[];
  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];

  final List<dynamic> completedSteps = <dynamic>[];
  for (final dynamic itemRaw in executed) {
    final Map<String, dynamic> item = itemRaw is Map
        ? Map<String, dynamic>.from(itemRaw)
        : <String, dynamic>{};
    if (item['completed'] == true) {
      completedSteps.add(item['step_id']);
    }
  }

  return <String, dynamic>{
    'current_step': currentStep,
    'completed_steps': completedSteps,
    'retries': 0,
    'runtime_state': <String, dynamic>{
      'objective': plan['objective'] ?? '',
      'total_steps': steps.length,
    },
    'extraction_outputs': <dynamic>[],
    'semantic_checkpoints': <dynamic>[],
    'bounded': true,
  };
}
