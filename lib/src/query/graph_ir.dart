/// Native Dart port of the deterministic graph-consistency / semantic-graph IR
/// pipeline (Python `core/graph/*` + `core/ir/semantic_graph_ir.py`).
///
/// Parity proven against `core.crypto.kaalka_runtime_engine
/// .compute_deterministic_hash` (see test/parity/query_parity_test.dart).
library;

List<dynamic> _asList(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

/// Port of `core.graph.graph_invariant_engine.check_graph_invariants`.
Map<String, dynamic> checkGraphInvariants(Map<String, dynamic> graph) {
  final nodes = _asList(graph['nodes']);
  final edges = _asList(graph['edges']);
  final nodeIds = <dynamic>{};
  for (final n in nodes) {
    if (n is Map && n['id'] != null && n['id'] != '') {
      nodeIds.add(n['id']);
    }
  }
  final violations = <Map<String, String>>[];
  for (final e in edges) {
    if (e is! Map) continue;
    if (e.containsKey('type')) {
      violations.add(<String, String>{
        'rule': 'no_edge_type',
        'edge': '${e['from']}',
      });
    }
    if (!nodeIds.contains(e['from']) || !nodeIds.contains(e['to'])) {
      if (nodeIds.isNotEmpty) {
        violations.add(<String, String>{
          'rule': 'dangling_edge',
          'from': '${e['from']}',
          'to': '${e['to']}',
        });
      }
    }
  }
  return <String, dynamic>{
    'valid': violations.isEmpty,
    'violations': violations,
    'node_count': nodes.length,
    'edge_count': edges.length,
    'deterministic_inputs': <String>['violations=${violations.length}'],
  };
}

/// Port of `core.graph.semantic_edge_validation_engine.validate_semantic_edge`.
Map<String, dynamic> validateSemanticEdge(Map<String, dynamic> edge) {
  if (edge.containsKey('type')) {
    return <String, dynamic>{'valid': false, 'reason': 'forbidden_type_field'};
  }
  final from = edge['from'];
  final to = edge['to'];
  if (from == null || from == '' || to == null || to == '') {
    return <String, dynamic>{'valid': false, 'reason': 'missing_endpoints'};
  }
  var ev = edge['evidence'] ?? <dynamic>[];
  if (ev is String) {
    ev = <dynamic>[ev];
  }
  final evList = _asList(ev);
  return <String, dynamic>{
    'valid': evList.isNotEmpty,
    'evidence_count': evList.length,
    'grounding': edge['grounding'] ?? <String, dynamic>{},
    'uncertainty': edge['uncertainty'] ?? <String, dynamic>{},
    'justification': edge['justification'] ?? <String, dynamic>{},
  };
}

/// Port of `core.graph.semantic_graph_validator.validate_semantic_graph`.
Map<String, dynamic> validateSemanticGraph(Map<String, dynamic> graph) {
  final inv = checkGraphInvariants(graph);
  final edgeResults = <Map<String, dynamic>>[];
  for (final e in _asList(graph['edges'])) {
    if (e is Map) {
      edgeResults.add(validateSemanticEdge(Map<String, dynamic>.from(e)));
    }
  }
  final invalid = <int>[];
  for (var i = 0; i < edgeResults.length; i++) {
    if (edgeResults[i]['valid'] != true) {
      invalid.add(i);
    }
  }
  return <String, dynamic>{
    'valid': (inv['valid'] == true) && invalid.isEmpty,
    'invariants': inv,
    'invalid_edges': invalid,
    'edge_count': edgeResults.length,
    'deterministic_inputs': inv['deterministic_inputs'] ?? <String>[],
  };
}

/// Port of `core.graph.graph_consistency_engine.assess_graph_consistency`.
Map<String, dynamic> assessGraphConsistency(Map<String, dynamic> graph) {
  final inv = checkGraphInvariants(graph);
  return <String, dynamic>{
    'consistent': inv['valid'],
    'invariants': inv,
    'deterministic_inputs': inv['deterministic_inputs'],
  };
}

/// Port of `core.graph.graph_consistency_prover.prove_graph_consistency`.
Map<String, dynamic> proveGraphConsistency(Map<String, dynamic> graph) {
  final validation = validateSemanticGraph(graph);
  final consistency = assessGraphConsistency(graph);
  final proved =
      (validation['valid'] == true) && (consistency['consistent'] == true);
  return <String, dynamic>{
    'proved': proved,
    'validation': validation,
    'consistency': consistency,
    'deterministic_inputs': validation['deterministic_inputs'] ?? <String>[],
  };
}

/// Port of `core.ir.semantic_graph_ir.compile_semantic_graph_ir`.
Map<String, dynamic> compileSemanticGraphIr(Map<String, dynamic> graph) {
  final proof = proveGraphConsistency(graph);
  return <String, dynamic>{
    'nodes': _asList(graph['nodes']),
    'edges': _asList(graph['edges']),
    'proof': proof,
    'lineage': emptyLineage('semantic_graph_ir'),
    'confidence': <String, dynamic>{
      'score': proof['proved'] == true ? 1.0 : 0.3,
      'basis': proof['deterministic_inputs'] ?? <dynamic>[],
      'deterministic': true,
    },
  };
}

/// Port of `core.ir._base.empty_lineage`.
Map<String, dynamic> emptyLineage([String stage = 'ir']) => <String, dynamic>{
      'stages': <Map<String, dynamic>>[
        <String, dynamic>{'stage': stage}
      ],
      'depth': 1,
    };

/// Port of `core.ir._base.empty_confidence`.
Map<String, dynamic> emptyConfidence() => <String, dynamic>{
      'score': 0.0,
      'basis': <dynamic>[],
      'deterministic': true,
    };

/// Port of `core.agents.graph_query_engine.query_nodes`.
List<dynamic> queryNodes(Map<String, dynamic> graph, {String node = ''}) {
  final nodes = _asList(graph['nodes']);
  if (node.isEmpty) return nodes;
  return nodes
      .where((n) => n is Map && '${n['id'] ?? ''}'.contains(node))
      .toList();
}

/// Port of `core.agents.graph_query_engine.query_edges`.
List<dynamic> queryEdges(Map<String, dynamic> graph, {String node = ''}) {
  final edges = _asList(graph['edges']);
  if (node.isEmpty) return edges;
  return edges.where((e) {
    if (e is! Map) return false;
    final from = '${e['from'] ?? ''}';
    final to = '${e['to'] ?? ''}';
    return from.contains(node) || to.contains(node);
  }).toList();
}
