/// Native Dart port of the deterministic topology reasoning pipeline
/// (Python `core/graph/topology_*`, `core/graph/graph_entropy_engine.py`,
/// `core/graph/semantic_cycle_analysis_engine.py`,
/// `core/reasoning/topology_reasoning_engine.py`).
library;

List<dynamic> _asList(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

/// Port of `core.graph.topology_proof_engine.prove_topology`.
Map<String, dynamic> proveTopology(Map<String, dynamic> graph) {
  final edges = _asList(graph['edges']);
  final degree = <String, int>{};
  for (final e in edges) {
    if (e is! Map) continue;
    final f = e['from'];
    final t = e['to'];
    if (f != null && f != '' && f != false) {
      degree['$f'] = (degree['$f'] ?? 0) + 1;
    }
    if (t != null && t != '' && t != false) {
      degree['$t'] = (degree['$t'] ?? 0) + 1;
    }
  }
  final hubs = degree.entries
      .where((kv) => kv.value >= 3)
      .map((kv) => kv.key)
      .toList()
    ..sort();
  final maxDeg =
      degree.isEmpty ? 0 : degree.values.reduce((a, b) => a > b ? a : b);
  return <String, dynamic>{
    'proved': true,
    'max_degree': maxDeg,
    'hubs': hubs.take(20).toList(),
    'edge_count': edges.length,
    'deterministic_inputs': <String>[
      'max_degree=$maxDeg',
      'hubs=${hubs.length}',
    ],
  };
}

/// Port of `core.graph.graph_entropy_engine.model_graph_entropy`.
Map<String, dynamic> modelGraphEntropy(Map<String, dynamic> graph) {
  final nodes = _asList(graph['nodes']);
  final edges = _asList(graph['edges']);
  final kinds = <dynamic>{};
  for (final n in nodes) {
    if (n is Map) kinds.add(n['kind']);
  }
  final entropy = _round(
      _min(
          1.0, nodes.length * 0.02 + edges.length * 0.03 + kinds.length * 0.05),
      3);
  return <String, dynamic>{
    'entropy': entropy,
    'kind_diversity': kinds.length,
    'deterministic_inputs': <String>['H=$entropy'],
  };
}

/// Port of `core.graph.topology_reasoning_engine.reason_topology`.
Map<String, dynamic> reasonTopology(Map<String, dynamic> graph) {
  final proof = proveTopology(graph);
  final entropy = modelGraphEntropy(graph);
  final entropyVal = entropy['entropy'] ?? 0;
  return <String, dynamic>{
    ...proof,
    'entropy': entropyVal,
    'evidence': <String>['graph:topology_proof'],
    'justification': <String, dynamic>{
      'hubs': proof['hubs'] ?? <dynamic>[],
      'max_degree': proof['max_degree'] ?? 0,
    },
    'uncertainty': <String, dynamic>{'visible': (entropyVal as num) > 0},
    'deterministic_inputs': proof['deterministic_inputs'] ?? <dynamic>[],
  };
}

/// Port of `core.graph.semantic_cycle_analysis_engine.detect_cycles`.
Map<String, dynamic> detectCycles(Map<String, dynamic> graph,
    {int maxDepth = 50}) {
  final edges = _asList(graph['edges']);
  final adj = <String, List<String>>{};
  for (final e in edges) {
    if (e is Map &&
        e['from'] != null &&
        e['from'] != '' &&
        e['to'] != null &&
        e['to'] != '') {
      adj.putIfAbsent('${e['from']}', () => <String>[]).add('${e['to']}');
    }
  }
  final cycles = <List<String>>[];
  final visited = <String>{};
  final stack = <String>{};
  final path = <String>[];

  void dfs(String n, int depth) {
    if (depth > maxDepth) return;
    if (stack.contains(n)) {
      if (path.contains(n)) {
        final i = path.indexOf(n);
        cycles.add(<String>[...path.sublist(i), n]);
      }
      return;
    }
    if (visited.contains(n)) return;
    visited.add(n);
    stack.add(n);
    path.add(n);
    for (final nb in adj[n] ?? <String>[]) {
      dfs(nb, depth + 1);
    }
    path.removeLast();
    stack.remove(n);
  }

  final starts = adj.keys.take(100).toList();
  for (final start in starts) {
    dfs(start, 0);
  }
  return <String, dynamic>{
    'cycles': cycles.take(20).toList(),
    'cycle_count': cycles.length,
    'bounded': maxDepth,
    'contradiction_pressure': _min(1.0, cycles.length * 0.2),
  };
}

/// Port of `core.reasoning.topology_reasoning_engine.reason_topology_semantic`.
Map<String, dynamic> reasonTopologySemantic(Map<String, dynamic> graph) {
  final topo = reasonTopology(graph);
  final cycles = detectCycles(graph);
  return <String, dynamic>{
    ...topo,
    'cycles': cycles,
    'contradiction_pressure': cycles['contradiction_pressure'] ?? 0,
    'explainable': true,
  };
}

num _min(num a, num b) => a < b ? a : b;

num _round(num value, int digits) {
  final factor = _pow10(digits);
  final scaled = value * factor;
  final floor = scaled.floorToDouble();
  final diff = scaled - floor;
  double rounded;
  if (diff > 0.5) {
    rounded = floor + 1;
  } else if (diff < 0.5) {
    rounded = floor;
  } else {
    rounded = (floor % 2 == 0) ? floor : floor + 1;
  }
  return rounded / factor;
}

double _pow10(int n) {
  var r = 1.0;
  for (var i = 0; i < n; i++) {
    r *= 10;
  }
  return r;
}
