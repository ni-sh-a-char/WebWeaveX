/// Pure deterministic builder engines for the runtime-memory family.
///
/// Faithful Dart port of the Python `core.memory.*` engines transitively
/// reached by `run_runtime_memory` / `run_memory_for_extraction` /
/// `search_runtime_memory`. Every list ordering mirrors Python `sorted`
/// (stable, index-tiebreak) and every Map mirrors the exact value structure
/// Python builds so `computeDeterministicHash` is byte-identical.
library;

import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Stable sort matching CPython `sorted`: compares by [keyOf], breaking ties on
/// original index so equal keys preserve insertion order.
List<T> stableSortBy<T>(
  List<T> items,
  Comparable<dynamic> Function(T item) keyOf,
) {
  final List<MapEntry<int, T>> indexed = <MapEntry<int, T>>[
    for (int i = 0; i < items.length; i++) MapEntry<int, T>(i, items[i]),
  ];
  indexed.sort((MapEntry<int, T> a, MapEntry<int, T> b) {
    final int c = keyOf(a.value).compareTo(keyOf(b.value));
    if (c != 0) return c;
    return a.key.compareTo(b.key);
  });
  return <T>[for (final MapEntry<int, T> e in indexed) e.value];
}

/// Stable sort by a list of (string) sub-keys, lexicographic, index tiebreak.
List<T> stableSortByKeys<T>(
  List<T> items,
  List<String> Function(T item) keysOf,
) {
  final List<MapEntry<int, T>> indexed = <MapEntry<int, T>>[
    for (int i = 0; i < items.length; i++) MapEntry<int, T>(i, items[i]),
  ];
  indexed.sort((MapEntry<int, T> a, MapEntry<int, T> b) {
    final List<String> ka = keysOf(a.value);
    final List<String> kb = keysOf(b.value);
    for (int i = 0; i < ka.length; i++) {
      final int c = ka[i].compareTo(kb[i]);
      if (c != 0) return c;
    }
    return a.key.compareTo(b.key);
  });
  return <T>[for (final MapEntry<int, T> e in indexed) e.value];
}

String _str(dynamic v) => v == null ? '' : v.toString();

int _intTick(Map<String, dynamic> item) {
  final dynamic tick = item.containsKey('tick')
      ? item['tick']
      : (item.containsKey('step') ? item['step'] : 0);
  if (tick is int) return tick;
  if (tick is num) return tick.toInt();
  return int.tryParse(tick.toString()) ?? 0;
}

// ---------------------------------------------------------------------------
// stable_memory_hash.py
// ---------------------------------------------------------------------------

String stableMemoryHash(Map<String, dynamic> memory) {
  final List<Map<String, dynamic>> history =
      _mapList(memory['runtime_history']);
  final List<Map<String, dynamic>> lineage = _mapList(memory['lineage']);
  final List<Map<String, dynamic>> relations =
      _mapList(memory['semantic_relations']);

  final Map<String, dynamic> canonical = <String, dynamic>{
    'memory_id': memory['memory_id'] ?? '',
    'runtime_history': stableSortByKeys<Map<String, dynamic>>(
      history,
      (Map<String, dynamic> h) => <String>[
        _intTick(h).toString().padLeft(20, '0'),
        _str(h['kind']),
        _str(h['source']),
      ],
    ),
    'lineage': stableSortBy<Map<String, dynamic>>(
        lineage, (Map<String, dynamic> x) => _str(x['id'])),
    'semantic_relations': stableSortByKeys<Map<String, dynamic>>(
      relations,
      (Map<String, dynamic> r) => <String>[_str(r['from']), _str(r['to'])],
    ),
  };
  // Python uses json.dumps(sort_keys=True, separators=(",",":")) then sha256.
  final String payload = _compactSortedJson(canonical);
  return sha256.convert(utf8.encode(payload)).toString();
}

/// json.dumps(value, sort_keys=True, separators=(",",":")) equivalent.
String _compactSortedJson(dynamic value) {
  if (value is Map) {
    final List<String> keys =
        value.keys.map((dynamic k) => k.toString()).toList()..sort();
    final StringBuffer b = StringBuffer('{');
    for (int i = 0; i < keys.length; i++) {
      if (i > 0) b.write(',');
      b.write(jsonEncode(keys[i]));
      b.write(':');
      b.write(_compactSortedJson(value[keys[i]]));
    }
    b.write('}');
    return b.toString();
  }
  if (value is List) {
    final StringBuffer b = StringBuffer('[');
    for (int i = 0; i < value.length; i++) {
      if (i > 0) b.write(',');
      b.write(_compactSortedJson(value[i]));
    }
    b.write(']');
    return b.toString();
  }
  return jsonEncode(value);
}

List<Map<String, dynamic>> _mapList(dynamic v) {
  if (v is List) {
    return <Map<String, dynamic>>[
      for (final dynamic e in v)
        if (e is Map) Map<String, dynamic>.from(e),
    ];
  }
  return <Map<String, dynamic>>[];
}

// ---------------------------------------------------------------------------
// runtime_history_engine.py
// ---------------------------------------------------------------------------

List<Map<String, dynamic>> appendRuntimeHistory(
  List<Map<String, dynamic>> history,
  Map<String, dynamic> entry,
) {
  final List<Map<String, dynamic>> updated =
      List<Map<String, dynamic>>.from(history)..add(entry);
  final List<Map<String, dynamic>> sorted = stableSortBy<Map<String, dynamic>>(
      updated, (Map<String, dynamic> item) => _intTick(item));
  return sorted.length > 100000 ? sorted.sublist(0, 100000) : sorted;
}

// ---------------------------------------------------------------------------
// runtime_memory_engine.py — build_runtime_memory
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeMemory({
  List<Map<String, dynamic>>? runtimeHistory,
  List<Map<String, dynamic>>? lineage,
  List<Map<String, dynamic>>? semanticRelations,
}) {
  final List<Map<String, dynamic>> history = List<Map<String, dynamic>>.from(
      runtimeHistory ?? <Map<String, dynamic>>[]);
  final List<Map<String, dynamic>> lin =
      List<Map<String, dynamic>>.from(lineage ?? <Map<String, dynamic>>[]);
  final List<Map<String, dynamic>> rels = List<Map<String, dynamic>>.from(
      semanticRelations ?? <Map<String, dynamic>>[]);

  final List<String> parts = <String>[
    for (final Map<String, dynamic> item in history)
      (item.containsKey('tick')
              ? item['tick']
              : (item.containsKey('step') ? item['step'] : ''))
          .toString(),
    for (final Map<String, dynamic> item in lin) _str(item['id']),
  ];
  final String memoryId =
      sha256.convert(utf8.encode(parts.join('|'))).toString().substring(0, 32);

  final Map<String, dynamic> result = <String, dynamic>{
    'memory_id': memoryId,
    'runtime_history': stableSortBy<Map<String, dynamic>>(
        history, (Map<String, dynamic> item) => _intTick(item)),
    'workflow_history': <Map<String, dynamic>>[
      for (final Map<String, dynamic> item in history)
        if (item['kind'] == 'workflow') item,
    ],
    'synchronization_history': <Map<String, dynamic>>[
      for (final Map<String, dynamic> item in history)
        if (item['kind'] == 'sync') item,
    ],
    'evolution_history': <Map<String, dynamic>>[
      for (final Map<String, dynamic> item in history)
        if (item['kind'] == 'evolution') item,
    ],
    'lineage': stableSortBy<Map<String, dynamic>>(
        lin, (Map<String, dynamic> item) => _str(item['id'])),
    'semantic_relations': stableSortByKeys<Map<String, dynamic>>(
      rels,
      (Map<String, dynamic> item) =>
          <String>[_str(item['from']), _str(item['to'])],
    ),
    'bounded': true,
  };
  result['stable_hash'] = stableMemoryHash(result);
  return result;
}

// ---------------------------------------------------------------------------
// knowledge_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildKnowledgeMemory({
  List<Map<String, dynamic>>? entities,
  List<Map<String, dynamic>>? relations,
  Map<String, dynamic>? topology,
}) {
  final List<Map<String, dynamic>> ent =
      List<Map<String, dynamic>>.from(entities ?? <Map<String, dynamic>>[]);
  final List<Map<String, dynamic>> rels =
      List<Map<String, dynamic>>.from(relations ?? <Map<String, dynamic>>[]);
  final Map<String, dynamic> topo = topology ?? <String, dynamic>{};

  return <String, dynamic>{
    'entities': stableSortBy<Map<String, dynamic>>(
        ent, (Map<String, dynamic> item) => _str(item['id'])),
    'semantic_relations': stableSortByKeys<Map<String, dynamic>>(
      rels,
      (Map<String, dynamic> item) => <String>[
        _str(item['from']),
        _str(item['to']),
        _str(item['relation']),
      ],
    ),
    'runtime_graphs':
        List<dynamic>.from((topo['graphs'] as List<dynamic>?) ?? <dynamic>[]),
    'distributed_topology': Map<String, dynamic>.from(
        (topo['distributed'] as Map<dynamic, dynamic>?) ?? <String, dynamic>{}),
    'application_cognition': Map<String, dynamic>.from(
        (topo['application'] as Map<dynamic, dynamic>?) ?? <String, dynamic>{}),
    'operational_structures': List<dynamic>.from(
        (topo['operations'] as List<dynamic>?) ?? <dynamic>[]),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_memory_engine.py — build_semantic_memory
// ---------------------------------------------------------------------------

Map<String, dynamic> buildSemanticMemory(
  Map<String, dynamic>? semantic,
  List<Map<String, dynamic>>? history,
) {
  final Map<String, dynamic> sem = semantic ?? <String, dynamic>{};
  final List<Map<String, dynamic>> hist = history ?? <Map<String, dynamic>>[];
  final Map<String, dynamic> inner = (sem['semantic'] is Map)
      ? Map<String, dynamic>.from(sem['semantic'] as Map)
      : sem;

  final List<String> concepts = <String>[];
  final dynamic entitiesBlock = inner['entities'];
  final List<dynamic> innerEntities =
      (entitiesBlock is Map && entitiesBlock['entities'] is List)
          ? List<dynamic>.from(entitiesBlock['entities'] as List<dynamic>)
          : <dynamic>[];
  for (final dynamic entity in innerEntities) {
    if (entity is Map) {
      final String label = _str(entity.containsKey('label')
          ? entity['label']
          : (entity.containsKey('type') ? entity['type'] : ''));
      if (label.isNotEmpty) concepts.add(label);
    }
  }
  final List<String> uniqueSorted = (concepts.toSet().toList())..sort();

  final dynamic domainBlock = inner['domain'];
  final String domain = (domainBlock is Map) ? _str(domainBlock['domain']) : '';

  return <String, dynamic>{
    'semantic_convergence': List<String>.from(uniqueSorted),
    'recurring_concepts': List<String>.from(uniqueSorted),
    'recurring_workflows': <String>[
      for (final Map<String, dynamic> item in hist)
        if (item['kind'] == 'workflow') _str(item['objective']),
    ],
    'recurring_structures':
        (inner.keys.map((dynamic k) => k.toString()).toList()..sort()),
    'domain': domain,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_lineage_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeLineageMemory({
  List<Map<String, dynamic>>? selector,
  List<Map<String, dynamic>>? workflow,
  List<Map<String, dynamic>>? sync,
  List<Map<String, dynamic>>? evolution,
  List<Map<String, dynamic>>? extraction,
}) {
  final List<Map<String, dynamic>> lineage = <Map<String, dynamic>>[];
  final List<List<dynamic>> buckets = <List<dynamic>>[
    <dynamic>['selector', selector ?? <Map<String, dynamic>>[]],
    <dynamic>['workflow', workflow ?? <Map<String, dynamic>>[]],
    <dynamic>['sync', sync ?? <Map<String, dynamic>>[]],
    <dynamic>['evolution', evolution ?? <Map<String, dynamic>>[]],
    <dynamic>['extraction', extraction ?? <Map<String, dynamic>>[]],
  ];
  for (final List<dynamic> bucketPair in buckets) {
    final String bucket = bucketPair[0] as String;
    final List<Map<String, dynamic>> items =
        (bucketPair[1] as List<Map<String, dynamic>>);
    final int limit = items.length < 1000 ? items.length : 1000;
    for (int index = 0; index < limit; index++) {
      final Map<String, dynamic> item = items[index];
      lineage.add(<String, dynamic>{
        'id': _str(item.containsKey('id') ? item['id'] : '$bucket:$index'),
        'kind': bucket,
        'ancestor': _str(item['ancestor']),
      });
    }
  }

  List<Map<String, dynamic>> ancestry(String kind) => <Map<String, dynamic>>[
        for (final Map<String, dynamic> item in lineage)
          if (item['kind'] == kind) item,
      ];

  return <String, dynamic>{
    'lineage': stableSortByKeys<Map<String, dynamic>>(
      lineage,
      (Map<String, dynamic> item) =>
          <String>[_str(item['kind']), _str(item['id'])],
    ),
    'selector_ancestry': ancestry('selector'),
    'workflow_ancestry': ancestry('workflow'),
    'sync_ancestry': ancestry('sync'),
    'evolution_ancestry': ancestry('evolution'),
    'extraction_ancestry': ancestry('extraction'),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_graph_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeMemoryGraph(
  List<Map<String, dynamic>> entities,
  List<Map<String, dynamic>> relations,
) {
  final List<Map<String, dynamic>> nodes = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> edges = <Map<String, dynamic>>[];

  final int eLimit = entities.length < 10000 ? entities.length : 10000;
  for (int i = 0; i < eLimit; i++) {
    final Map<String, dynamic> entity = entities[i];
    final String nodeId = _str(entity.containsKey('id')
        ? entity['id']
        : (entity.containsKey('label') ? entity['label'] : ''));
    if (nodeId.isEmpty) continue;
    nodes.add(<String, dynamic>{
      'id': nodeId,
      'type': _str(entity.containsKey('type') ? entity['type'] : 'entity'),
    });
  }

  final int rLimit = relations.length < 10000 ? relations.length : 10000;
  for (int i = 0; i < rLimit; i++) {
    final Map<String, dynamic> relation = relations[i];
    edges.add(<String, dynamic>{
      'from': _str(relation['from']),
      'to': _str(relation['to']),
      'relation': _str(relation.containsKey('relation')
          ? relation['relation']
          : 'relates_to'),
    });
  }

  if (nodes.isEmpty) {
    nodes.add(<String, dynamic>{'id': 'memory:root', 'type': 'memory'});
  }

  return <String, dynamic>{
    'nodes': stableSortBy<Map<String, dynamic>>(
        nodes, (Map<String, dynamic> item) => _str(item['id'])),
    'edges': stableSortByKeys<Map<String, dynamic>>(
      edges,
      (Map<String, dynamic> item) => <String>[
        _str(item['from']),
        _str(item['to']),
        _str(item['relation']),
      ],
    ),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_index_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeIndex({
  required List<Map<String, dynamic>> entities,
  required List<Map<String, dynamic>> workflows,
  required List<Map<String, dynamic>> graphs,
  required List<Map<String, dynamic>> streams,
  required List<Map<String, dynamic>> connectors,
}) {
  final Map<String, dynamic> entityIndex = <String, dynamic>{};
  for (final Map<String, dynamic> item in entities) {
    final bool hasId = item['id'] != null && _str(item['id']).isNotEmpty;
    final bool hasLabel =
        item['label'] != null && _str(item['label']).isNotEmpty;
    if (!hasId && !hasLabel) continue;
    final String key = _str(item.containsKey('id') && item['id'] != null
        ? item['id']
        : item['label']);
    entityIndex[key] = item;
  }
  final Map<String, dynamic> workflowIndex = <String, dynamic>{};
  for (final Map<String, dynamic> item in workflows) {
    final String key = _str(item.containsKey('id') && item['id'] != null
        ? item['id']
        : item['objective']);
    workflowIndex[key] = item;
  }
  final Map<String, dynamic> graphIndex = <String, dynamic>{
    for (int i = 0; i < graphs.length; i++) i.toString(): graphs[i],
  };

  Map<String, dynamic> sortedByKey(Map<String, dynamic> m) {
    final List<String> keys = m.keys.toList()..sort();
    return <String, dynamic>{for (final String k in keys) k: m[k]};
  }

  return <String, dynamic>{
    'entity_index': sortedByKey(entityIndex),
    'workflow_index': sortedByKey(workflowIndex),
    'graph_index': graphIndex,
    'stream_index': <String, dynamic>{
      for (int i = 0; i < streams.length; i++) i.toString(): streams[i],
    },
    'connector_index': <String, dynamic>{
      for (int i = 0; i < connectors.length; i++) i.toString(): connectors[i],
    },
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_replication_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> replicateRuntimeMemory(
  Map<String, dynamic> source,
  List<Map<String, dynamic>> nodes,
) {
  final List<Map<String, dynamic>> replicas = <Map<String, dynamic>>[];
  final int limit = nodes.length < 1000 ? nodes.length : 1000;
  for (int index = 0; index < limit; index++) {
    final Map<String, dynamic> node = nodes[index];
    replicas.add(<String, dynamic>{
      'node_id':
          _str(node.containsKey('node_id') ? node['node_id'] : 'node:$index'),
      'memory_id': _str(source['memory_id']),
      'runtime_history': List<dynamic>.from(
          (source['runtime_history'] as List<dynamic>?) ?? <dynamic>[]),
      'lineage': List<dynamic>.from(
          (source['lineage'] as List<dynamic>?) ?? <dynamic>[]),
      'replicated': true,
    });
  }
  return <String, dynamic>{
    'replicas': replicas,
    'replica_count': replicas.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_convergence_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> convergeRuntimeMemory(
    List<Map<String, dynamic>> replicas) {
  if (replicas.isEmpty) {
    return <String, dynamic>{
      'converged': true,
      'memory_id': '',
      'bounded': true
    };
  }
  final Map<String, dynamic> base = replicas[0];
  for (int i = 1; i < replicas.length; i++) {
    if (replicas[i]['memory_id'] != base['memory_id']) {
      return <String, dynamic>{
        'converged': false,
        'conflict': true,
        'bounded': true,
      };
    }
  }
  return <String, dynamic>{
    'converged': true,
    'memory_id': _str(base['memory_id']),
    'replica_count': replicas.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// distributed_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildDistributedMemory(List<Map<String, dynamic>> nodes) {
  final List<Map<String, dynamic>> merged = stableSortBy<Map<String, dynamic>>(
      nodes, (Map<String, dynamic> item) => _str(item['node_id']));

  bool allSynced = true;
  int conflicts = 0;
  for (final Map<String, dynamic> item in merged) {
    final dynamic synced = item.containsKey('synced') ? item['synced'] : true;
    if (synced != true) allSynced = false;
    final dynamic cr = item['conflicts_resolved'];
    if (cr is int) {
      conflicts += cr;
    } else if (cr is num) {
      conflicts += cr.toInt();
    } else if (cr != null) {
      conflicts += int.tryParse(cr.toString()) ?? 0;
    }
  }

  return <String, dynamic>{
    'nodes': merged,
    'replication': merged.length,
    'synchronized': allSynced,
    'conflicts_resolved': conflicts,
    'converged': merged.isNotEmpty,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_federation_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> federateRuntimeMemory(
    List<Map<String, dynamic>> memories) {
  final List<Map<String, dynamic>> fedHistory = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> fedLineage = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> fedRelations = <Map<String, dynamic>>[];

  for (final Map<String, dynamic> memory in memories) {
    fedHistory.addAll(_mapList(memory['runtime_history']));
    fedLineage.addAll(_mapList(memory['lineage']));
    fedRelations.addAll(_mapList(memory['semantic_relations']));
  }

  return <String, dynamic>{
    'federated_count': memories.length,
    'runtime_history': stableSortBy<Map<String, dynamic>>(
        fedHistory, (Map<String, dynamic> item) => _intTick(item)),
    'lineage': stableSortBy<Map<String, dynamic>>(
        fedLineage, (Map<String, dynamic> item) => _str(item['id'])),
    'semantic_relations': stableSortByKeys<Map<String, dynamic>>(
      fedRelations,
      (Map<String, dynamic> item) =>
          <String>[_str(item['from']), _str(item['to'])],
    ),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_merge_engine.py — merge_runtime_memories
// NOTE: Python mutates each memory's runtime_history in place (aliasing the
// `runtime` dict that the orchestrator later returns). We replicate that
// side-effect by sorting the live maps before federating.
// ---------------------------------------------------------------------------

Map<String, dynamic> mergeRuntimeMemories(List<Map<String, dynamic>> memories) {
  final List<Map<String, dynamic>> ordered = stableSortBy<Map<String, dynamic>>(
    memories,
    (Map<String, dynamic> m) =>
        _str(m.containsKey('memory_id') ? m['memory_id'] : m['runtime_id']),
  );
  for (final Map<String, dynamic> mem in ordered) {
    final dynamic history = mem['runtime_history'];
    if (history is List) {
      mem['runtime_history'] = stableSortByKeys<Map<String, dynamic>>(
        _mapList(history),
        (Map<String, dynamic> h) => <String>[
          _intTick(h).toString().padLeft(20, '0'),
          _str(h['kind']),
          _str(h['source']),
        ],
      );
    }
  }
  final Map<String, dynamic> federated = federateRuntimeMemory(ordered);
  return buildRuntimeMemory(
    runtimeHistory: _mapList(federated['runtime_history']),
    lineage: _mapList(federated['lineage']),
    semanticRelations: _mapList(federated['semantic_relations']),
  );
}

// ---------------------------------------------------------------------------
// runtime_memory_policy_engine.py
// ---------------------------------------------------------------------------

const int maxHistory = 100000;
const int maxLineage = 100000;
const int maxReplay = 10000;
const int maxReplicationDepth = 1000;
const int maxFederationNodes = 1000;

Map<String, dynamic> buildRuntimeMemoryPolicy() => <String, dynamic>{
      'memory_bounds': maxHistory,
      'replay_limits': maxReplay,
      'synchronization_ceilings': maxLineage,
      'replication_depth': maxReplicationDepth,
      'federation_constraints': maxFederationNodes,
      'bounded': true,
    };

Map<String, dynamic> enforceMemoryPolicy(
  Map<String, dynamic> policy,
  List<Map<String, dynamic>> history,
  List<Map<String, dynamic>> lineage,
  int replicas,
) {
  final bool within = history.length <= (policy['memory_bounds'] as int) &&
      lineage.length <= (policy['synchronization_ceilings'] as int) &&
      replicas <= (policy['replication_depth'] as int);
  return <String, dynamic>{
    'within_bounds': within,
    'history_count': history.length,
    'lineage_count': lineage.length,
    'replicas': replicas,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_diff_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> diffRuntimeMemory(
  Map<String, dynamic> previous,
  Map<String, dynamic> current,
) {
  final Set<String> prevIds = <String>{
    for (final Map<String, dynamic> item in _mapList(previous['lineage']))
      _str(item['id']),
  };
  final Set<String> currIds = <String>{
    for (final Map<String, dynamic> item in _mapList(current['lineage']))
      _str(item['id']),
  };
  final List<String> added = currIds.difference(prevIds).toList()..sort();
  final List<String> removed = prevIds.difference(currIds).toList()..sort();

  return <String, dynamic>{
    'memory_changed': previous['memory_id'] != current['memory_id'],
    'lineage_added': added,
    'lineage_removed': removed,
    'history_delta': _mapList(current['runtime_history']).length -
        _mapList(previous['runtime_history']).length,
    'revertible': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_snapshot_memory_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> captureMemorySnapshot(
  Map<String, dynamic> state, {
  int tick = 0,
}) =>
    <String, dynamic>{
      'snapshot_id': 'memory_snapshot:$tick',
      'tick': tick,
      'state': Map<String, dynamic>.from(state),
      'bounded': true,
    };

// ---------------------------------------------------------------------------
// runtime_query_engine.py — query_runtime_memory
// ---------------------------------------------------------------------------

Map<String, dynamic> queryRuntimeMemory(
  Map<String, dynamic> memory, [
  String queryType = 'semantic',
  String term = '',
]) {
  final List<Map<String, dynamic>> results = <Map<String, dynamic>>[];

  if (queryType == 'semantic') {
    for (final Map<String, dynamic> r
        in _mapList(memory['semantic_relations'])) {
      if (_str(r['from']).contains(term) || _str(r['to']).contains(term)) {
        results.add(r);
      }
    }
  } else if (queryType == 'lineage') {
    for (final Map<String, dynamic> item in _mapList(memory['lineage'])) {
      if (_str(item['id']).contains(term)) results.add(item);
    }
  } else if (queryType == 'topology') {
    for (final Map<String, dynamic> item
        in _mapList(memory['runtime_history'])) {
      if (_str(item['runtime']).contains(term)) results.add(item);
    }
  } else if (queryType == 'sync') {
    results.addAll(_mapList(memory['synchronization_history']));
  } else {
    for (final Map<String, dynamic> item
        in _mapList(memory['runtime_history'])) {
      if (pythonRepr(item).contains(term)) results.add(item);
    }
  }

  return <String, dynamic>{
    'query_type': queryType,
    'term': term,
    'results': stableSortBy<Map<String, dynamic>>(
        results, (Map<String, dynamic> item) => pythonRepr(item)),
    'count': results.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_memory_ir.py
// ---------------------------------------------------------------------------

Map<String, dynamic> compileRuntimeMemoryIr(Map<String, dynamic> payload) =>
    <String, dynamic>{
      'ir': 'runtime_memory',
      'memory_graphs': payload['graph'] ?? <String, dynamic>{},
      'semantic_indexes': payload['index'] ?? <String, dynamic>{},
      'lineage': payload['lineage'] ?? <String, dynamic>{},
      'runtime_history': payload['runtime'] ?? <String, dynamic>{},
      'distributed_memory': payload['distributed'] ?? <String, dynamic>{},
      'knowledge': payload['knowledge'] ?? <String, dynamic>{},
      'semantic': payload['semantic'] ?? <String, dynamic>{},
      'bounded': true,
    };

Map<String, dynamic> runtimeMemoryIrToGraph(Map<String, dynamic> memoryIr) {
  final Map<String, dynamic> graph = (memoryIr['memory_graphs'] is Map)
      ? Map<String, dynamic>.from(memoryIr['memory_graphs'] as Map)
      : <String, dynamic>{};
  List<Map<String, dynamic>> nodes = _mapList(graph['nodes']);
  final List<Map<String, dynamic>> edges = _mapList(graph['edges']);

  if (nodes.isEmpty) {
    nodes = <Map<String, dynamic>>[
      <String, dynamic>{'id': 'memory:root', 'type': 'memory'},
    ];
  }

  return <String, dynamic>{
    'ir': 'runtime_memory_graph',
    'nodes': stableSortBy<Map<String, dynamic>>(
        nodes, (Map<String, dynamic> item) => _str(item['id'])),
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_graph_engine.py — build_runtime_graph (LIST-of-IRs merge, ported
// privately for the family). Deterministic, source-preserving.
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeGraphFromIrs(
    List<Map<String, dynamic>> runtimeIrs) {
  final List<Map<String, dynamic>> nodes = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> edges = <Map<String, dynamic>>[];
  final Set<String> seenNodes = <String>{};
  final Set<String> seenEdges = <String>{};

  final int irLimit = runtimeIrs.length < 10000 ? runtimeIrs.length : 10000;
  for (int r = 0; r < irLimit; r++) {
    final Map<String, dynamic> runtime = runtimeIrs[r];
    final String runtimeType =
        _str(runtime.containsKey('ir') ? runtime['ir'] : 'unknown');

    for (final Map<String, dynamic> node in _mapList(runtime['nodes'])) {
      final String nodeId = _str(node['id']).trim();
      if (nodeId.isEmpty || seenNodes.contains(nodeId)) continue;
      seenNodes.add(nodeId);
      final Map<String, dynamic> enriched = Map<String, dynamic>.from(node)
        ..['runtime_type'] = runtimeType;
      nodes.add(enriched);
    }

    for (final Map<String, dynamic> edge in _mapList(runtime['edges'])) {
      final String src = _str(edge['from']).trim();
      final String dst = _str(edge['to']).trim();
      final String relation =
          _str(edge.containsKey('relation') ? edge['relation'] : 'related_to')
              .trim();
      if (src.isEmpty || dst.isEmpty) continue;
      final String edgeKey = '$src $dst $relation';
      if (seenEdges.contains(edgeKey)) continue;
      seenEdges.add(edgeKey);
      final Map<String, dynamic> enriched = Map<String, dynamic>.from(edge)
        ..['runtime_type'] = runtimeType;
      edges.add(enriched);
    }
  }

  return <String, dynamic>{
    'ir': 'unified_runtime_graph',
    'nodes': stableSortBy<Map<String, dynamic>>(
        nodes, (Map<String, dynamic> x) => _str(x['id'])),
    'edges': stableSortByKeys<Map<String, dynamic>>(
      edges,
      (Map<String, dynamic> x) => <String>[
        _str(x['from']),
        _str(x['to']),
        _str(x['relation']),
      ],
    ),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// search_runtime_memory — runtime_search_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> searchRuntimeMemory(
  Map<String, dynamic> index,
  String term, [
  String searchType = 'structural',
]) {
  final List<Map<String, dynamic>> matches = <Map<String, dynamic>>[];
  final String normalized = term.toLowerCase().trim();

  Map<String, dynamic> bucket(String name) => (index[name] is Map)
      ? Map<String, dynamic>.from(index[name] as Map)
      : <String, dynamic>{};

  if (searchType == 'semantic') {
    final Map<String, dynamic> b = bucket('entity_index');
    for (final String key in b.keys) {
      if (key.toLowerCase().contains(normalized)) {
        matches.add(<String, dynamic>{
          'match': key,
          'value': b[key],
          'kind': 'entity',
        });
      }
    }
  } else if (searchType == 'lineage') {
    final Map<String, dynamic> b = bucket('workflow_index');
    for (final String key in b.keys) {
      if (key.toLowerCase().contains(normalized)) {
        matches.add(<String, dynamic>{
          'match': key,
          'value': b[key],
          'kind': 'workflow',
        });
      }
    }
  } else if (searchType == 'graph') {
    final Map<String, dynamic> b = bucket('graph_index');
    for (final String key in b.keys) {
      matches.add(<String, dynamic>{
        'match': key,
        'value': b[key],
        'kind': 'graph',
      });
    }
  } else {
    for (final String name in <String>[
      'entity_index',
      'workflow_index',
      'connector_index'
    ]) {
      final Map<String, dynamic> b = bucket(name);
      for (final String key in b.keys) {
        if (key.toLowerCase().contains(normalized) ||
            pythonRepr(b[key]).toLowerCase().contains(normalized)) {
          matches.add(<String, dynamic>{
            'match': key,
            'value': b[key],
            'kind': name,
          });
        }
      }
    }
  }

  return <String, dynamic>{
    'search_type': searchType,
    'term': term,
    'matches': stableSortBy<Map<String, dynamic>>(
        matches, (Map<String, dynamic> item) => _str(item['match'])),
    'count': matches.length,
    'bounded': true,
  };
}

/// Python `str(obj)` repr for dict/list/scalars — used by search/query sort &
/// substring filters so behaviour matches CPython exactly.
String pythonRepr(dynamic value) {
  if (value is Map) {
    final StringBuffer b = StringBuffer('{');
    bool first = true;
    value.forEach((dynamic k, dynamic v) {
      if (!first) b.write(', ');
      first = false;
      b.write(pythonReprScalar(k));
      b.write(': ');
      b.write(pythonRepr(v));
    });
    b.write('}');
    return b.toString();
  }
  if (value is List) {
    final StringBuffer b = StringBuffer('[');
    for (int i = 0; i < value.length; i++) {
      if (i > 0) b.write(', ');
      b.write(pythonRepr(value[i]));
    }
    b.write(']');
    return b.toString();
  }
  return pythonReprScalar(value);
}

String pythonReprScalar(dynamic value) {
  if (value is String) return "'$value'";
  if (value is bool) return value ? 'True' : 'False';
  if (value == null) return 'None';
  return value.toString();
}
