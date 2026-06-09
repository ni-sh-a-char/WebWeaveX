import 'runtime_adaptation_engine.dart';
import 'runtime_convergence_engine.dart';
import 'runtime_diff_engine.dart';
import 'runtime_evolution_engine.dart';
import 'runtime_evolution_graph_engine.dart';
import 'runtime_lineage_engine.dart';
import 'runtime_memory_engine.dart';
import 'runtime_mutation_engine.dart';
import 'runtime_optimization_engine.dart';
import 'runtime_pattern_engine.dart';
import 'runtime_policy_engine.dart';
import 'runtime_recovery_engine.dart';
import 'runtime_repair_engine.dart';
import 'runtime_semantic_engine.dart';
import 'runtime_strategy_engine.dart';
import 'runtime_topology_engine.dart';
import 'runtime_workflow_engine.dart';
import 'selector_evolution_engine.dart';
import 'evolution_runtime_ir.dart';
import 'unified_runtime_graph.dart';

Map<String, dynamic> _asMap(dynamic v) =>
    v is Map ? Map<String, dynamic>.from(v) : <String, dynamic>{};

List<dynamic> _asList(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

List<Map<String, dynamic>> _asMapList(dynamic v) =>
    _asList(v).map((e) => Map<String, dynamic>.from(e as Map)).toList();

int _failureCount(List<dynamic> failures, String needle) =>
    failures.where((f) => f == needle).length;

/// Port of core/evolution_runtime/runtime_evolution_orchestrator.run_evolution_runtime
Map<String, dynamic> runEvolutionRuntime({
  Map<String, dynamic>? adaptiveMemory,
  Map<String, dynamic>? workflowResult,
  Map<String, dynamic>? semanticResult,
  Map<String, dynamic>? syncResult,
  Map<String, dynamic>? distributedResult,
  List<String>? failures,
  Map<String, dynamic>? memory,
  int tick = 0,
}) {
  final mem = Map<String, dynamic>.from(memory ?? <String, dynamic>{});
  final adaptive = adaptiveMemory ?? <String, dynamic>{};
  final fails = failures ?? <String>[];

  final healed = _asMap(adaptive['healed_selectors']);
  final selector = evolveSelectorRuntime(_asMap(adaptive['selectors']), healed);

  final workflowOuter = _asMap(workflowResult);
  final workflowInner = workflowOuter.containsKey('workflow')
      ? _asMap(workflowOuter['workflow'])
      : workflowOuter;
  final workflow = evolveWorkflowRuntime(
    _asMap(workflowInner['plan']),
    _asMap(workflowInner['execution']),
    _asList(mem['evolution_histories']),
  );

  final semantic = evolveSemanticRuntime(
    semanticResult,
    _asList(mem['evolution_histories']),
  );

  final syncOuter = _asMap(syncResult);
  final syncInner = syncOuter.containsKey('synchronization')
      ? _asMap(syncOuter['synchronization'])
      : syncOuter;
  final topology = evolveRuntimeTopology(
    _asList(_asMap(distributedResult)['workers']),
    syncInner,
    syncOuter['causality'] is Map
        ? _asMap(syncOuter['causality'])
        : (syncOuter['causality'] == null ? null : <String, dynamic>{}),
  );

  final drifts = _asList(_asMap(syncInner['drift'])['drifts']);
  final evidence = <String, dynamic>{
    'drift_count': drifts.length,
    'failed_steps': _failureCount(fails, 'failed_workflow'),
  };
  final strategy = buildRuntimeStrategy(evidence);
  final repairs = repairRuntimeFailures(fails, healed);
  final recovery = evolveRecoveryOrder(_asMapList(repairs['repairs']));

  final depth = _asList(workflow['execution_ordering']).length;
  final optimization = optimizeRuntimeExecution(
    depth: depth,
    replayCost: _asList(mem['evolution_histories']).length,
    syncOverhead: _asList(syncInner['deltas']).length,
  );
  final adaptedStrategy = adaptRuntimeStrategy(strategy, optimization);

  final mutations = buildRuntimeMutations(
    selector,
    workflow,
    semantic,
    _asMap(syncInner['convergence']),
  );
  final parentId = '${mem['last_evolution_id'] ?? ''}';
  final initialLineage = buildRuntimeLineage('', mutations, parentId);
  final evolution = buildRuntimeEvolution(mutations, initialLineage);
  final lineage = buildRuntimeLineage(
    '${evolution['evolution_id']}',
    mutations,
    parentId,
  );

  final policy = buildRuntimePolicy();
  final enforcement = enforceRuntimePolicy(
    policy,
    mutations,
    _asList(repairs['repairs']),
    depth,
  );

  final patterns = buildRuntimePatterns(
    ui: _asMap(_asMap(_asMap(semanticResult)['semantic'])['ui']),
    workflows: <dynamic>[_asMap(workflowInner['plan'])],
    semantic: semanticResult,
    syncHistory: _asList(mem['evolution_histories']),
  );

  final graph = buildRuntimeEvolutionGraph(evolution, repairs, optimization);

  final prior = _asMap(mem['last_evolution']);
  final diff = prior.isNotEmpty
      ? diffEvolutionRuntime(prior, evolution)
      : <String, dynamic>{'revertible': true};

  final distributedEvolutions = <Map<String, dynamic>>[evolution];
  final memDistributed = mem['distributed_evolutions'];
  if (memDistributed is List && memDistributed.isNotEmpty) {
    distributedEvolutions.addAll(_asMapList(memDistributed));
  }
  final convergence = convergeRuntimeEvolution(distributedEvolutions);

  final payload = <String, dynamic>{
    'evolution': evolution,
    'selector': selector,
    'workflow': workflow,
    'semantic': semantic,
    'topology': topology,
    'strategy': adaptedStrategy,
    'repairs': repairs,
    'recovery': recovery,
    'optimization': optimization,
    'patterns': patterns,
    'lineage': lineage,
    'graph': graph,
    'policy': policy,
    'enforcement': enforcement,
    'convergence': convergence,
    'diff': diff,
    'tick': tick,
    'bounded': true,
  };

  final trimmedDistributed = distributedEvolutions.length > 10
      ? distributedEvolutions.sublist(distributedEvolutions.length - 10)
      : distributedEvolutions;

  final updatedMemory = rememberEvolutionRuntime(
    mem,
    <String, dynamic>{
      'evolution_histories': <dynamic>[
        ..._asList(mem['evolution_histories']),
        evolution
      ],
      'selector_lineage': lineage,
      'workflow_evolution': workflow,
      'semantic_evolution': semantic,
      'optimization_histories': <dynamic>[
        ..._asList(mem['optimization_histories']),
        optimization
      ],
      'last_evolution': evolution,
      'last_evolution_id': evolution['evolution_id'],
      'distributed_evolutions': trimmedDistributed,
    },
  );
  payload['memory'] = updatedMemory;
  payload['replay'] = <String, dynamic>{
    'lineage': lineage,
    'evolution': evolution,
    'replayed': true,
    'bounded': true,
  };
  payload['evolution_ir'] = compileEvolutionRuntimeIr(payload);
  return payload;
}

/// Port of run_evolution_for_extraction
Map<String, dynamic> runEvolutionForExtraction({
  bool evolvingRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  Map<String, dynamic>? adaptiveMemory,
  Map<String, dynamic>? workflowResult,
  Map<String, dynamic>? semanticResult,
  Map<String, dynamic>? syncResult,
  Map<String, dynamic>? distributedResult,
  List<String>? failures,
  int tick = 0,
  bool mergeGraph = true,
}) {
  if (!evolvingRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  var memory = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final loaded = loadEvolutionRuntime(memoryPath, memoryKey);
    if (loaded['available'] == true) {
      final m = loaded['memory'];
      if (m is Map) memory = Map<String, dynamic>.from(m);
    }
  }

  final result = runEvolutionRuntime(
    adaptiveMemory: adaptiveMemory,
    workflowResult: workflowResult,
    semanticResult: semanticResult,
    syncResult: syncResult,
    distributedResult: distributedResult,
    failures: failures,
    memory: memory,
    tick: tick,
  );

  var persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveEvolutionRuntime(memoryPath, _asMap(result['memory']), memoryKey);
    persisted = true;
  }

  final graphIr = evolutionRuntimeIrToGraph(_asMap(result['evolution_ir']));
  var unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = buildUnifiedRuntimeGraph(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'evolution': result,
    'evolution_ir': _asMap(result['evolution_ir']),
    'evolution_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': _asMap(result['replay']),
    'memory_persisted': persisted,
    'bounded': true,
  };
}
