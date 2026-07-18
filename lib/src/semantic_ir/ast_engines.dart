/// Phase A.2 (core.ast leaves) of the Category-A semantic-IR port.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'py_compat.dart';

const int maxExecutionPaths = 100;

/// Port of core.ast.control_flow_engine.build_control_flow_graph.
Map<String, dynamic> buildControlFlowGraph(Map<dynamic, dynamic> astIr) {
  final funcs = pyGet(astIr, 'functions', <dynamic>[]) as List;
  final nodes = <Map<String, dynamic>>[
    for (final fn in funcs)
      <String, dynamic>{'id': (fn as Map)['name'], 'type': 'function'}
  ];
  final edges = <Map<String, dynamic>>[
    for (var i = 0; i < funcs.length - 1; i++)
      <String, dynamic>{
        'from': (funcs[i] as Map)['name'],
        'to': (funcs[i + 1] as Map)['name'],
        'relation': 'possible_flow',
      }
  ];
  return <String, dynamic>{
    'nodes': nodes,
    'edges': edges,
    'bounded': true,
    'deterministic': true,
  };
}

/// Port of core.ast.execution_path_engine.reconstruct_execution_paths.
Map<String, dynamic> reconstructExecutionPaths(Map<dynamic, dynamic> cfg) {
  final nodes = pyGet(cfg, 'nodes', <dynamic>[]) as List;
  final paths = <List<dynamic>>[
    for (final node in nodes.take(maxExecutionPaths))
      <dynamic>[(node as Map)['id']]
  ];
  return <String, dynamic>{
    'paths': paths,
    'path_count': paths.length,
    'bounded': true,
  };
}

/// Port of core.ast.symbol_resolution_engine.resolve_symbols.
/// Python's `sorted(..., key=lambda x: x["symbol"])` is stable — equal keys
/// keep insertion order (functions before classes), hence [pyStableSortedBy].
Map<String, dynamic> resolveSymbols(Map<dynamic, dynamic> astIr) {
  final symbols = <Map<String, dynamic>>[];
  for (final fn in pyGet(astIr, 'functions', <dynamic>[]) as List) {
    symbols.add(<String, dynamic>{
      'symbol': (fn as Map)['name'],
      'kind': 'function',
      'args': pyGet(fn, 'args', <dynamic>[]),
    });
  }
  for (final cls in pyGet(astIr, 'classes', <dynamic>[]) as List) {
    symbols.add(<String, dynamic>{
      'symbol': (cls as Map)['name'],
      'kind': 'class',
      'bases': pyGet(cls, 'bases', <dynamic>[]),
    });
  }
  final sortedSymbols = pyStableSortedBy(symbols, (s) => s['symbol'] as String);
  return <String, dynamic>{
    'symbols': sortedSymbols,
    'symbol_count': symbols.length,
    'grounded': true,
  };
}
