import 'dart:convert';

import 'normalization_core.dart';
import 'py_float_repr.dart';

/// Compact canonical JSON encoder — byte-identical to Python
/// `json.dumps(value, ensure_ascii=False, separators=(",", ":"),
/// sort_keys=True)` and the aligned JavaScript runtime.
///
/// `dart:convert`'s `jsonEncode` cannot be used for whole structures because
/// its double formatting (`double.toString`) diverges from Python `repr`
/// outside [1e-6, 1e21); string escaping, however, matches, so string leaves
/// still delegate to `jsonEncode`.
String canonicalJsonEncode(dynamic value) {
  final v = canonicalizeNumber(value);
  if (v == null) return 'null';
  if (v is bool) return v ? 'true' : 'false';
  if (v is int) return v.toString();
  if (v is double) return pyFloatRepr(v);
  if (v is String) return jsonEncode(v);
  if (v is List) return '[${v.map(canonicalJsonEncode).join(',')}]';
  if (v is Map) {
    final byKey = <String, dynamic>{};
    for (final k in v.keys) {
      byKey[k.toString()] = v[k];
    }
    final keys = byKey.keys.toList()..sort(codePointCompare);
    final parts = <String>[
      for (final k in keys) '${jsonEncode(k)}:${canonicalJsonEncode(byKey[k])}'
    ];
    return '{${parts.join(',')}}';
  }
  return jsonEncode(v.toString());
}
