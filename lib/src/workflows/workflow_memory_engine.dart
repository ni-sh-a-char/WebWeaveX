// Port of core/workflows/workflow_memory_engine.py
import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart';

/// Recursively sort map keys for a stable JSON payload (mirrors
/// Python json.dumps(sort_keys=True)).
dynamic _sortKeysDeep(dynamic value) {
  if (value is Map) {
    final List<String> keys = value.keys.map((dynamic k) => '$k').toList()
      ..sort();
    final Map<String, dynamic> out = <String, dynamic>{};
    for (final String k in keys) {
      out[k] = _sortKeysDeep(value[k]);
    }
    return out;
  }
  if (value is List) {
    return value.map<dynamic>(_sortKeysDeep).toList();
  }
  return value;
}

Map<String, dynamic> saveWorkflowMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final String payload = jsonEncode(_sortKeysDeep(memory));
  final String encrypted = encryptValue(payload, key);
  final File target = File(path);
  final Directory parent = target.parent;
  if (!parent.existsSync()) {
    parent.createSync(recursive: true);
  }
  target.writeAsStringSync(
    jsonEncode(_sortKeysDeep(<String, dynamic>{
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

Map<String, dynamic> loadWorkflowMemory(
  String path,
  String key,
) {
  final File target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': emptyWorkflowMemory(),
      'bounded': true,
    };
  }

  final Map<String, dynamic> wrapper =
      jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  final dynamic decrypted = decryptValue(wrapper['encrypted'] as String, key);
  final String decryptedStr =
      decrypted is String ? decrypted : jsonEncode(decrypted);
  final Map<String, dynamic> memory =
      jsonDecode(decryptedStr) as Map<String, dynamic>;

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> rememberWorkflowRuntime(
  Map<String, dynamic> memory,
  Map<String, dynamic> update,
) {
  final Map<String, dynamic> merged = Map<String, dynamic>.from(memory);
  const List<String> fields = <String>[
    'objectives',
    'workflow_states',
    'execution_graphs',
    'semantic_checkpoints',
    'runtime_transitions',
  ];
  for (final String field in fields) {
    // setdefault: only set when absent.
    if (!merged.containsKey(field)) {
      merged[field] =
          update.containsKey(field) ? update[field] : <String, dynamic>{};
    }
  }
  merged.addAll(update);
  merged['bounded'] = true;
  return merged;
}

Map<String, dynamic> emptyWorkflowMemory() {
  return <String, dynamic>{
    'objectives': <String, dynamic>{},
    'workflow_states': <String, dynamic>{},
    'execution_graphs': <String, dynamic>{},
    'semantic_checkpoints': <dynamic>[],
    'runtime_transitions': <dynamic>[],
    'bounded': true,
  };
}
