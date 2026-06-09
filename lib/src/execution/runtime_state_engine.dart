/// Port of core/execution/runtime_state_engine.build_execution_state.
Map<String, dynamic> buildExecutionState({
  String runtime = 'browser',
  List<dynamic>? activeActions,
  List<dynamic>? queue,
  List<dynamic>? mutations,
  Map<String, dynamic>? checkpoint,
  Map<String, dynamic>? transaction,
  Map<String, dynamic>? federation,
}) {
  return <String, dynamic>{
    'current_runtime': runtime,
    'active_actions': <dynamic>[...(activeActions ?? <dynamic>[])],
    'pending_queues': <dynamic>[...(queue ?? <dynamic>[])],
    'mutations': <dynamic>[...(mutations ?? <dynamic>[])],
    'checkpoint': <String, dynamic>{...?checkpoint},
    'transaction': <String, dynamic>{...?transaction},
    'federation_state': <String, dynamic>{...?federation},
    'bounded': true,
  };
}
