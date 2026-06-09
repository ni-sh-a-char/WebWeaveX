/// Persistence engine for the runtime-memory family — port of
/// `core.memory.runtime_memory_persistence_engine`.
///
/// save → json.dumps(memory, sort_keys=True) → encrypt_value → write wrapper.
/// load → read wrapper → decrypt_value → json.loads → memory.
library;

import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart';
import '../crypto/kaalka_v5_proc.dart';

/// json.dumps(value, sort_keys=True) — DEFAULT separators ", " and ": ".
String _sortedJson(dynamic value) {
  if (value is Map) {
    final List<String> keys =
        value.keys.map((dynamic k) => k.toString()).toList()..sort();
    final StringBuffer b = StringBuffer('{');
    for (int i = 0; i < keys.length; i++) {
      if (i > 0) b.write(', ');
      b.write(jsonEncode(keys[i]));
      b.write(': ');
      b.write(_sortedJson(value[keys[i]]));
    }
    b.write('}');
    return b.toString();
  }
  if (value is List) {
    final StringBuffer b = StringBuffer('[');
    for (int i = 0; i < value.length; i++) {
      if (i > 0) b.write(', ');
      b.write(_sortedJson(value[i]));
    }
    b.write(']');
    return b.toString();
  }
  return jsonEncode(value);
}

Map<String, dynamic> saveRuntimeMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final String payload = _sortedJson(memory);
  final String encrypted = encryptValue(payload, key);
  final File target = File(path);
  target.parent.createSync(recursive: true);
  // Wrapper itself written with sort_keys=True (keys: algorithm, encrypted).
  final String wrapper = _sortedJson(<String, dynamic>{
    'encrypted': encrypted,
    'algorithm': 'kaalka',
  });
  target.writeAsStringSync(wrapper, encoding: utf8);
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> loadRuntimeMemory(String path, String key) {
  final File target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': _emptyStore(),
      'bounded': true,
    };
  }

  final Map<String, dynamic> wrapper =
      (jsonDecode(target.readAsStringSync(encoding: utf8)) as Map)
          .cast<String, dynamic>();
  final String decryptedPayload =
      _decryptToString(wrapper['encrypted'] as String, key);
  final Map<String, dynamic> memory =
      (jsonDecode(decryptedPayload) as Map).cast<String, dynamic>();

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// decryptValue may jsonDecode; here we need the raw decrypted JSON STRING
/// (Python decrypt_value returns the decrypted text, then json.loads runs).
String _decryptToString(String encrypted, String key) {
  final dynamic decoded = decryptValue(encrypted, key);
  if (decoded is String) return decoded;
  // decryptValue parsed it to a structure — re-serialize is lossy for ordering,
  // so instead re-run the byte path to recover the exact string.
  return _rawDecrypt(encrypted, key);
}

String _rawDecrypt(String encrypted, String key) {
  // Mirror crypto/kaalka_runtime.dart decrypt path without the jsonDecode.
  final String timeKey = deriveKaalkaTimeKey(key);
  final List<int> raw = decodeKaalkaCiphertext(encrypted);
  return utf8.decode(kaalkaV5DecryptBytes(raw, timeKey));
}

Map<String, dynamic> _emptyStore() => <String, dynamic>{
      'runtime': <String, dynamic>{},
      'knowledge': <String, dynamic>{},
      'semantic': <String, dynamic>{},
      'index': <String, dynamic>{},
      'graph': <String, dynamic>{},
      'lineage': <String, dynamic>{},
      'bounded': true,
    };
