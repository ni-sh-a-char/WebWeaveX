import 'dart:convert';

import '../crypto/kaalka_runtime.dart';
import '../determinism/dom_stabilization.dart';
import '../determinism/fingerprint.dart';
import '../graph/runtime_graph.dart';

String _graphHash(RuntimeGraph graph) {
  final n = normalizeRuntimeGraph(graph);
  return computeDeterministicHash(
    jsonEncode({
      'nodes': n.nodes.map((e) => e.toJson()).toList(),
      'edges': n.edges.map((e) => e.toJson()).toList()
    }),
  );
}

String? _domSnapshotHash(Map<String, dynamic> envelope) {
  final raw = envelope['dom_snapshot'] ??
      envelope['dom_html'] ??
      (envelope['browser_ir'] as Map?)?['dom_html'];
  if (raw is! String || raw.isEmpty) return null;
  return computeStableDomHash(raw);
}

RuntimeGraph _graphFromEnvelope(Map<String, dynamic> envelope) {
  final g = envelope['unified_runtime_graph'] ?? envelope['graph'];
  if (g is RuntimeGraph) return g;
  if (g is Map<String, dynamic>) {
    final nodes = (g['nodes'] as List? ?? [])
        .map((n) => RuntimeNode(
              id: (n as Map)['id'] as String?,
              type: n['type'] as String?,
              payload: n['payload'],
            ))
        .toList();
    final edges = (g['edges'] as List? ?? [])
        .map((e) => RuntimeEdge(
              source: (e as Map)['source'] as String?,
              target: e['target'] as String?,
              type: e['type'] as String?,
            ))
        .toList();
    return RuntimeGraph(nodes: nodes, edges: edges);
  }
  return RuntimeGraph(nodes: [], edges: []);
}

Map<String, dynamic> validateReplayEquivalence(
  Map<String, dynamic> original,
  Map<String, dynamic> replayed,
) {
  final origGraph = _graphFromEnvelope(original);
  final replayGraph = _graphFromEnvelope(replayed);
  final origFp = computeGlobalRuntimeFingerprint(original, origGraph);
  final replayFp = computeGlobalRuntimeFingerprint(replayed, replayGraph);
  final origDom = _domSnapshotHash(original);
  final replayDom = _domSnapshotHash(replayed);

  final checks = <Map<String, dynamic>>[
    {
      'name': 'graph_hash',
      'ok': _graphHash(origGraph) == _graphHash(replayGraph),
    },
    {
      'name': 'global_fingerprint',
      'ok': origFp == replayFp,
    },
    {
      'name': 'browser_identity',
      'ok': (original['browser_ir'] as Map?)?['runtime_identity'] ==
          (replayed['browser_ir'] as Map?)?['runtime_identity'],
    },
  ];

  if (origDom != null && replayDom != null) {
    checks.add({
      'name': 'dom_stabilized_hash',
      'ok': origDom == replayDom,
    });
  }

  checks.add({
    'name': 'semantic_fingerprint',
    'ok':
        origFp == replayFp && _graphHash(origGraph) == _graphHash(replayGraph),
  });

  final origMem = original['runtime_memory'];
  final replayMem = replayed['runtime_memory'];
  if (origMem is Map<String, dynamic> && replayMem is Map<String, dynamic>) {
    checks.add({
      'name': 'memory_stable_hash',
      'ok': origMem['stable_hash'] == replayMem['stable_hash'],
    });
  }

  return {
    'equivalent': checks.every((c) => c['ok'] == true),
    'checks': checks,
    'bounded': true,
  };
}
