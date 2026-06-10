/// Phase A.2 (core.repository leaves) of the Category-A semantic-IR port.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'py_compat.dart';

/// Port of core.repository.api_surface_reasoning_engine.reason_api_surface.
Map<String, dynamic> reasonApiSurface(dynamic spec) {
  dynamic paths =
      spec is Map ? pyGet(spec, 'paths', <dynamic, dynamic>{}) : <dynamic, dynamic>{};
  if (paths is! Map) paths = <dynamic, dynamic>{};
  final endpoints = <Map<String, String>>[];
  for (final entry in paths.entries) {
    final methods = entry.value;
    if (methods is Map) {
      for (final method in methods.keys) {
        endpoints.add(<String, String>{
          'path': entry.key as String,
          'method': (method as String).toUpperCase(),
        });
      }
    }
  }
  return <String, dynamic>{
    'paths': endpoints,
    'path_count': endpoints.length,
    'evidence':
        endpoints.isNotEmpty ? <String>['openapi:paths'] : <String>[],
    'deterministic_inputs': <String>['paths=${endpoints.length}'],
  };
}

/// Port of core.repository.execution_flow_engine.reconstruct_execution_flow.
Map<String, dynamic> reconstructExecutionFlow(dynamic parsed) {
  final p = pyTruthy(parsed) ? parsed as Map : const <dynamic, dynamic>{};
  dynamic sym = pyGet(p, 'symbols', <dynamic, dynamic>{});
  if (!pyTruthy(sym)) sym = <dynamic, dynamic>{};
  final funcs =
      sym is Map ? pyGet(sym, 'functions', <dynamic>[]) : <dynamic>[];
  dynamic callsOuter = pyGet(p, 'calls', <dynamic, dynamic>{});
  if (!pyTruthy(callsOuter)) callsOuter = <dynamic, dynamic>{};
  dynamic calls = pyGet(callsOuter as Map, 'calls', <dynamic>[]);
  if (!pyTruthy(calls)) calls = <dynamic>[];
  final entrypoints = <dynamic>[
    for (final f in funcs as List)
      if (pyToStr(f).startsWith('main') ||
          pyToStr(f).startsWith('run_') ||
          pyToStr(f).startsWith('handle_'))
        f
  ];
  // Python: [{"step": i, "call": c} for i, c in enumerate(calls[:50])
  //          if isinstance(c, dict)] — step keeps the enumerate index, so
  // steps are non-contiguous when non-dict entries are skipped.
  final limited = (calls as List).take(50).toList();
  final flow = <Map<String, dynamic>>[
    for (var i = 0; i < limited.length; i++)
      if (limited[i] is Map) <String, dynamic>{'step': i, 'call': limited[i]}
  ];
  return <String, dynamic>{
    'entrypoints': entrypoints.take(20).toList(),
    'flow': flow,
    'evidence': pyTruthy(funcs)
        ? <String>['parser:functions', 'parser:call_graph']
        : <String>[],
  };
}

const List<String> _infraMarkers = <String>[
  'docker-compose',
  'Dockerfile',
  'kubernetes',
  'k8s/',
  'deployment.yaml',
  'helm/',
  '.github/workflows',
  'terraform',
  'pulumi',
];

/// Port of core.repository.infra_semantic_engine.detect_infra_signals.
Map<String, dynamic> detectInfraSignals(List<dynamic>? files) {
  final signals = <Map<String, String>>[];
  for (final f in files ?? const <dynamic>[]) {
    final fl = (f as String).replaceAll('\\', '/').toLowerCase();
    for (final m in _infraMarkers) {
      if (fl.contains(m.toLowerCase())) {
        signals.add(<String, String>{'file': f, 'signal': m});
        break;
      }
    }
  }
  return <String, dynamic>{
    'signals': signals,
    'evidence': <String>[for (final s in signals) 'infra:${s['signal']}'],
    'deterministic_inputs': <String>['signals=${signals.length}'],
  };
}

final RegExp _requirementsLine =
    RegExp(r'^([A-Za-z0-9_.\-]+)\s*(?:==|>=)', multiLine: true);

/// Port of core.repository.runtime_dependency_engine.resolve_runtime_dependencies.
Map<String, dynamic> resolveRuntimeDependencies(dynamic parsed,
    [String textFallback = '']) {
  var deps = <dynamic>[];
  final evidence = <String>[];
  if (pyTruthy(parsed)) {
    final p = parsed as Map;
    dynamic d = pyGet(p, 'dependencies', <dynamic, dynamic>{});
    if (!pyTruthy(d)) d = <dynamic, dynamic>{};
    dynamic depList = pyGet(d as Map, 'dependencies', <dynamic>[]);
    if (!pyTruthy(depList)) depList = <dynamic>[];
    deps = List<dynamic>.from(depList as List);
    if (deps.isNotEmpty) {
      evidence.add('parser:dependencies');
    }
    dynamic runtime = pyGet(p, 'runtime', <dynamic, dynamic>{});
    if (!pyTruthy(runtime)) runtime = <dynamic, dynamic>{};
    for (final k in const <String>['packages', 'modules']) {
      dynamic items = pyGet(runtime as Map, k, <dynamic>[]);
      if (!pyTruthy(items)) items = <dynamic>[];
      if ((items as List).isNotEmpty) {
        deps.addAll(<String>[for (final x in items.take(100)) pyToStr(x)]);
        evidence.add('parser:runtime_$k');
      }
    }
  }
  if (deps.isEmpty && pyTruthy(textFallback)) {
    // Python re.M: ^ matches after \n only — fixtures use \n line endings.
    for (final m in _requirementsLine.allMatches(textFallback)) {
      deps.add(m.group(1));
      evidence.add('fallback:requirements_line');
    }
  }
  final depSet = <dynamic>{...deps}.toList()
    ..sort((a, b) => (a as Comparable<dynamic>).compareTo(b));
  final evSet = evidence.toSet().toList()..sort();
  return <String, dynamic>{
    'dependencies': depSet.take(200).toList(),
    'evidence': evSet,
    'parser_first': pyTruthy(parsed) &&
        evidence.isNotEmpty &&
        evidence[0].startsWith('parser'),
  };
}

/// Port of core.repository.service_interaction_engine.infer_service_interactions.
Map<String, dynamic> inferServiceInteractions(
    dynamic parsed, List<dynamic> files) {
  dynamic calls = pyGet(
      pyTruthy(parsed) ? parsed as Map : const <dynamic, dynamic>{},
      'calls',
      <dynamic, dynamic>{});
  if (!pyTruthy(calls)) calls = <dynamic, dynamic>{};
  final callList =
      calls is Map ? pyGet(calls, 'calls', <dynamic>[]) : <dynamic>[];
  final services = <String>{
    for (final f in files)
      if ((f as String).contains('docker-compose') ||
          f.contains('k8s') ||
          f.contains('deployment'))
        f
  };
  final interactions = <Map<String, dynamic>>[
    for (final c in (callList as List).take(100))
      if (c is Map && pyTruthy(pyGet(c, 'caller', null)))
        <String, dynamic>{
          'from': pyGet(c, 'caller', ''),
          'to': pyGet(c, 'callee', ''),
          'evidence': <String>['parser:call_graph'],
        }
  ];
  return <String, dynamic>{
    'interactions': interactions,
    'service_files': services.toList()..sort(),
    'evidence':
        interactions.isNotEmpty ? <String>['parser:call_graph'] : <String>[],
  };
}
