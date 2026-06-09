// Port of core/workflows/workflow_navigation_engine.py

const Map<String, String> runtimeNavigators = <String, String>{
  'browser': 'browser_navigation',
  'electron': 'electron_navigation',
  'desktop': 'modal_traversal',
  'terminal': 'terminal_progression',
  'native': 'vm_runtime_transition',
  'remote': 'remote_runtime_traversal',
  'application': 'application_navigation',
  'repository': 'repository_navigation',
};

Map<String, dynamic> navigateRuntimeWorkflow(
  Map<String, dynamic> plan, {
  int tick = 0,
}) {
  final List<Map<String, dynamic>> navigations = <Map<String, dynamic>>[];
  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];

  int index = 0;
  for (final dynamic stepRaw in steps.take(10000)) {
    final Map<String, dynamic> step = stepRaw is Map
        ? Map<String, dynamic>.from(stepRaw)
        : <String, dynamic>{};
    final String runtime = '${step['runtime'] ?? 'browser'}';
    navigations.add(<String, dynamic>{
      'step_id': '${step['id'] ?? 'step:$index'}',
      'runtime': runtime,
      'navigator': runtimeNavigators[runtime] ?? 'browser_navigation',
      'action': '${step['action'] ?? ''}',
      'tick': tick + index,
    });
    index++;
  }

  return <String, dynamic>{
    'navigations': navigations,
    'count': navigations.length,
    'bounded': true,
  };
}
