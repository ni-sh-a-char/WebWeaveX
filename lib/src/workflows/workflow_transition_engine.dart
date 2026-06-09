// Port of core/workflows/workflow_transition_engine.py

List<Map<String, dynamic>> buildWorkflowTransitions(
  Map<String, dynamic> execution,
) {
  final List<Map<String, dynamic>> transitions = <Map<String, dynamic>>[];
  final List<dynamic> executed = execution['executed'] is List
      ? List<dynamic>.from(execution['executed'] as List<dynamic>)
      : <dynamic>[];

  for (int index = 1; index < executed.length; index++) {
    final dynamic prevRaw = executed[index - 1];
    final dynamic currRaw = executed[index];
    final Map<String, dynamic> prev = prevRaw is Map
        ? Map<String, dynamic>.from(prevRaw)
        : <String, dynamic>{};
    final Map<String, dynamic> curr = currRaw is Map
        ? Map<String, dynamic>.from(currRaw)
        : <String, dynamic>{};
    transitions.add(<String, dynamic>{
      'from': '${prev['step_id'] ?? ''}',
      'to': '${curr['step_id'] ?? ''}',
      'relation': 'transitions',
    });
  }

  return transitions;
}
