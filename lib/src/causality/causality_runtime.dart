// Faithful Dart port of core/causality/causality_orchestrator.py,
// causal_memory_engine.py and causal_replay_engine.py.

import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart' show encryptValue, decryptValue;
import 'causality_engines.dart';

/// Port of run_causality_runtime.
Map<String, dynamic> runCausalityRuntime({
  List<Map<String, dynamic>>? browserEvents,
  Map<String, dynamic>? nativeCognition,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? distributedResult,
  Map<String, dynamic>? memory,
  List<dynamic>? interactions,
}) {
  final mem = Map<String, dynamic>.from(memory ?? <String, dynamic>{});
  final browser = browserEvents != null
      ? List<Map<String, dynamic>>.from(browserEvents)
      : normalizeInteractionEvents(interactions ?? <dynamic>[], 'browser');

  final nativeEvents =
      eventsFromNativeCognition(nativeCognition ?? <String, dynamic>{});

  if (applicationResult != null && _truthyMap(applicationResult)) {
    final workflow = Map<String, dynamic>.from(
      (applicationResult['workflow'] as Map?) ?? <String, dynamic>{},
    );
    final wfNodes = (workflow['nodes'] as List<dynamic>?) ?? <dynamic>[];
    final boundedNodes =
        wfNodes.length > 100 ? wfNodes.sublist(0, 100) : wfNodes;
    for (var index = 0; index < boundedNodes.length; index++) {
      browser.add(<String, dynamic>{
        'id': 'application:evt:$index',
        'runtime': 'application',
        'type': 'workflow',
        'step': browser.length + index,
      });
    }
  }

  final allEvents = <Map<String, dynamic>>[...browser, ...nativeEvents];
  final sortedAll = _stableSortByStep(allEvents);

  final origins = <String, dynamic>{
    'browser': browser.length,
    'native': nativeEvents.length,
    'distributed': distributedResult != null && _truthyMap(distributedResult),
  };

  final causality = buildRuntimeCausality(sortedAll, origins);
  final eventChain = buildEventChain(sortedAll);
  final alignment = alignCrossRuntimeEvents(sortedAll);
  var dependencies = buildRuntimeDependencies(
    sortedAll,
    <String, dynamic>{'synchronization_chains': <dynamic>[]},
  );
  final propagation = buildWorkflowPropagation(alignment, dependencies);
  dependencies = buildRuntimeDependencies(sortedAll, propagation);
  final causalGraph = buildCausalGraph(sortedAll, causality);
  final transitions = buildStateTransitions(sortedAll);
  final sequence = buildRuntimeSequence(sortedAll);
  final timeline = buildRuntimeTimeline(sortedAll, propagation);

  final cognition = nativeCognition ?? <String, dynamic>{};
  final desktop = Map<String, dynamic>.from(
    (cognition['desktop'] as Map?) ?? <String, dynamic>{},
  );
  final terminal = Map<String, dynamic>.from(
    (cognition['terminal'] as Map?) ?? <String, dynamic>{},
  );
  final processesContainer = Map<String, dynamic>.from(
    (cognition['processes'] as Map?) ?? <String, dynamic>{},
  );
  final notifications =
      (desktop['notifications'] as List<dynamic>?) ?? <dynamic>[];
  final terminalLines = (terminal['output'] as List<dynamic>?) ?? <dynamic>[];
  final processEvents =
      (processesContainer['processes'] as List<dynamic>?) ?? <dynamic>[];

  final correlation = correlateRuntimeMutations(
    browserEvents: browser,
    nativeEvents: nativeEvents,
    notifications: notifications,
    terminalLines: terminalLines,
    processEvents: processEvents,
  );
  final distributed = buildDistributedCausality(distributedResult);
  final browserBridge = bridgeBrowserNativeRuntime(browser, nativeEvents);
  final electronEvents =
      nativeEvents.where((e) => e['runtime'] == 'electron').toList();
  final terminalEvents =
      nativeEvents.where((e) => e['runtime'] == 'terminal').toList();
  final electronBridge =
      bridgeElectronTerminalRuntime(electronEvents, terminalEvents);
  final notificationCausality =
      trackNotificationCausality(notifications, sortedAll);
  final processCausality = trackProcessCausality(processEvents, sortedAll);
  final recovery = recoverCausalRuntime(causality, sortedAll);

  final payload = <String, dynamic>{
    'causality': causality,
    'event_chain': eventChain,
    'alignment': alignment,
    'propagation': propagation,
    'dependencies': dependencies,
    'causal_graph': causalGraph,
    'transitions': transitions,
    'sequence': sequence,
    'timeline': timeline,
    'correlation': correlation,
    'distributed': distributed,
    'browser_bridge': browserBridge,
    'electron_bridge': electronBridge,
    'notification_causality': notificationCausality,
    'process_causality': processCausality,
    'recovery': recovery,
    'bounded': true,
  };

  final updatedMemory = rememberCausalRuntime(mem, <String, dynamic>{
    'event_chains': eventChain,
    'runtime_propagation': causality,
    'causal_graphs': causalGraph,
    'distributed_workflows': distributed,
    'synchronization_state': alignment,
    'alignment': alignment,
    'timeline': timeline,
  });
  payload['memory'] = updatedMemory;
  payload['replay'] = replayCausalRuntime(updatedMemory);
  payload['causal_ir'] = compileCausalRuntimeIr(payload);
  return payload;
}

/// Port of run_causality_for_extraction.
Map<String, dynamic> runCausalityForExtraction({
  bool causalityRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  List<Map<String, dynamic>>? browserEvents,
  Map<String, dynamic>? nativeCognition,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? distributedResult,
  List<dynamic>? interactions,
  bool mergeGraph = true,
}) {
  if (!causalityRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  var memory = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final loaded = loadCausalMemory(memoryPath, memoryKey);
    if (_truthy(loaded['available'])) {
      memory = Map<String, dynamic>.from(
        (loaded['memory'] as Map?) ?? memory,
      );
    }
  }

  final result = runCausalityRuntime(
    browserEvents: browserEvents,
    nativeCognition: nativeCognition,
    applicationResult: applicationResult,
    distributedResult: distributedResult,
    memory: memory,
    interactions: interactions,
  );

  var persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveCausalMemory(
      memoryPath,
      Map<String, dynamic>.from(
          (result['memory'] as Map?) ?? <String, dynamic>{}),
      memoryKey,
    );
    persisted = true;
  }

  final graphIr = causalRuntimeIrToGraph(
    Map<String, dynamic>.from(
        (result['causal_ir'] as Map?) ?? <String, dynamic>{}),
  );
  var unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = buildUnifiedRuntimeGraph(<Map<String, dynamic>>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'causality': result,
    'causal_ir': result['causal_ir'] ?? <String, dynamic>{},
    'causal_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': result['replay'] ?? <String, dynamic>{},
    'memory_persisted': persisted,
    'bounded': true,
  };
}

/// Port of replay_causal_runtime.
Map<String, dynamic> replayCausalRuntime(Map<String, dynamic> memory) {
  return <String, dynamic>{
    'event_propagation': memory['runtime_propagation'] ?? <String, dynamic>{},
    'workflow_evolution': memory['event_chains'] ?? <String, dynamic>{},
    'synchronization': memory['synchronization_state'] ?? <String, dynamic>{},
    'causal_graph': memory['causal_graphs'] ?? <String, dynamic>{},
    'cross_runtime': memory['alignment'] ?? <String, dynamic>{},
    'replayed': true,
    'bounded': true,
  };
}

/// Port of remember_causal_runtime.
Map<String, dynamic> rememberCausalRuntime(
  Map<String, dynamic> memory,
  Map<String, dynamic> update,
) {
  final merged = Map<String, dynamic>.from(memory);
  for (final field in <String>[
    'event_chains',
    'runtime_propagation',
    'causal_graphs',
    'distributed_workflows',
    'synchronization_state',
  ]) {
    // setdefault(field, update.get(field, merged.get(field, {})))
    if (!merged.containsKey(field)) {
      if (update.containsKey(field)) {
        merged[field] = update[field];
      } else if (merged.containsKey(field)) {
        merged[field] = merged[field];
      } else {
        merged[field] = <String, dynamic>{};
      }
    }
  }
  merged.addAll(update);
  merged['bounded'] = true;
  return merged;
}

/// Port of save_causal_memory.
Map<String, dynamic> saveCausalMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  // json.dumps(memory, sort_keys=True) with Python default separators ", " ": ".
  final payload = _pyJsonSortKeys(memory);
  final encrypted = encryptValue(payload, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  final wrapper = <String, dynamic>{
    'encrypted': encrypted,
    'algorithm': 'kaalka',
  };
  target.writeAsStringSync(_pyJsonSortKeys(wrapper));
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Port of load_causal_memory.
Map<String, dynamic> loadCausalMemory(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': _emptyMemory(),
      'bounded': true,
    };
  }

  final wrapper = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  final decrypted = decryptValue(wrapper['encrypted'] as String, key);
  // decryptValue returns the parsed JSON when possible (the memory object).
  final memory = decrypted is Map
      ? Map<String, dynamic>.from(decrypted)
      : jsonDecode(decrypted as String) as Map<String, dynamic>;

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _emptyMemory() => <String, dynamic>{
      'event_chains': <String, dynamic>{},
      'runtime_propagation': <String, dynamic>{},
      'causal_graphs': <String, dynamic>{},
      'distributed_workflows': <String, dynamic>{},
      'synchronization_state': <String, dynamic>{},
      'bounded': true,
    };

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------

List<Map<String, dynamic>> _stableSortByStep(
    List<Map<String, dynamic>> events) {
  final indexed = <List<dynamic>>[];
  for (var i = 0; i < events.length; i++) {
    indexed.add(<dynamic>[events[i], i]);
  }
  int stepOf(Map<String, dynamic> m) {
    final s = m['step'];
    if (s is int) return s;
    if (s is num) return s.toInt();
    if (s is String) return int.tryParse(s) ?? 0;
    return 0;
  }

  indexed.sort((a, b) {
    final cmp = stepOf(a[0] as Map<String, dynamic>)
        .compareTo(stepOf(b[0] as Map<String, dynamic>));
    if (cmp != 0) return cmp;
    return (a[1] as int).compareTo(b[1] as int);
  });
  return indexed.map((e) => e[0] as Map<String, dynamic>).toList();
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

bool _truthyMap(Map<String, dynamic> m) => m.isNotEmpty;

/// json.dumps(obj, sort_keys=True) — Python default separators (", ", ": ").
/// Keys recursively sorted; this matches the on-disk bytes Python writes, which
/// is what gets encrypted. (Memory contains no volatile keys.)
String _pyJsonSortKeys(dynamic value) {
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
    return value.map(_deepSort).toList();
  }
  return value;
}

/// Emits JSON with Python's default separators: ', ' and ': '.
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
      value.forEach((k, v) {
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
      for (final v in value) {
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
