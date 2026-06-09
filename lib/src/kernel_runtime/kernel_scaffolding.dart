/// Port of the deterministic kernel scaffolding modules:
///   core/kernel/runtime_scheduler.py, runtime_registry.py, runtime_bus.py,
///   runtime_topology.py, runtime_coordination.py, runtime_replay.py,
///   runtime_policy.py, runtime_lifecycle.py, runtime_state.py,
///   runtime_context.py, runtime_boundary.py
///
/// Every function here is byte-identical to its Python counterpart under
/// `compute_deterministic_hash`. `enforceRuntimeBoundary` additionally
/// reproduces Python `json.dumps(..., sort_keys=True, default=str)` byte length.
library;

const int maxBusEvents = 100000;
const int maxPayloadBytes = 50000000;
const int maxIrCount = 10000;

const List<String> _registryPhases = <String>[
  'browser',
  'semantic',
  'workflow',
  'synchronization',
  'evolution',
  'connectors',
  'memory',
  'execution',
  'reconstruction',
];

// --- runtime_scheduler.py ---
Map<String, dynamic> scheduleKernelPhases(List<String> phases, {int tick = 0}) {
  final scheduled = <Map<String, dynamic>>[];
  for (var i = 0; i < phases.length; i++) {
    scheduled.add(<String, dynamic>{
      'phase': phases[i],
      'tick': tick + i,
      'priority': i,
    });
  }
  // sorted by priority (already ascending; stable index-tiebreak).
  final indexed = scheduled.asMap().entries.toList()
    ..sort((a, b) {
      final cmp =
          (a.value['priority'] as int).compareTo(b.value['priority'] as int);
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });
  return <String, dynamic>{
    'scheduled': indexed.map((e) => e.value).toList(),
    'deterministic': true,
    'bounded': true,
  };
}

// --- runtime_registry.py ---
Map<String, dynamic> registerRuntimePhase(
  Map<String, dynamic> registry,
  String phase,
  Map<String, dynamic> payload,
) {
  final priorRaw = registry['phases'];
  final phases = priorRaw is Map
      ? Map<String, dynamic>.from(priorRaw)
      : <String, dynamic>{};
  phases[phase] = payload;
  final registered = phases.keys.toList()..sort();
  return <String, dynamic>{
    'phases': phases,
    'registered': registered,
    'bounded': true,
  };
}

List<String> listRuntimePhases() => List<String>.from(_registryPhases);

// --- runtime_bus.py ---
Map<String, dynamic> publishRuntimeEvent(
  List<Map<String, dynamic>> bus,
  String eventType,
  Map<String, dynamic> payload, {
  int tick = 0,
}) {
  final events = List<Map<String, dynamic>>.from(bus);
  events.add(<String, dynamic>{
    'type': eventType,
    'tick': tick,
    'payload': Map<String, dynamic>.from(payload),
    'order': events.length,
  });
  final indexed = events.asMap().entries.toList()
    ..sort((a, b) {
      final at = a.value['tick'] as int;
      final bt = b.value['tick'] as int;
      if (at != bt) return at.compareTo(bt);
      final ao = a.value['order'] as int;
      final bo = b.value['order'] as int;
      if (ao != bo) return ao.compareTo(bo);
      return a.key.compareTo(b.key);
    });
  final sorted = indexed.map((e) => e.value).take(maxBusEvents).toList();
  return <String, dynamic>{
    'bus': sorted,
    'size': sorted.length,
    'bounded': true
  };
}

// --- runtime_topology.py ---
Map<String, dynamic> buildKernelTopology([Map<String, dynamic>? graph]) {
  final g = graph ?? <String, dynamic>{};
  final rawNodes = (g['nodes'] as List<dynamic>?) ?? <dynamic>[];
  final rawEdges = (g['edges'] as List<dynamic>?) ?? <dynamic>[];

  final nodes = rawNodes.asMap().entries.toList()
    ..sort((a, b) {
      final cmp = '${(a.value as Map)['id'] ?? ''}'
          .compareTo('${(b.value as Map)['id'] ?? ''}');
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });
  final edges = rawEdges.asMap().entries.toList()
    ..sort((a, b) {
      final ma = a.value as Map;
      final mb = b.value as Map;
      var cmp = '${ma['from'] ?? ''}'.compareTo('${mb['from'] ?? ''}');
      if (cmp != 0) return cmp;
      cmp = '${ma['to'] ?? ''}'.compareTo('${mb['to'] ?? ''}');
      if (cmp != 0) return cmp;
      cmp = '${ma['relation'] ?? ''}'.compareTo('${mb['relation'] ?? ''}');
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });

  final sortedNodes = nodes.map((e) => e.value).toList();
  return <String, dynamic>{
    'nodes': sortedNodes,
    'edges': edges.map((e) => e.value).toList(),
    'node_count': sortedNodes.length,
    'bounded': true,
  };
}

// --- runtime_coordination.py ---
Map<String, dynamic> coordinateKernelPhases(
  List<Map<String, dynamic>> phaseResults, {
  int tick = 0,
}) {
  final ordered = phaseResults.asMap().entries.toList()
    ..sort((a, b) {
      final cmp =
          '${a.value['phase'] ?? ''}'.compareTo('${b.value['phase'] ?? ''}');
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });
  return <String, dynamic>{
    'phases': ordered.map((e) => e.value).toList(),
    'tick': tick,
    'coordinated': true,
    'bounded': true,
  };
}

// --- runtime_replay.py ---
Map<String, dynamic> replayKernelState(List<Map<String, dynamic>> events) {
  final ordered = events.asMap().entries.toList()
    ..sort((a, b) {
      final at = (a.value['tick'] as int?) ?? 0;
      final bt = (b.value['tick'] as int?) ?? 0;
      if (at != bt) return at.compareTo(bt);
      final ao = (a.value['order'] as int?) ?? 0;
      final bo = (b.value['order'] as int?) ?? 0;
      if (ao != bo) return ao.compareTo(bo);
      return a.key.compareTo(b.key);
    });
  return <String, dynamic>{
    'events': ordered.map((e) => e.value).toList(),
    'replayed': true,
    'identical': true,
    'bounded': true,
  };
}

// --- runtime_policy.py ---
Map<String, dynamic> buildKernelPolicy({
  int maxPhases = 20,
  int maxGraphNodes = 1000000,
  bool requireKaalkaPersistence = true,
  bool allowSimulation = true,
}) {
  return <String, dynamic>{
    'max_phases': maxPhases,
    'max_graph_nodes': maxGraphNodes,
    'require_kaalka_persistence': requireKaalkaPersistence,
    'allow_simulation': allowSimulation,
    'deterministic': true,
    'bounded': true,
  };
}

Map<String, dynamic> enforceKernelPolicy(
  Map<String, dynamic> policy,
  int phaseCount,
  int nodeCount,
) {
  final withinPhases = phaseCount <= ((policy['max_phases'] as int?) ?? 20);
  final withinGraph =
      nodeCount <= ((policy['max_graph_nodes'] as int?) ?? 1000000);
  final allowed = withinPhases && withinGraph;
  return <String, dynamic>{
    'allowed': allowed,
    'within_bounds': allowed,
    'bounded': true,
  };
}

// --- runtime_context.py ---
Map<String, dynamic> buildRuntimeContext({
  String runtimeType = 'browser',
  int tick = 0,
  Map<String, dynamic>? sources,
  Map<String, dynamic>? policy,
}) {
  return <String, dynamic>{
    'runtime_type': runtimeType,
    'tick': tick,
    'sources': Map<String, dynamic>.from(sources ?? <String, dynamic>{}),
    'policy': Map<String, dynamic>.from(policy ?? <String, dynamic>{}),
    'phase_state': <String, dynamic>{},
    'bounded': true,
  };
}

// --- runtime_state.py ---
Map<String, dynamic> buildKernelState(
  Map<String, dynamic> context, {
  List<Map<String, dynamic>>? irs,
  Map<String, dynamic>? graph,
}) {
  return <String, dynamic>{
    'context': Map<String, dynamic>.from(context),
    'irs': List<Map<String, dynamic>>.from(irs ?? <Map<String, dynamic>>[]),
    'graph': Map<String, dynamic>.from(graph ?? <String, dynamic>{}),
    'tick': (context['tick'] as int?) ?? 0,
    'bounded': true,
  };
}

Map<String, dynamic> mergeKernelState(
  Map<String, dynamic> prior,
  Map<String, dynamic> update,
) {
  final merged = Map<String, dynamic>.from(prior);
  merged.addAll(update);
  final priorIrs = (prior['irs'] as List<dynamic>?) ?? <dynamic>[];
  final updateIrs = (update['irs'] as List<dynamic>?) ?? <dynamic>[];
  merged['irs'] = <dynamic>[...priorIrs, ...updateIrs];
  return merged;
}

// --- runtime_lifecycle.py ---
Map<String, dynamic> initializeRuntime({
  String runtimeType = 'browser',
  int tick = 0,
}) {
  final context = buildRuntimeContext(runtimeType: runtimeType, tick: tick);
  final policy = buildKernelPolicy();
  final state = buildKernelState(context);
  return <String, dynamic>{
    'context': context,
    'policy': policy,
    'state': state,
    'initialized': true,
    'bounded': true,
  };
}

Map<String, dynamic> shutdownRuntime(Map<String, dynamic> state) {
  return <String, dynamic>{
    'shutdown': true,
    'final_tick': (state['tick'] as int?) ?? 0,
    'bounded': true,
  };
}

// --- runtime_boundary.py ---
/// Reproduces Python `json.dumps(payload, sort_keys=True, default=str)` byte
/// length: keys sorted, separators `", "`/`": "`, `true/false/null`, floats
/// rendered as Python `repr(float)` (e.g. `1.0`).
String _pyJsonDumps(dynamic value) {
  final buf = StringBuffer();
  _encode(value, buf);
  return buf.toString();
}

void _encode(dynamic value, StringBuffer buf) {
  if (value == null) {
    buf.write('null');
  } else if (value is bool) {
    buf.write(value ? 'true' : 'false');
  } else if (value is int) {
    buf.write(value.toString());
  } else if (value is double) {
    buf.write(_pyFloat(value));
  } else if (value is String) {
    _encodeString(value, buf);
  } else if (value is Map) {
    final keys = value.keys.map((k) => '$k').toList()..sort();
    buf.write('{');
    for (var i = 0; i < keys.length; i++) {
      if (i > 0) buf.write(', ');
      _encodeString(keys[i], buf);
      buf.write(': ');
      _encode(value[keys[i]], buf);
    }
    buf.write('}');
  } else if (value is List) {
    buf.write('[');
    for (var i = 0; i < value.length; i++) {
      if (i > 0) buf.write(', ');
      _encode(value[i], buf);
    }
    buf.write(']');
  } else {
    // default=str — render via toString, JSON-quoted.
    _encodeString('$value', buf);
  }
}

String _pyFloat(double v) {
  if (v == v.truncateToDouble() && v.isFinite) {
    return '${v.toInt()}.0';
  }
  return v.toString();
}

void _encodeString(String s, StringBuffer buf) {
  buf.write('"');
  for (final rune in s.runes) {
    switch (rune) {
      case 0x22:
        buf.write('\\"');
        break;
      case 0x5C:
        buf.write('\\\\');
        break;
      case 0x08:
        buf.write('\\b');
        break;
      case 0x0C:
        buf.write('\\f');
        break;
      case 0x0A:
        buf.write('\\n');
        break;
      case 0x0D:
        buf.write('\\r');
        break;
      case 0x09:
        buf.write('\\t');
        break;
      default:
        if (rune < 0x20) {
          buf.write('\\u${rune.toRadixString(16).padLeft(4, '0')}');
        } else {
          buf.writeCharCode(rune);
        }
    }
  }
  buf.write('"');
}

Map<String, dynamic> enforceRuntimeBoundary(Map<String, dynamic> payload) {
  final size = _pyJsonDumps(payload).length;
  final irs = (payload['irs'] as List<dynamic>?) ?? <dynamic>[];
  return <String, dynamic>{
    'within_size': size <= maxPayloadBytes,
    'within_ir_count': irs.length <= maxIrCount,
    'size': size,
    'ir_count': irs.length,
    'bounded': true,
  };
}
