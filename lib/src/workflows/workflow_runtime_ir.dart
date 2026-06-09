// Port of core/ir/workflow_runtime_ir.py

Map<String, dynamic> compileWorkflowRuntimeIr(
  Map<String, dynamic> workflow,
) {
  return <String, dynamic>{
    'ir': 'workflow_runtime',
    'objective': workflow['objective'] ?? <String, dynamic>{},
    'plan': workflow['plan'] ?? <String, dynamic>{},
    'execution': workflow['execution'] ?? <String, dynamic>{},
    'state': workflow['state'] ?? <String, dynamic>{},
    'workflow_graph': workflow['workflow_graph'] ?? <String, dynamic>{},
    'dependencies': workflow['dependencies'] ?? <String, dynamic>{},
    'federation': workflow['federation'] ?? <String, dynamic>{},
    'semantic_alignment': workflow['semantic_alignment'] ?? <String, dynamic>{},
    'recovery': workflow['recovery'] ?? <String, dynamic>{},
    'bounded': true,
  };
}

Map<String, dynamic> workflowRuntimeIrToGraph(
  Map<String, dynamic> workflowIr,
) {
  final dynamic graphRaw = workflowIr['workflow_graph'];
  final Map<String, dynamic> graph = graphRaw is Map
      ? Map<String, dynamic>.from(graphRaw)
      : <String, dynamic>{};
  List<dynamic> nodes = graph['nodes'] is List
      ? List<dynamic>.from(graph['nodes'] as List<dynamic>)
      : <dynamic>[];
  final List<dynamic> edges = graph['edges'] is List
      ? List<dynamic>.from(graph['edges'] as List<dynamic>)
      : <dynamic>[];

  if (nodes.isEmpty) {
    nodes = <dynamic>[
      <String, dynamic>{'id': 'workflow:root', 'type': 'workflow'}
    ];
  }

  final List<dynamic> sortedNodes = List<dynamic>.from(nodes);
  sortedNodes.sort((dynamic a, dynamic b) {
    final String ida = a is Map ? '${a['id'] ?? ''}' : '';
    final String idb = b is Map ? '${b['id'] ?? ''}' : '';
    return ida.compareTo(idb);
  });

  return <String, dynamic>{
    'ir': 'workflow_runtime_graph',
    'nodes': sortedNodes,
    'edges': edges,
    'bounded': true,
  };
}
