/// Port of core/execution/runtime_sandbox_engine.build_runtime_sandbox.
Map<String, dynamic> buildRuntimeSandbox({
  String runtime = 'browser',
  List<String>? allowedActions,
  bool rollbackEnabled = true,
  int maxActions = 1000,
  int timeoutTicks = 10000,
  String replayPolicy = 'strict',
}) {
  List<String> defaultAllowed = <String>[
    'browser_click',
    'browser_focus',
    'native_focus',
  ];
  if (runtime == 'terminal') {
    defaultAllowed = <String>['terminal_command'];
  } else if (runtime == 'native') {
    defaultAllowed = <String>['native_focus'];
  } else if (runtime == 'vm') {
    defaultAllowed = <String>['vm_execute'];
  }

  final List<String> allowed = <String>[...(allowedActions ?? defaultAllowed)]
    ..sort();

  return <String, dynamic>{
    'runtime': runtime,
    'allowed_actions': allowed,
    'rollback_enabled': rollbackEnabled,
    'max_actions': maxActions,
    'execution_boundaries': <String, dynamic>{
      'max_depth': 50,
      'max_mutations': 100,
      'timeout_ticks': timeoutTicks,
    },
    'mutation_limits': <String, dynamic>{'max_mutations': 100},
    'rollback_policy': <String, dynamic>{'enabled': rollbackEnabled},
    'timeout_policy': <String, dynamic>{'ticks': timeoutTicks},
    'replay_policy': replayPolicy,
    'bounded': true,
  };
}
