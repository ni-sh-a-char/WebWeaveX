/// Port of core/execution/runtime_policy_engine.
Map<String, dynamic> buildRuntimePolicy({
  bool allowTerminal = false,
  bool allowBrowserMutation = true,
  int maxMutations = 100,
  int maxActions = 1000,
  int maxDepth = 50,
  bool requireRollback = true,
  bool replayGuaranteed = true,
}) {
  return <String, dynamic>{
    'allow_terminal': allowTerminal,
    'allow_browser_mutation': allowBrowserMutation,
    'max_mutations': maxMutations,
    'max_actions': maxActions,
    'max_depth': maxDepth,
    'forbidden_actions':
        allowTerminal ? <String>[] : <String>['terminal_command'],
    'rollback_required': requireRollback,
    'replay_guaranteed': replayGuaranteed,
    'bounded': true,
  };
}

Map<String, dynamic> enforceRuntimePolicy(
  Map<String, dynamic> policy,
  Map<String, dynamic> action,
  int mutationCount,
  int actionCount,
) {
  final String actionType = '${action['action_type'] ?? action['type'] ?? ''}';
  final Set<dynamic> forbidden = <dynamic>{
    ...((policy['forbidden_actions'] as List<dynamic>?) ?? <dynamic>[])
  };

  bool allowed = !forbidden.contains(actionType);
  if (actionType == 'terminal_command' && policy['allow_terminal'] != true) {
    allowed = false;
  }
  if (actionType.startsWith('browser_') &&
      policy['allow_browser_mutation'] == false) {
    allowed = false;
  }

  final int maxMut = (policy['max_mutations'] as int?) ?? 100;
  final int maxAct = (policy['max_actions'] as int?) ?? 1000;
  final bool withinMutations = mutationCount <= maxMut;
  final bool withinActions = actionCount <= maxAct;

  return <String, dynamic>{
    'allowed': allowed && withinMutations && withinActions,
    'within_bounds': withinMutations && withinActions,
    'policy_violation': !allowed,
    'bounded': true,
  };
}
