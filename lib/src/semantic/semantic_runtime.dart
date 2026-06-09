/// Semantic runtime family — Dart port of the Python `webweavex` public
/// semantic APIs (`run_semantic_runtime`, `run_semantic_for_extraction`,
/// `save_semantic_memory`, `load_semantic_memory`, `replay_semantic_runtime`).
///
/// Parity contract: `computeDeterministicHash` over the Dart result equals
/// Python's `compute_deterministic_hash` over the equivalent Python result.
library;

import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_v5_proc.dart'
    show kaalkaV5EncryptBytes, kaalkaV5DecryptBytes;
import '../crypto/time_key.dart' show deriveKaalkaTimeKey;
import '../determinism/stable_serialize.dart' show stableSerialize;
import 'semantic_engines.dart';

export 'semantic_engines.dart';

// ---------------------------------------------------------------------------
// semantic_memory_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> _emptyMemory() => <String, dynamic>{
      'ontology': <String, dynamic>{},
      'semantic_graph': <String, dynamic>{},
      'entity_mappings': <String, dynamic>{},
      'semantic_workflows': <String, dynamic>{},
      'runtime_semantics': <String, dynamic>{},
      'bounded': true,
    };

Map<String, dynamic> rememberSemanticRuntime(
  Map<String, dynamic> memory,
  Map<String, dynamic> update,
) {
  final merged = Map<String, dynamic>.from(memory);
  for (final field in const <String>[
    'ontology',
    'semantic_graph',
    'entity_mappings',
    'semantic_workflows',
    'runtime_semantics',
  ]) {
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

/// Mirrors Python `save_semantic_memory`: canonical JSON (sorted keys) →
/// kaalka-encrypted → `{encrypted, algorithm}` wrapper written to [path].
Map<String, dynamic> saveSemanticMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final payload = _canonicalJson(memory);
  final timeKey = deriveKaalkaTimeKey(key);
  final raw = kaalkaV5EncryptBytes(utf8.encode(payload), timeKey);
  final encrypted = base64Encode(raw);
  final target = File(path);
  target.parent.createSync(recursive: true);
  target.writeAsStringSync(
    jsonEncode(_sortMap(<String, dynamic>{
      'encrypted': encrypted,
      'algorithm': 'kaalka',
    })),
  );
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Mirrors Python `load_semantic_memory`: reads the wrapper, decrypts the
/// payload and returns the decoded memory.
Map<String, dynamic> loadSemanticMemory(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': _emptyMemory(),
      'bounded': true,
    };
  }
  final wrapper = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  final timeKey = deriveKaalkaTimeKey(key);
  final raw = base64Decode(wrapper['encrypted'] as String);
  final decrypted = utf8.decode(kaalkaV5DecryptBytes(raw, timeKey));
  final memory = jsonDecode(decrypted);
  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_replay_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> replaySemanticRuntime(Map<String, dynamic> memory) {
  return <String, dynamic>{
    'semantic_graph': memory['semantic_graph'] ?? <String, dynamic>{},
    'ontology_mappings': memory['ontology'] ?? <String, dynamic>{},
    'workflow_meaning': memory['semantic_workflows'] ?? <String, dynamic>{},
    'semantic_propagation': memory['runtime_semantics'] ?? <String, dynamic>{},
    'entity_mappings': memory['entity_mappings'] ?? <String, dynamic>{},
    'replayed': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_orchestrator
// ---------------------------------------------------------------------------

Map<String, dynamic> runSemanticRuntime({
  String url = '',
  String html = '',
  String text = '',
  List<Map<String, dynamic>>? interactions,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? nativeCognition,
  List<String>? repositoryFiles,
  Map<String, dynamic>? runtimeGraph,
  Map<String, dynamic>? memory,
  String objective = '',
}) {
  final mem = Map<String, dynamic>.from(memory ?? <String, dynamic>{});
  final ix = List<Map<String, dynamic>>.from(
      interactions ?? const <Map<String, dynamic>>[]);
  var combinedText = '$text $html';
  if (combinedText.length > 100000) {
    combinedText = combinedText.substring(0, 100000);
  }

  final structure = <String, dynamic>{
    'actions': <Map<String, dynamic>>[
      for (final i in ix)
        <String, dynamic>{
          'label': i['action'] ?? '',
          'type': i['action'] ?? '',
        }
    ],
    'artifacts': nativeCognition != null
        ? <String>['${nativeCognition['runtime'] ?? ''}']
        : <String>[],
  };

  final entitiesRaw = extractSemanticEntities(combinedText, structure);
  final resolved =
      resolveSemanticEntities(entitiesRaw['entities'] as List<dynamic>);
  entitiesRaw['entities'] = resolved['entities'];

  final domain = classifySemanticDomain(
    combinedText,
    objective.isNotEmpty ? <String>[objective] : <String>[],
  );
  final ontology = buildSemanticOntology(
    entitiesRaw['entities'] as List<dynamic>,
    domain['domain'] as String,
  );
  entitiesRaw['ontology'] = ontology;

  final ui = extractUiSemantics(html, ix);
  final tables = extractTableSemantics(html);
  final document = extractDocumentSemantics(combinedText);
  final repository = extractRepositorySemantics(repositoryFiles, combinedText);
  final application = extractApplicationSemantics(applicationResult);
  final causality = extractCausalitySemantics(causalityResult);
  final workflow = extractWorkflowSemantics(
    (applicationResult ?? <String, dynamic>{})['workflow']
        as Map<String, dynamic>?,
    objective,
  );
  final browser = extractBrowserSemantics(url, html);
  final runtime = extractRuntimeSemantics(
    runtimeGraph,
    <String, dynamic>{
      'browser': browser.isNotEmpty,
      'native': nativeCognition != null,
      'application': applicationResult != null,
    },
  );

  final semanticGraph = buildSemanticGraph(
    entitiesRaw['entities'] as List<dynamic>,
    entitiesRaw['relations'] as List<dynamic>,
  );

  final alignment = alignSemanticRuntimes(
    browser: <String, dynamic>{...browser, 'domain': domain['domain']},
    native: nativeCognition,
    repository: repository,
    document: document,
    runtime: runtime,
  );

  var diff = <String, dynamic>{};
  final memEntities = mem['entities'];
  final hasEntities = memEntities != null &&
      (memEntities is! Map || memEntities.isNotEmpty) &&
      (memEntities is! List || memEntities.isNotEmpty) &&
      (memEntities is! String || memEntities.isNotEmpty);
  if (hasEntities) {
    diff = diffSemanticRuntime(mem, <String, dynamic>{
      'entities': entitiesRaw,
      'domain': domain,
      'ontology': ontology,
      'workflow': workflow,
    });
  }

  final payload = <String, dynamic>{
    'entities': entitiesRaw,
    'domain': domain,
    'ontology': ontology,
    'ui': ui,
    'tables': tables,
    'document': document,
    'repository': repository,
    'application': application,
    'causality': causality,
    'workflow': workflow,
    'browser': browser,
    'runtime': runtime,
    'semantic_graph': semanticGraph,
    'alignment': alignment,
    'diff': diff,
    'bounded': true,
  };

  final updatedMemory = rememberSemanticRuntime(
    mem,
    <String, dynamic>{
      'ontology': ontology,
      'semantic_graph': semanticGraph,
      'entity_mappings': resolved['canonical_map'] ?? <String, dynamic>{},
      'semantic_workflows': workflow,
      'runtime_semantics': runtime,
      'entities': entitiesRaw,
      'domain': domain,
    },
  );
  payload['memory'] = updatedMemory;
  payload['replay'] = replaySemanticRuntime(updatedMemory);
  payload['semantic_ir'] = compileSemanticRuntimeIr(payload);
  return payload;
}

Map<String, dynamic> runSemanticForExtraction({
  bool semanticRuntime = true,
  String memoryPath = '',
  String memoryKey = '',
  String url = '',
  String html = '',
  List<Map<String, dynamic>>? interactions,
  Map<String, dynamic>? applicationResult,
  Map<String, dynamic>? causalityResult,
  Map<String, dynamic>? nativeCognition,
  Map<String, dynamic>? runtimeGraph,
  String objective = '',
  bool mergeGraph = true,
}) {
  if (!semanticRuntime) {
    return <String, dynamic>{'enabled': false, 'bounded': true};
  }

  var memory = <String, dynamic>{};
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    final loaded = loadSemanticMemory(memoryPath, memoryKey);
    if (loaded['available'] == true) {
      memory = Map<String, dynamic>.from(
          loaded['memory'] as Map<dynamic, dynamic>? ?? memory);
    }
  }

  final result = runSemanticRuntime(
    url: url,
    html: html,
    interactions: interactions,
    applicationResult: applicationResult,
    causalityResult: causalityResult,
    nativeCognition: nativeCognition,
    runtimeGraph: runtimeGraph,
    memory: memory,
    objective: objective,
  );

  var persisted = false;
  if (memoryPath.isNotEmpty && memoryKey.isNotEmpty) {
    saveSemanticMemory(
      memoryPath,
      Map<String, dynamic>.from(
          result['memory'] as Map<dynamic, dynamic>? ?? <String, dynamic>{}),
      memoryKey,
    );
    persisted = true;
  }

  final graphIr = semanticRuntimeIrToGraph(Map<String, dynamic>.from(
      result['semantic_ir'] as Map<dynamic, dynamic>? ?? <String, dynamic>{}));
  var unifiedGraph = <String, dynamic>{};
  if (mergeGraph) {
    unifiedGraph = mergeRuntimeIrsToGraph(<dynamic>[graphIr]);
  }

  return <String, dynamic>{
    'enabled': true,
    'semantic': result,
    'semantic_ir': result['semantic_ir'] ?? <String, dynamic>{},
    'semantic_graph_ir': graphIr,
    'unified_graph': unifiedGraph,
    'replay': result['replay'] ?? <String, dynamic>{},
    'memory_persisted': persisted,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// helpers: canonical JSON (Python json.dumps(sort_keys=True) equivalent)
// ---------------------------------------------------------------------------

dynamic _sortValue(dynamic value) {
  if (value is Map) {
    return _sortMap(
        Map<String, dynamic>.from(value.map((k, v) => MapEntry('$k', v))));
  }
  if (value is List) {
    return value.map(_sortValue).toList();
  }
  return value;
}

Map<String, dynamic> _sortMap(Map<String, dynamic> map) {
  final keys = map.keys.toList()..sort();
  final out = <String, dynamic>{};
  for (final k in keys) {
    out[k] = _sortValue(map[k]);
  }
  return out;
}

String _canonicalJson(Map<String, dynamic> memory) =>
    jsonEncode(_sortValue(memory));

/// Re-export so the parity test can hash via the same serializer if needed.
String semanticStableSerialize(dynamic value) => stableSerialize(value);
