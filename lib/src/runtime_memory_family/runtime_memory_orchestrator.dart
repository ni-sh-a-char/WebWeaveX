/// Orchestrator for the runtime-memory family — port of
/// `core.memory.runtime_memory_orchestrator`.
library;

import 'runtime_memory_engines.dart';
import 'runtime_memory_persistence_engine.dart';

List<Map<String, dynamic>> _mapList(dynamic v) {
  if (v is List) {
    return <Map<String, dynamic>>[
      for (final dynamic e in v)
        if (e is Map) Map<String, dynamic>.from(e),
    ];
  }
  return <Map<String, dynamic>>[];
}

Map<String, dynamic> _asMap(dynamic v) =>
    (v is Map) ? Map<String, dynamic>.from(v) : <String, dynamic>{};

List<Map<String, dynamic>> _collectHistory(
  Map<String, dynamic> sources,
  int tick,
) {
  final List<Map<String, dynamic>> history = <Map<String, dynamic>>[];
  bool truthy(dynamic v) {
    if (v == null) return false;
    if (v is bool) return v;
    if (v is Map) return v.isNotEmpty;
    if (v is List) return v.isNotEmpty;
    if (v is String) return v.isNotEmpty;
    if (v is num) return v != 0;
    return true;
  }

  if (truthy(sources['workflow'])) {
    history.add(<String, dynamic>{
      'tick': tick,
      'kind': 'workflow',
      'source': 'workflow'
    });
  }
  if (truthy(sources['sync'])) {
    history
        .add(<String, dynamic>{'tick': tick, 'kind': 'sync', 'source': 'sync'});
  }
  if (truthy(sources['evolution'])) {
    history.add(<String, dynamic>{
      'tick': tick,
      'kind': 'evolution',
      'source': 'evolution'
    });
  }
  if (truthy(sources['live'])) {
    history.add(<String, dynamic>{
      'tick': tick,
      'kind': 'live',
      'source': 'connectors'
    });
  }
  if (truthy(sources['extraction'])) {
    history.add(<String, dynamic>{
      'tick': tick,
      'kind': 'extraction',
      'source': 'browser'
    });
  }
  return history;
}

Map<String, dynamic> runRuntimeMemory({
  Map<String, dynamic>? sources,
  Map<String, dynamic>? stored,
  List<Map<String, dynamic>>? nodes,
  int tick = 0,
}) {
  final Map<String, dynamic> src = sources ?? <String, dynamic>{};
  final Map<String, dynamic> storedMap =
      Map<String, dynamic>.from(stored ?? <String, dynamic>{});
  final List<Map<String, dynamic>> nodeList =
      List<Map<String, dynamic>>.from(nodes ??
          <Map<String, dynamic>>[
            <String, dynamic>{'node_id': 'primary', 'synced': true}
          ]);

  final Map<String, dynamic> priorRuntime = _asMap(storedMap['runtime']);
  List<Map<String, dynamic>> history =
      _mapList(priorRuntime['runtime_history']);
  for (final Map<String, dynamic> entry in _collectHistory(src, tick)) {
    history = appendRuntimeHistory(history, entry);
  }

  List<Map<String, dynamic>> entities = <Map<String, dynamic>>[];
  List<Map<String, dynamic>> relations = <Map<String, dynamic>>[];
  final Map<String, dynamic> semanticSrc = _asMap(src['semantic']);
  if (semanticSrc.isNotEmpty) {
    final Map<String, dynamic> inner = (semanticSrc['semantic'] is Map)
        ? _asMap(semanticSrc['semantic'])
        : semanticSrc;
    final Map<String, dynamic> entBlock = _asMap(inner['entities']);
    entities = _mapList(entBlock['entities']);
    relations = _mapList(entBlock['relations']);
  }

  final Map<String, dynamic> knowledge = buildKnowledgeMemory(
    entities: entities,
    relations: relations,
    topology: <String, dynamic>{
      'graphs': <dynamic>[_asMap(src['graph'])],
      'distributed': _asMap(src['distributed']),
      'application': _asMap(src['application']),
    },
  );
  final Map<String, dynamic> semantic =
      buildSemanticMemory(semanticSrc, history);

  final Map<String, dynamic> evolutionSrc = _asMap(src['evolution']);
  final List<Map<String, dynamic>> selectors =
      _mapList(_asMap(evolutionSrc['selector'])['selectors']);
  final Map<String, dynamic> lineage = buildRuntimeLineageMemory(
    selector: selectors,
    workflow: <Map<String, dynamic>>[
      <String, dynamic>{'id': 'wf:0', 'ancestor': ''}
    ],
    sync: _mapList(_asMap(src['sync'])['lineage']),
    evolution: _mapList(evolutionSrc['lineage']),
    extraction: <Map<String, dynamic>>[
      <String, dynamic>{'id': 'extract:$tick', 'ancestor': ''}
    ],
  );

  final Map<String, dynamic> runtime = buildRuntimeMemory(
    runtimeHistory: history,
    lineage: _mapList(lineage['lineage']),
    semanticRelations: _mapList(knowledge['semantic_relations']),
  );

  final Map<String, dynamic> graph = buildRuntimeMemoryGraph(
    _mapList(knowledge['entities']),
    _mapList(knowledge['semantic_relations']),
  );

  final Map<String, dynamic> workflowSrc = _asMap(src['workflow']);
  final Map<String, dynamic> liveSrc = _asMap(src['live']);
  final Map<String, dynamic> index = buildRuntimeIndex(
    entities: _mapList(knowledge['entities']),
    workflows: <Map<String, dynamic>>[
      <String, dynamic>{
        'id': workflowSrc.containsKey('objective')
            ? workflowSrc['objective']
            : 'operate'
      }
    ],
    graphs: <Map<String, dynamic>>[graph],
    streams: _mapList(_asMap(liveSrc['streams'])['streams']),
    connectors: <Map<String, dynamic>>[liveSrc],
  );

  final Map<String, dynamic> replication =
      replicateRuntimeMemory(runtime, nodeList);
  final Map<String, dynamic> convergence =
      convergeRuntimeMemory(_mapList(replication['replicas']));
  final Map<String, dynamic> distributed = buildDistributedMemory(nodeList);

  final List<Map<String, dynamic>> memSet = priorRuntime.isNotEmpty
      ? <Map<String, dynamic>>[runtime, priorRuntime]
      : <Map<String, dynamic>>[runtime];
  final Map<String, dynamic> federated = federateRuntimeMemory(memSet);
  // merge_runtime_memories mutates runtime['runtime_history'] in place — the
  // returned `runtime` object is later embedded in the payload, so this
  // side-effect IS observable (Python parity).
  final Map<String, dynamic> merged = mergeRuntimeMemories(memSet);

  final Map<String, dynamic> policy = buildRuntimeMemoryPolicy();
  final Map<String, dynamic> enforcement = enforceMemoryPolicy(
    policy,
    _mapList(runtime['runtime_history']),
    _mapList(runtime['lineage']),
    (replication['replica_count'] as int?) ?? 0,
  );

  final Map<String, dynamic> diff = priorRuntime.isNotEmpty
      ? diffRuntimeMemory(priorRuntime, runtime)
      : <String, dynamic>{'revertible': true};
  final Map<String, dynamic> snapshot = captureMemorySnapshot(
    <String, dynamic>{
      'runtime': runtime,
      'knowledge': knowledge,
      'graph': graph,
    },
    tick: tick,
  );

  final Map<String, dynamic> payload = <String, dynamic>{
    'runtime': runtime,
    'knowledge': knowledge,
    'semantic': semantic,
    'lineage': lineage,
    'graph': graph,
    'index': index,
    'distributed': distributed,
    'federation': federated,
    'merged': merged,
    'replication': replication,
    'convergence': convergence,
    'policy': policy,
    'enforcement': enforcement,
    'diff': diff,
    'snapshot': snapshot,
    'bounded': true,
  };

  payload['replay'] = <String, dynamic>{
    'lineage': _mapList(lineage['lineage']),
    'runtime_history': _mapList(runtime['runtime_history']),
    'memory_id': runtime['memory_id'] ?? '',
    'replayed': true,
    'bounded': true,
  };
  payload['memory_ir'] = compileRuntimeMemoryIr(payload);
  return payload;
}

Map<String, dynamic> runMemoryForExtraction({
  bool federatedMemory = true,
  String memoryPath = '',
  String memoryKey = '',
  Map<String, dynamic>? sources,
  List<Map<String, dynamic>>? nodes,
  int tick = 0,
  bool mergeGraph = true,
}) {
  if (!federatedMemory) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  Map<String, dynamic> stored = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final Map<String, dynamic> loaded =
        loadRuntimeMemory(memoryPath, memoryKey);
    if (loaded['available'] == true) {
      stored = _asMap(loaded['memory']);
    }
  }

  final Map<String, dynamic> result = runRuntimeMemory(
    sources: sources,
    stored: stored,
    nodes: nodes,
    tick: tick,
  );

  final Map<String, dynamic> store = <String, dynamic>{
    'runtime': _asMap(result['runtime']),
    'knowledge': _asMap(result['knowledge']),
    'semantic': _asMap(result['semantic']),
    'index': _asMap(result['index']),
    'graph': _asMap(result['graph']),
    'lineage': _asMap(result['lineage']),
    'snapshot': _asMap(result['snapshot']),
    'bounded': true,
  };

  bool persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveRuntimeMemory(memoryPath, store, memoryKey);
    persisted = true;
  }

  final Map<String, dynamic> graphIr =
      runtimeMemoryIrToGraph(_asMap(result['memory_ir']));
  Map<String, dynamic> unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = buildRuntimeGraphFromIrs(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'memory': result,
    'memory_ir': _asMap(result['memory_ir']),
    'memory_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': _asMap(result['replay']),
    'query': queryRuntimeMemory(_asMap(result['runtime']), 'semantic', ''),
    'search': searchRuntimeMemory(_asMap(result['index']), ''),
    'memory_persisted': persisted,
    'bounded': true,
  };
}
