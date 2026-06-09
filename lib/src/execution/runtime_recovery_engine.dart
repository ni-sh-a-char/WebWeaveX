/// Port of core/execution/runtime_recovery_engine.recover_runtime_execution.
Map<String, dynamic> recoverRuntimeExecution({
  List<Map<String, dynamic>>? failedActions,
  Map<String, dynamic>? checkpoint,
  List<dynamic>? interruptedWorkflows,
}) {
  final List<Map<String, dynamic>> failed = <Map<String, dynamic>>[
    ...(failedActions ?? <Map<String, dynamic>>[])
  ];
  final Map<String, dynamic> cp = checkpoint ?? <String, dynamic>{};
  final List<dynamic> workflows = <dynamic>[
    ...(interruptedWorkflows ?? <dynamic>[])
  ];

  final List<Map<String, dynamic>> sortedFailed = <Map<String, dynamic>>[
    ...failed
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));

  final List<Map<String, dynamic>> recoveredActions = <Map<String, dynamic>>[];
  for (int index = 0; index < sortedFailed.length; index++) {
    recoveredActions.add(<String, dynamic>{
      ...sortedFailed[index],
      'recovered': true,
      'replay_index': index,
    });
  }

  return <String, dynamic>{
    'recovered_actions': recoveredActions,
    'checkpoint_restored': cp.isNotEmpty,
    'workflows_resumed': workflows.length,
    'sync_divergence_resolved': true,
    'replay_safe': true,
    'bounded': true,
  };
}
