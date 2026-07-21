/// Python-semantics helpers for the semantic-IR port (Category-A closure).
/// Each helper is bit-faithful to CPython for the JSON value domain
/// (null/bool/int/double/String/List/Map) — the only types that cross the
/// 3-language parity boundary. Mirrors javascript/src/runtime/pyCompat.ts.
library;

import 'dart:math' as math;
import 'dart:typed_data';

/// Python `round(x, ndigits)` for float input — exact round-half-to-even on
/// the binary double, via integer decomposition (x = mant * 2^exp), matching
/// CPython and javascript pyCompat.round bit-for-bit.
double pythonRound(num xIn, int ndigits) {
  final x = xIn.toDouble();
  if (!x.isFinite) return x;
  final n = ndigits;

  final buf = ByteData(8)..setFloat64(0, x.abs());
  final hi = buf.getUint32(0);
  final lo = buf.getUint32(4);
  final biasedExp = (hi >> 20) & 0x7ff;
  var mant = (BigInt.from(hi & 0xfffff) << 32) | BigInt.from(lo);
  int exp;
  if (biasedExp == 0) {
    exp = -1074; // subnormal
  } else {
    mant |= BigInt.one << 52;
    exp = biasedExp - 1075;
  }
  if (mant == BigInt.zero) return 0.0;

  // q = round_half_even(|x| * 10^n); |x| * 10^n = mant * 2^exp * 10^n
  var numer = mant;
  var den = BigInt.one;
  if (n >= 0) {
    numer *= BigInt.from(10).pow(n);
  } else {
    den *= BigInt.from(10).pow(-n);
  }
  if (exp >= 0) {
    numer <<= exp;
  } else {
    den <<= -exp;
  }

  var q = numer ~/ den;
  final rem = numer % den;
  final twice = rem * BigInt.two;
  if (twice > den || (twice == den && (q & BigInt.one) == BigInt.one)) {
    q += BigInt.one;
  }

  final sign = x < 0 ? -1.0 : 1.0;
  if (n <= 0) {
    return (q * BigInt.from(10).pow(-n)).toDouble() * sign;
  }
  return sign * q.toDouble() / (math.pow(10.0, n) as double);
}

/// Python truthiness for the JSON value domain.
bool pyTruthy(dynamic v) {
  if (v == null || v == false) return false;
  if (v == true) return true;
  if (v is double && v.isNaN) return false;
  if (v is num) return v != 0;
  if (v is String) return v.isNotEmpty;
  if (v is List) return v.isNotEmpty;
  if (v is Map) return v.isNotEmpty;
  if (v is Set) return v.isNotEmpty;
  return true;
}

/// Python `dict.get(key, default)` — distinguishes a missing key from an
/// explicit null value (Dart's `m[k] ?? d` does not).
dynamic pyGet(Map<dynamic, dynamic> m, String key, dynamic dflt) =>
    m.containsKey(key) ? m[key] : dflt;

/// Python `repr(float)` / `str(float)` — shortest repr with Python's
/// formatting thresholds (mirrors javascript pyCompat floatStr).
String pyFloatStr(double x) {
  if (x.isNaN) return 'nan';
  if (x == double.infinity) return 'inf';
  if (x == double.negativeInfinity) return '-inf';
  if (x == x.truncateToDouble()) {
    if (x.abs() >= 1e16) return x.toStringAsExponential();
    return '${x.truncate()}.0';
  }
  if (x != 0 && x.abs() < 1e-4) {
    return x
        .toStringAsExponential()
        .replaceAllMapped(RegExp(r'e([+-])(\d)$'), (m) => 'e${m[1]}0${m[2]}');
  }
  return x.toString();
}

/// Python `str(value)` for the JSON value domain.
String pyToStr(dynamic v) {
  if (v == null) return 'None';
  if (v is bool) return v ? 'True' : 'False';
  if (v is String) return v;
  if (v is double) return pyFloatStr(v);
  if (v is int) return v.toString();
  return _pyRepr(v);
}

String _pyRepr(dynamic v) {
  if (v is String) {
    if (v.contains("'") && !v.contains('"')) {
      return '"${v.replaceAll('\\', r'\\')}"';
    }
    return "'${v.replaceAll('\\', r'\\').replaceAll("'", r"\'")}'";
  }
  if (v is List) return '[${v.map(_pyRepr).join(', ')}]';
  if (v is Map) {
    return '{${v.entries.map((e) => '${_pyRepr(e.key)}: ${_pyRepr(e.value)}').join(', ')}}';
  }
  return pyToStr(v);
}

/// Python `==` deep structural equality for the JSON value domain
/// (numbers compare by value: `1 == 1.0` is true, as in Python).
bool pyDeepEq(dynamic a, dynamic b) {
  if (a is num && b is num) return a == b;
  if (a is Map && b is Map) {
    if (a.length != b.length) return false;
    for (final k in a.keys) {
      if (!b.containsKey(k) || !pyDeepEq(a[k], b[k])) return false;
    }
    return true;
  }
  if (a is List && b is List) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (!pyDeepEq(a[i], b[i])) return false;
    }
    return true;
  }
  return a == b;
}

/// Python `sorted(items, key=...)` — stable (Dart's List.sort is not).
/// Python-faithful MULTILINE regex: CPython's `^` matches only at start
/// or after newline, and `$` only before newline or at end - Dart (like
/// JS) also treats carriage return as a line terminator, which diverges
/// on CRLF text (Python captures the trailing CR; Dart would not).
/// Rewrites the anchors and compiles WITHOUT multiLine.
RegExp pyMultiLineRegExp(String pattern, {bool caseSensitive = true}) {
  var p = pattern;
  if (p.startsWith('^')) {
    p = '(?:^|(?<=\n))${p.substring(1)}';
  }
  if (p.endsWith(r'$') && !p.endsWith(r'\$')) {
    p = '${p.substring(0, p.length - 1)}(?=\n|\$)';
  }
  // CPython '.' excludes only newline; Dart (like JS) also excludes CR and
  // U+2028/29 — rewrite unescaped dots outside character classes.
  final buf = StringBuffer();
  var inClass = false;
  for (var i = 0; i < p.length; i++) {
    final ch = p[i];
    if (ch == r'\') {
      buf.write(ch);
      if (i + 1 < p.length) buf.write(p[++i]);
      continue;
    }
    if (inClass) {
      if (ch == ']') inClass = false;
      buf.write(ch);
      continue;
    }
    if (ch == '[') {
      inClass = true;
      buf.write(ch);
      continue;
    }
    buf.write(ch == '.' ? '[^\n]' : ch);
  }
  return RegExp(buf.toString(), caseSensitive: caseSensitive);
}

List<T> pyStableSortedBy<T>(
    List<T> items, Comparable<dynamic> Function(T) key) {
  final indices = List<int>.generate(items.length, (i) => i);
  indices.sort((a, b) {
    final c = key(items[a]).compareTo(key(items[b]));
    return c != 0 ? c : a - b;
  });
  return <T>[for (final i in indices) items[i]];
}

/// Split text into lines (CRLF, LF, or CR).
List<String> splitlines(String text) {
  return text.split(RegExp(r'\\r\\n|\\r|\\n'));
}
