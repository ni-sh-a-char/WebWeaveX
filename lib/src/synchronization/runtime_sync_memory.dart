// Native Dart port of `core.synchronization.runtime_sync_memory_engine`
// save_sync_memory / load_sync_memory — encrypted on-disk runtime memory.
//
// Python contract:
//   payload    = json.dumps(memory, sort_keys=True)        # str
//   encrypted  = encrypt_value(payload, key)["encrypted"]  # base64 (kaalka v5)
//   file body  = json.dumps({"encrypted":..,"algorithm":"kaalka"}, sort_keys=True)
//
// encrypt_value(str) → stable_serialize(str) == normalize_runtime_value(str),
// so the canonical bytes encrypted are the normalized json.dumps string.
import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart' show encryptValue, decryptValue;
import '../determinism/normalization.dart' show normalizeRuntimeValue;
import 'synchronization_engines.dart' show emptySyncMemory;

/// Python `json.dumps(obj, sort_keys=True)` with default separators
/// (`", "` / `": "`) — recursively key-sorted, compact-ish.
String pythonJsonDumpsSorted(dynamic value) {
  final buffer = StringBuffer();
  _dump(value, buffer);
  return buffer.toString();
}

void _dump(dynamic value, StringBuffer out) {
  if (value == null) {
    out.write('null');
  } else if (value is bool) {
    out.write(value ? 'true' : 'false');
  } else if (value is num) {
    out.write(_numToPy(value));
  } else if (value is String) {
    out.write(jsonEncode(value));
  } else if (value is Map) {
    final keys = value.keys.map((k) => k.toString()).toList()..sort();
    out.write('{');
    var first = true;
    for (final key in keys) {
      if (!first) out.write(', ');
      first = false;
      out.write(jsonEncode(key));
      out.write(': ');
      _dump(value[key], out);
    }
    out.write('}');
  } else if (value is List) {
    out.write('[');
    var first = true;
    for (final item in value) {
      if (!first) out.write(', ');
      first = false;
      _dump(item, out);
    }
    out.write(']');
  } else {
    out.write(jsonEncode(value));
  }
}

String _numToPy(num value) {
  if (value is int) return value.toString();
  if (value == value.roundToDouble() && value.isFinite) {
    // Python json renders integral floats as "1.0".
    return '${value.toInt()}.0';
  }
  return value.toString();
}

Map<String, dynamic> saveSyncMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final payload = pythonJsonDumpsSorted(memory);
  final encrypted = encryptValue(payload, key);
  final target = File(path);
  final parent = target.parent;
  if (!parent.existsSync()) {
    parent.createSync(recursive: true);
  }
  final body = pythonJsonDumpsSorted(<String, dynamic>{
    'encrypted': encrypted,
    'algorithm': 'kaalka',
  });
  target.writeAsStringSync(body, encoding: utf8);
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> loadSyncMemory(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': emptySyncMemory(),
      'bounded': true,
    };
  }

  final wrapper = jsonDecode(target.readAsStringSync(encoding: utf8))
      as Map<String, dynamic>;
  final decrypted = decryptValue('${wrapper['encrypted']}', key);
  // decryptValue tries jsonDecode first; the stored payload is a json string,
  // so it round-trips to the original memory map/list. If it stayed a String
  // (decode failed), parse it explicitly.
  final dynamic memory =
      decrypted is String ? jsonDecode(decrypted) : decrypted;

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Re-normalize a string the way Python `encrypt_value` does before encryption.
/// Exposed for parity diagnostics.
String normalizeForEncryption(String value) => normalizeRuntimeValue(value);
