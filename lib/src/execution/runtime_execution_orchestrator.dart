import 'execution_runtime_ir.dart';
import 'runtime_coordination_engine.dart';
import 'runtime_execution_engine.dart';
import 'runtime_federation_engine.dart';
import 'runtime_mutation_engine.dart';
import 'runtime_permissions_engine.dart';
import 'runtime_policy_engine.dart';
import 'runtime_queue_engine.dart';
import 'runtime_recovery_engine.dart';
import 'runtime_replay_engine.dart';
import 'runtime_rollback_engine.dart';
import 'runtime_sandbox_engine.dart';
import 'runtime_scheduler_engine.dart';
import 'runtime_simulation_engine.dart';
import 'runtime_state_engine.dart';
import 'runtime_transaction_engine.dart';
import 'runtime_transition_engine.dart';

List<Map<String, dynamic>> _defaultActions(String runtime) {
  if (runtime == 'native') {
    return <Map<String, dynamic>>[
      <String, dynamic>{'type': 'native_focus', 'window': 'application'}
    ];
  }
  if (runtime == 'terminal') {
    return <Map<String, dynamic>>[
      <String, dynamic>{'type': 'terminal_command', 'command': 'pwd'}
    ];
  }
  return <Map<String, dynamic>>[
    <String, dynamic>{'type': 'browser_click', 'selector': '#submit'}
  ];
}

/// Port of core/execution/runtime_execution_orchestrator.run_execution_runtime.
Map<String, dynamic> runExecutionRuntime({
  Map<String, dynamic>? sources,
  Map<String, dynamic>? stored,
  List<Map<String, dynamic>>? workers,
  String runtime = 'browser',
  int tick = 0,
  bool simulate = false,
  bool rollbackEnabled = true,
}) {
  final Map<String, dynamic> src = sources ?? <String, dynamic>{};
  final Map<String, dynamic> storedMap = <String, dynamic>{...?stored};
  final List<Map<String, dynamic>> workerList = workers ??
      <Map<String, dynamic>>[
        <String, dynamic>{
          'worker_id': 'primary',
          'runtime': runtime,
          'synced': true,
        }
      ];

  final Map<String, dynamic> sandbox = buildRuntimeSandbox(runtime: runtime);
  final Map<String, dynamic> policy =
      buildRuntimePolicy(allowTerminal: runtime == 'terminal');
  final Map<String, dynamic> permissions = buildRuntimePermissions(
    scopes: runtime == 'browser'
        ? <String>['browser', 'native', 'terminal', 'connector', 'vm']
        : <String>[runtime],
  );

  final Map<String, dynamic> priorCheckpoint =
      (storedMap['checkpoint'] as Map?)?.cast<String, dynamic>() ??
          <String, dynamic>{};
  Map<String, dynamic> checkpointBody = <String, dynamic>{};
  if (priorCheckpoint.isNotEmpty) {
    final dynamic state = priorCheckpoint['state'];
    checkpointBody =
        state is Map ? state.cast<String, dynamic>() : priorCheckpoint;
  }

  final List<Map<String, dynamic>> rawActions =
      ((src['actions'] as List<dynamic>?)?.cast<Map<String, dynamic>>()) ??
          _defaultActions(runtime);
  final List<Map<String, dynamic>> executedActions = <Map<String, dynamic>>[];
  int mutationCount = 0;

  List<Map<String, dynamic>> queue = <Map<String, dynamic>>[];
  final int maxActions = (sandbox['max_actions'] as int?) ?? 1000;
  final List<Map<String, dynamic>> sliced = rawActions.length > maxActions
      ? rawActions.sublist(0, maxActions)
      : rawActions;
  for (final Map<String, dynamic> raw in sliced) {
    final Map<String, dynamic> enqueueResult =
        enqueueRuntimeAction(queue, raw, priority: 0);
    queue =
        (enqueueResult['queue'] as List<dynamic>).cast<Map<String, dynamic>>();
  }

  if (simulate) {
    final Map<String, dynamic> simulation =
        simulateRuntimeExecution(rawActions, sandbox: sandbox, tick: tick);
    final Map<String, dynamic> transition =
        applyRuntimeTransition('idle', 'simulate');
    final Map<String, dynamic> payload = <String, dynamic>{
      'simulation': simulation,
      'transition': transition,
      'sandbox': sandbox,
      'bounded': true,
    };
    payload['execution_ir'] = compileExecutionRuntimeIr(payload);
    return payload;
  }

  Map<String, dynamic> transaction = beginRuntimeTransaction(tick: tick);
  Map<String, dynamic> transition = applyRuntimeTransition('idle', 'enqueue');

  while (queue.isNotEmpty) {
    final Map<String, dynamic> dequeueResult = dequeueRuntimeAction(queue);
    queue =
        (dequeueResult['queue'] as List<dynamic>).cast<Map<String, dynamic>>();
    final dynamic actionRaw = dequeueResult['action'];
    if (actionRaw == null) break;

    final Map<String, dynamic> actionRawMap =
        (actionRaw as Map).cast<String, dynamic>();
    // Python: raw = action_raw.get("action", action_raw)
    final dynamic nested = actionRawMap['action'];
    final Map<String, dynamic> raw =
        nested is Map ? nested.cast<String, dynamic>() : actionRawMap;

    final Map<String, dynamic> result = executeRuntimeAction(
      raw,
      sandbox: sandbox,
      policy: policy,
      permissions: permissions,
      tick: tick,
      mutationCount: mutationCount,
      actionCount: executedActions.length,
    );
    if (result['executed'] == true) {
      executedActions.add((result['action'] as Map?)?.cast<String, dynamic>() ??
          <String, dynamic>{});
      mutationCount += 1;
      final Map<String, dynamic> trackResult = trackRuntimeMutations(
        prior: ((transaction['mutations'] as List<dynamic>?) ?? <dynamic>[])
            .cast<Map<String, dynamic>>(),
        mutation: <String, dynamic>{
          'kind': '${result['runtime'] ?? 'action'}',
          'target': '${result['action_id'] ?? ''}',
          'tick': tick,
        },
      );
      transaction['mutations'] = trackResult['mutations'];
      transaction['actions'] = executedActions;
    }

    transition = applyRuntimeTransition('${transition['to']}', 'execute');
  }

  transaction = commitRuntimeTransaction(transaction);
  transition = applyRuntimeTransition('${transition['to']}', 'commit');

  final Map<String, dynamic> mutations = trackRuntimeMutations(
    prior: ((transaction['mutations'] as List<dynamic>?) ?? <dynamic>[])
        .cast<Map<String, dynamic>>(),
  );
  final Map<String, dynamic> federation =
      federateRuntimeExecution(workerList, executedActions);
  final Map<String, dynamic> schedule =
      scheduleRuntimeExecution(executedActions, tick: tick);
  final Map<String, dynamic> coordination = coordinateRuntimeExecution(
    <Map<String, dynamic>>[],
    federation,
    workflow: (src['workflow'] as Map?)?.cast<String, dynamic>(),
    syncState: (src['sync'] as Map?)?.cast<String, dynamic>(),
  );

  Map<String, dynamic> rollbackResult = <String, dynamic>{};
  if (rollbackEnabled && checkpointBody.isNotEmpty) {
    rollbackResult = rollbackRuntimeState(
        checkpointBody, buildExecutionState(runtime: runtime));
  }

  final dynamic workflow = src['workflow'];
  final Map<String, dynamic> recovery = recoverRuntimeExecution(
    failedActions:
        executedActions.where((Map<String, dynamic> a) => a.isEmpty).toList(),
    checkpoint: checkpointBody,
    interruptedWorkflows: workflow != null ? <dynamic>[workflow] : <dynamic>[],
  );

  final Map<String, dynamic> state = buildExecutionState(
    runtime: runtime,
    activeActions: executedActions,
    queue: queue,
    mutations: (mutations['mutations'] as List<dynamic>?) ?? <dynamic>[],
    checkpoint: checkpointBody,
    transaction: transaction,
    federation: federation,
  );

  final Map<String, dynamic> replay = replayRuntimeExecution(
    executedActions,
    transactions: <Map<String, dynamic>>[transaction],
    mutations: ((mutations['mutations'] as List<dynamic>?) ?? <dynamic>[])
        .cast<Map<String, dynamic>>(),
    tick: tick,
  );

  final Map<String, dynamic> payload = <String, dynamic>{
    'actions': executedActions,
    'queue': <String, dynamic>{'queue': queue, 'size': queue.length},
    'transactions': <Map<String, dynamic>>[transaction],
    'mutations': mutations,
    'checkpoints': checkpointBody.isNotEmpty
        ? <Map<String, dynamic>>[checkpointBody]
        : <Map<String, dynamic>>[],
    'federation': federation,
    'synchronization':
        (src['sync'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{},
    'state': state,
    'coordination': coordination,
    'schedule': schedule,
    'sandbox': sandbox,
    'policy': policy,
    'permissions': permissions,
    'rollback': rollbackResult,
    'recovery': recovery,
    'replay': replay,
    'transition': transition,
    'bounded': true,
  };
  payload['execution_ir'] = compileExecutionRuntimeIr(payload);
  return payload;
}

/// Port of run_execution_for_extraction.
///
/// The memory-checkpoint path (load/save) touches the filesystem and is
/// intentionally NOT exercised for parity: with memoryPath/memoryKey empty,
/// the function is fully deterministic. merge_graph uses the local list-of-IRs
/// graph merge (mergeRuntimeGraph), matching Python's
/// core.runtime_graph.build_runtime_graph.
Map<String, dynamic> runExecutionForExtraction({
  bool executionRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  Map<String, dynamic>? sources,
  List<Map<String, dynamic>>? workers,
  String runtime = 'browser',
  int tick = 0,
  bool simulateExecution = false,
  bool rollbackEnabled = true,
  bool mergeGraph = true,
}) {
  if (!executionRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  // NOTE: memory load path skipped for determinism — see doc comment.
  final Map<String, dynamic> stored = <String, dynamic>{};

  final Map<String, dynamic> result = runExecutionRuntime(
    sources: sources,
    stored: stored,
    workers: workers,
    runtime: runtime,
    tick: tick,
    simulate: simulateExecution,
    rollbackEnabled: rollbackEnabled,
  );

  final bool persisted = false;

  final Map<String, dynamic> executionIr =
      (result['execution_ir'] as Map?)?.cast<String, dynamic>() ??
          <String, dynamic>{};
  final Map<String, dynamic> graphIr = executionRuntimeIrToGraph(executionIr);
  Map<String, dynamic> unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = mergeRuntimeGraph(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'execution': result,
    'execution_ir': executionIr,
    'execution_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': (result['replay'] as Map?)?.cast<String, dynamic>() ??
        <String, dynamic>{},
    'simulation': (result['simulation'] as Map?)?.cast<String, dynamic>() ??
        <String, dynamic>{},
    'execution_persisted': persisted,
    'bounded': true,
  };
}
