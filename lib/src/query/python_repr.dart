/// Faithful reproduction of Python `str()` on JSON-shaped values (dicts, lists,
/// strings, bools, ints, doubles, None) — needed because
/// `query_semantics` embeds `str(payload)[:80]` into its IR target field.
library;

/// Reproduce CPython `str(value)` / `repr(value)` for JSON-shaped data.
String pythonStr(dynamic value) => _repr(value);

String _repr(dynamic value) {
  if (value == null) return 'None';
  if (value is bool) return value ? 'True' : 'False';
  if (value is String) return _reprStr(value);
  if (value is int) return '$value';
  if (value is double) return _reprDouble(value);
  if (value is Map) {
    final parts = <String>[];
    value.forEach((k, v) {
      parts.add('${_repr(k)}: ${_repr(v)}');
    });
    return '{${parts.join(', ')}}';
  }
  if (value is List) {
    return '[${value.map<String>(_repr).join(', ')}]';
  }
  return '$value';
}

String _reprStr(String s) {
  // CPython prefers single quotes unless the string contains a single quote
  // (and no double quote), in which case it uses double quotes.
  final hasSingle = s.contains("'");
  final hasDouble = s.contains('"');
  final useDouble = hasSingle && !hasDouble;
  final quote = useDouble ? '"' : "'";
  final buf = StringBuffer(quote);
  for (final rune in s.runes) {
    final ch = String.fromCharCode(rune);
    if (ch == '\\') {
      buf.write('\\\\');
    } else if (ch == quote) {
      buf.write('\\$quote');
    } else if (ch == '\n') {
      buf.write('\\n');
    } else if (ch == '\r') {
      buf.write('\\r');
    } else if (ch == '\t') {
      buf.write('\\t');
    } else {
      buf.write(ch);
    }
  }
  buf.write(quote);
  return buf.toString();
}

String _reprDouble(double d) {
  if (d == d.toInt() && d.isFinite) {
    return '${d.toInt()}.0';
  }
  return '$d';
}
