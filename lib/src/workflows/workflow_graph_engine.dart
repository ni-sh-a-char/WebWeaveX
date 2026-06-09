// Port of core/workflows/workflow_graph_engine.py

Map<String, dynamic> buildWorkflowGraph(
  Map<String, dynamic> objective,
  Map<String, dynamic> plan,
  Map<String, dynamic> state,
  Map<String, dynamic> execution,
  List<Map<String, dynamic>> transitions,
) {
  final List<Map<String, dynamic>> nodes = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> edges = <Map<String, dynamic>>[];

  final String objName = '${objective['objective'] ?? 'objective'}';
  nodes.add(<String, dynamic>{'id': 'objective:$objName', 'type': 'objective'});

  final List<dynamic> steps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];
  for (final dynamic stepRaw in steps.take(10000)) {
    final Map<String, dynamic> step = stepRaw is Map
        ? Map<String, dynamic>.from(stepRaw)
        : <String, dynamic>{};
    final String stepId = '${step['id'] ?? ''}';
    nodes.add(<String, dynamic>{
      'id': stepId,
      'type': 'step',
      'runtime': '${step['runtime'] ?? ''}',
    });
    final String dependsOn = '${step['depends_on'] ?? ''}';
    if (dependsOn.isNotEmpty) {
      edges.add(<String, dynamic>{
        'from': dependsOn,
        'to': stepId,
        'relation': 'depends_on',
      });
    }
    edges.add(<String, dynamic>{
      'from': 'objective:$objName',
      'to': stepId,
      'relation': 'executes',
    });
  }

  for (final Map<String, dynamic> transition in transitions.take(10000)) {
    edges.add(<String, dynamic>{
      'from': '${transition['from'] ?? ''}',
      'to': '${transition['to'] ?? ''}',
      'relation': 'transitions',
    });
  }

  final int retries = state['retries'] is int ? state['retries'] as int : 0;
  if (retries > 0) {
    nodes.add(
        <String, dynamic>{'id': 'checkpoint:recovery', 'type': 'checkpoint'});
    edges.add(<String, dynamic>{
      'from': 'checkpoint:recovery',
      'to': 'objective:$objName',
      'relation': 'recovers',
    });
  }

  nodes.add(<String, dynamic>{
    'id': 'semantic:state',
    'type': 'semantic_state',
  });

  nodes.sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      '${a['id']}'.compareTo('${b['id']}'));
  edges.sort((Map<String, dynamic> a, Map<String, dynamic> b) {
    final int c1 = '${a['from'] ?? ''}'.compareTo('${b['from'] ?? ''}');
    if (c1 != 0) {
      return c1;
    }
    final int c2 = '${a['to'] ?? ''}'.compareTo('${b['to'] ?? ''}');
    if (c2 != 0) {
      return c2;
    }
    return '${a['relation'] ?? ''}'.compareTo('${b['relation'] ?? ''}');
  });

  return <String, dynamic>{
    'nodes': nodes,
    'edges': edges,
    'bounded': true,
  };
}
