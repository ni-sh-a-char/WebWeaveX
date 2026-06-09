// Port of core/workflows/workflow_dependency_engine.py

Map<String, dynamic> buildWorkflowDependencies(
  Map<String, dynamic> plan,
) {
  final List<Map<String, dynamic>> ordering = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> prerequisites = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> runtimeDeps = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> chains = <Map<String, dynamic>>[];

  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];
  final List<dynamic> bounded = steps.take(10000).toList();

  for (int index = 0; index < bounded.length; index++) {
    final dynamic stepRaw = bounded[index];
    final Map<String, dynamic> step = stepRaw is Map
        ? Map<String, dynamic>.from(stepRaw)
        : <String, dynamic>{};
    final String dependsOn = '${step['depends_on'] ?? ''}';
    if (dependsOn.isNotEmpty) {
      ordering.add(<String, dynamic>{
        'step': '${step['id'] ?? ''}',
        'depends_on': dependsOn,
      });
      prerequisites.add(<String, dynamic>{
        'step': '${step['id'] ?? ''}',
        'requires': dependsOn,
      });
    }

    if (index > 0) {
      final dynamic prevRaw = bounded[index - 1];
      final Map<String, dynamic> prev = prevRaw is Map
          ? Map<String, dynamic>.from(prevRaw)
          : <String, dynamic>{};
      final String prevRuntime = '${prev['runtime'] ?? ''}';
      final String currRuntime = '${step['runtime'] ?? ''}';
      if (prevRuntime != currRuntime) {
        runtimeDeps.add(<String, dynamic>{
          'from': prevRuntime,
          'to': currRuntime,
        });
      }
    }

    chains.add(<String, dynamic>{
      'step': '${step['id'] ?? ''}',
      'action': '${step['action'] ?? ''}',
    });
  }

  return <String, dynamic>{
    'execution_ordering': ordering,
    'semantic_prerequisites': prerequisites,
    'runtime_dependencies': runtimeDeps,
    'extraction_chains': chains,
    'bounded': true,
  };
}
