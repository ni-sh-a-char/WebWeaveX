/// Phase C ast/document/graph/repository composites of the Category-A
/// semantic-IR port. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'ast_engines.dart'
    show buildControlFlowGraph, reconstructExecutionPaths, resolveSymbols;
import 'composites_b.dart' show modelInfraRelationships, reasonTopology;
import 'document_composites.dart'
    show buildArgumentGraph, extractInstructionalFlow, parseRhetoricalStructure;
import 'document_parser.dart'
    show assignSemanticRoles, extractRhetoricalStructure, resolveCoreferences;
import 'graph_engines.dart' show detectCycles;
import 'py_compat.dart';
import 'python_ast_parser.dart' show parsePythonAst;

/// Port of core.ast.semantic_ast_ir_engine.compile_semantic_ast_ir.
Map<String, dynamic> compileSemanticAstIr(String code) {
  final astIr = parsePythonAst(code);
  final symbols = resolveSymbols(astIr);
  final cfg = buildControlFlowGraph(astIr);
  final executionPaths = reconstructExecutionPaths(cfg);
  return <String, dynamic>{
    'ast': astIr,
    'symbols': symbols,
    'control_flow_graph': cfg,
    'execution_paths': executionPaths,
    'semantic_grounded': true,
    'deterministic': true,
  };
}

/// Port of core.documents.coreference_graph_engine.build_coreference_graph.
Map<String, dynamic> buildCoreferenceGraph(String text) {
  final coref = resolveCoreferences(text);
  final rhet = parseRhetoricalStructure(text);
  final headings = <dynamic>[
    for (final u in pyGet(rhet, 'units', const <dynamic>[]) as List)
      if (pyGet(u as Map, 'type', null) == 'heading') pyGet(u, 'title', '')
  ];
  final nodes = <Map<String, dynamic>>[
    for (final h in headings)
      if (pyTruthy(h)) <String, dynamic>{'id': h, 'kind': 'entity'}
  ];
  final edges = <Map<String, dynamic>>[
    for (final c in pyGet(coref, 'chains', const <dynamic>[]) as List)
      if (pyTruthy(pyGet(c as Map, 'antecedent', null)))
        <String, dynamic>{
          'from': pyGet(c, 'pronoun', ''),
          'to': pyGet(c, 'antecedent', ''),
          'evidence': <String>['discourse:coref'],
        }
  ];
  return <String, dynamic>{
    'nodes': nodes,
    'edges': edges.length > 100 ? edges.sublist(0, 100) : edges,
    'chains': pyGet(coref, 'chains', const <dynamic>[]),
  };
}

/// Port of core.documents.instructional_semantics_engine
/// .analyze_instructional_semantics.
Map<String, dynamic> analyzeInstructionalSemantics(String text) {
  final flow = extractInstructionalFlow(text);
  final roles = assignSemanticRoles(text);
  final steps = pyGet(flow, 'steps', const <dynamic>[]) as List;
  final ordering = <Map<String, dynamic>>[
    for (var i = 0; i < steps.length; i++)
      <String, dynamic>{
        'step': i + 1,
        'title': pyGet(steps[i] as Map, 'title', ''),
      }
  ];
  return <String, dynamic>{
    'ordering': ordering,
    'prerequisites': pyGet(flow, 'prerequisites', const <dynamic>[]),
    'notices': <dynamic>[
      for (final r in pyGet(roles, 'roles', const <dynamic>[]) as List)
        if (pyGet(r as Map, 'role', null) == 'notice') r
    ],
    'evidence': <String>['discourse:instructional_flow'],
    'deterministic_inputs': <String>['steps=${ordering.length}'],
  };
}

/// Port of core.documents.semantic_discourse_parser.parse_semantic_discourse.
Map<String, dynamic> parseSemanticDiscourse(String text) {
  final rhet = extractRhetoricalStructure(text);
  final arg = buildArgumentGraph(text);
  return <String, dynamic>{
    'rhetorical': rhet,
    'argument': arg,
    'transitions': pyGet(arg, 'edges', const <dynamic>[]),
    'deterministic_inputs': <dynamic>[
      ...pyGet(rhet, 'deterministic_inputs', const <dynamic>[]) as List,
      'args=${(pyGet(arg, 'nodes', const <dynamic>[]) as List).length}',
    ],
  };
}

/// Port of core.reasoning.topology_reasoning_engine.reason_topology_semantic.
Map<String, dynamic> reasonTopologySemantic(Map<dynamic, dynamic> graph) {
  final topo = reasonTopology(graph);
  final cycles = detectCycles(graph);
  return <String, dynamic>{
    ...topo,
    'cycles': cycles,
    'contradiction_pressure': pyGet(cycles, 'contradiction_pressure', 0),
    'explainable': true,
  };
}

/// Port of core.repository.deployment_semantics_engine
/// .analyze_deployment_semantics.
Map<String, dynamic> analyzeDeploymentSemantics(List<dynamic> files) {
  final infra = modelInfraRelationships(files);
  const keywords = <String>['docker', 'k8s', 'helm', 'deploy', 'workflow'];
  final deployFiles = <dynamic>[
    for (final f in files)
      if (keywords.any(
          (f as String).replaceAll(r'\', '/').toLowerCase().contains))
        f
  ];
  return <String, dynamic>{
    'deployment_artifacts': deployFiles,
    'infra': infra,
    'semantics': deployFiles.isNotEmpty ? 'container_orchestration' : 'unknown',
    'evidence': <dynamic>[
      ...pyGet(infra, 'evidence', const <dynamic>[]) as List,
      'deploy:${deployFiles.length}',
    ],
  };
}
