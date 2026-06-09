// Port of core/workflows/workflow_orchestrator.py
import 'objective_engine.dart';
import 'unified_runtime_graph.dart';
import 'workflow_alignment_engine.dart';
import 'workflow_dependency_engine.dart';
import 'workflow_execution_engine.dart';
import 'workflow_federation_engine.dart';
import 'workflow_graph_engine.dart';
import 'workflow_memory_engine.dart';
import 'workflow_navigation_engine.dart';
import 'workflow_planner_engine.dart';
import 'workflow_recovery_engine.dart';
import 'workflow_replay_engine.dart';
import 'workflow_runtime_engine.dart';
import 'workflow_runtime_ir.dart';
import 'workflow_scheduler_engine.dart';
import 'workflow_semantic_alignment_engine.dart';
import 'workflow_state_engine.dart';
import 'workflow_transition_engine.dart';

Map<String, dynamic> runAutonomousWorkflow({
  String objective = 'extract_dashboard',
  int priority = 0,
  Map<String, dynamic>? semanticRuntime,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? distributedResult,
  Map<String, dynamic>? nativeCognition,
  String url = '',
  Map<String, dynamic>? memory,
  int tick = 0,
  List<String>? failures,
}) {
  final Map<String, dynamic> workingMemory =
      Map<String, dynamic>.from(memory ?? <String, dynamic>{});
  final Map<String, dynamic> runtimeObjective =
      buildRuntimeObjective(objective, priority);

  final Map<String, dynamic> semanticOuter =
      semanticRuntime ?? <String, dynamic>{};
  final dynamic semanticInnerRaw = semanticOuter['semantic'];
  final Map<String, dynamic> semanticInner = semanticInnerRaw is Map
      ? Map<String, dynamic>.from(semanticInnerRaw)
      : semanticOuter;

  final Map<String, dynamic> plan = buildWorkflowPlan(
    objective,
    semanticRuntime: semanticInner,
    causality: causalityResult,
    applicationRuntime: applicationResult,
  );
  plan['priority'] = priority;

  final Map<String, dynamic> execution = executeWorkflowPlan(plan, tick: tick);
  final Map<String, dynamic> state = buildWorkflowState(plan, execution);
  final Map<String, dynamic> navigation =
      navigateRuntimeWorkflow(plan, tick: tick);
  final List<Map<String, dynamic>> transitions =
      buildWorkflowTransitions(execution);
  final Map<String, dynamic> dependencies = buildWorkflowDependencies(plan);
  final Map<String, dynamic> recovery = recoverWorkflowRuntime(state, failures);
  final Map<String, dynamic> alignment =
      alignWorkflowRuntime(plan, state, execution);
  final Map<String, dynamic> semanticAlignment = alignWorkflowSemantics(
    plan,
    semanticRuntime: semanticRuntime,
    causality: causalityResult,
  );

  final List<dynamic> workers =
      (distributedResult != null && distributedResult['workers'] is List)
          ? List<dynamic>.from(distributedResult['workers'] as List<dynamic>)
          : <dynamic>[];
  final Map<String, dynamic> federation = federateWorkflowRuntime(
    browser: <String, dynamic>{'url': url},
    native: nativeCognition,
    distributed: distributedResult,
    semantic: semanticRuntime,
    workers: workers,
  );

  final Map<String, dynamic> schedule =
      scheduleWorkflowExecution(<Map<String, dynamic>>[plan], tick: tick);

  final List<dynamic> planSteps = plan['steps'] is List
      ? List<dynamic>.from(plan['steps'] as List<dynamic>)
      : <dynamic>[];
  String primaryRuntime = 'browser';
  if (planSteps.isNotEmpty) {
    final dynamic first = planSteps[0];
    if (first is Map && first['runtime'] != null) {
      primaryRuntime = '${first['runtime']}';
    }
  }
  final Map<String, dynamic> context = buildWorkflowRuntimeContext(
    url: url,
    runtime: primaryRuntime,
    sources: <String, dynamic>{
      'semantic': semanticRuntime != null && semanticRuntime.isNotEmpty,
      'causality': causalityResult != null && causalityResult.isNotEmpty,
      'application': applicationResult != null && applicationResult.isNotEmpty,
      'distributed': distributedResult != null && distributedResult.isNotEmpty,
    },
  );

  final Map<String, dynamic> workflowGraph = buildWorkflowGraph(
    runtimeObjective,
    plan,
    state,
    execution,
    transitions,
  );

  final Map<String, dynamic> payload = <String, dynamic>{
    'objective': runtimeObjective,
    'plan': plan,
    'execution': execution,
    'state': state,
    'navigation': navigation,
    'transitions': transitions,
    'dependencies': dependencies,
    'recovery': recovery,
    'alignment': alignment,
    'semantic_alignment': semanticAlignment,
    'federation': federation,
    'schedule': schedule,
    'context': context,
    'workflow_graph': workflowGraph,
    'bounded': true,
  };

  final Map<String, dynamic> updatedMemory = rememberWorkflowRuntime(
    workingMemory,
    <String, dynamic>{
      'objectives': runtimeObjective,
      'workflow_states': state,
      'execution_graphs': execution,
      'semantic_checkpoints': <dynamic>[semanticAlignment],
      'runtime_transitions': transitions,
      'workflow_graph': workflowGraph,
    },
  );
  payload['memory'] = updatedMemory;
  payload['replay'] = replayWorkflowRuntime(updatedMemory);
  payload['workflow_ir'] = compileWorkflowRuntimeIr(payload);
  return payload;
}

Map<String, dynamic> runWorkflowForExtraction({
  bool autonomousWorkflow = true,
  String objective = 'extract_dashboard',
  String memoryPath = '',
  String memoryKey = '',
  String url = '',
  Map<String, dynamic>? semanticRuntime,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? distributedResult,
  Map<String, dynamic>? nativeCognition,
  bool mergeGraph = true,
  int tick = 0,
}) {
  if (!autonomousWorkflow) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  Map<String, dynamic> memory = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final Map<String, dynamic> loaded =
        loadWorkflowMemory(memoryPath, memoryKey);
    if (loaded['available'] == true) {
      final dynamic mem = loaded['memory'];
      memory = mem is Map ? Map<String, dynamic>.from(mem) : memory;
    }
  }

  final Map<String, dynamic> result = runAutonomousWorkflow(
    objective: objective,
    semanticRuntime: semanticRuntime,
    causalityResult: causalityResult,
    applicationResult: applicationResult,
    distributedResult: distributedResult,
    nativeCognition: nativeCognition,
    url: url,
    memory: memory,
    tick: tick,
  );

  bool persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final dynamic memOut = result['memory'];
    saveWorkflowMemory(
      memoryPath,
      memOut is Map ? Map<String, dynamic>.from(memOut) : <String, dynamic>{},
      memoryKey,
    );
    persisted = true;
  }

  final dynamic wfIrRaw = result['workflow_ir'];
  final Map<String, dynamic> wfIr =
      wfIrRaw is Map ? Map<String, dynamic>.from(wfIrRaw) : <String, dynamic>{};
  final Map<String, dynamic> graphIr = workflowRuntimeIrToGraph(wfIr);
  Map<String, dynamic> unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = buildUnifiedRuntimeGraph(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'workflow': result,
    'workflow_ir': wfIr,
    'workflow_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': result['replay'] ?? <String, dynamic>{},
    'memory_persisted': persisted,
    'bounded': true,
  };
}
