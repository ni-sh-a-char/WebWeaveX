// Faithful Dart port of core/causality/* engine modules.
//
// Output structures are byte-for-byte parity with the Python reference under
// `computeDeterministicHash` (which sorts keys, so Dart map key order is
// irrelevant; only the set of keys + scalar/array values + array order matter).
//
// Python's `sorted()` is stable. Dart's `List.sort` is NOT, so every sort here
// uses a stable comparator (index tiebreaker) to match Python exactly.

/// Stable sort: matches Python `sorted(list, key=...)` (preserves input order
/// for equal keys). Returns a new list.
List<T> _stableSortBy<T>(
  List<T> items,
  Comparable<dynamic> Function(T) keyOf,
) {
  final indexed = <List<dynamic>>[];
  for (var i = 0; i < items.length; i++) {
    indexed.add(<dynamic>[items[i], i]);
  }
  indexed.sort((a, b) {
    final ka = keyOf(a[0] as T);
    final kb = keyOf(b[0] as T);
    final cmp = ka.compareTo(kb);
    if (cmp != 0) return cmp;
    return (a[1] as int).compareTo(b[1] as int);
  });
  return indexed.map((e) => e[0] as T).toList();
}

/// Stable multi-key sort.
List<T> _stableSortByList<T>(
  List<T> items,
  List<Comparable<dynamic>> Function(T) keysOf,
) {
  final indexed = <List<dynamic>>[];
  for (var i = 0; i < items.length; i++) {
    indexed.add(<dynamic>[items[i], i]);
  }
  indexed.sort((a, b) {
    final ka = keysOf(a[0] as T);
    final kb = keysOf(b[0] as T);
    for (var i = 0; i < ka.length; i++) {
      final cmp = ka[i].compareTo(kb[i]);
      if (cmp != 0) return cmp;
    }
    return (a[1] as int).compareTo(b[1] as int);
  });
  return indexed.map((e) => e[0] as T).toList();
}

int _stepOf(Map<String, dynamic> item) {
  final s = item['step'];
  if (s is int) return s;
  if (s is num) return s.toInt();
  if (s is String) return int.tryParse(s) ?? 0;
  return 0;
}

String _str(dynamic v) => v == null ? '' : v.toString();

// ---------------------------------------------------------------------------
// causality_orchestrator: event normalization helpers
// ---------------------------------------------------------------------------

List<Map<String, dynamic>> normalizeInteractionEvents(
  List<dynamic> interactions, [
  String runtime = 'browser',
]) {
  final events = <Map<String, dynamic>>[];
  final bounded = interactions.length > 10000
      ? interactions.sublist(0, 10000)
      : interactions;
  for (var index = 0; index < bounded.length; index++) {
    final interaction = Map<String, dynamic>.from(bounded[index] as Map);
    events.add(<String, dynamic>{
      'id': '$runtime:evt:$index',
      'runtime': runtime,
      'type': _str(interaction['action'] ?? interaction['type'] ?? 'mutation'),
      'step': index,
      'source': _str(interaction['from'] ?? interaction['selector'] ?? ''),
      'target': _str(interaction['to'] ?? ''),
      'state': _str(interaction['state'] ?? ''),
    });
  }
  return events;
}

List<Map<String, dynamic>> eventsFromNativeCognition(
  Map<String, dynamic> cognition,
) {
  final events = <Map<String, dynamic>>[];
  var step = 0;

  final interactions =
      (cognition['interactions'] as List<dynamic>?) ?? <dynamic>[];
  for (final raw in interactions) {
    final interaction = Map<String, dynamic>.from(raw as Map);
    events.add(<String, dynamic>{
      'id': 'native:evt:$step',
      'runtime': _str(cognition['runtime'] ?? 'desktop'),
      'type': _str(interaction['action'] ?? 'interaction'),
      'step': step,
    });
    step += 1;
  }

  final terminal = Map<String, dynamic>.from(
      (cognition['terminal'] as Map?) ?? <String, dynamic>{});
  final output = (terminal['output'] as List<dynamic>?) ?? <dynamic>[];
  final boundedOutput = output.length > 1000 ? output.sublist(0, 1000) : output;
  for (final line in boundedOutput) {
    events.add(<String, dynamic>{
      'id': 'terminal:evt:$step',
      'runtime': 'terminal',
      'type': 'log',
      'step': step,
      'state': line,
    });
    step += 1;
  }

  final electron = Map<String, dynamic>.from(
      (cognition['electron'] as Map?) ?? <String, dynamic>{});
  final routes = (electron['routes'] as List<dynamic>?) ?? <dynamic>[];
  for (final route in routes) {
    events.add(<String, dynamic>{
      'id': 'electron:evt:$step',
      'runtime': 'electron',
      'type': 'route',
      'step': step,
      'state': route,
    });
    step += 1;
  }

  final desktop = Map<String, dynamic>.from(
      (cognition['desktop'] as Map?) ?? <String, dynamic>{});
  final notifications =
      (desktop['notifications'] as List<dynamic>?) ?? <dynamic>[];
  for (final notification in notifications) {
    events.add(<String, dynamic>{
      'id': 'desktop:notif:$step',
      'runtime': 'desktop',
      'type': 'notification',
      'step': step,
      'state': _pyStr(notification),
    });
    step += 1;
  }

  return events;
}

// ---------------------------------------------------------------------------
// runtime_causality_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeCausality(
  List<Map<String, dynamic>> events,
  Map<String, dynamic> origins,
) {
  final ordered = _stableSortBy(events, _stepOf);
  final causalEdges = <Map<String, dynamic>>[];

  for (var index = 1; index < ordered.length; index++) {
    final prevId = _str(ordered[index - 1]['id'] ?? 'evt:${index - 1}');
    final currId = _str(ordered[index]['id'] ?? 'evt:$index');
    causalEdges.add(<String, dynamic>{
      'from': prevId,
      'to': currId,
      'relation': 'propagates',
    });
  }

  final propagationOrder =
      ordered.map((event) => _str(event['id'] ?? '')).toList();

  return <String, dynamic>{
    'events': ordered,
    'causal_edges': causalEdges,
    'runtime_origins': Map<String, dynamic>.from(origins),
    'propagation_order': propagationOrder,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// event_chain_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildEventChain(List<Map<String, dynamic>> events) {
  final ordered = _stableSortBy(events, _stepOf);
  final boundedOrdered =
      ordered.length > 10000 ? ordered.sublist(0, 10000) : ordered;
  final chain = <Map<String, dynamic>>[];

  for (var index = 0; index < boundedOrdered.length; index++) {
    final event = boundedOrdered[index];
    chain.add(<String, dynamic>{
      'id': _str(event['id'] ?? 'evt:$index'),
      'runtime': _str(event['runtime'] ?? 'unknown'),
      'type': _str(event['type'] ?? 'mutation'),
      'step': index,
      'depth': index,
    });
  }

  final firstRuntime = chain.isNotEmpty ? chain[0]['runtime'] : null;
  final synchronized = <dynamic>[];
  for (final item in chain) {
    if (chain.isNotEmpty && item['runtime'] != firstRuntime) {
      synchronized.add(item['id']);
    }
  }

  return <String, dynamic>{
    'chain': chain,
    'length': chain.length,
    'max_depth': chain.isNotEmpty ? chain.length - 1 : 0,
    'synchronized': synchronized,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// cross_runtime_alignment_engine
// ---------------------------------------------------------------------------

const _runtimeOrder = <String>[
  'browser',
  'application',
  'electron',
  'desktop',
  'terminal',
  'vm',
  'remote',
  'distributed',
];

Map<String, dynamic> alignCrossRuntimeEvents(
  List<Map<String, dynamic>> events,
) {
  final buckets = <String, List<Map<String, dynamic>>>{};
  for (final runtime in _runtimeOrder) {
    buckets[runtime] = <Map<String, dynamic>>[];
  }

  final bounded = events.length > 20000 ? events.sublist(0, 20000) : events;
  for (final event in bounded) {
    final runtime = _str(event['runtime'] ?? 'browser').toLowerCase();
    buckets.putIfAbsent(runtime, () => <Map<String, dynamic>>[]);
    buckets[runtime]!.add(event);
  }

  final aligned = <Map<String, dynamic>>[];
  var step = 0;
  for (final runtime in _runtimeOrder) {
    final sortedBucket =
        _stableSortBy(buckets[runtime] ?? <Map<String, dynamic>>[], _stepOf);
    for (final event in sortedBucket) {
      aligned.add(<String, dynamic>{
        ...event,
        'aligned_step': step,
        'aligned_runtime': runtime,
      });
      step += 1;
    }
  }

  final correlations = <Map<String, dynamic>>[];
  for (var index = 1; index < aligned.length; index++) {
    final prev = aligned[index - 1];
    final curr = aligned[index];
    correlations.add(<String, dynamic>{
      'from_runtime': prev['runtime'] ?? '',
      'to_runtime': curr['runtime'] ?? '',
      'from_event': prev['id'] ?? '',
      'to_event': curr['id'] ?? '',
      'correlation_id': 'corr:$index',
    });
  }

  final runtimeSet = <dynamic>{};
  for (final e in aligned) {
    runtimeSet.add(e['runtime']);
  }

  return <String, dynamic>{
    'aligned_events': aligned,
    'correlations': correlations,
    'runtime_count': runtimeSet.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// workflow_propagation_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildWorkflowPropagation(
  Map<String, dynamic> aligned,
  Map<String, dynamic> dependencies,
) {
  final events = List<Map<String, dynamic>>.from(
    (aligned['aligned_events'] as List<dynamic>? ?? <dynamic>[])
        .map((e) => Map<String, dynamic>.from(e as Map)),
  );
  final handoffs = <Map<String, dynamic>>[];

  for (var index = 1; index < events.length; index++) {
    final prev = events[index - 1];
    final curr = events[index];
    if (prev['runtime'] != curr['runtime']) {
      handoffs.add(<String, dynamic>{
        'from': _str(prev['runtime'] ?? ''),
        'to': _str(curr['runtime'] ?? ''),
        'step': index,
        'workflow_id': 'wf:$index',
      });
    }
  }

  final syncChains =
      (dependencies['synchronization_chains'] as List<dynamic>?) ?? <dynamic>[];

  return <String, dynamic>{
    'continuations': handoffs,
    'handoffs': handoffs,
    'distributed': List<dynamic>.from(syncChains),
    'synchronized_steps':
        events.map((event) => event['aligned_step'] ?? 0).toList(),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_dependency_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeDependencies(
  List<Map<String, dynamic>> events,
  Map<String, dynamic> propagation,
) {
  final dependencies = <Map<String, dynamic>>[];
  final consumers = <Map<String, dynamic>>[];
  final syncChains = <Map<String, dynamic>>[];

  final runtimesSeen = <String>[];
  final ordered = _stableSortBy(events, _stepOf);
  for (final event in ordered) {
    final runtime = _str(event['runtime'] ?? '');
    if (runtime.isNotEmpty && !runtimesSeen.contains(runtime)) {
      if (runtimesSeen.isNotEmpty) {
        dependencies.add(<String, dynamic>{
          'from': runtimesSeen.last,
          'to': runtime,
          'relation': 'depends_on',
        });
      }
      runtimesSeen.add(runtime);
      consumers.add(<String, dynamic>{
        'runtime': runtime,
        'event_id': _str(event['id'] ?? ''),
      });
    }
  }

  final handoffs = (propagation['handoffs'] as List<dynamic>?) ?? <dynamic>[];
  final boundedHandoffs =
      handoffs.length > 5000 ? handoffs.sublist(0, 5000) : handoffs;
  for (final raw in boundedHandoffs) {
    final handoff = Map<String, dynamic>.from(raw as Map);
    syncChains.add(<String, dynamic>{
      'from': handoff['from'] ?? '',
      'to': handoff['to'] ?? '',
      'workflow_id': handoff['workflow_id'] ?? '',
    });
  }

  return <String, dynamic>{
    'dependencies': dependencies,
    'consumers': consumers,
    'synchronization_chains': syncChains,
    'causal_relationships': dependencies,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// causal_graph_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildCausalGraph(
  List<Map<String, dynamic>> events,
  Map<String, dynamic> causality,
) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];
  final seenRuntimes = <String>{};

  final boundedEvents =
      events.length > 10000 ? events.sublist(0, 10000) : events;
  for (final event in boundedEvents) {
    final eventId = _str(event['id'] ?? '');
    nodes.add(<String, dynamic>{
      'id': eventId,
      'type': 'event',
      'runtime': _str(event['runtime'] ?? ''),
    });

    final runtime = _str(event['runtime'] ?? '');
    if (runtime.isNotEmpty && !seenRuntimes.contains(runtime)) {
      seenRuntimes.add(runtime);
      nodes.add(<String, dynamic>{
        'id': 'runtime:$runtime',
        'type': 'runtime',
      });
      edges.add(<String, dynamic>{
        'from': 'runtime:$runtime',
        'to': eventId,
        'relation': 'triggers',
      });
    }
  }

  final causalEdges =
      (causality['causal_edges'] as List<dynamic>?) ?? <dynamic>[];
  final boundedCausal =
      causalEdges.length > 10000 ? causalEdges.sublist(0, 10000) : causalEdges;
  for (final raw in boundedCausal) {
    final edge = Map<String, dynamic>.from(raw as Map);
    edges.add(<String, dynamic>{
      'from': _str(edge['from'] ?? ''),
      'to': _str(edge['to'] ?? ''),
      'relation': 'propagates',
    });
  }

  for (var index = 0; index < boundedEvents.length; index++) {
    final event = boundedEvents[index];
    if (event['type'] == 'notification') {
      final eventId = _str(event['id'] ?? 'evt:$index');
      edges.add(<String, dynamic>{
        'from': eventId,
        'to': 'workflow:$index',
        'relation': 'mutates',
      });
    }
  }

  if (nodes.isEmpty) {
    nodes.add(<String, dynamic>{'id': 'causality:root', 'type': 'causality'});
  }

  final sortedNodes = _stableSortBy(nodes, (n) => _str(n['id']));
  final sortedEdges = _stableSortByList(
    edges,
    (e) => <Comparable<dynamic>>[
      _str(e['from'] ?? ''),
      _str(e['to'] ?? ''),
      _str(e['relation'] ?? ''),
    ],
  );

  return <String, dynamic>{
    'nodes': sortedNodes,
    'edges': sortedEdges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// state_transition_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildStateTransitions(List<Map<String, dynamic>> events) {
  final transitions = <Map<String, dynamic>>[];

  for (var index = 1; index < events.length; index++) {
    final prev = events[index - 1];
    final curr = events[index];
    transitions.add(<String, dynamic>{
      'from_state': _str(prev['state'] ?? prev['type'] ?? ''),
      'to_state': _str(curr['state'] ?? curr['type'] ?? ''),
      'runtime': _str(curr['runtime'] ?? ''),
      'step': index,
    });
  }

  return <String, dynamic>{
    'transitions': transitions,
    'count': transitions.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_sequence_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeSequence(List<Map<String, dynamic>> events) {
  final ordered = _stableSortBy(events, _stepOf);
  final bounded = ordered.length > 10000 ? ordered.sublist(0, 10000) : ordered;

  final sequence = <Map<String, dynamic>>[];
  for (var index = 0; index < bounded.length; index++) {
    final event = bounded[index];
    final step = event.containsKey('step') ? _stepOf(event) : index;
    sequence.add(<String, dynamic>{
      'id': _str(event['id'] ?? ''),
      'runtime': _str(event['runtime'] ?? ''),
      'type': _str(event['type'] ?? ''),
      'step': step,
    });
  }

  return <String, dynamic>{
    'sequence': sequence,
    'length': ordered.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_timeline_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildRuntimeTimeline(
  List<Map<String, dynamic>> events,
  Map<String, dynamic> propagation,
) {
  final ordered = _stableSortBy(events, _stepOf);
  final bounded = ordered.length > 10000 ? ordered.sublist(0, 10000) : ordered;
  final timeline = <Map<String, dynamic>>[];

  final handoffs = (propagation['handoffs'] as List<dynamic>?) ?? <dynamic>[];

  for (var index = 0; index < bounded.length; index++) {
    final event = bounded[index];
    final propagationMap = <dynamic>[];
    for (final raw in handoffs) {
      final handoff = Map<String, dynamic>.from(raw as Map);
      if (handoff['step'] == index) {
        propagationMap.add(handoff['workflow_id'] ?? '');
      }
    }
    timeline.add(<String, dynamic>{
      'step': index,
      'event_id': _str(event['id'] ?? 'evt:$index'),
      'runtime': _str(event['runtime'] ?? ''),
      'type': _str(event['type'] ?? 'mutation'),
      'propagation_map': propagationMap,
    });
  }

  return <String, dynamic>{
    'timeline': timeline,
    'evolution_history': timeline.map((entry) => entry['event_id']).toList(),
    'propagation_maps': List<dynamic>.from(handoffs),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_correlation_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> correlateRuntimeMutations({
  List<Map<String, dynamic>>? browserEvents,
  List<Map<String, dynamic>>? nativeEvents,
  List<dynamic>? notifications,
  List<dynamic>? terminalLines,
  List<dynamic>? processEvents,
}) {
  final correlations = <Map<String, dynamic>>[];
  var step = 0;

  for (final event in browserEvents ?? <Map<String, dynamic>>[]) {
    correlations.add(<String, dynamic>{
      'kind': 'ui_change',
      'event_id': _str(event['id'] ?? 'browser:$step'),
      'runtime': 'browser',
      'step': step,
    });
    step += 1;
  }

  final lines = terminalLines ?? <dynamic>[];
  final boundedLines = lines.length > 1000 ? lines.sublist(0, 1000) : lines;
  for (final line in boundedLines) {
    correlations.add(<String, dynamic>{
      'kind': 'terminal_log',
      'line': line,
      'runtime': 'terminal',
      'step': step,
    });
    step += 1;
  }

  for (final notification in notifications ?? <dynamic>[]) {
    correlations.add(<String, dynamic>{
      'kind': 'notification',
      'payload': notification,
      'runtime': 'desktop',
      'step': step,
    });
    step += 1;
  }

  for (final event in nativeEvents ?? <Map<String, dynamic>>[]) {
    correlations.add(<String, dynamic>{
      'kind': 'native_mutation',
      'event_id': _str(event['id'] ?? ''),
      'runtime': _str(event['runtime'] ?? 'desktop'),
      'step': step,
    });
    step += 1;
  }

  for (final raw in processEvents ?? <dynamic>[]) {
    final proc = Map<String, dynamic>.from(raw as Map);
    correlations.add(<String, dynamic>{
      'kind': 'process_mutation',
      'process': _str(proc['name'] ?? ''),
      'runtime': 'process',
      'step': step,
    });
    step += 1;
  }

  final sorted = _stableSortBy(
    correlations,
    (item) => item['step'] as int,
  );

  return <String, dynamic>{
    'correlations': sorted,
    'count': correlations.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// distributed_causality_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildDistributedCausality([
  Map<String, dynamic>? distributedResult,
  List<Map<String, dynamic>>? workerEvents,
]) {
  final result = distributedResult ?? <String, dynamic>{};
  final workerList = workerEvents ?? <Map<String, dynamic>>[];

  final workers = (result['workers'] as List<dynamic>?) ?? <dynamic>[];
  final chains = <Map<String, dynamic>>[];

  final bounded =
      workerList.length > 10000 ? workerList.sublist(0, 10000) : workerList;
  for (var index = 0; index < bounded.length; index++) {
    final event = bounded[index];
    chains.add(<String, dynamic>{
      'worker_id': _str(event['worker_id'] ?? 'worker_$index'),
      'event_id': _str(event['id'] ?? 'dist:$index'),
      'step': index,
      'relation': 'cluster_sync',
    });
  }

  final tasks = (result['tasks'] as List<dynamic>?) ?? <dynamic>[];
  final boundedTasks = tasks.length > 1000 ? tasks.sublist(0, 1000) : tasks;

  return <String, dynamic>{
    'worker_causality': chains,
    'autonomous_propagation': result['autonomous'] ?? false,
    'remote_chains': List<dynamic>.from(boundedTasks),
    'cluster_synchronization': <String, dynamic>{
      'worker_count': workers.length,
      'synced': workers.isNotEmpty,
    },
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// browser_native_bridge_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> bridgeBrowserNativeRuntime(
  List<Map<String, dynamic>> browserEvents,
  List<Map<String, dynamic>> nativeEvents,
) {
  final bridges = <Map<String, dynamic>>[];
  final step = browserEvents.length;

  final bounded =
      nativeEvents.length > 5000 ? nativeEvents.sublist(0, 5000) : nativeEvents;
  for (var index = 0; index < bounded.length; index++) {
    final nativeEvent = bounded[index];
    final source = browserEvents.isNotEmpty
        ? browserEvents.last
        : <String, dynamic>{'id': 'browser:root'};
    bridges.add(<String, dynamic>{
      'from_runtime': 'browser',
      'to_runtime': _str(nativeEvent['runtime'] ?? 'desktop'),
      'from_event': _str(source['id'] ?? ''),
      'to_event': _str(nativeEvent['id'] ?? 'native:$index'),
      'relation': 'propagates',
      'step': step + index,
    });
  }

  return <String, dynamic>{
    'bridges': bridges,
    'chain_length': bridges.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// electron_terminal_bridge_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> bridgeElectronTerminalRuntime(
  List<Map<String, dynamic>> electronEvents,
  List<Map<String, dynamic>> terminalEvents,
) {
  final bridges = <Map<String, dynamic>>[];

  final electronRef = electronEvents.isNotEmpty
      ? electronEvents.last
      : <String, dynamic>{'id': 'electron:root'};

  final bounded = terminalEvents.length > 5000
      ? terminalEvents.sublist(0, 5000)
      : terminalEvents;
  for (var index = 0; index < bounded.length; index++) {
    final terminalEvent = bounded[index];
    bridges.add(<String, dynamic>{
      'from_runtime': 'electron',
      'to_runtime': 'terminal',
      'from_event': _str(electronRef['id'] ?? ''),
      'to_event': _str(terminalEvent['id'] ?? 'terminal:$index'),
      'relation': 'triggers',
      'step': index,
    });
  }

  return <String, dynamic>{
    'bridges': bridges,
    'synchronization_chain': bridges.map((b) => b['to_event']).toList(),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// notification_causality_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> trackNotificationCausality(
  List<dynamic> notifications,
  List<Map<String, dynamic>> originEvents,
) {
  final tracked = <Map<String, dynamic>>[];

  final originId =
      originEvents.isNotEmpty ? _str(originEvents.last['id'] ?? '') : '';

  final bounded = notifications.length > 5000
      ? notifications.sublist(0, 5000)
      : notifications;
  for (var index = 0; index < bounded.length; index++) {
    final notification = bounded[index];
    String notificationId;
    bool userInteraction;
    if (notification is Map) {
      final m = Map<String, dynamic>.from(notification);
      notificationId = _str(m['id'] ?? 'notif:$index');
      userInteraction = _truthy(m['interaction']);
    } else {
      notificationId = 'notif:$index';
      userInteraction = false;
    }

    tracked.add(<String, dynamic>{
      'notification_id': notificationId,
      'origin_event': originId,
      'downstream_workflow': 'workflow:notif:$index',
      'user_interaction': userInteraction,
      'payload': _pyStr(notification),
    });
  }

  return <String, dynamic>{
    'notifications': tracked,
    'origin_event': originId,
    'count': tracked.length,
    'bounded': true,
  };
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

// ---------------------------------------------------------------------------
// process_causality_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> trackProcessCausality(
  List<dynamic> processes,
  List<Map<String, dynamic>> events,
) {
  final chains = <Map<String, dynamic>>[];

  final bounded =
      processes.length > 5000 ? processes.sublist(0, 5000) : processes;
  for (var index = 0; index < bounded.length; index++) {
    final process = Map<String, dynamic>.from(bounded[index] as Map);
    final parent = _str(process['parent'] ?? '');
    chains.add(<String, dynamic>{
      'process': _str(process['name'] ?? process['pid'] ?? 'proc:$index'),
      'parent': parent,
      'launched_at_step': index,
      'mutation_event':
          _str(index < events.length ? (events[index]['id'] ?? '') : ''),
    });
  }

  var subprocessDepth = 0;
  for (final c in chains) {
    final d = c['launched_at_step'] as int;
    if (d > subprocessDepth) subprocessDepth = d;
  }

  return <String, dynamic>{
    'process_chains': chains,
    'subprocess_depth': subprocessDepth,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// causal_recovery_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> recoverCausalRuntime(
  Map<String, dynamic> causality,
  List<Map<String, dynamic>> events,
) {
  var propagationOrder = List<dynamic>.from(
    (causality['propagation_order'] as List<dynamic>?) ?? <dynamic>[],
  );
  final recoveredEvents = List<Map<String, dynamic>>.from(events);

  if (propagationOrder.isEmpty && events.isNotEmpty) {
    propagationOrder = events.map((event) => _str(event['id'] ?? '')).toList();
  }

  final gaps = <int>[];
  for (var index = 1; index < propagationOrder.length; index++) {
    final v = propagationOrder[index];
    if (v == null || v == '' || v == false || v == 0) {
      gaps.add(index);
    }
  }

  for (final gapIndex in gaps) {
    recoveredEvents.add(<String, dynamic>{
      'id': 'recovered:evt:$gapIndex',
      'runtime': 'recovery',
      'type': 'restore',
      'step': gapIndex,
      'recovered': true,
    });
  }

  final recoveredOrder = _stableSortBy(recoveredEvents, _stepOf);

  return <String, dynamic>{
    'recovered_events': recoveredOrder,
    'propagation_order':
        recoveredOrder.map((event) => _str(event['id'] ?? '')).toList(),
    'broken_chains_fixed': gaps.length,
    'synchronization_restored': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// ir/causal_runtime_ir
// ---------------------------------------------------------------------------

Map<String, dynamic> compileCausalRuntimeIr(Map<String, dynamic> cognition) {
  return <String, dynamic>{
    'ir': 'causal_runtime',
    'causal_graphs': cognition['causal_graph'] ?? <String, dynamic>{},
    'timelines': cognition['timeline'] ?? <String, dynamic>{},
    'event_chains': cognition['event_chain'] ?? <String, dynamic>{},
    'propagation_maps': cognition['propagation'] ?? <String, dynamic>{},
    'distributed_synchronization':
        cognition['distributed'] ?? <String, dynamic>{},
    'runtime_dependencies': cognition['dependencies'] ?? <String, dynamic>{},
    'alignment': cognition['alignment'] ?? <String, dynamic>{},
    'bridges': <String, dynamic>{
      'browser_native': cognition['browser_bridge'] ?? <String, dynamic>{},
      'electron_terminal': cognition['electron_bridge'] ?? <String, dynamic>{},
    },
    'recovery_state': cognition['recovery'] ?? <String, dynamic>{},
    'bounded': true,
  };
}

Map<String, dynamic> causalRuntimeIrToGraph(Map<String, dynamic> causalIr) {
  final graph = Map<String, dynamic>.from(
    (causalIr['causal_graphs'] as Map?) ?? <String, dynamic>{},
  );
  var nodes = List<Map<String, dynamic>>.from(
    (graph['nodes'] as List<dynamic>? ?? <dynamic>[])
        .map((n) => Map<String, dynamic>.from(n as Map)),
  );
  final edges = List<dynamic>.from(
    (graph['edges'] as List<dynamic>?) ?? <dynamic>[],
  );

  if (nodes.isEmpty) {
    nodes = <Map<String, dynamic>>[
      <String, dynamic>{'id': 'causality:root', 'type': 'causality'},
    ];
  }

  final timeline = Map<String, dynamic>.from(
    (causalIr['timelines'] as Map?) ?? <String, dynamic>{},
  );
  final timelineEntries =
      (timeline['timeline'] as List<dynamic>?) ?? <dynamic>[];
  final boundedTimeline = timelineEntries.length > 5000
      ? timelineEntries.sublist(0, 5000)
      : timelineEntries;
  for (final raw in boundedTimeline) {
    final entry = Map<String, dynamic>.from(raw as Map);
    nodes.add(<String, dynamic>{
      'id': _str(entry['event_id'] ?? ''),
      'type': 'timeline_event',
      'runtime': _str(entry['runtime'] ?? ''),
    });
  }

  final sortedNodes = _stableSortBy(nodes, (n) => _str(n['id'] ?? ''));

  return <String, dynamic>{
    'ir': 'causal_runtime_graph',
    'nodes': sortedNodes,
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_graph_engine (build_runtime_graph) — minimal faithful port for the
// merge_graph=True path.
// ---------------------------------------------------------------------------

Map<String, dynamic> buildUnifiedRuntimeGraph(
  List<Map<String, dynamic>> runtimeIrs,
) {
  const maxNodes = 1000000;
  const maxEdges = 5000000;

  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];
  final seenNodes = <String>{};
  final seenEdges = <String>{};

  final boundedIrs =
      runtimeIrs.length > 10000 ? runtimeIrs.sublist(0, 10000) : runtimeIrs;
  for (final runtime in boundedIrs) {
    final runtimeType = _str(runtime['ir'] ?? 'unknown');

    final runtimeNodes = (runtime['nodes'] as List<dynamic>?) ?? <dynamic>[];
    final runtimeEdges = (runtime['edges'] as List<dynamic>?) ?? <dynamic>[];

    for (final raw in runtimeNodes) {
      final node = Map<String, dynamic>.from(raw as Map);
      final nodeId = _str(node['id'] ?? '').trim();
      if (nodeId.isEmpty) continue;
      if (seenNodes.contains(nodeId)) continue;
      seenNodes.add(nodeId);
      final enriched = Map<String, dynamic>.from(node);
      enriched['runtime_type'] = runtimeType;
      nodes.add(enriched);
      if (nodes.length >= maxNodes) break;
    }

    for (final raw in runtimeEdges) {
      final edge = Map<String, dynamic>.from(raw as Map);
      final src = _str(edge['from'] ?? '').trim();
      final dst = _str(edge['to'] ?? '').trim();
      final relation = _str(edge['relation'] ?? 'related_to').trim();
      if (src.isEmpty || dst.isEmpty) continue;
      final edgeKey = '$src $dst $relation';
      if (seenEdges.contains(edgeKey)) continue;
      seenEdges.add(edgeKey);
      final enriched = Map<String, dynamic>.from(edge);
      enriched['runtime_type'] = runtimeType;
      edges.add(enriched);
      if (edges.length >= maxEdges) break;
    }
  }

  final sortedNodes = _stableSortBy(nodes, (n) => _str(n['id'] ?? ''));
  final sortedEdges = _stableSortByList(
    edges,
    (e) => <Comparable<dynamic>>[
      _str(e['from'] ?? ''),
      _str(e['to'] ?? ''),
      _str(e['relation'] ?? ''),
    ],
  );

  return <String, dynamic>{
    'ir': 'unified_runtime_graph',
    'nodes': sortedNodes,
    'edges': sortedEdges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// Python-compatible str() for arbitrary values (used by notification payload).
// ---------------------------------------------------------------------------

String _pyStr(dynamic value) {
  if (value is String) return value;
  if (value is bool) return value ? 'True' : 'False';
  if (value == null) return 'None';
  if (value is Map) {
    final entries = value.entries
        .map((e) => '${_pyRepr(e.key)}: ${_pyRepr(e.value)}')
        .join(', ');
    return '{$entries}';
  }
  if (value is List) {
    final entries = value.map(_pyRepr).join(', ');
    return '[$entries]';
  }
  return value.toString();
}

String _pyRepr(dynamic value) {
  if (value is String) return "'$value'";
  if (value is bool) return value ? 'True' : 'False';
  if (value == null) return 'None';
  if (value is Map || value is List) return _pyStr(value);
  return value.toString();
}
