/// Repository-IR closure of the Category-A semantic-IR port — the 11
/// formerly parse_source-gated engines, now unblocked by parsers.dart:
/// the B/C/D-phase deferrals plus `compile_repository_ir`,
/// `query_repository`, and `reason_runtime_semantic`.
///
/// semantic_ast 3-way domain: Python's compile_semantic_ast_ir uses
/// ast.parse, which raises on non-Python source where the certified
/// line/indent scanner returns a sparse summary; sources that trip BOTH
/// (empty source, or a first logical line starting with one of `<>)]}%?\`,
/// e.g. JSX/Vue files) — or scanner-envelope-valid Python — are the
/// certified parity domain. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'composites_b.dart' show emptyRepositoryIr, reasonApiContract;
import 'composites_c.dart'
    show analyzeDeploymentSemantics, compileSemanticAstIr;
import 'ir_base.dart' show emptyLineage, mergeEvidence;
import 'parsers.dart' show parseSource;
import 'py_compat.dart';
import 'repository_engines.dart'
    show
        inferServiceInteractions,
        reconstructExecutionFlow,
        resolveRuntimeDependencies;

dynamic _orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;

/// Port of core.repository.repository_semantic_ir_engine
/// .build_repository_semantic_ir.
Map<String, dynamic> buildRepositorySemanticIr(String? source,
    [String path = '', List<dynamic>? files]) {
  var parsed = <String, dynamic>{};
  if (pyTruthy(source)) {
    parsed = parseSource(source, path);
  }
  return <String, dynamic>{
    'language': pyGet(parsed, 'language', 'text'),
    'symbols': pyGet(parsed, 'symbols', <dynamic, dynamic>{}),
    'runtime_dependencies': resolveRuntimeDependencies(parsed, source ?? ''),
    'execution_flow': reconstructExecutionFlow(parsed),
    'service_interactions':
        inferServiceInteractions(parsed, files ?? const <dynamic>[]),
    'parser_grounding':
        pyGet(parsed, 'parser_grounding', <dynamic, dynamic>{}),
    'evidence': pyGet(
        pyGet(parsed, 'parser_grounding', <dynamic, dynamic>{}) as Map,
        'deterministic_inputs',
        const <dynamic>[]),
  };
}

/// Port of core.repository.execution_dependency_engine
/// .model_execution_dependencies.
Map<String, dynamic> modelExecutionDependencies(String? source,
    [String path = '']) {
  final parsed =
      pyTruthy(source) ? parseSource(source, path) : <String, dynamic>{};
  final flow = reconstructExecutionFlow(parsed);
  final edges = <Map<String, dynamic>>[];
  dynamic prev;
  for (final step in pyGet(flow, 'flow', const <dynamic>[]) as List) {
    final callRaw = pyGet(step as Map, 'call', null);
    final call = callRaw is Map ? callRaw : <dynamic, dynamic>{};
    final cur = _orElse(pyGet(call, 'callee', null),
        _orElse(pyGet(call, 'caller', null), ''));
    if (pyTruthy(prev) && pyTruthy(cur)) {
      edges.add(<String, dynamic>{
        'from': pyToStr(prev),
        'to': pyToStr(cur),
        'evidence': <String>['parser:call_graph'],
      });
    }
    prev = pyTruthy(cur) ? cur : prev;
  }
  return <String, dynamic>{
    'edges': edges,
    'entrypoints': pyGet(flow, 'entrypoints', const <dynamic>[]),
    'evidence': pyGet(flow, 'evidence', const <dynamic>[]),
  };
}

/// Port of core.repository.runtime_semantics_engine.analyze_runtime_semantics.
Map<String, dynamic> analyzeRuntimeSemantics(String? source,
    [String path = '']) {
  final parsed =
      pyTruthy(source) ? parseSource(source, path) : <String, dynamic>{};
  final deps = resolveRuntimeDependencies(parsed, source ?? '');
  final runtime = pyTruthy(parsed)
      ? pyGet(parsed, 'runtime', <dynamic, dynamic>{})
      : <dynamic, dynamic>{};
  return <String, dynamic>{
    'dependencies': deps['dependencies'],
    'runtime': runtime,
    'parser_first': pyGet(deps, 'parser_first', false),
    'evidence': pyGet(deps, 'evidence', const <dynamic>[]),
    'deterministic_inputs': pyGet(
        pyGet(parsed, 'parser_grounding', <dynamic, dynamic>{}) as Map,
        'deterministic_inputs',
        const <dynamic>[]),
  };
}

/// Port of core.repository.service_runtime_graph_engine
/// .build_service_runtime_graph.
Map<String, dynamic> buildServiceRuntimeGraph(String? source,
    [String path = '', List<dynamic>? files]) {
  final parsed =
      pyTruthy(source) ? parseSource(source, path) : <String, dynamic>{};
  final interactions =
      inferServiceInteractions(parsed, files ?? const <dynamic>[]);
  final inter =
      pyGet(interactions, 'interactions', const <dynamic>[]) as List;
  final fromNodes = <dynamic>{
    for (final i in inter)
      if (pyTruthy(pyGet(i as Map, 'from', null))) pyGet(i, 'from', null)
  }.toList()
    ..sort((a, b) => pyToStr(a).compareTo(pyToStr(b)));
  final toNodes = <dynamic>{
    for (final i in inter)
      if (pyTruthy(pyGet(i as Map, 'to', null))) pyGet(i, 'to', null)
  }.toList()
    ..sort((a, b) => pyToStr(a).compareTo(pyToStr(b)));
  final nodes = <String>{
    for (final n in <dynamic>[...fromNodes, ...toNodes])
      if (pyTruthy(n)) pyToStr(n)
  }.toList()
    ..sort();
  final boundedNodes = nodes.length > 200 ? nodes.sublist(0, 200) : nodes;
  final boundedEdges = inter.length > 200 ? inter.sublist(0, 200) : inter;
  return <String, dynamic>{
    'nodes': boundedNodes,
    'edges': boundedEdges,
    'service_files': pyGet(interactions, 'service_files', const <dynamic>[]),
    'evidence': pyGet(interactions, 'evidence', const <dynamic>[]),
  };
}

/// Port of core.repository.runtime_execution_engine.analyze_runtime_execution.
Map<String, dynamic> analyzeRuntimeExecution(String? source,
    [String path = '']) {
  final parsed =
      pyTruthy(source) ? parseSource(source, path) : <String, dynamic>{};
  final runtime = analyzeRuntimeSemantics(source, path);
  final flow = reconstructExecutionFlow(parsed);
  return <String, dynamic>{
    'runtime': runtime,
    'execution': flow,
    'evidence': (<String>{
      for (final e in pyGet(runtime, 'evidence', const <dynamic>[]) as List)
        e as String,
      for (final e in pyGet(flow, 'evidence', const <dynamic>[]) as List)
        e as String,
    }.toList()
      ..sort()),
    'parser_backed': pyGet(runtime, 'parser_first', false),
  };
}

/// Port of core.repository.runtime_flow_reasoner.reason_runtime_flow.
Map<String, dynamic> reasonRuntimeFlow(String? source,
    [String path = '', List<dynamic>? files]) {
  final runtime = analyzeRuntimeSemantics(source, path);
  final execDeps = modelExecutionDependencies(source, path);
  return <String, dynamic>{
    'runtime': runtime,
    'execution_flow': execDeps,
    'topology': <String, dynamic>{
      'edges': pyGet(execDeps, 'edges', const <dynamic>[]),
    },
    'evidence': (<String>{
      for (final e in pyGet(runtime, 'evidence', const <dynamic>[]) as List)
        e as String,
      for (final e in pyGet(execDeps, 'evidence', const <dynamic>[]) as List)
        e as String,
    }.toList()
      ..sort()),
  };
}

/// Port of core.repository.repository_execution_ir_engine
/// .build_repository_execution_ir.
Map<String, dynamic> buildRepositoryExecutionIr(String? source,
    [String path = '',
    List<dynamic>? files,
    Map<dynamic, dynamic>? openapiSpec]) {
  final base = buildRepositorySemanticIr(source, path, files);
  final flow = reasonRuntimeFlow(source, path, files);
  final services = buildServiceRuntimeGraph(source, path, files);
  final deploy = analyzeDeploymentSemantics(files ?? const <dynamic>[]);
  final api = pyTruthy(openapiSpec)
      ? reasonApiContract(openapiSpec!)
      : <dynamic, dynamic>{};
  return <String, dynamic>{
    ...base,
    'execution': flow,
    'services': services,
    'deployment': deploy,
    'api_contracts': api,
    'evidence': (<String>{
      for (final e in <dynamic>[
        ..._orElse(pyGet(base, 'evidence', null), const <dynamic>[]) as List,
        ..._orElse(pyGet(flow, 'evidence', null), const <dynamic>[]) as List,
      ])
        if (pyTruthy(e)) pyToStr(e)
    }.toList()
      ..sort()),
  };
}

/// Port of core.repository.runtime_state_engine.model_runtime_state.
Map<String, dynamic> modelRuntimeState(String? source, [String path = '']) {
  final ex = analyzeRuntimeExecution(source, path);
  final parserBacked = pyTruthy(pyGet(ex, 'parser_backed', null));
  return <String, dynamic>{
    'state': parserBacked ? 'active' : 'unknown',
    'dependencies': pyGet(
        pyGet(ex, 'runtime', <dynamic, dynamic>{}) as Map,
        'dependencies',
        const <dynamic>[]),
    'execution': pyGet(ex, 'execution', <dynamic, dynamic>{}),
    'evidence': pyGet(ex, 'evidence', const <dynamic>[]),
    'transitions': <Map<String, String>>[
      <String, String>{'from': 'init', 'to': parserBacked ? 'parsed' : 'text'},
    ],
  };
}

/// Port of core.ir.repository_ir.compile_repository_ir.
Map<String, dynamic> compileRepositoryIr(
    [String source = '',
    String path = '',
    List<dynamic>? files,
    Map<dynamic, dynamic>? openapiSpec]) {
  final raw = buildRepositoryExecutionIr(source, path, files, openapiSpec);
  final deps = _orElse(pyGet(raw, 'runtime_dependencies', <dynamic, dynamic>{}),
      <dynamic, dynamic>{}) as Map;
  final flow = _orElse(
      pyGet(raw, 'execution', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final services = _orElse(
      pyGet(raw, 'services', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final deploy = _orElse(
      pyGet(raw, 'deployment', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final api = _orElse(
      pyGet(raw, 'api_contracts', <dynamic, dynamic>{}), <dynamic, dynamic>{}) as Map;
  final ir = emptyRepositoryIr();
  ir['dependencies'] = pyGet(deps, 'dependencies', const <dynamic>[]);
  ir['runtimes'] = <Map<String, dynamic>>[
    <String, dynamic>{
      'language': pyGet(raw, 'language', 'text'),
      'evidence': pyGet(deps, 'evidence', const <dynamic>[]),
    }
  ];
  ir['execution_flows'] = pyGet(
      pyGet(flow, 'execution_flow', <dynamic, dynamic>{}) as Map,
      'flow',
      const <dynamic>[]);
  ir['services'] = pyGet(services, 'nodes', const <dynamic>[]);
  ir['topology'] = pyGet(
      pyGet(flow, 'topology', <dynamic, dynamic>{}) as Map,
      'edges',
      const <dynamic>[]);
  ir['deployments'] = pyGet(deploy, 'deployment_artifacts', const <dynamic>[]);
  ir['infra'] = <dynamic>[
    for (final s in pyGet(
        pyGet(deploy, 'infra', <dynamic, dynamic>{}) as Map,
        'signals',
        const <dynamic>[]) as List)
      if (s is Map) pyGet(s, 'file', null)
  ];
  ir['apis'] = pyGet(api, 'contracts', const <dynamic>[]);
  ir['graph'] = <String, dynamic>{
    'nodes': pyGet(services, 'nodes', const <dynamic>[]),
    'edges': pyGet(services, 'edges', const <dynamic>[]),
  };
  ir['semantic_evidence'] =
      mergeEvidence(<dynamic>[pyGet(raw, 'evidence', const <dynamic>[])]);
  ir['lineage'] = emptyLineage('repository_execution_ir');
  ir['confidence'] = <String, dynamic>{
    'score': pyTruthy(pyGet(deps, 'parser_first', null)) ? 0.8 : 0.4,
    'basis': pyGet(raw, 'evidence', const <dynamic>[]),
    'deterministic': true,
  };
  Map<String, dynamic> semanticAst;
  try {
    semanticAst = compileSemanticAstIr(source);
  } on FormatException {
    // Python catches SyntaxError from ast.parse; the scanner's validity
    // gate raises FormatException on the same inputs within the domain.
    semanticAst = <String, dynamic>{
      'semantic_grounded': false,
      'deterministic': true,
    };
  }
  ir['semantic_ast'] = semanticAst;
  ir['_raw'] = raw;
  return ir;
}

/// Port of core.query.repository_query_engine.query_repository.
Map<String, dynamic> queryRepositoryIr(
    [String source = '', String path = '', List<dynamic>? files]) {
  final ir = compileRepositoryIr(source, path, files);
  return <String, dynamic>{
    'ir': ir,
    'evidence': pyGet(ir, 'semantic_evidence', <dynamic, dynamic>{}),
    'explainable': true,
    'bounded': true,
  };
}

/// Port of core.reasoning.runtime_reasoning_engine.reason_runtime_semantic.
Map<String, dynamic> reasonRuntimeSemantic(String source, [String path = '']) {
  final ir = compileRepositoryIr(source, path);
  final state = modelRuntimeState(source, path);
  return <String, dynamic>{
    'ir': ir,
    'state': state,
    'evidence': pyGet(ir, 'semantic_evidence', <dynamic, dynamic>{}),
    'explainable': true,
  };
}
