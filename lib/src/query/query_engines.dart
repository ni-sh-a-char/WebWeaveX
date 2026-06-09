/// Native Dart port of the WebWeaveX public query / reasoning / IR APIs.
///
/// Mirrors the Python `webweavex.__init__` body wrappers and the deterministic
/// `core.query.*` / `core.reasoning.*` / `core.ir.*` engines. Parity proven via
/// `computeDeterministicHash` (see test/parity/query_parity_test.dart).
///
/// Heavy NLP (`compile_document` / document-discourse) and source-parsing
/// (`compile_repository` / runtime-reasoning) paths are intentionally NOT
/// ported — see report. The deterministic dict-extraction and graph/knowledge/
/// topology paths are ported with proven hash parity.
library;

import 'graph_ir.dart';
import 'knowledge_ir.dart';
import 'python_repr.dart';
import 'topology_reasoning.dart';

Map<String, dynamic> _asMap(dynamic v) =>
    v is Map ? Map<String, dynamic>.from(v) : <String, dynamic>{};

List<dynamic> _asList(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

/// Port of `core.query.graph_query_engine.query_graph`.
Map<String, dynamic> _queryGraphIr(Map<String, dynamic> graph,
    {String node = ''}) {
  final ir = compileSemanticGraphIr(graph);
  return <String, dynamic>{
    'ir': ir,
    'nodes': queryNodes(graph, node: node),
    'edges': queryEdges(graph, node: node),
    'explainable': true,
    'bounded': true,
  };
}

/// Port of `core.query.ontology_query_engine.query_knowledge`.
Map<String, dynamic> _queryKnowledgeIr(
    List<dynamic> entities, List<dynamic> edges) {
  final ir = compileKnowledgeIr(entities, edges);
  return <String, dynamic>{
    'ir': ir,
    'relations': ir['relations'] ?? <dynamic>[],
    'contradictions': ir['contradictions'] ?? <dynamic>[],
    'explainable': true,
  };
}

/// Port of the `webweavex.query_graph` body wrapper.
///
/// Pass [graph] for the direct IR path, or [result] for the extraction-result
/// path (`relationships.execution_graph` or the raw graph dict).
Map<String, dynamic> queryGraph(
    {Map<String, dynamic>? result,
    String node = '',
    Map<String, dynamic>? graph}) {
  if (graph != null) {
    return _queryGraphIr(graph, node: node);
  }
  if (result == null) {
    return _queryGraphIr(<String, dynamic>{}, node: node);
  }
  Map<String, dynamic> g;
  if (result.containsKey('relationships')) {
    g = _asMap(_asMap(result['relationships'])['execution_graph']);
  } else {
    g = result;
  }
  return _queryGraphIr(g, node: node);
}

/// Port of the `webweavex.query_repo` body wrapper.
Map<String, dynamic> queryRepo(Map<String, dynamic> result) =>
    _asMap(_asMap(result['content'])['repository']);

/// Port of the `webweavex.query_knowledge` body wrapper.
Map<String, dynamic> queryKnowledge(
    {Map<String, dynamic>? result,
    List<dynamic>? entities,
    List<dynamic>? edges}) {
  if (entities != null || edges != null) {
    return _queryKnowledgeIr(entities ?? <dynamic>[], edges ?? <dynamic>[]);
  }
  final content = _asMap(_asMap(result)['content']);
  return <String, dynamic>{
    'knowledge_v2': content['knowledge_v2'] ?? <String, dynamic>{},
    'knowledge_v18':
        content['knowledge_reconstruction_v18'] ?? <String, dynamic>{},
  };
}

/// Port of the `webweavex.query_repository` body wrapper.
///
/// The `source`-driven path delegates to `compile_repository_ir`, which is NOT
/// ported (heavy source parsing). Only the [result] dict-extraction path has
/// proven parity.
Map<String, dynamic> queryRepository(
    {Map<String, dynamic>? result, String source = '', String path = ''}) {
  if (result != null && source.isEmpty) {
    return queryRepo(result);
  }
  throw UnsupportedError(
      'query_repository source path delegates to compile_repository_ir '
      '(unported: heavy source parsing)');
}

/// Port of the `webweavex.query_documents` body wrapper.
///
/// The `text`-driven path delegates to `compile_document_ir`, which is NOT
/// ported (heavy NLP). Only the [result] dict-extraction path has proven parity.
Map<String, dynamic> queryDocuments(
    {Map<String, dynamic>? result, String text = ''}) {
  if (text.isNotEmpty) {
    throw UnsupportedError(
        'query_documents text path delegates to compile_document_ir '
        '(unported: heavy NLP)');
  }
  if (result != null) {
    return _asMap(_asMap(result['content'])['documents']);
  }
  throw UnsupportedError(
      'query_documents empty path delegates to compile_document_ir '
      '(unported: heavy NLP)');
}

/// Port of `core.query.semantic_query_engine.query_semantics`.
///
/// Only the deterministic `graph` / `knowledge` dispatch + unknown path are
/// ported; `repository` / `document` delegate to unported IR compilers.
Map<String, dynamic> querySemantics(
    String queryType, Map<String, dynamic> payload) {
  Map<String, dynamic> result;
  switch (queryType) {
    case 'graph':
      result = _queryGraphIr(_asMap(payload['graph']));
      break;
    case 'knowledge':
      result = _queryKnowledgeIr(
          _asList(payload['entities']), _asList(payload['edges']));
      break;
    case 'repository':
    case 'document':
      throw UnsupportedError(
          'query_semantics "$queryType" delegates to unported IR compiler');
    default:
      return _compileSemanticQueryIr(
          queryType, '', <String, dynamic>{'error': 'unknown_query_type'});
  }
  return _compileSemanticQueryIr(
      queryType, _truncate(pythonStr(payload), 80), result);
}

/// Port of `core.ir.semantic_query_ir.compile_semantic_query_ir`.
Map<String, dynamic> _compileSemanticQueryIr(
    String queryType, String target, Map<String, dynamic> result) {
  return <String, dynamic>{
    'query_type': queryType,
    'target': target,
    'result': result,
    'evidence': result['evidence'] ??
        result['semantic_evidence'] ??
        <String, dynamic>{},
    'explainable': true,
    'deterministic': true,
  };
}

/// Port of `core.reasoning.semantic_reasoning_engine.reason_semantically`.
///
/// Only the deterministic `topology` domain + unknown path are ported;
/// `runtime` / `discourse` delegate to unported IR compilers.
Map<String, dynamic> reasonSemantically(
    String domain, Map<String, dynamic> payload) {
  Map<String, dynamic> result;
  switch (domain) {
    case 'topology':
      result = reasonTopologySemantic(_asMap(payload['graph']));
      break;
    case 'runtime':
    case 'discourse':
      throw UnsupportedError(
          'reason_semantically "$domain" delegates to unported IR compiler');
    default:
      return <String, dynamic>{'error': 'unknown_domain', 'explainable': true};
  }
  return <String, dynamic>{
    ...result,
    'domain': domain,
    'deterministic': true,
  };
}

/// Port of `core.intelligence.graph_analyzer.analyze_graph` (the `analyze`
/// edges-path). The no-edges path runs `extract()` (network/fs) and is NOT
/// ported.
Map<String, dynamic> analyze(List<dynamic> nodes, List<dynamic> edges) {
  final n = nodes.length;
  final e = edges.length;
  var density = 0.0;
  if (n > 1) {
    density = e / (n * (n - 1));
  }
  final degree = <String, int>{};
  for (final node in nodes) {
    final nodeId = node is Map ? (node['id'] ?? '') : '';
    if (nodeId != '' && nodeId != null) {
      degree['$nodeId'] = 0;
    }
  }
  for (final edge in edges) {
    final f = edge is Map ? (edge['from'] ?? '') : '';
    final t = edge is Map ? (edge['to'] ?? '') : '';
    if (f != '' && degree.containsKey('$f')) {
      degree['$f'] = degree['$f']! + 1;
    }
    if (t != '' && degree.containsKey('$t')) {
      degree['$t'] = degree['$t']! + 1;
    }
  }
  final sortedKeys = degree.keys.toList()..sort();
  final degreeMap = <String, dynamic>{};
  for (final k in sortedKeys) {
    degreeMap[k] = degree[k];
  }
  return <String, dynamic>{
    'node_count': n,
    'edge_count': e,
    'density': density,
    'degree_map': degreeMap,
  };
}

/// `compile_document` — NOT ported (heavy NLP discourse pipeline).
Never compileDocument(String text) => throw UnsupportedError(
    'compile_document is unported: requires the document_semantic_ir NLP '
    'pipeline (rhetorical/argument/progression/coreference parsers) with no '
    'bundled Dart equivalent.');

/// `compile_repository` — NOT ported (heavy source-AST parsing).
Never compileRepository(String source, {String path = ''}) =>
    throw UnsupportedError(
        'compile_repository is unported: requires the repository_execution_ir '
        'AST/source-parsing pipeline with no bundled Dart equivalent.');

String _truncate(String s, int n) => s.length <= n ? s : s.substring(0, n);
