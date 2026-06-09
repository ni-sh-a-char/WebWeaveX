import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_evolution_graph_engine.py
Map<String, dynamic> buildRuntimeEvolutionGraph(
  Map<String, dynamic> evolution,
  Map<String, dynamic> repairs,
  Map<String, dynamic> optimization,
) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];

  final evolutionId = '${evolution['evolution_id'] ?? 'evolution:root'}';
  nodes.add(<String, dynamic>{'id': evolutionId, 'type': 'evolution'});

  final mutations = (evolution['mutations'] as List?) ?? <dynamic>[];
  for (final raw in mutations.take(5000)) {
    final mutation = raw as Map;
    final nodeId = 'mutation:${mutation['kind']}:${mutation['target']}';
    nodes.add(<String, dynamic>{'id': nodeId, 'type': 'mutation'});
    edges.add(<String, dynamic>{
      'from': evolutionId,
      'to': nodeId,
      'relation': 'evolves',
    });
  }

  final repairList = (repairs['repairs'] as List?) ?? <dynamic>[];
  for (final raw in repairList.take(5000)) {
    final repair = raw as Map;
    final nodeId = "repair:${repair['action'] ?? ''}";
    nodes.add(<String, dynamic>{'id': nodeId, 'type': 'repair'});
    edges.add(<String, dynamic>{
      'from': nodeId,
      'to': evolutionId,
      'relation': 'repairs',
    });
  }

  const optId = 'optimization:root';
  nodes.add(<String, dynamic>{'id': optId, 'type': 'optimization'});
  edges.add(<String, dynamic>{
    'from': optId,
    'to': evolutionId,
    'relation': 'optimizes',
  });

  edges.add(<String, dynamic>{
    'from': evolutionId,
    'to': evolutionId,
    'relation': 'converges',
  });

  return <String, dynamic>{
    'nodes': stableSorted<Map<String, dynamic>>(
      nodes,
      (a, b) => pyStrCompare('${a['id']}', '${b['id']}'),
    ),
    'edges': stableSorted<Map<String, dynamic>>(edges, (a, b) {
      var c = pyStrCompare('${a['from'] ?? ''}', '${b['from'] ?? ''}');
      if (c != 0) return c;
      c = pyStrCompare('${a['to'] ?? ''}', '${b['to'] ?? ''}');
      if (c != 0) return c;
      return pyStrCompare('${a['relation'] ?? ''}', '${b['relation'] ?? ''}');
    }),
    'bounded': true,
  };
}
