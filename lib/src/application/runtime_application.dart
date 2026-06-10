/// Canonical Python-aligned application/native runtime APIs (Group D of the
/// Final Completion Protocol). Snapshot/data/persistence-input deterministic
/// functions — no live runtime required.
///
/// - execute_runtime_objective: proven Python ≡ JavaScript ≡ Dart by execution.
/// - save/load_application_memory + save/load_native_runtime: Kaalka persistence,
///   proven by save → load → deep-equality roundtrip (the persistence proof
///   standard; encryptSessionState/decryptSessionState are separately
///   executable-proven).
library;

import 'dart:convert';
import 'dart:io';

import '../persistence/persistence_runtime.dart';

const Map<String, List<String>> _objectives = <String, List<String>>{
  'login': <String>['open_login', 'fill_credentials', 'submit'],
  'extract_dashboard': <String>[
    'navigate_dashboard',
    'capture_widgets',
    'capture_tables'
  ],
  'export_report': <String>['open_reports', 'select_report', 'export'],
  'extract_invoices': <String>['open_invoices', 'paginate', 'extract_rows'],
  'monitor_metrics': <String>[
    'open_dashboard',
    'observe_metrics',
    'checkpoint'
  ],
};

/// Port of core.application.runtime_goal_engine.build_runtime_goal.
Map<String, dynamic> buildRuntimeGoal(String objective) => <String, dynamic>{
      'objective': objective,
      'steps': List<String>.from(
          _objectives[objective] ?? const <String>['observe', 'extract']),
      'bounded': true,
    };

/// Port of webweavex.execute_runtime_objective.
Map<String, dynamic> executeRuntimeObjective(
  String objective,
  Map<String, dynamic> workflowGraph,
  Map<String, dynamic> actionGraph,
  Map<String, dynamic> navigation, {
  Map<String, dynamic>? adaptiveRuntime,
}) {
  final goal = buildRuntimeGoal(objective);
  final steps = goal['steps'] as List<dynamic>;
  final wfNodes = (workflowGraph['nodes'] is List
          ? workflowGraph['nodes'] as List
          : const <dynamic>[])
      .length;
  final acNodes = (actionGraph['nodes'] is List
          ? actionGraph['nodes'] as List
          : const <dynamic>[])
      .length;
  final routes = navigation['routes'] is List
      ? navigation['routes'] as List
      : <dynamic>[<String, dynamic>{}];
  final firstRoute = routes.isNotEmpty && routes[0] is Map
      ? routes[0] as Map
      : const <String, dynamic>{};
  final route = (firstRoute['path'] ?? '').toString();

  final executed = <Map<String, dynamic>>[];
  for (var index = 0; index < steps.length; index++) {
    executed.add(<String, dynamic>{
      'step': index,
      'name': steps[index],
      'workflow_nodes': wfNodes,
      'action_nodes': acNodes,
      'route': route,
      'adaptive': adaptiveRuntime != null && adaptiveRuntime.isNotEmpty,
      'completed': true,
    });
  }
  return <String, dynamic>{
    'objective': objective,
    'goal': goal,
    'executed': executed,
    'bounded': true,
  };
}

Map<String, dynamic> _emptyMemory() => <String, dynamic>{
      'workflows': <String, dynamic>{},
      'forms': <String, dynamic>{},
      'action_graphs': <String, dynamic>{},
      'navigation_flows': <String, dynamic>{},
      'dashboard_structures': <String, dynamic>{},
      'bounded': true,
    };

Map<String, dynamic> _emptyRuntime() => <String, dynamic>{
      'accessibility_trees': <String, dynamic>{},
      'windows': <String, dynamic>{},
      'workflows': <String, dynamic>{},
      'runtime_graphs': <String, dynamic>{},
      'electron_state': <String, dynamic>{},
      'terminal_streams': <String, dynamic>{},
      'bounded': true,
    };

Map<String, dynamic> _save(String path, Map<String, dynamic> data, String key) {
  final encrypted = encryptSessionState(data, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  target.writeAsStringSync(jsonEncode(encrypted));
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _load(String path, String key, String dataKey,
    Map<String, dynamic> Function() empty) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      dataKey: empty(),
      'bounded': true
    };
  }
  final encrypted =
      Map<String, dynamic>.from(jsonDecode(target.readAsStringSync()) as Map);
  final decrypted = decryptSessionState(encrypted, key);
  final session = decrypted['session'];
  return <String, dynamic>{
    'available': true,
    dataKey: session is Map ? Map<String, dynamic>.from(session) : empty(),
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Port of webweavex.save_application_memory(path, memory, key).
Map<String, dynamic> saveApplicationMemory(
        String path, Map<String, dynamic> memory, String key) =>
    _save(path, memory, key);

/// Port of webweavex.load_application_memory(path, key).
Map<String, dynamic> loadApplicationMemory(String path, String key) =>
    _load(path, key, 'memory', _emptyMemory);

/// Port of webweavex.save_native_runtime(path, runtime, key).
Map<String, dynamic> saveNativeRuntime(
        String path, Map<String, dynamic> runtime, String key) =>
    _save(path, runtime, key);

/// Port of webweavex.load_native_runtime(path, key).
Map<String, dynamic> loadNativeRuntime(String path, String key) =>
    _load(path, key, 'runtime', _emptyRuntime);
