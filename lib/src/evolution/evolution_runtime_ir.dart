import '_sort_util.dart';

/// Port of core/ir/evolution_runtime_ir.py
Map<String, dynamic> compileEvolutionRuntimeIr(Map<String, dynamic> evolution) {
  return <String, dynamic>{
    'ir': 'evolution_runtime',
    'evolution': evolution['evolution'] ?? <String, dynamic>{},
    'selector': evolution['selector'] ?? <String, dynamic>{},
    'workflow': evolution['workflow'] ?? <String, dynamic>{},
    'semantic': evolution['semantic'] ?? <String, dynamic>{},
    'topology': evolution['topology'] ?? <String, dynamic>{},
    'strategy': evolution['strategy'] ?? <String, dynamic>{},
    'repairs': evolution['repairs'] ?? <String, dynamic>{},
    'optimization': evolution['optimization'] ?? <String, dynamic>{},
    'patterns': evolution['patterns'] ?? <String, dynamic>{},
    'lineage': evolution['lineage'] ?? <dynamic>[],
    'graph': evolution['graph'] ?? <String, dynamic>{},
    'policy': evolution['policy'] ?? <String, dynamic>{},
    'bounded': true,
  };
}

Map<String, dynamic> evolutionRuntimeIrToGraph(
  Map<String, dynamic> evolutionIr,
) {
  final graph = (evolutionIr['graph'] is Map)
      ? Map<String, dynamic>.from(evolutionIr['graph'] as Map)
      : <String, dynamic>{};
  var nodes = List<dynamic>.from((graph['nodes'] as List?) ?? <dynamic>[]);
  final edges = List<dynamic>.from((graph['edges'] as List?) ?? <dynamic>[]);

  if (nodes.isEmpty) {
    nodes = <dynamic>[
      <String, dynamic>{'id': 'evolution:root', 'type': 'evolution'},
    ];
  }

  return <String, dynamic>{
    'ir': 'evolution_runtime_graph',
    'nodes': stableSorted<dynamic>(
      nodes,
      (a, b) => pyStrCompare(
          '${(a as Map)['id'] ?? ''}', '${(b as Map)['id'] ?? ''}'),
    ),
    'edges': edges,
    'bounded': true,
  };
}
