import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Port of core/execution/runtime_action_engine.build_runtime_action.
///
/// Action id is sha256 of canonical JSON (Python json.dumps sort_keys=True)
/// truncated to 32 hex chars. Mirrors Python byte-for-byte.
Map<String, dynamic> buildRuntimeAction(
  String actionType,
  String runtime,
  Map<String, dynamic>? payload, {
  int tick = 0,
}) {
  final Map<String, dynamic> pl = <String, dynamic>{...?payload};
  final String canonical = _pyJsonSortKeys(<String, dynamic>{
    'runtime': runtime,
    'action_type': actionType,
    'payload': pl,
    'tick': tick,
  });
  final String actionId =
      sha256.convert(utf8.encode(canonical)).toString().substring(0, 32);

  return <String, dynamic>{
    'id': actionId,
    'runtime': runtime,
    'action_type': actionType,
    'payload': pl,
    'timestamp': tick,
    'bounded': true,
  };
}

/// Emulates Python `json.dumps(obj, sort_keys=True)` default separators
/// (", " and ": ") for the bounded action shapes produced here.
String _pyJsonSortKeys(dynamic value) {
  if (value is Map) {
    final List<String> keys = value.keys.map((dynamic k) => '$k').toList()
      ..sort();
    final StringBuffer sb = StringBuffer('{');
    for (int i = 0; i < keys.length; i++) {
      if (i > 0) sb.write(', ');
      sb.write(jsonEncode(keys[i]));
      sb.write(': ');
      sb.write(_pyJsonSortKeys(value[keys[i]]));
    }
    sb.write('}');
    return sb.toString();
  }
  if (value is List) {
    final StringBuffer sb = StringBuffer('[');
    for (int i = 0; i < value.length; i++) {
      if (i > 0) sb.write(', ');
      sb.write(_pyJsonSortKeys(value[i]));
    }
    sb.write(']');
    return sb.toString();
  }
  return jsonEncode(value);
}
