// Faithful Dart port of:
//   core/reconstruction/runtime_reconstruction_orchestrator.py
//   core/reconstruction/runtime_fabrication_engine.py
//   core/reconstruction/runtime_clone_engine.py
//   core/reconstruction/runtime_validation_engine.py
//   core/reconstruction/runtime_snapshot_engine.py (save/load)
//
// Public-name parity with the Python webweavex.__all__ reconstruction exports.

import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart' show encryptValue, decryptValue;
import '../evolution/unified_runtime_graph.dart' show buildUnifiedRuntimeGraph;
import 'reconstruction_runtime_engines.dart';

// ---------------------------------------------------------------------------
// run_reconstruction_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> runReconstructionRuntime({
  Map<String, dynamic>? sources,
  Map<String, dynamic>? stored,
  Map<String, dynamic>? runtimeGraph,
  String runtimeType = 'browser',
  int tick = 0,
  bool fabricate = false,
  bool clone = false,
}) {
  final src = sources ?? <String, dynamic>{};
  final storedMap = Map<String, dynamic>.from(stored ?? <String, dynamic>{});
  final graph = runtimeGraph ?? asMap(src['graph']);

  final semanticIr = asMap(
      getAny(src, <String>['semantic_ir', 'semantic'], <String, dynamic>{}));
  final workflowIr = asMap(
      getAny(src, <String>['workflow_ir', 'workflow'], <String, dynamic>{}));
  final syncIr =
      asMap(getAny(src, <String>['sync_ir', 'sync'], <String, dynamic>{}));
  final executionIr = asMap(
      getAny(src, <String>['execution_ir', 'execution'], <String, dynamic>{}));
  final memoryIr =
      asMap(getAny(src, <String>['memory_ir', 'memory'], <String, dynamic>{}));

  final runtime = reconstructRuntime(
    semanticIr: semanticIr,
    workflowIr: workflowIr,
    synchronizationIr: syncIr,
    executionIr: executionIr,
    memoryIr: memoryIr,
    runtimeGraph: graph,
    runtimeType: runtimeType,
    tick: tick,
  );

  final browser = reconstructBrowserRuntime(
    browserIr: asMap(
        getAny(src, <String>['browser_ir', 'browser'], <String, dynamic>{})),
    interactionIr: asMap(src['interaction_ir']),
    identity: asMap(src['identity']),
    session: asMap(src['session']),
    streaming:
        asMap(getAny(src, <String>['streaming', 'live'], <String, dynamic>{})),
    dom: asMap(src['dom']),
  );

  final application = reconstructApplicationRuntime(
    applicationIr: asMap(getAny(
        src, <String>['application_ir', 'application'], <String, dynamic>{})),
    workflowIr: workflowIr,
    executionIr: executionIr,
    runtimeType: runtimeType,
  );

  final session = reconstructRuntimeSession(
    session: asMap(src['session']),
    identity: asMap(src['identity']),
    syncState: syncIr,
    adaptiveMemory: asMap(src['adaptive_memory']),
  );

  final environment = buildRuntimeEnvironment(
    runtime: runtimeType,
    connectors: asList(src['connectors']),
    workers: asList(src['workers']),
  );

  // lineage = sources.get('lineage', memory_ir.get('lineage', {}))
  final dynamic lineage =
      src.containsKey('lineage') ? src['lineage'] : memoryIr['lineage'];

  final memoryRebuilt = reconstructRuntimeMemory(
    memoryIr: memoryIr,
    semantic: semanticIr,
    lineage: lineage ?? <String, dynamic>{},
  );

  // queues: execution_ir.get('queues',{}).get('queue',[]) if queues is dict
  final queuesRaw = executionIr['queues'];
  final queues = queuesRaw is Map ? asList(queuesRaw['queue']) : <dynamic>[];
  final mutationsRaw = executionIr['mutations'];
  final mutations =
      mutationsRaw is Map ? asList(mutationsRaw['mutations']) : <dynamic>[];
  final lineageSrc = src['lineage'];
  final executionLineage =
      lineageSrc is Map ? asList(lineageSrc['lineage']) : <dynamic>[];

  final state = rebuildRuntimeState(
    queues: queues,
    synchronization: syncIr,
    mutations: mutations,
    transactions: asList(executionIr['transactions']),
    memory: memoryRebuilt,
    executionLineage: executionLineage,
    workflows: asList(application['workflows']),
  );

  // workers: sources.get('workers', execution_ir.federation.workers)
  final topologyWorkers = src.containsKey('workers')
      ? asList(src['workers'])
      : asList(asMap(executionIr['federation'])['workers']);

  final topology = reconstructRuntimeTopology(
    runtimeGraph: graph,
    workers: topologyWorkers,
    connectors: asList(src['connectors']),
    executionTopology: asMap(executionIr['federation']),
    syncTopology: syncIr,
  );

  // execution_id = str(execution_ir.transactions[0].transaction_id) if any
  final txList = asMaps(executionIr['transactions']);
  final executionId =
      txList.isNotEmpty ? asStr(txList[0]['transaction_id']) : '';
  // worker_id = str((sources.get('workers') or [{}])[0].get('worker_id',''))
  final workersList = asMaps(src['workers']);
  final firstWorkerId =
      workersList.isNotEmpty ? asStr(workersList[0]['worker_id']) : '';

  final identity = reconstructRuntimeIdentity(
    browserIdentity: asMap(src['identity']),
    session: asMap(src['session']),
    runtimeId: asStr(runtime['runtime_id']),
    executionId: executionId,
    workerId: firstWorkerId,
  );

  final connectors = reconstructConnectorRuntime(
    connectors: asList(src['connectors']),
    liveIr:
        asMap(getAny(src, <String>['live', 'live_ir'], <String, dynamic>{})),
  );

  final actions = asList(executionIr['actions']);
  // synchronization = [{id:sync:i, tick:tick} for i,_ in enumerate(sync.lineage[:100])]
  final syncLineage = asList(syncIr['lineage']);
  final syncEvents = <Map<String, dynamic>>[];
  final boundedSync =
      syncLineage.length > 100 ? syncLineage.sublist(0, 100) : syncLineage;
  for (var i = 0; i < boundedSync.length; i++) {
    syncEvents.add(<String, dynamic>{'id': 'sync:$i', 'tick': tick});
  }

  final timeline = buildRuntimeTimeline(
    actions: actions,
    mutations: asList(state['mutations']),
    synchronization: syncEvents,
    execution: actions,
    tick: tick,
  );

  final replay = buildRuntimeReplay(
    actions: actions,
    transactions: asList(executionIr['transactions']),
    timeline: timeline,
    tick: tick,
  );

  var cloneResult = <String, dynamic>{};
  if (clone) {
    final sourceBody = <String, dynamic>{
      'runtime_graph': graph,
      'browser': browser,
      'application': application,
      'synchronization': syncIr,
      'workflows': asList(application['workflows']),
      'queues': asList(state['queues']),
    };
    cloneResult = cloneRuntimeEnvironment(sourceBody);
  }

  var fabrication = <String, dynamic>{};
  if (fabricate) {
    fabrication = fabricateRuntimeReality(
      runtime: runtime,
      environment: environment,
      browser: browser,
      application: application,
    );
  }

  final validation = validateReconstructedRuntime(
    runtime: !fabricate ? runtime : asMap(fabrication['runtime']),
    replay: replay,
    topology: topology,
    execution: executionIr,
    mutations: asList(state['mutations']),
  );

  final priorSnapshot = asMap(storedMap['snapshot']);
  final recovery = recoverReconstructedRuntime(checkpoint: priorSnapshot);

  final snapshot = captureReconstructionSnapshot(<String, dynamic>{
    'runtime': runtime,
    'browser': browser,
    'application': application,
    'topology': topology,
    'identities': identity,
    'workflows': asList(application['workflows']),
    'replay_chains': asList(replay['replay_chains']),
    'state': state,
  });

  final payload = <String, dynamic>{
    'runtime': runtime,
    'browser': browser,
    'application': application,
    'session': session,
    'environment': environment,
    'memory': memoryRebuilt,
    'state': state,
    'topology': topology,
    'identity': identity,
    'connectors': connectors,
    'timeline': timeline,
    'replay': replay,
    'clone': cloneResult,
    'fabrication': fabrication,
    'validation': validation,
    'recovery': recovery,
    'snapshot': snapshot,
    'bounded': true,
  };
  payload['reconstruction_ir'] = compileReconstructionRuntimeIr(payload);
  return payload;
}

// ---------------------------------------------------------------------------
// run_reconstruction_for_extraction
// ---------------------------------------------------------------------------

Map<String, dynamic> runReconstructionForExtraction({
  bool reconstructionRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  Map<String, dynamic>? sources,
  Map<String, dynamic>? runtimeGraph,
  String runtimeType = 'browser',
  int tick = 0,
  bool fabricateRuntime = false,
  bool cloneRuntime = false,
  bool mergeGraph = true,
}) {
  if (!reconstructionRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  var storedMap = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final loaded = loadReconstructionSnapshot(memoryPath, memoryKey);
    if (truthy(loaded['available'])) {
      storedMap = asMap(loaded['snapshot']);
    }
  }

  final result = runReconstructionRuntime(
    sources: sources,
    stored: storedMap,
    runtimeGraph: runtimeGraph,
    runtimeType: runtimeType,
    tick: tick,
    fabricate: fabricateRuntime,
    clone: cloneRuntime,
  );

  final store = captureReconstructionSnapshot(<String, dynamic>{
    'runtime': asMap(result['runtime']),
    'topology': asMap(result['topology']),
    'identities': asMap(result['identity']),
    'workflows': asList(asMap(result['application'])['workflows']),
    'replay_chains': asList(asMap(result['replay'])['replay_chains']),
    'state': asMap(result['state']),
  });

  var persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveReconstructionSnapshot(memoryPath, store, memoryKey);
    persisted = true;
  }

  final graphIr =
      reconstructionRuntimeIrToGraph(asMap(result['reconstruction_ir']));
  var unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = buildUnifiedRuntimeGraph(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'reconstruction': result,
    'reconstruction_ir': result['reconstruction_ir'] ?? <String, dynamic>{},
    'reconstruction_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': result['replay'] ?? <String, dynamic>{},
    'validation': result['validation'] ?? <String, dynamic>{},
    'reconstruction_persisted': persisted,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// fabricate_runtime_reality
// ---------------------------------------------------------------------------

Map<String, dynamic> fabricateRuntimeReality({
  Map<String, dynamic>? runtime,
  Map<String, dynamic>? environment,
  Map<String, dynamic>? browser,
  Map<String, dynamic>? application,
  bool portable = true,
}) {
  final base = runtime ??
      reconstructRuntime(
        runtimeType: asStr(
          environment != null
              ? (environment.containsKey('runtime')
                  ? environment['runtime']
                  : 'browser')
              : 'browser',
        ),
      );
  final fabricatedRuntime = <String, dynamic>{
    ...base,
    'environment':
        Map<String, dynamic>.from(environment ?? <String, dynamic>{}),
    'browser': Map<String, dynamic>.from(browser ?? <String, dynamic>{}),
    'application':
        Map<String, dynamic>.from(application ?? <String, dynamic>{}),
  };

  return <String, dynamic>{
    'fabricated': true,
    'runtime': fabricatedRuntime,
    'portable': portable,
    'replay_safe': true,
    'operational_twin': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// clone_runtime_environment
// ---------------------------------------------------------------------------

Map<String, dynamic> cloneRuntimeEnvironment(
  Map<String, dynamic> source, {
  bool includeGraph = true,
  bool includeQueues = true,
}) {
  dynamic deep(dynamic v) => v == null ? null : jsonDecode(jsonEncode(v));

  final browserState = source.containsKey('browser')
      ? source['browser']
      : (source.containsKey('browser_state')
          ? source['browser_state']
          : <String, dynamic>{});
  final appState = source.containsKey('application')
      ? source['application']
      : (source.containsKey('application_state')
          ? source['application_state']
          : <String, dynamic>{});
  final queuesV = source.containsKey('queues')
      ? source['queues']
      : (source.containsKey('execution_queues')
          ? source['execution_queues']
          : <dynamic>[]);
  final syncV = source.containsKey('synchronization')
      ? source['synchronization']
      : (source.containsKey('sync') ? source['sync'] : <String, dynamic>{});

  return <String, dynamic>{
    'runtime_graph': includeGraph
        ? deep(source.containsKey('runtime_graph')
            ? source['runtime_graph']
            : <String, dynamic>{})
        : <String, dynamic>{},
    'browser_state': deep(browserState),
    'application_state': deep(appState),
    'execution_queues': includeQueues ? deep(queuesV) : <dynamic>[],
    'synchronization_state': deep(syncV),
    'workflows': deep(
        source.containsKey('workflows') ? source['workflows'] : <dynamic>[]),
    'source_mutated': false,
    'cloned': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// validate_reconstructed_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> validateReconstructedRuntime({
  Map<String, dynamic>? runtime,
  Map<String, dynamic>? replay,
  Map<String, dynamic>? topology,
  Map<String, dynamic>? execution,
  dynamic mutations,
}) {
  final rt = runtime ?? <String, dynamic>{};
  final rp = replay ?? <String, dynamic>{};
  final tp = topology ?? <String, dynamic>{};
  final ex = execution ?? <String, dynamic>{};

  final replayOk = truthy(rp['replay_chains']) ||
      truthy(rp['replay_package']) ||
      truthy(rp['replayed']);
  bool syncOk;
  bool topologyOk;
  if (tp.isNotEmpty) {
    syncOk =
        truthy(tp['synchronization_topology']) || truthy(tp['reconstructed']);
    topologyOk = truthy(tp['runtime_graph']) || truthy(tp['reconstructed']);
  } else {
    syncOk = true;
    topologyOk = true;
  }
  final executionOk = truthy(ex['executed']) ||
      truthy(ex['actions']) ||
      truthy(rt['reconstructed']) ||
      truthy(rt['fabricated']);

  final List<dynamic> mutationList =
      mutations is Map ? asList(mutations['mutations']) : asList(mutations);
  final mutationOk = mutationList.isEmpty ||
      mutationList.every((dynamic m) =>
          m is Map && (m.containsKey('kind') || m.containsKey('target')));

  final checks = <bool>[
    replayOk || truthy(rt['replay_safe']),
    syncOk || topologyOk,
    topologyOk,
    executionOk,
    mutationOk,
  ];
  final valid = (truthy(rt['reconstructed']) || truthy(rt['fabricated']))
      ? checks.every((c) => c)
      : (truthy(rt) && replayOk);

  return <String, dynamic>{
    'valid': valid,
    'integrity_score': valid ? 1.0 : 0.0,
    'replay_integrity': replayOk,
    'synchronization_integrity': syncOk,
    'topology_integrity': topologyOk,
    'execution_integrity': executionOk,
    'mutation_consistency': mutationOk,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// snapshot persistence (save/load) — kaalka-encrypted, json.dumps(sort_keys)
// ---------------------------------------------------------------------------

Map<String, dynamic> saveReconstructionSnapshot(
  String path,
  Map<String, dynamic> snapshot,
  String key,
) {
  final payload = pyJsonSortKeys(snapshot);
  final encrypted = encryptValue(payload, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  final wrapper = <String, dynamic>{
    'encrypted': encrypted,
    'algorithm': 'kaalka',
  };
  target.writeAsStringSync(pyJsonSortKeys(wrapper));
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> loadReconstructionSnapshot(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'snapshot': _emptySnapshot(),
      'bounded': true,
    };
  }

  final wrapper = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  final decrypted = decryptValue(wrapper['encrypted'] as String, key);
  final snapshot = decrypted is Map
      ? Map<String, dynamic>.from(decrypted)
      : jsonDecode(decrypted as String) as Map<String, dynamic>;

  return <String, dynamic>{
    'available': true,
    'snapshot': snapshot,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _emptySnapshot() => <String, dynamic>{
      'state': <String, dynamic>{},
      'topology': <String, dynamic>{},
      'identities': <String, dynamic>{},
      'workflows': <dynamic>[],
      'replay_chains': <dynamic>[],
      'bounded': true,
    };
