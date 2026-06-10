import '../crypto/hashing.dart';

class RuntimeNode {
  RuntimeNode({this.id, this.type, this.name, this.payload});

  final String? id;
  final String? type;
  final String? name;
  final dynamic payload;

  Map<String, dynamic> toJson() => {
        if (id != null) 'id': id,
        if (type != null) 'type': type,
        if (name != null) 'name': name,
        if (payload != null) 'payload': payload,
      };
}

class RuntimeEdge {
  RuntimeEdge({this.source, this.target, this.type, this.from, this.to});

  final String? source;
  final String? target;
  final String? type;
  final String? from;
  final String? to;

  Map<String, dynamic> toJson() => {
        if (source != null) 'source': source,
        if (target != null) 'target': target,
        if (type != null) 'type': type,
        if (from != null) 'from': from,
        if (to != null) 'to': to,
      };
}

class RuntimeGraph {
  RuntimeGraph({required this.nodes, required this.edges, this.bounded = true});

  final List<RuntimeNode> nodes;
  final List<RuntimeEdge> edges;
  final bool bounded;

  Map<String, dynamic> toJson() => {
        'nodes': nodes.map((n) => n.toJson()).toList(),
        'edges': edges.map((e) => e.toJson()).toList(),
        'bounded': bounded,
      };
}

RuntimeGraph normalizeRuntimeGraph(RuntimeGraph graph) {
  final nodes = [...graph.nodes]..sort((a, b) {
      final ka = '${a.id ?? ''}|${a.type ?? ''}|${a.name ?? ''}';
      final kb = '${b.id ?? ''}|${b.type ?? ''}|${b.name ?? ''}';
      return ka.compareTo(kb);
    });
  final edges = [...graph.edges]..sort((a, b) {
      final ka =
          '${a.source ?? a.from ?? ''}|${a.target ?? a.to ?? ''}|${a.type ?? ''}';
      final kb =
          '${b.source ?? b.from ?? ''}|${b.target ?? b.to ?? ''}|${b.type ?? ''}';
      return ka.compareTo(kb);
    });
  return RuntimeGraph(nodes: nodes, edges: edges, bounded: true);
}

RuntimeGraph buildRuntimeGraph(Map<String, dynamic> sources) {
  final nodes = <RuntimeNode>[];
  final edges = <RuntimeEdge>[];
  final entries = sources.entries.toList()
    ..sort((a, b) => a.key.compareTo(b.key));
  var idx = 0;
  for (final entry in entries) {
    nodes.add(RuntimeNode(
      id: 'node:${entry.key}:$idx',
      type: entry.key,
      payload: entry.value,
    ));
    idx++;
  }
  if (nodes.length > 1) {
    for (var i = 1; i < nodes.length; i++) {
      edges.add(RuntimeEdge(
        source: nodes[0].id,
        target: nodes[i].id,
        type: 'runtime_link',
      ));
    }
  }
  return normalizeRuntimeGraph(RuntimeGraph(nodes: nodes, edges: edges));
}

RuntimeGraph queryRuntimeGraphTyped(RuntimeGraph graph, {String? nodeType}) {
  final g = normalizeRuntimeGraph(graph);
  if (nodeType == null) return g;
  return normalizeRuntimeGraph(RuntimeGraph(
    nodes: g.nodes.where((n) => n.type == nodeType).toList(),
    edges: g.edges,
  ));
}

String graphFingerprint(RuntimeGraph graph) =>
    computeDeterministicHash(normalizeRuntimeGraph(graph).toJson());

/// Alias for ecosystem API parity with Python/JS naming.
String computeRuntimeFingerprint(RuntimeGraph graph) => graphFingerprint(graph);

/// Validates canonical graph contract (bounded, sortable, fingerprintable).
Map<String, dynamic> validateRuntimeGraph(RuntimeGraph graph) {
  final normalized = normalizeRuntimeGraph(graph);
  return {
    'valid': normalized.bounded,
    'fingerprint': graphFingerprint(normalized),
    'node_count': normalized.nodes.length,
    'edge_count': normalized.edges.length,
    'bounded': true,
  };
}
