// Faithful Dart port of the leaf engines that the reconstruction runtime
// orchestrator composes. Mirrors core/reconstruction/*.py and
// core/ir/reconstruction_runtime_ir.py exactly, including key order and the
// SHA-256 runtime/identity id derivation (json.dumps(sort_keys=True)[:32]).

import 'dart:convert';

import 'package:crypto/crypto.dart' as crypto;

import '../evolution/_sort_util.dart';

// ---------------------------------------------------------------------------
// id hashing: hashlib.sha256(json.dumps(payload, sort_keys=True)).hexdigest()[:32]
// ---------------------------------------------------------------------------

/// json.dumps(value, sort_keys=True) — Python default separators (", ", ": ").
String pyJsonSortKeys(dynamic value) {
  final sorted = _deepSort(value);
  return _PyJsonEncoder().convert(sorted);
}

dynamic _deepSort(dynamic value) {
  if (value is Map) {
    final m = Map<String, dynamic>.from(value);
    final out = <String, dynamic>{};
    final keys = m.keys.toList()..sort();
    for (final k in keys) {
      out[k] = _deepSort(m[k]);
    }
    return out;
  }
  if (value is List) {
    return value.map<dynamic>(_deepSort).toList();
  }
  return value;
}

class _PyJsonEncoder {
  String convert(dynamic value) {
    final buf = StringBuffer();
    _write(value, buf);
    return buf.toString();
  }

  void _write(dynamic value, StringBuffer buf) {
    if (value is Map) {
      buf.write('{');
      var first = true;
      value.forEach((dynamic k, dynamic v) {
        if (!first) buf.write(', ');
        first = false;
        buf.write(jsonEncode(k.toString()));
        buf.write(': ');
        _write(v, buf);
      });
      buf.write('}');
    } else if (value is List) {
      buf.write('[');
      var first = true;
      for (final dynamic v in value) {
        if (!first) buf.write(', ');
        first = false;
        _write(v, buf);
      }
      buf.write(']');
    } else {
      buf.write(jsonEncode(value));
    }
  }
}

String _idHash(Map<String, dynamic> payload) {
  final canonical = pyJsonSortKeys(payload);
  final digest = crypto.sha256.convert(utf8.encode(canonical)).toString();
  return digest.substring(0, 32);
}

// ---------------------------------------------------------------------------
// coercion helpers
// ---------------------------------------------------------------------------

Map<String, dynamic> _map(dynamic v) =>
    v is Map ? Map<String, dynamic>.from(v) : <String, dynamic>{};

List<dynamic> _list(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

List<Map<String, dynamic>> _maps(dynamic v) => _list(v)
    .whereType<Map>()
    .map((dynamic e) => Map<String, dynamic>.from(e as Map))
    .toList();

String _str(dynamic v) => v == null ? '' : '$v';

int _int(dynamic v, [int fallback = 0]) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? fallback;
  return fallback;
}

bool _truthy(dynamic v) {
  if (v == null) return false;
  if (v is bool) return v;
  if (v is num) return v != 0;
  if (v is String) return v.isNotEmpty;
  if (v is Iterable) return v.isNotEmpty;
  if (v is Map) return v.isNotEmpty;
  return true;
}

/// sources.get(a, sources.get(b, {}))
dynamic _getAny(Map<String, dynamic> src, List<String> keys, dynamic fallback) {
  for (final k in keys) {
    if (src.containsKey(k)) return src[k];
  }
  return fallback;
}

// ---------------------------------------------------------------------------
// reconstruct_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructRuntime({
  Map<String, dynamic>? semanticIr,
  Map<String, dynamic>? workflowIr,
  Map<String, dynamic>? synchronizationIr,
  Map<String, dynamic>? executionIr,
  Map<String, dynamic>? memoryIr,
  Map<String, dynamic>? runtimeGraph,
  String runtimeType = 'browser',
  int tick = 0,
}) {
  final graph = runtimeGraph ?? <String, dynamic>{};
  final canonical = <String, dynamic>{
    'semantic': semanticIr ?? <String, dynamic>{},
    'workflow': workflowIr ?? <String, dynamic>{},
    'sync': synchronizationIr ?? <String, dynamic>{},
    'execution': executionIr ?? <String, dynamic>{},
    'memory': memoryIr ?? <String, dynamic>{},
    'graph_nodes': _list(graph['nodes']).length,
    'runtime_type': runtimeType,
    'tick': tick,
  };
  final runtimeId = _idHash(canonical);

  return <String, dynamic>{
    'runtime_id': runtimeId,
    'runtime_type': runtimeType,
    'reconstructed': true,
    'graph_grounded': _truthy(graph),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_browser_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructBrowserRuntime({
  Map<String, dynamic>? browserIr,
  Map<String, dynamic>? interactionIr,
  Map<String, dynamic>? identity,
  Map<String, dynamic>? session,
  Map<String, dynamic>? streaming,
  Map<String, dynamic>? dom,
}) {
  final bIr = browserIr ?? <String, dynamic>{};
  final iIr = interactionIr ?? <String, dynamic>{};
  final id = identity ?? <String, dynamic>{};
  final sess = session ?? <String, dynamic>{};
  final stream = streaming ?? <String, dynamic>{};
  final domBody = dom ?? <String, dynamic>{};

  // tab source: interaction tab_states.tabs OR browser routes.history OR [{path:url}]
  var tabSource = _list(_map(iIr['tab_states'])['tabs']);
  if (tabSource.isEmpty) {
    tabSource = _list(_map(bIr['routes'])['history']);
  }
  if (tabSource.isEmpty) {
    tabSource = <dynamic>[
      <String, dynamic>{'path': bIr.containsKey('url') ? bIr['url'] : '/'}
    ];
  }
  final tabs = <Map<String, dynamic>>[];
  for (var index = 0; index < tabSource.length; index++) {
    final route = _map(tabSource[index]);
    tabs.add(<String, dynamic>{
      'id': 'tab:$index',
      'path': _str(route['path']),
    });
  }
  final sortedTabs = stableSorted<Map<String, dynamic>>(
    tabs,
    (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
  );

  var navSource = _list(_map(iIr['route_transitions'])['routes']);
  if (navSource.isEmpty) {
    navSource = _list(_map(bIr['navigation'])['history']);
  }
  final nav = <Map<String, dynamic>>[];
  for (var index = 0; index < navSource.length; index++) {
    final item = _map(navSource[index]);
    nav.add(<String, dynamic>{
      'path': _str(item['path']),
      'order': item.containsKey('order') ? _int(item['order']) : index,
    });
  }
  final sortedNav = stableSorted<Map<String, dynamic>>(
    nav,
    (a, b) => _int(a['order']).compareTo(_int(b['order'])),
  );

  final cookies = _maps(sess['cookies']);
  final sortedCookies = stableSorted<Map<String, dynamic>>(
    cookies,
    (a, b) => pyStrCompare(_str(a['name']), _str(b['name'])),
  );

  var interactionFlows = _list(iIr['interactions']);
  if (interactionFlows.length > 1000) {
    interactionFlows = interactionFlows.sublist(0, 1000);
  }

  return <String, dynamic>{
    'tabs': sortedTabs,
    'navigation_history': sortedNav,
    'dom_structure': domBody.containsKey('structure')
        ? _map(domBody['structure'])
        : _map(domBody['nodes']),
    'interaction_flows': interactionFlows,
    'browser_identity': Map<String, dynamic>.from(id),
    'authenticated_state': <String, dynamic>{
      'authenticated': sess['authenticated'] == true,
      'cookies': sortedCookies,
    },
    'storage': <String, dynamic>{
      'local': _map(sess['local_storage']),
      'session': _map(sess['session_storage']),
    },
    'streaming_state': Map<String, dynamic>.from(stream),
    'replay_safe': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_application_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructApplicationRuntime({
  Map<String, dynamic>? applicationIr,
  Map<String, dynamic>? workflowIr,
  Map<String, dynamic>? executionIr,
  String runtimeType = 'browser',
}) {
  final aIr = applicationIr ?? <String, dynamic>{};
  final wIr = workflowIr ?? <String, dynamic>{};
  final eIr = executionIr ?? <String, dynamic>{};

  dynamic workflows =
      wIr.containsKey('workflows') ? wIr['workflows'] : wIr['workflow'];
  workflows ??= <String, dynamic>{};
  if (workflows is Map && workflows.containsKey('objective')) {
    workflows = <dynamic>[workflows];
  }

  return <String, dynamic>{
    'runtime_type': runtimeType,
    'workflows':
        workflows is List ? List<dynamic>.from(workflows) : <dynamic>[],
    'forms': _map(aIr['forms']),
    'dashboards': _list(aIr['dashboards']),
    'modals': _list(aIr['modals']),
    'tabs': _list(aIr['tabs']),
    'application_graph': aIr.containsKey('graph')
        ? _map(aIr['graph'])
        : _map(aIr['action_graphs']),
    'execution_state': eIr.containsKey('execution_state')
        ? _map(eIr['execution_state'])
        : _map(eIr['state']),
    'replay_safe': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_runtime_session
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructRuntimeSession({
  Map<String, dynamic>? session,
  Map<String, dynamic>? identity,
  Map<String, dynamic>? syncState,
  Map<String, dynamic>? adaptiveMemory,
}) {
  final sess = session ?? <String, dynamic>{};
  final id = identity ?? <String, dynamic>{};
  final sync = syncState ?? <String, dynamic>{};
  final adaptive = adaptiveMemory ?? <String, dynamic>{};

  final cookies = stableSorted<Map<String, dynamic>>(
    _maps(sess['cookies']),
    (a, b) => pyStrCompare(_str(a['name']), _str(b['name'])),
  );

  return <String, dynamic>{
    'authenticated_session': <String, dynamic>{
      'authenticated': sess['authenticated'] == true,
      'session_id': sess.containsKey('session_id')
          ? _str(sess['session_id'])
          : _str(id['identity_id']),
    },
    'cookies': cookies,
    'csrf_state': sess.containsKey('csrf')
        ? _map(sess['csrf'])
        : _map(sess['csrf_state']),
    'browser_identity': Map<String, dynamic>.from(id),
    'synchronization_state': Map<String, dynamic>.from(sync),
    'adaptive_memory': Map<String, dynamic>.from(adaptive),
    'replay_safe': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// build_runtime_environment
// ---------------------------------------------------------------------------

const _envTypes = <String>{
  'browser',
  'terminal',
  'electron',
  'connector',
  'vm',
  'distributed',
};

Map<String, dynamic> buildRuntimeEnvironment({
  String runtime = 'browser',
  List<dynamic>? connectors,
  List<dynamic>? workers,
}) {
  final rt = _envTypes.contains(runtime) ? runtime : 'browser';
  final conn = stableSorted<Map<String, dynamic>>(
    _maps(connectors ?? <dynamic>[]),
    (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
  );
  final wks = stableSorted<Map<String, dynamic>>(
    _maps(workers ?? <dynamic>[]),
    (a, b) => pyStrCompare(_str(a['worker_id']), _str(b['worker_id'])),
  );

  return <String, dynamic>{
    'runtime': rt,
    'browser': rt == 'browser',
    'terminal': rt == 'terminal',
    'electron': rt == 'electron',
    'connector': rt == 'connector',
    'vm': rt == 'vm',
    'distributed': rt == 'distributed',
    'connectors': conn,
    'workers': wks,
    'execution_ready': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_runtime_memory
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructRuntimeMemory({
  Map<String, dynamic>? memoryIr,
  Map<String, dynamic>? semantic,
  dynamic lineage,
}) {
  final mIr = memoryIr ?? <String, dynamic>{};
  final sem = semantic ?? <String, dynamic>{};

  final runtimeHistory = mIr['runtime_history'];
  List<dynamic> historyList;
  if (runtimeHistory is Map) {
    historyList = _list(runtimeHistory['runtime_history']);
  } else if (runtimeHistory is List) {
    historyList = List<dynamic>.from(runtimeHistory);
  } else {
    historyList = <dynamic>[];
  }

  // lineage_body = lineage or memory_ir.get('lineage', {})
  dynamic lineageBody = _truthy(lineage) ? lineage : mIr['lineage'];
  lineageBody ??= <String, dynamic>{};
  dynamic lineageEntries;
  if (lineageBody is Map) {
    lineageEntries = lineageBody.containsKey('lineage')
        ? lineageBody['lineage']
        : lineageBody;
  } else {
    lineageEntries = lineageBody;
  }
  final lineageList =
      lineageEntries is List ? _maps(lineageEntries) : <Map<String, dynamic>>[];
  final sortedLineage = stableSorted<Map<String, dynamic>>(
    lineageList,
    (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
  );

  final syncHistory = historyList
      .whereType<Map>()
      .where((m) => m['kind'] == 'sync')
      .map((dynamic e) => Map<String, dynamic>.from(e as Map))
      .toList();

  return <String, dynamic>{
    'semantic_memory':
        _truthy(sem) ? Map<String, dynamic>.from(sem) : _map(mIr['semantic']),
    'lineage': sortedLineage,
    'continuity': _map(mIr['knowledge']),
    'runtime_graph_memory': _map(mIr['memory_graphs']),
    'synchronization_history': syncHistory,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// rebuild_runtime_state
// ---------------------------------------------------------------------------

Map<String, dynamic> rebuildRuntimeState({
  List<dynamic>? queues,
  Map<String, dynamic>? synchronization,
  List<dynamic>? mutations,
  List<dynamic>? transactions,
  Map<String, dynamic>? memory,
  List<dynamic>? executionLineage,
  List<dynamic>? workflows,
}) {
  final orderedMutations = stableSorted<Map<String, dynamic>>(
    _maps(mutations ?? <dynamic>[]),
    (a, b) {
      var c = _int(a['tick']).compareTo(_int(b['tick']));
      if (c != 0) return c;
      c = _int(a['ordered_index']).compareTo(_int(b['ordered_index']));
      if (c != 0) return c;
      return pyStrCompare(_str(a['kind']), _str(b['kind']));
    },
  );
  final orderedTx = stableSorted<Map<String, dynamic>>(
    _maps(transactions ?? <dynamic>[]),
    (a, b) =>
        pyStrCompare(_str(a['transaction_id']), _str(b['transaction_id'])),
  );
  final orderedQueues = stableSorted<Map<String, dynamic>>(
    _maps(queues ?? <dynamic>[]),
    (a, b) {
      // key=(-priority, order); compare priority descending then order asc.
      final c = (-_int(a['priority'])).compareTo(-_int(b['priority']));
      if (c != 0) return c;
      return _int(a['order']).compareTo(_int(b['order']));
    },
  );

  return <String, dynamic>{
    'queues': orderedQueues,
    'synchronization': Map<String, dynamic>.from(synchronization ?? {}),
    'mutations': orderedMutations,
    'transactions': orderedTx,
    'memory': Map<String, dynamic>.from(memory ?? {}),
    'execution_lineage': stableSorted<Map<String, dynamic>>(
      _maps(executionLineage ?? <dynamic>[]),
      (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
    ),
    'workflows': stableSorted<Map<String, dynamic>>(
      _maps(workflows ?? <dynamic>[]),
      (a, b) => pyStrCompare(
        _str(a.containsKey('id') ? a['id'] : a['objective']),
        _str(b.containsKey('id') ? b['id'] : b['objective']),
      ),
    ),
    'deterministic_order': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_runtime_topology
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructRuntimeTopology({
  Map<String, dynamic>? runtimeGraph,
  List<dynamic>? workers,
  List<dynamic>? connectors,
  Map<String, dynamic>? executionTopology,
  Map<String, dynamic>? syncTopology,
}) {
  final graph = runtimeGraph ?? <String, dynamic>{};
  final nodes = stableSorted<Map<String, dynamic>>(
    _maps(graph['nodes']),
    (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
  );
  final edges = stableSorted<Map<String, dynamic>>(
    _maps(graph['edges']),
    (a, b) {
      var c = pyStrCompare(_str(a['from']), _str(b['from']));
      if (c != 0) return c;
      c = pyStrCompare(_str(a['to']), _str(b['to']));
      if (c != 0) return c;
      return pyStrCompare(_str(a['relation']), _str(b['relation']));
    },
  );
  final workerList = stableSorted<Map<String, dynamic>>(
    _maps(workers ?? <dynamic>[]),
    (a, b) => pyStrCompare(_str(a['worker_id']), _str(b['worker_id'])),
  );
  final connectorList = stableSorted<Map<String, dynamic>>(
    _maps(connectors ?? <dynamic>[]),
    (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
  );

  return <String, dynamic>{
    'distributed_workers': workerList,
    'runtime_graph': <String, dynamic>{'nodes': nodes, 'edges': edges},
    'connector_topology': connectorList,
    'execution_topology': Map<String, dynamic>.from(executionTopology ?? {}),
    'synchronization_topology': Map<String, dynamic>.from(syncTopology ?? {}),
    'reconstructed': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_runtime_identity
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructRuntimeIdentity({
  Map<String, dynamic>? browserIdentity,
  Map<String, dynamic>? session,
  String runtimeId = '',
  String executionId = '',
  String workerId = '',
}) {
  final browser = Map<String, dynamic>.from(browserIdentity ?? {});
  final sessionBody = Map<String, dynamic>.from(session ?? {});

  final browserHash = _idHash(<String, dynamic>{'browser': browser});
  final sessionHash = _idHash(<String, dynamic>{'session': sessionBody});
  final runtimeHash = _idHash(<String, dynamic>{'runtime_id': runtimeId});
  final executionHash = _idHash(<String, dynamic>{'execution_id': executionId});
  final workerHash = _idHash(<String, dynamic>{'worker_id': workerId});

  final continuity = <String>[browserHash, sessionHash, runtimeHash];
  final sortedContinuity = stableSorted<String>(continuity, pyStrCompare);

  return <String, dynamic>{
    'browser_identity': <String, dynamic>{
      ...browser,
      'identity_hash': browserHash,
    },
    'session_identity': <String, dynamic>{
      ...sessionBody,
      'identity_hash': sessionHash,
    },
    'runtime_identity': <String, dynamic>{
      'runtime_id': runtimeId,
      'identity_hash': runtimeHash,
    },
    'execution_identity': <String, dynamic>{
      'execution_id': executionId,
      'identity_hash': executionHash,
    },
    'worker_identity': <String, dynamic>{
      'worker_id': workerId,
      'identity_hash': workerHash,
    },
    'continuity_hashes': sortedContinuity,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruct_connector_runtime
// ---------------------------------------------------------------------------

const _connectorKinds = <String>{
  'database',
  'api',
  'kubernetes',
  'docker',
  'telemetry',
  'ide',
  'cicd',
};

Map<String, dynamic> reconstructConnectorRuntime({
  List<dynamic>? connectors,
  Map<String, dynamic>? liveIr,
}) {
  final conn = connectors ?? <dynamic>[];
  final live = liveIr ?? <String, dynamic>{};

  final bounded = conn.length > 1000 ? conn.sublist(0, 1000) : conn;
  final rebuilt = <Map<String, dynamic>>[];
  for (var index = 0; index < bounded.length; index++) {
    final connector = _map(bounded[index]);
    var kind = connector.containsKey('kind')
        ? _str(connector['kind'])
        : _str(connector['type']);
    if (kind.isEmpty && !connector.containsKey('kind')) kind = 'api';
    if (!_connectorKinds.contains(kind)) kind = 'api';
    rebuilt.add(<String, dynamic>{
      'id': connector.containsKey('id')
          ? _str(connector['id'])
          : 'connector:$index',
      'kind': kind,
      'state': _map(connector['state']),
      'reconstructed': true,
    });
  }

  dynamic streams =
      live.containsKey('streams') ? live['streams'] : live['connectors'];
  streams ??= <dynamic>[];
  if (streams is Map) {
    streams = _list(streams['streams']);
  }
  var streamList = streams is List ? List<dynamic>.from(streams) : <dynamic>[];
  if (streamList.length > 1000) streamList = streamList.sublist(0, 1000);

  return <String, dynamic>{
    'connectors': stableSorted<Map<String, dynamic>>(
      rebuilt,
      (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
    ),
    'streams': streamList,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// build_runtime_timeline
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeTimeline({
  List<dynamic>? events,
  List<dynamic>? actions,
  List<dynamic>? mutations,
  List<dynamic>? synchronization,
  List<dynamic>? execution,
  List<dynamic>? recovery,
  List<dynamic>? replay,
  int tick = 0,
}) {
  final timeline = <Map<String, dynamic>>[];
  final groups = <List<dynamic>>[
    <dynamic>['event', events ?? <dynamic>[]],
    <dynamic>['action', actions ?? <dynamic>[]],
    <dynamic>['mutation', mutations ?? <dynamic>[]],
    <dynamic>['sync', synchronization ?? <dynamic>[]],
    <dynamic>['execution', execution ?? <dynamic>[]],
    <dynamic>['recovery', recovery ?? <dynamic>[]],
    <dynamic>['replay', replay ?? <dynamic>[]],
  ];

  for (final group in groups) {
    final kind = group[0] as String;
    final items = group[1] as List<dynamic>;
    for (var index = 0; index < items.length; index++) {
      final item = _map(items[index]);
      timeline.add(<String, dynamic>{
        'kind': kind,
        'tick': item.containsKey('tick') ? _int(item['tick']) : tick + index,
        'id': item.containsKey('id') ? _str(item['id']) : '$kind:$index',
        'payload': Map<String, dynamic>.from(item),
      });
    }
  }

  final ordered = stableSorted<Map<String, dynamic>>(timeline, (a, b) {
    final c = _int(a['tick']).compareTo(_int(b['tick']));
    if (c != 0) return c;
    final ck = pyStrCompare(_str(a['kind']), _str(b['kind']));
    if (ck != 0) return ck;
    return pyStrCompare(_str(a['id']), _str(b['id']));
  });

  return <String, dynamic>{
    'timeline': ordered,
    'count': ordered.length,
    'replay_deterministic': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// build_runtime_replay
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeReplay({
  List<dynamic>? actions,
  List<dynamic>? transactions,
  Map<String, dynamic>? timeline,
  int tick = 0,
}) {
  final orderedActions = stableSorted<Map<String, dynamic>>(
    _maps(actions ?? <dynamic>[]),
    (a, b) => pyStrCompare(
      _str(a.containsKey('id') ? a['id'] : a['action_id']),
      _str(b.containsKey('id') ? b['id'] : b['action_id']),
    ),
  );
  final orderedTx = stableSorted<Map<String, dynamic>>(
    _maps(transactions ?? <dynamic>[]),
    (a, b) =>
        pyStrCompare(_str(a['transaction_id']), _str(b['transaction_id'])),
  );

  final chain = <Map<String, dynamic>>[];
  for (var index = 0; index < orderedActions.length; index++) {
    final action = orderedActions[index];
    chain.add(<String, dynamic>{
      'step': index,
      'action_id':
          _str(action.containsKey('id') ? action['id'] : action['action_id']),
      'tick': tick + index,
    });
  }

  return <String, dynamic>{
    'replay_chains': chain,
    'execution_restoration': <String, dynamic>{
      'actions': orderedActions,
      'transactions': orderedTx,
    },
    'runtime_continuity': <String, dynamic>{
      'tick': tick,
      'steps': chain.length
    },
    'replay_package': <String, dynamic>{
      'actions': orderedActions,
      'timeline': timeline != null ? _list(timeline['timeline']) : <dynamic>[],
      'deterministic': true,
    },
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// recover_reconstructed_runtime
// ---------------------------------------------------------------------------

Map<String, dynamic> recoverReconstructedRuntime({
  Map<String, dynamic>? checkpoint,
  List<dynamic>? failedSegments,
}) {
  final cp = checkpoint ?? <String, dynamic>{};
  final failed = _maps(failedSegments ?? <dynamic>[]);
  return <String, dynamic>{
    'checkpoint_restored': _truthy(cp),
    'failed_segments_recovered': failed.length,
    'segments': stableSorted<Map<String, dynamic>>(
      failed,
      (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
    ),
    'replay_safe': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// capture_reconstruction_snapshot
// ---------------------------------------------------------------------------

Map<String, dynamic> captureReconstructionSnapshot(Map<String, dynamic> state) {
  return <String, dynamic>{
    'state': Map<String, dynamic>.from(state),
    'topology': _map(state['topology']),
    'identities': _map(state['identities']),
    'workflows': _list(state['workflows']),
    'replay_chains': _list(state['replay_chains']),
    'captured': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// compile_reconstruction_runtime_ir
// ---------------------------------------------------------------------------

Map<String, dynamic> compileReconstructionRuntimeIr(
    Map<String, dynamic> payload) {
  return <String, dynamic>{
    'ir': 'reconstruction_runtime',
    'reconstructed_runtimes': _map(payload['runtime']),
    'replay_chains': _list(_map(payload['replay'])['replay_chains']),
    'topology': _map(payload['topology']),
    'runtime_identities': _map(payload['identity']),
    'fabricated_environments': _map(payload['fabrication']),
    'execution_continuity': _map(payload['state']),
    'validation': _map(payload['validation']),
    'browser': _map(payload['browser']),
    'application': _map(payload['application']),
    'timeline': _map(payload['timeline']),
    'clone': _map(payload['clone']),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// reconstruction_runtime_ir_to_graph
// ---------------------------------------------------------------------------

Map<String, dynamic> reconstructionRuntimeIrToGraph(
    Map<String, dynamic> reconstructionIr) {
  final nodes = <Map<String, dynamic>>[
    <String, dynamic>{'id': 'reconstruction:root', 'type': 'reconstruction'},
  ];
  final edges = <Map<String, dynamic>>[];

  final runtime = _map(reconstructionIr['reconstructed_runtimes']);
  final runtimeId = _str(runtime['runtime_id']);
  if (runtimeId.isNotEmpty) {
    nodes.add(<String, dynamic>{'id': 'runtime:$runtimeId', 'type': 'runtime'});
    edges.add(<String, dynamic>{
      'from': 'reconstruction:root',
      'to': 'runtime:$runtimeId',
      'relation': 'reconstructs',
    });
  }

  var chains = _maps(reconstructionIr['replay_chains']);
  if (chains.length > 10000) chains = chains.sublist(0, 10000);
  for (var index = 0; index < chains.length; index++) {
    final chain = chains[index];
    final stepId = _str(
        chain.containsKey('action_id') ? chain['action_id'] : 'step:$index');
    final nodeId = 'replay:$stepId';
    nodes.add(<String, dynamic>{'id': nodeId, 'type': 'replay'});
    edges.add(<String, dynamic>{
      'from': nodeId,
      'to': 'reconstruction:root',
      'relation': 'replays',
    });
  }

  final fabrication = _map(reconstructionIr['fabricated_environments']);
  if (_truthy(fabrication['fabricated'])) {
    nodes.add(
        <String, dynamic>{'id': 'fabrication:reality', 'type': 'fabrication'});
    edges.add(<String, dynamic>{
      'from': 'fabrication:reality',
      'to': 'reconstruction:root',
      'relation': 'fabricates',
    });
  }

  final clone = _map(reconstructionIr['clone']);
  if (_truthy(clone['cloned'])) {
    nodes.add(<String, dynamic>{'id': 'clone:environment', 'type': 'clone'});
    edges.add(<String, dynamic>{
      'from': 'clone:environment',
      'to': 'reconstruction:root',
      'relation': 'clones',
    });
  }

  final graph = _map(_map(reconstructionIr['topology'])['runtime_graph']);
  var graphNodes = _maps(graph['nodes']);
  if (graphNodes.length > 5000) graphNodes = graphNodes.sublist(0, 5000);
  for (final node in graphNodes) {
    final nodeId = _str(node['id']);
    if (nodeId.isNotEmpty) {
      nodes.add(<String, dynamic>{
        'id': nodeId,
        'type': node.containsKey('type') ? _str(node['type']) : 'node',
      });
    }
  }

  return <String, dynamic>{
    'ir': 'reconstruction_runtime_graph',
    'nodes': stableSorted<Map<String, dynamic>>(
      nodes,
      (a, b) => pyStrCompare(_str(a['id']), _str(b['id'])),
    ),
    'edges': edges,
    'bounded': true,
  };
}

// exported coercion helpers for the orchestrator file
Map<String, dynamic> asMap(dynamic v) => _map(v);
List<dynamic> asList(dynamic v) => _list(v);
List<Map<String, dynamic>> asMaps(dynamic v) => _maps(v);
String asStr(dynamic v) => _str(v);
bool truthy(dynamic v) => _truthy(v);
dynamic getAny(Map<String, dynamic> src, List<String> keys, dynamic fb) =>
    _getAny(src, keys, fb);
