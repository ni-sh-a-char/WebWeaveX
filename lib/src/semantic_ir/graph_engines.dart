/// Phase A.2 (core.graph leaves) of the Category-A semantic-IR port.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.graph.graph_entropy_engine.model_graph_entropy.
Map<String, dynamic> modelGraphEntropy(Map<dynamic, dynamic> graph) {
  dynamic nodes = pyGet(graph, 'nodes', <dynamic>[]);
  if (!pyTruthy(nodes)) nodes = <dynamic>[];
  dynamic edges = pyGet(graph, 'edges', <dynamic>[]);
  if (!pyTruthy(edges)) edges = <dynamic>[];
  // Python: {n.get("kind") for n in nodes if isinstance(n, dict)} — a missing
  // "kind" contributes None to the set.
  final kinds = <Object?>{};
  for (final n in nodes as List) {
    if (n is Map) kinds.add(pyGet(n, 'kind', null));
  }
  final entropy = pythonRound(
      math.min(
          1.0,
          nodes.length * 0.02 +
              (edges as List).length * 0.03 +
              kinds.length * 0.05),
      3);
  return <String, dynamic>{
    'entropy': entropy,
    'kind_diversity': kinds.length,
    'deterministic_inputs': <String>['H=${pyFloatStr(entropy)}'],
  };
}

/// Port of core.graph.semantic_cycle_analysis_engine.detect_cycles.
Map<String, dynamic> detectCycles(Map<dynamic, dynamic> graph,
    [int maxDepth = 50]) {
  dynamic edges = pyGet(graph, 'edges', <dynamic>[]);
  if (!pyTruthy(edges)) edges = <dynamic>[];
  final adj = <String, List<String>>{};
  for (final e in edges as List) {
    if (e is Map &&
        pyTruthy(pyGet(e, 'from', null)) &&
        pyTruthy(pyGet(e, 'to', null))) {
      adj.putIfAbsent(pyToStr(e['from']), () => <String>[])
          .add(pyToStr(e['to']));
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
    for (final nb in adj[n] ?? const <String>[]) {
      dfs(nb, depth + 1);
    }
    path.removeLast();
    stack.remove(n);
  }

  for (final start in adj.keys.toList().take(100)) {
    dfs(start, 0);
  }
  return <String, dynamic>{
    'cycles': cycles.take(20).toList(),
    'cycle_count': cycles.length,
    'bounded': maxDepth,
    'contradiction_pressure': math.min(1.0, cycles.length * 0.2),
  };
}

/// Port of core.graph.topology_proof_engine.prove_topology.
Map<String, dynamic> proveTopology(Map<dynamic, dynamic> graph) {
  dynamic edges = pyGet(graph, 'edges', <dynamic>[]);
  if (!pyTruthy(edges)) edges = <dynamic>[];
  final degree = <String, int>{};
  for (final e in edges as List) {
    if (e is! Map) continue;
    final f = pyGet(e, 'from', null);
    final t = pyGet(e, 'to', null);
    if (pyTruthy(f)) {
      final k = pyToStr(f);
      degree[k] = (degree[k] ?? 0) + 1;
    }
    if (pyTruthy(t)) {
      final k = pyToStr(t);
      degree[k] = (degree[k] ?? 0) + 1;
    }
  }
  final hubs = <String>[
    for (final entry in degree.entries)
      if (entry.value >= 3) entry.key
  ]..sort();
  final maxDeg = degree.isEmpty ? 0 : degree.values.reduce(math.max);
  return <String, dynamic>{
    'proved': true,
    'max_degree': maxDeg,
    'hubs': hubs.take(20).toList(),
    'edge_count': edges.length,
    'deterministic_inputs': <String>[
      'max_degree=$maxDeg',
      'hubs=${hubs.length}'
    ],
  };
}
