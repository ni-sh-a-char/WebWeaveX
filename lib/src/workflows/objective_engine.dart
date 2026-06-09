// Port of core/workflows/objective_engine.py

const Map<String, List<String>> objectiveSteps = <String, List<String>>{
  'extract_dashboard': <String>[
    'navigate_dashboard',
    'capture_widgets',
    'capture_tables'
  ],
  'extract_invoices': <String>['open_invoices', 'paginate', 'extract_rows'],
  'monitor_metrics': <String>[
    'open_dashboard',
    'observe_metrics',
    'checkpoint'
  ],
  'capture_notifications': <String>[
    'observe_notifications',
    'capture_events',
    'checkpoint'
  ],
  'extract_repository': <String>[
    'scan_repository',
    'extract_structure',
    'compile_graph'
  ],
  'monitor_runtime': <String>[
    'observe_runtime',
    'capture_mutations',
    'checkpoint'
  ],
  'capture_terminal': <String>['open_terminal', 'capture_output', 'checkpoint'],
  'monitor_application': <String>[
    'observe_application',
    'capture_state',
    'checkpoint'
  ],
  'extract_api_surface': <String>[
    'discover_routes',
    'extract_endpoints',
    'compile_api'
  ],
  'monitor_infrastructure': <String>[
    'observe_infra',
    'capture_status',
    'checkpoint'
  ],
};

Map<String, dynamic> buildRuntimeObjective(
  String objective, [
  int priority = 0,
]) {
  final List<String> steps = List<String>.from(
    objectiveSteps[objective] ?? <String>['observe', 'extract', 'checkpoint'],
  );

  return <String, dynamic>{
    'objective': objective,
    'priority': priority,
    'steps': steps,
    'bounded': true,
  };
}
