// Native Dart port of the WebWeaveX Python `core.synchronization` runtime
// family. Faithful, deterministic, bounded — mirrors the exact output
// structure and key set of the Python reference so that
// `computeDeterministicHash` agrees byte-for-byte across languages.
//
// Reference: C:/Projects/WebWeaveX/core/synchronization/*.py
import 'dart:convert';

import 'package:crypto/crypto.dart';

import 'runtime_sync_memory.dart' show loadSyncMemory, saveSyncMemory;

// ---------------------------------------------------------------------------
// Small helpers (Python dict/list coercion semantics).
// ---------------------------------------------------------------------------

Map<String, dynamic> _asMap(dynamic value) {
  if (value is Map) return Map<String, dynamic>.from(value);
  return <String, dynamic>{};
}

List<dynamic> _asList(dynamic value) {
  if (value is List) return List<dynamic>.from(value);
  return <dynamic>[];
}

bool _truthy(dynamic value) {
  if (value == null) return false;
  if (value is bool) return value;
  if (value is Map) return value.isNotEmpty;
  if (value is List) return value.isNotEmpty;
  if (value is String) return value.isNotEmpty;
  if (value is num) return value != 0;
  return true;
}

int _asInt(dynamic value) {
  if (value is int) return value;
  if (value is num) return value.toInt();
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}

/// Deep structural equality matching Python `==` for JSON-shaped values.
bool _deepEquals(dynamic a, dynamic b) {
  if (identical(a, b)) return true;
  if (a is Map && b is Map) {
    if (a.length != b.length) return false;
    for (final key in a.keys) {
      if (!b.containsKey(key)) return false;
      if (!_deepEquals(a[key], b[key])) return false;
    }
    return true;
  }
  if (a is List && b is List) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (!_deepEquals(a[i], b[i])) return false;
    }
    return true;
  }
  return a == b;
}

// ---------------------------------------------------------------------------
// runtime_delta_engine.py
// ---------------------------------------------------------------------------

String _classifyChange(String field) {
  if (field.contains('semantic')) return 'semantic_change';
  if (field.contains('workflow')) return 'workflow_change';
  if (field.contains('dom') || field.contains('ui')) return 'ui_mutation';
  if (field.contains('state')) return 'application_state_mutation';
  return 'runtime_transition';
}

String _jsonKey(List<Map<String, dynamic>> changes) {
  final sorted = [...changes]
    ..sort((a, b) => '${a['field']}'.compareTo('${b['field']}'));
  return sorted.map((c) => '${c['field']}:${c['kind']}').join('|');
}

Map<String, dynamic> buildRuntimeDelta(
  Map<String, dynamic>? previous,
  Map<String, dynamic>? current, {
  int tick = 0,
}) {
  final prev = previous ?? <String, dynamic>{};
  final cur = current ?? <String, dynamic>{};
  final changes = <Map<String, dynamic>>[];

  final keys = <String>{...prev.keys, ...cur.keys}.toList()..sort();
  for (final key in keys) {
    if (!_deepEquals(prev[key], cur[key])) {
      changes.add(<String, dynamic>{
        'field': key,
        'from': prev[key],
        'to': cur[key],
        'kind': _classifyChange(key),
      });
    }
  }

  final payload = _jsonKey(changes);
  final deltaId =
      sha256.convert(utf8.encode(payload)).toString().substring(0, 32);

  return <String, dynamic>{
    'delta_id': deltaId,
    'changes': changes,
    'timestamp': tick,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_replay_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> replaySynchronizedRuntime(Map<String, dynamic> memory) {
  return <String, dynamic>{
    'synchronized_histories': memory['history'] ?? <String, dynamic>{},
    'runtime_deltas': memory['deltas'] ?? <dynamic>[],
    'semantic_timelines': memory['timeline'] ?? <String, dynamic>{},
    'distributed_realities': memory['realities'] ?? <dynamic>[],
    'convergence': memory['convergence'] ?? <String, dynamic>{},
    'replayed': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reality_replication_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> replicateRuntimeReality(
  Map<String, dynamic> source,
  List<dynamic> workers,
) {
  final replicas = <Map<String, dynamic>>[];
  final bounded = workers.take(1000).toList();
  for (var index = 0; index < bounded.length; index++) {
    final worker = _asMap(bounded[index]);
    replicas.add(<String, dynamic>{
      'worker_id': '${worker['worker_id'] ?? worker['id'] ?? 'worker:$index'}',
      'reality_id': '${source['reality_id'] ?? 'primary'}',
      'semantic_state': _asMap(source['semantic_state']),
      'runtime_state': _asMap(source['runtime_state']),
      'workflows': _asMap(source['workflows']),
      'checkpoints': _asList(source['checkpoints']),
      'causality_graph': _asMap(source['causality_graph']),
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
// runtime_alignment_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> alignRuntimeLayers(
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? semantic,
  Map<String, dynamic>? workflow,
) {
  return <String, dynamic>{
    'browser': _truthy(browser),
    'native': _truthy(native),
    'semantic': _truthy(semantic),
    'workflow': _truthy(workflow),
    'aligned': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_continuity_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> maintainRuntimeContinuity({
  Map<String, dynamic>? session,
  Map<String, dynamic>? identity,
  Map<String, dynamic>? workflow,
  Map<String, dynamic>? semantic,
  Map<String, dynamic>? checkpoint,
}) {
  return <String, dynamic>{
    'authenticated_session': _asMap(session),
    'browser_identity': _asMap(identity),
    'workflows': _asMap(workflow),
    'semantic_state': _asMap(semantic),
    'distributed_checkpoint': _asMap(checkpoint),
    'continuous': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_convergence_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> convergeRuntimeState(
    List<Map<String, dynamic>> realities) {
  final merged = <String, dynamic>{};
  final histories = <String>[];

  final sorted = [...realities]..sort((a, b) =>
      '${a['reality_id'] ?? ''}'.compareTo('${b['reality_id'] ?? ''}'));

  for (var index = 0; index < sorted.length; index++) {
    final reality = sorted[index];
    final realityId = '${reality['reality_id'] ?? 'reality:$index'}';
    histories.add(realityId);
    for (final entry in reality.entries) {
      if (entry.key == 'reality_id') continue;
      if (!merged.containsKey(entry.key)) {
        merged[entry.key] = entry.value;
      } else if (!_deepEquals(merged[entry.key], entry.value)) {
        merged[entry.key] = entry.value;
      }
    }
  }

  return <String, dynamic>{
    'converged_state': merged,
    'reality_count': realities.length,
    'histories': histories,
    'converged': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_diff_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> diffRuntimeState(
  Map<String, dynamic> previous,
  Map<String, dynamic> current,
) {
  final runtimeChanges = <Map<String, dynamic>>[];
  final semanticMutations = <Map<String, dynamic>>[];
  final workflowMutations = <Map<String, dynamic>>[];
  final distributedChanges = <Map<String, dynamic>>[];

  final keys = <String>{...previous.keys, ...current.keys}.toList()..sort();
  for (final key in keys) {
    if (_deepEquals(previous[key], current[key])) continue;
    final entry = <String, dynamic>{
      'field': key,
      'from': previous[key],
      'to': current[key],
    };
    if (key.contains('semantic')) {
      semanticMutations.add(entry);
    } else if (key.contains('workflow')) {
      workflowMutations.add(entry);
    } else if (key.contains('distributed') || key.contains('worker')) {
      distributedChanges.add(entry);
    } else {
      runtimeChanges.add(entry);
    }
  }

  return <String, dynamic>{
    'runtime_changes': runtimeChanges,
    'semantic_mutations': semanticMutations,
    'workflow_mutations': workflowMutations,
    'distributed_changes': distributedChanges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_drift_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> detectRuntimeDrift(
  Map<String, dynamic> baseline,
  Map<String, dynamic> current,
) {
  final drifts = <Map<String, dynamic>>[];
  const checks = <List<String>>[
    <String>['selector_drift', 'selectors'],
    <String>['semantic_drift', 'semantic'],
    <String>['workflow_drift', 'workflow'],
    <String>['topology_drift', 'topology'],
    <String>['application_drift', 'application'],
    <String>['runtime_divergence', 'runtime'],
  ];

  for (final check in checks) {
    final driftType = check[0];
    final field = check[1];
    if (!_deepEquals(baseline[field], current[field])) {
      drifts.add(<String, dynamic>{
        'type': driftType,
        'field': field,
        'detected': true,
      });
    }
  }

  return <String, dynamic>{
    'drifts': drifts,
    'drift_count': drifts.length,
    'diverged': drifts.isNotEmpty,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_federation_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> federateRuntimeRealities({
  List<dynamic>? workers,
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? semantic,
  Map<String, dynamic>? application,
}) {
  final boundedWorkers = (workers ?? <dynamic>[]).take(1000).toList();
  final federated = <Map<String, dynamic>>[];
  for (var index = 0; index < boundedWorkers.length; index++) {
    final worker = _asMap(boundedWorkers[index]);
    federated.add(<String, dynamic>{
      'worker_id': '${worker['worker_id'] ?? worker['id'] ?? 'w:$index'}',
      'federated': true,
    });
  }

  return <String, dynamic>{
    'workers': federated,
    'browser_runtime': _truthy(browser),
    'native_runtime': _truthy(native),
    'semantic_state': _truthy(semantic),
    'application_cognition': _truthy(application),
    'federated': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_history_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeHistory(
  List<Map<String, dynamic>> deltas, {
  List<dynamic>? transitions,
  List<dynamic>? workflows,
}) {
  final transitionsList = transitions ?? <dynamic>[];
  final workflowsList = workflows ?? <dynamic>[];

  final sortedDeltas = [...deltas]
    ..sort((a, b) => _asInt(a['timestamp']).compareTo(_asInt(b['timestamp'])));

  final mutations = <dynamic>[];
  for (final delta in deltas) {
    for (final change in _asList(delta['changes'])) {
      mutations.add(change);
    }
  }

  final semanticEvolution = <dynamic>[];
  for (final delta in deltas) {
    for (final change in _asList(delta['changes'])) {
      if (change is Map && change['kind'] == 'semantic_change') {
        semanticEvolution.add(change);
      }
    }
  }

  return <String, dynamic>{
    'deltas': sortedDeltas,
    'transitions': transitionsList,
    'mutations': mutations,
    'workflows': workflowsList,
    'semantic_evolution': semanticEvolution,
    'length': deltas.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_merge_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> mergeRuntimeRealities(
    List<Map<String, dynamic>> realities) {
  final mergedSemantic = <String, dynamic>{};
  final mergedWorkflow = <String, dynamic>{};
  final mergedApplication = <String, dynamic>{};
  final timelines = <Map<String, dynamic>>[];

  for (final reality in realities.take(1000)) {
    timelines.add(<String, dynamic>{
      'reality_id': '${reality['reality_id'] ?? ''}',
      'tick': _asInt(reality['tick']),
    });
    mergedSemantic.addAll(_asMap(reality['semantic']));
    mergedWorkflow.addAll(_asMap(reality['workflow']));
    mergedApplication.addAll(_asMap(reality['application']));
  }

  timelines.sort((a, b) => _asInt(a['tick']).compareTo(_asInt(b['tick'])));

  return <String, dynamic>{
    'semantic': mergedSemantic,
    'workflow': mergedWorkflow,
    'application': mergedApplication,
    'timelines': timelines,
    'reality_count': realities.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_mutation_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> trackRuntimeMutations(
  List<dynamic> changes, {
  int tick = 0,
}) {
  final sorted = [...changes]..sort((a, b) {
      final fa = a is Map ? '${a['field'] ?? ''}' : '';
      final fb = b is Map ? '${b['field'] ?? ''}' : '';
      return fa.compareTo(fb);
    });
  return <String, dynamic>{
    'mutations': sorted,
    'count': changes.length,
    'tick': tick,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_snapshot_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> captureRuntimeSnapshot({
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? semantic,
  Map<String, dynamic>? workflow,
  Map<String, dynamic>? causality,
  Map<String, dynamic>? syncState,
  int tick = 0,
}) {
  return <String, dynamic>{
    'snapshot_id': 'snapshot:$tick',
    'tick': tick,
    'browser_runtime': _asMap(browser),
    'native_runtime': _asMap(native),
    'semantic_runtime': _asMap(semantic),
    'workflow_state': _asMap(workflow),
    'causality_state': _asMap(causality),
    'synchronization_state': _asMap(syncState),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_state_graph_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeStateGraph(
  Map<String, dynamic> snapshot,
  Map<String, dynamic> delta,
  Map<String, dynamic> convergence,
) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];

  final snapshotId = '${snapshot['snapshot_id'] ?? 'snapshot:0'}';
  nodes.add(<String, dynamic>{'id': snapshotId, 'type': 'snapshot'});

  final deltaId = '${delta['delta_id'] ?? 'delta:0'}';
  nodes.add(<String, dynamic>{'id': deltaId, 'type': 'delta'});
  edges.add(<String, dynamic>{
    'from': snapshotId,
    'to': deltaId,
    'relation': 'mutates',
  });

  final changes = _asList(delta['changes']);
  for (final change in changes.take(5000)) {
    final field = change is Map ? '${change['field'] ?? ''}' : '';
    final nodeId = 'change:$field';
    nodes.add(<String, dynamic>{'id': nodeId, 'type': 'mutation'});
    edges.add(<String, dynamic>{
      'from': deltaId,
      'to': nodeId,
      'relation': 'propagates',
    });
  }

  const convergedId = 'convergence:root';
  nodes.add(<String, dynamic>{'id': convergedId, 'type': 'convergence'});
  edges.add(<String, dynamic>{
    'from': deltaId,
    'to': convergedId,
    'relation': 'converges',
  });

  if (changes.isNotEmpty) {
    edges.add(<String, dynamic>{
      'from': convergedId,
      'to': snapshotId,
      'relation': 'synchronizes',
    });
  }

  nodes.add(<String, dynamic>{'id': 'checkpoint:sync', 'type': 'checkpoint'});
  edges.add(<String, dynamic>{
    'from': convergedId,
    'to': 'checkpoint:sync',
    'relation': 'restores',
  });

  nodes.sort((a, b) => '${a['id']}'.compareTo('${b['id']}'));
  edges.sort((a, b) {
    final ka = '${a['from'] ?? ''} ${a['to'] ?? ''} ${a['relation'] ?? ''}';
    final kb = '${b['from'] ?? ''} ${b['to'] ?? ''} ${b['relation'] ?? ''}';
    return ka.compareTo(kb);
  });

  return <String, dynamic>{
    'nodes': nodes,
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_sync_engine.py
// ---------------------------------------------------------------------------

const List<String> runtimeSyncHandlers = <String>[
  'browser',
  'electron',
  'terminal',
  'vm',
  'remote',
];

Map<String, dynamic> synchronizeRuntime(
  List<Map<String, dynamic>> snapshots, {
  int tick = 0,
}) {
  final synchronized = <Map<String, dynamic>>[];

  for (final runtime in runtimeSyncHandlers) {
    Map<String, dynamic> payload = <String, dynamic>{};
    for (final snapshot in snapshots) {
      var key = runtime != 'browser' ? '${runtime}_runtime' : 'browser_runtime';
      if (runtime == 'electron') key = 'native_runtime';
      dynamic value = snapshot.containsKey(key)
          ? snapshot[key]
          : (snapshot['native_runtime'] ?? <String, dynamic>{});
      if (_truthy(value)) {
        final extra = value is Map
            ? Map<String, dynamic>.from(value)
            : <String, dynamic>{'data': value};
        payload = <String, dynamic>{...payload, ...extra};
      }
    }
    synchronized.add(<String, dynamic>{
      'runtime': runtime,
      'synced': payload.isNotEmpty,
      'tick': tick,
      'handler': 'sync_$runtime',
    });
  }

  final count = synchronized.where((item) => item['synced'] == true).length;
  return <String, dynamic>{
    'synchronized': synchronized,
    'count': count,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_consistency_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> verifyRuntimeConsistency(
  Map<String, dynamic> history,
  Map<String, dynamic> convergence,
  Map<String, dynamic> replay,
) {
  final deltas = _asList(history['deltas']);
  final issues = <String>[];

  if (!_truthy(convergence['converged'])) {
    issues.add('convergence_incomplete');
  }
  if (!_truthy(replay['replayed'])) {
    issues.add('replay_not_ready');
  }
  for (var index = 1; index < deltas.length; index++) {
    final cur = _asInt(_asMap(deltas[index])['timestamp']);
    final prev = _asInt(_asMap(deltas[index - 1])['timestamp']);
    if (cur < prev) {
      issues.add('timeline_order_violation');
      break;
    }
  }

  return <String, dynamic>{
    'consistent': issues.isEmpty,
    'issues': issues,
    'synchronization_integrity': issues.isEmpty,
    'semantic_continuity': history.containsKey('semantic_evolution'),
    'replay_consistency': replay['replayed'] ?? false,
    'distributed_convergence': convergence['converged'] ?? false,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_timeline_engine.py
// ---------------------------------------------------------------------------

Map<String, dynamic> buildSyncTimeline(Map<String, dynamic> history) {
  final entries = <Map<String, dynamic>>[];
  for (final delta in _asList(history['deltas'])) {
    final d = _asMap(delta);
    entries.add(<String, dynamic>{
      'tick': _asInt(d['timestamp']),
      'delta_id': '${d['delta_id'] ?? ''}',
      'change_count': _asList(d['changes']).length,
    });
  }
  entries.sort((a, b) => _asInt(a['tick']).compareTo(_asInt(b['tick'])));
  return <String, dynamic>{
    'timeline': entries,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core/ir/synchronization_runtime_ir.py
// ---------------------------------------------------------------------------

Map<String, dynamic> compileSynchronizationRuntimeIr(
    Map<String, dynamic> sync) {
  return <String, dynamic>{
    'ir': 'synchronization_runtime',
    'snapshot': sync['snapshot'] ?? <String, dynamic>{},
    'delta': sync['delta'] ?? <String, dynamic>{},
    'history': sync['history'] ?? <String, dynamic>{},
    'timeline': sync['timeline'] ?? <String, dynamic>{},
    'convergence': sync['convergence'] ?? <String, dynamic>{},
    'synchronization': sync['synchronization'] ?? <String, dynamic>{},
    'replication': sync['replication'] ?? <String, dynamic>{},
    'continuity': sync['continuity'] ?? <String, dynamic>{},
    'state_graph': sync['state_graph'] ?? <String, dynamic>{},
    'consistency': sync['consistency'] ?? <String, dynamic>{},
    'bounded': true,
  };
}

Map<String, dynamic> synchronizationRuntimeIrToGraph(
  Map<String, dynamic> syncIr,
) {
  final graph = _asMap(syncIr['state_graph']);
  var nodes = _asList(graph['nodes']);
  final edges = _asList(graph['edges']);

  if (nodes.isEmpty) {
    nodes = <dynamic>[
      <String, dynamic>{'id': 'sync:root', 'type': 'synchronization'},
    ];
  }

  final sortedNodes = [...nodes]..sort((a, b) {
      final ia = a is Map ? '${a['id'] ?? ''}' : '';
      final ib = b is Map ? '${b['id'] ?? ''}' : '';
      return ia.compareTo(ib);
    });

  return <String, dynamic>{
    'ir': 'synchronization_runtime_graph',
    'nodes': sortedNodes,
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core/runtime_graph/runtime_graph_engine.py  (list-of-IRs variant)
//
// NOTE: the public Dart `buildRuntimeGraph` in lib/src/graph/runtime_graph.dart
// is a DIFFERENT function (dict-of-sources → RuntimeGraph). The Python sync
// orchestrator calls `core.runtime_graph.build_runtime_graph([ir])` which
// merges a LIST of heterogeneous IRs into a canonical dict graph. This is a
// private port faithful to that engine.
// ---------------------------------------------------------------------------

const int _maxGraphNodes = 1000000;
const int _maxGraphEdges = 5000000;

Map<String, dynamic> mergeRuntimeIrGraph(List<dynamic> runtimeIrs) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];
  final seenNodes = <String>{};
  final seenEdges = <String>{};

  for (final raw in runtimeIrs.take(10000)) {
    final runtime = _asMap(raw);
    final runtimeType = '${runtime['ir'] ?? 'unknown'}';

    for (final rawNode in _asList(runtime['nodes'])) {
      final node = _asMap(rawNode);
      final nodeId = '${node['id'] ?? ''}'.trim();
      if (nodeId.isEmpty) continue;
      if (seenNodes.contains(nodeId)) continue;
      seenNodes.add(nodeId);
      final enriched = Map<String, dynamic>.from(node);
      enriched['runtime_type'] = runtimeType;
      nodes.add(enriched);
      if (nodes.length >= _maxGraphNodes) break;
    }

    for (final rawEdge in _asList(runtime['edges'])) {
      final edge = _asMap(rawEdge);
      final src = '${edge['from'] ?? ''}'.trim();
      final dst = '${edge['to'] ?? ''}'.trim();
      final relation = '${edge['relation'] ?? 'related_to'}'.trim();
      if (src.isEmpty || dst.isEmpty) continue;
      final edgeKey = '$src $dst $relation';
      if (seenEdges.contains(edgeKey)) continue;
      seenEdges.add(edgeKey);
      final enriched = Map<String, dynamic>.from(edge);
      enriched['runtime_type'] = runtimeType;
      edges.add(enriched);
      if (edges.length >= _maxGraphEdges) break;
    }
  }

  nodes.sort((a, b) => '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));
  edges.sort((a, b) {
    final ka = '${a['from'] ?? ''} ${a['to'] ?? ''} ${a['relation'] ?? ''}';
    final kb = '${b['from'] ?? ''} ${b['to'] ?? ''} ${b['relation'] ?? ''}';
    return ka.compareTo(kb);
  });

  return <String, dynamic>{
    'ir': 'unified_runtime_graph',
    'nodes': nodes,
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_sync_memory_engine.py — remember (pure, no I/O)
// ---------------------------------------------------------------------------

Map<String, dynamic> rememberSyncRuntime(
  Map<String, dynamic> memory,
  Map<String, dynamic> update,
) {
  final merged = Map<String, dynamic>.from(memory);
  const fields = <String>[
    'deltas',
    'history',
    'timeline',
    'convergence',
    'realities',
    'continuity',
    'state_graph',
  ];
  for (final field in fields) {
    // dict.setdefault(field, update.get(field, merged.get(field, {})))
    if (!merged.containsKey(field)) {
      merged[field] = update.containsKey(field)
          ? update[field]
          : (merged[field] ?? <String, dynamic>{});
    }
  }
  merged.addAll(update);
  merged['bounded'] = true;
  return merged;
}

Map<String, dynamic> emptySyncMemory() {
  return <String, dynamic>{
    'deltas': <dynamic>[],
    'history': <String, dynamic>{},
    'timeline': <String, dynamic>{},
    'convergence': <String, dynamic>{},
    'realities': <dynamic>[],
    'continuity': <String, dynamic>{},
    'state_graph': <String, dynamic>{},
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_sync_orchestrator.py
// ---------------------------------------------------------------------------

Map<String, dynamic> _runtimeView(
  Map<String, dynamic>? extraction,
  Map<String, dynamic>? semantic,
  Map<String, dynamic>? workflow,
  Map<String, dynamic>? causality,
) {
  final ext = extraction ?? <String, dynamic>{};
  final sem = semantic ?? <String, dynamic>{};
  final wf = workflow ?? <String, dynamic>{};
  final cau = causality ?? <String, dynamic>{};
  return <String, dynamic>{
    'dom': ext['dom'] ?? <String, dynamic>{},
    // (semantic or {}).get("semantic", semantic or {})
    'semantic': sem.containsKey('semantic') ? sem['semantic'] : sem,
    'workflow': wf.containsKey('workflow') ? wf['workflow'] : wf,
    'causality': cau.containsKey('causality') ? cau['causality'] : cau,
    'runtime': ext['runtime'] ?? <String, dynamic>{},
  };
}

Map<String, dynamic> runSynchronizedRuntime({
  int tick = 0,
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? semanticResult,
  Map<String, dynamic>? workflowResult,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? distributedResult,
  Map<String, dynamic>? session,
  Map<String, dynamic>? identity,
  Map<String, dynamic>? memory,
  List<dynamic>? workers,
}) {
  final mem = Map<String, dynamic>.from(memory ?? <String, dynamic>{});
  final workerList =
      workers ?? _asList((distributedResult ?? <String, dynamic>{})['workers']);

  final previousView = _asMap(mem['last_view']);
  final currentView =
      _runtimeView(browser, semanticResult, workflowResult, causalityResult);

  final delta = buildRuntimeDelta(previousView, currentView, tick: tick);
  final snapshot = captureRuntimeSnapshot(
    browser: browser,
    native: native,
    semantic: semanticResult,
    workflow: workflowResult,
    causality: causalityResult,
    syncState: _asMap(mem['continuity']),
    tick: tick,
  );

  final drift = detectRuntimeDrift(
    <String, dynamic>{
      'selectors': _asMap(previousView['dom']),
      'semantic': previousView['semantic'] ?? <String, dynamic>{},
      'workflow': previousView['workflow'] ?? <String, dynamic>{},
      'topology': previousView['runtime'] ?? <String, dynamic>{},
      'application': previousView['workflow'] ?? <String, dynamic>{},
      'runtime': previousView['runtime'] ?? <String, dynamic>{},
    },
    <String, dynamic>{
      'selectors': _asMap(currentView['dom']),
      'semantic': currentView['semantic'] ?? <String, dynamic>{},
      'workflow': currentView['workflow'] ?? <String, dynamic>{},
      'topology': currentView['runtime'] ?? <String, dynamic>{},
      'application': currentView['workflow'] ?? <String, dynamic>{},
      'runtime': currentView['runtime'] ?? <String, dynamic>{},
    },
  );

  final stateDiff = diffRuntimeState(previousView, currentView);
  final mutations =
      trackRuntimeMutations(_asList(delta['changes']), tick: tick);

  final realities = <Map<String, dynamic>>[
    <String, dynamic>{
      'reality_id': 'primary',
      'tick': tick,
      'semantic': currentView['semantic'] ?? <String, dynamic>{},
      'workflow': currentView['workflow'] ?? <String, dynamic>{},
      'application': currentView['workflow'] ?? <String, dynamic>{},
    },
  ];
  if (_truthy(distributedResult)) {
    realities.add(<String, dynamic>{
      'reality_id': 'distributed',
      'tick': tick,
      'semantic': <String, dynamic>{},
      'workflow': distributedResult,
      'application': <String, dynamic>{},
    });
  }

  final merged = mergeRuntimeRealities(realities);
  final convergence = convergeRuntimeState(realities);
  final synchronization =
      synchronizeRuntime(<Map<String, dynamic>>[snapshot], tick: tick);
  final replication = replicateRuntimeReality(
    <String, dynamic>{
      'reality_id': 'primary',
      'semantic_state': currentView['semantic'] ?? <String, dynamic>{},
      'runtime_state': currentView['runtime'] ?? <String, dynamic>{},
      'workflows': currentView['workflow'] ?? <String, dynamic>{},
      'checkpoints': _asList(mem['checkpoints']),
      'causality_graph': currentView['causality'] ?? <String, dynamic>{},
    },
    workerList,
  );
  final federation = federateRuntimeRealities(
    workers: workerList,
    browser: browser,
    native: native,
    semantic: semanticResult,
    application: workflowResult,
  );
  final alignment =
      alignRuntimeLayers(browser, native, semanticResult, workflowResult);
  final continuity = maintainRuntimeContinuity(
    session: session,
    identity: identity,
    workflow: workflowResult,
    semantic: semanticResult,
    checkpoint: _asMap(mem['checkpoint']),
  );

  final priorDeltas = _asList(mem['deltas']);
  final allDeltas = <dynamic>[...priorDeltas, delta];
  final allDeltasMaps = allDeltas.map((d) => _asMap(d)).toList(growable: false);
  final history = buildRuntimeHistory(
    allDeltasMaps,
    workflows: <dynamic>[merged['workflow'] ?? <String, dynamic>{}],
  );
  final timeline = buildSyncTimeline(history);
  final stateGraph = buildRuntimeStateGraph(snapshot, delta, convergence);

  final payload = <String, dynamic>{
    'snapshot': snapshot,
    'delta': delta,
    'drift': drift,
    'diff': stateDiff,
    'mutations': mutations,
    'merge': merged,
    'convergence': convergence,
    'synchronization': synchronization,
    'replication': replication,
    'federation': federation,
    'alignment': alignment,
    'continuity': continuity,
    'history': history,
    'timeline': timeline,
    'state_graph': stateGraph,
    'bounded': true,
  };

  final updatedMemory = rememberSyncRuntime(
    mem,
    <String, dynamic>{
      'deltas': allDeltas,
      'history': history,
      'timeline': timeline,
      'convergence': convergence,
      'realities': realities,
      'continuity': continuity,
      'state_graph': stateGraph,
      'last_view': currentView,
    },
  );
  final replay = replaySynchronizedRuntime(updatedMemory);
  final consistency = verifyRuntimeConsistency(history, convergence, replay);

  payload['memory'] = updatedMemory;
  payload['replay'] = replay;
  payload['consistency'] = consistency;
  payload['sync_ir'] = compileSynchronizationRuntimeIr(payload);
  return payload;
}

Map<String, dynamic> runSyncForExtraction({
  bool synchronizedRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  int tick = 0,
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? semanticResult,
  Map<String, dynamic>? workflowResult,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? distributedResult,
  Map<String, dynamic>? session,
  Map<String, dynamic>? identity,
  bool mergeGraph = true,
}) {
  if (!synchronizedRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  Map<String, dynamic> memory = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final loaded = loadSyncMemory(memoryPath, memoryKey);
    if (_truthy(loaded['available'])) {
      memory = _asMap(loaded['memory']);
    }
  }

  final result = runSynchronizedRuntime(
    tick: tick,
    browser: browser,
    native: native,
    semanticResult: semanticResult,
    workflowResult: workflowResult,
    causalityResult: causalityResult,
    distributedResult: distributedResult,
    session: session,
    identity: identity,
    memory: memory,
  );

  var persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveSyncMemory(memoryPath, _asMap(result['memory']), memoryKey);
    persisted = true;
  }

  final graphIr = synchronizationRuntimeIrToGraph(_asMap(result['sync_ir']));
  Map<String, dynamic> unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = mergeRuntimeIrGraph(<dynamic>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'synchronization': result,
    'sync_ir': result['sync_ir'] ?? <String, dynamic>{},
    'sync_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': result['replay'] ?? <String, dynamic>{},
    'memory_persisted': persisted,
    'bounded': true,
  };
}
