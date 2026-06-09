import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart';

/// Replicates Python `json.dumps(obj, sort_keys=True)` (default separators
/// `", "` / `": "`, ensure_ascii=True). This exact byte layout is what gets
/// encrypted/decrypted, so it must match for save/load roundtrip parity.
String pyJsonDumpsSorted(dynamic value) {
  final buf = StringBuffer();
  _dump(value, buf);
  return buf.toString();
}

void _dump(dynamic v, StringBuffer buf) {
  if (v == null) {
    buf.write('null');
  } else if (v is bool) {
    buf.write(v ? 'true' : 'false');
  } else if (v is num) {
    buf.write(_numToPy(v));
  } else if (v is String) {
    buf.write(_jsonString(v));
  } else if (v is List) {
    buf.write('[');
    for (var i = 0; i < v.length; i++) {
      if (i > 0) buf.write(', ');
      _dump(v[i], buf);
    }
    buf.write(']');
  } else if (v is Map) {
    final keys = v.keys.map((k) => '$k').toList()..sort();
    buf.write('{');
    for (var i = 0; i < keys.length; i++) {
      if (i > 0) buf.write(', ');
      buf.write(_jsonString(keys[i]));
      buf.write(': ');
      _dump(v[keys[i]], buf);
    }
    buf.write('}');
  } else {
    buf.write(_jsonString('$v'));
  }
}

String _numToPy(num v) {
  if (v is int) return v.toString();
  if (v == v.roundToDouble() && v.isFinite) {
    return '${v.toInt()}.0';
  }
  return v.toString();
}

String _jsonString(String s) {
  // ensure_ascii=True: escape non-ASCII as \uXXXX, matching CPython json.
  final buf = StringBuffer('"');
  for (final code in s.runes) {
    switch (code) {
      case 0x22:
        buf.write(r'\"');
        break;
      case 0x5C:
        buf.write(r'\\');
        break;
      case 0x08:
        buf.write(r'\b');
        break;
      case 0x0C:
        buf.write(r'\f');
        break;
      case 0x0A:
        buf.write(r'\n');
        break;
      case 0x0D:
        buf.write(r'\r');
        break;
      case 0x09:
        buf.write(r'\t');
        break;
      default:
        if (code < 0x20 || code > 0x7E) {
          if (code > 0xFFFF) {
            final c = code - 0x10000;
            final high = 0xD800 + (c >> 10);
            final low = 0xDC00 + (c & 0x3FF);
            buf.write('\\u${high.toRadixString(16).padLeft(4, '0')}');
            buf.write('\\u${low.toRadixString(16).padLeft(4, '0')}');
          } else {
            buf.write('\\u${code.toRadixString(16).padLeft(4, '0')}');
          }
        } else {
          buf.writeCharCode(code);
        }
    }
  }
  buf.write('"');
  return buf.toString();
}

/// Port of core/evolution_runtime/runtime_memory_engine.save_evolution_runtime
Map<String, dynamic> saveEvolutionRuntime(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final payload = pyJsonDumpsSorted(memory);
  final encrypted = encryptValueEnvelope(payload, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  target.writeAsStringSync(
    pyJsonDumpsSorted(<String, dynamic>{
      'encrypted': encrypted['encrypted'],
      'algorithm': 'kaalka',
    }),
  );
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Port of core/evolution_runtime/runtime_memory_engine.load_evolution_runtime
Map<String, dynamic> loadEvolutionRuntime(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': emptyEvolutionMemory(),
      'bounded': true,
    };
  }

  final wrapper = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  // decryptValue already JSON-decodes the recovered payload when valid;
  // mirrors Python json.loads(decrypted["decrypted"]).
  final decrypted = decryptValue(wrapper['encrypted'] as String, key);
  final memory = decrypted is String ? jsonDecode(decrypted) : decrypted;

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Port of remember_evolution_runtime
Map<String, dynamic> rememberEvolutionRuntime(
  Map<String, dynamic> memory,
  Map<String, dynamic> update,
) {
  final merged = Map<String, dynamic>.from(memory);
  const fields = <String>[
    'evolution_histories',
    'selector_lineage',
    'workflow_evolution',
    'semantic_evolution',
    'optimization_histories',
  ];
  for (final field in fields) {
    if (!merged.containsKey(field)) {
      merged[field] =
          update.containsKey(field) ? update[field] : <String, dynamic>{};
    }
  }
  merged.addAll(update);
  merged['bounded'] = true;
  return merged;
}

Map<String, dynamic> emptyEvolutionMemory() => <String, dynamic>{
      'evolution_histories': <dynamic>[],
      'selector_lineage': <dynamic>[],
      'workflow_evolution': <String, dynamic>{},
      'semantic_evolution': <String, dynamic>{},
      'optimization_histories': <dynamic>[],
      'bounded': true,
    };
