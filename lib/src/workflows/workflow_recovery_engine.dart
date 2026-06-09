// Port of core/workflows/workflow_recovery_engine.py

const Map<String, String> recoveryActions = <String, String>{
  'selector_drift': 'heal_selector',
  'modal_interruption': 'recover_modal',
  'pagination_failure': 'retry_pagination',
  'runtime_mutation': 'realign_runtime',
  'authentication_expiration': 'reauthenticate',
  'worker_failure': 'redispatch_worker',
};

Map<String, dynamic> recoverWorkflowRuntime(
  Map<String, dynamic> state, [
  List<String>? failures,
]) {
  final List<String> failureList = failures ?? <String>[];
  final List<Map<String, dynamic>> recoveredSteps = <Map<String, dynamic>>[];

  for (final String failure in failureList.take(100)) {
    recoveredSteps.add(<String, dynamic>{
      'failure': failure,
      'action': recoveryActions[failure] ?? 'retry_step',
      'recovered': true,
    });
  }

  final int currentStep =
      state['current_step'] is int ? state['current_step'] as int : 0;
  if (failureList.isEmpty && currentStep > 0) {
    recoveredSteps.add(<String, dynamic>{
      'failure': 'implicit_retry',
      'action': 'retry_step',
      'recovered': true,
    });
  }

  final int retries = state['retries'] is int ? state['retries'] as int : 0;
  final Map<String, dynamic> newState = Map<String, dynamic>.from(state);
  newState['retries'] = retries + recoveredSteps.length;

  return <String, dynamic>{
    'state': newState,
    'recovered_steps': recoveredSteps,
    'recovered': true,
    'bounded': true,
  };
}
