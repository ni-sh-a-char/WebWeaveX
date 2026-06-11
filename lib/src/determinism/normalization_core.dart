const volatileRuntimeKeys = {
  'timestamp',
  'created_at',
  'updated_at',
  'nonce',
  'request_id',
  'csrf',
  'generated_at',
  'runtime_id',
  'random',
  'uuid',
};

/// Python `re` `\s` for str patterns — the canonical trailing-whitespace set.
/// ECMAScript `\s` (Dart/JS RegExp) additionally matches U+FEFF and misses
/// U+001C–U+001F, so a literal `\s+$` here would diverge from Python.
final RegExp _trailingWhitespace = RegExp('[\\t-\\r\\x1c-\\x1f '
    '\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]+\$');

String normalizeRuntimeValueCore(String value) {
  var s = value.replaceAll('\r\n', '\n').replaceAll('\r', '\n');
  s = s.replaceAll(_trailingWhitespace, '');
  return s;
}

/// Unicode code-point string comparison (Python `sorted()` semantics).
///
/// Dart's `String.compareTo` orders by UTF-16 code units, which inverts the
/// order of astral-plane characters (e.g. U+1F680) relative to BMP characters
/// in U+E000–U+FFFF. Cross-language canonical ordering is defined as
/// code-point order, matching Python and the aligned JavaScript runtime.
int codePointCompare(String a, String b) {
  final ra = a.runes.iterator;
  final rb = b.runes.iterator;
  while (true) {
    final ha = ra.moveNext();
    final hb = rb.moveNext();
    if (!ha && !hb) return 0;
    if (!ha) return -1;
    if (!hb) return 1;
    if (ra.current != rb.current) {
      return ra.current < rb.current ? -1 : 1;
    }
  }
}

/// Cross-language numeric canonicalization.
///
/// JavaScript has a single number type, so `2.0` cannot serialize differently
/// from `2`. The canonical contract: integral doubles serialize as integers,
/// non-finite doubles as null — in every language.
dynamic canonicalizeNumber(dynamic v) {
  if (v is double) {
    if (v.isNaN || v.isInfinite) return null;
    // 2^63: the largest range where int conversion is exact in Dart and
    // JavaScript prints the same full-digit form (JS switches to exponent
    // notation only at 1e21; integral doubles < 2^63 convert exactly).
    if (v == v.truncateToDouble() && v.abs() < 9223372036854775808.0) {
      return v.toInt();
    }
  }
  return v;
}

Map<String, dynamic> stableSortKeys(Map<String, dynamic> obj) {
  final sorted = <String, dynamic>{};
  final keys = obj.keys.toList()..sort(codePointCompare);
  for (final k in keys) {
    if (volatileRuntimeKeys.contains(k)) continue;
    final v = obj[k];
    if (v is Map) {
      sorted[k] = stableSortKeys(Map<String, dynamic>.from(v));
    } else if (v is List) {
      sorted[k] = v.map((item) {
        if (item is Map) {
          return stableSortKeys(Map<String, dynamic>.from(item));
        }
        return canonicalizeNumber(item);
      }).toList();
    } else {
      sorted[k] = canonicalizeNumber(v);
    }
  }
  return sorted;
}

dynamic normalizeRuntimeState(Map<String, dynamic> state) =>
    stableSortKeys(state);
