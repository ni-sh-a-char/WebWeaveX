// Faithful Dart port of core/crypto/kaalka_engine.py (hex_fingerprint / fingerprint)
// and the deterministic serializer it depends on
// (core/serialize/deterministic_serializer.py: dumps_deterministic).
//
// fingerprint(payload, token) = kaalka_encrypt_bytes(raw, token).hex()
//   where raw = payload (str/bytes pass through) OR dumps_deterministic(payload).
//
// NOTE: this uses the kaalka v1 byte cipher (kaalka_encrypt_bytes), which is a
// DIFFERENT primitive from the kaalka v5 path used by encrypt_value.

import 'dart:convert';

import 'package:unorm_dart/unorm_dart.dart' as unorm;

import '../determinism/normalization_core.dart' show codePointCompare;
import '../determinism/py_float_repr.dart';

/// Python `((value % 256) + 256) % 256`.
int _safeByte(int value) => ((value % 256) + 256) % 256;

/// Python `_derive_time_key(token, idx)` — token is bytes, idx is the position.
int _deriveTimeKey(List<int> token, int idx) {
  if (token.isEmpty) return 0;
  return token[idx % token.length];
}

/// Port of `kaalka_encrypt_bytes(data, token)`.
List<int> kaalkaEncryptBytes(List<int> data, List<int> token) {
  final encrypted = <int>[];
  final lnMod = data.length % 251;
  for (var i = 0; i < data.length; i++) {
    final n = data[i];
    final tk = _deriveTimeKey(token, i);
    final value = ((n ^ tk) + (i * 31) + lnMod) % 256;
    encrypted.add(_safeByte(value));
  }
  return encrypted;
}

String _toHex(List<int> bytes) {
  final buf = StringBuffer();
  for (final b in bytes) {
    buf.write(b.toRadixString(16).padLeft(2, '0'));
  }
  return buf.toString();
}

/// Port of `hex_fingerprint(payload, token="webweavex")` — exported as the
/// public Python `fingerprint`.
///
/// String/`List<int>` (bytes) payloads pass through verbatim (no normalization,
/// matching Python's `isinstance(payload,(str,bytes))` branch). Everything else
/// is canonicalized via [dumpsDeterministic].
String hexFingerprint(dynamic payload, [String token = 'webweavex']) {
  String rawText;
  if (payload is String) {
    rawText = payload;
  } else if (payload is List<int>) {
    // bytes.decode("utf-8", errors="ignore")
    rawText = utf8.decode(payload, allowMalformed: true);
  } else {
    rawText = dumpsDeterministic(payload);
  }
  final raw = utf8.encode(rawText);
  return _toHex(kaalkaEncryptBytes(raw, utf8.encode(token)));
}

// ---------------------------------------------------------------------------
// dumps_deterministic (core/serialize/deterministic_serializer.py)
// ---------------------------------------------------------------------------

/// NFC normalization (mirrors `_norm_str` = unicodedata.normalize("NFC", value)).
/// Pure Dart via `package:unorm_dart`, byte-verified against Python.
String _normStr(String value) => unorm.nfc(value);

/// Port of `_stable(value, _depth)`.
dynamic _stable(dynamic value, [int depth = 0]) {
  if (depth > 64) return _normStr(value.toString());
  if (value is String) return _normStr(value);
  if (value is bool || value == null) return value;
  if (value is int) return value;
  if (value is double) {
    if (value.isNaN || value.isInfinite) return 0;
    // Integral floats convert exactly, BEFORE .15g rounding (cross-language
    // contract: 16-digit integral floats must not lose a digit here).
    if (value == value.truncateToDouble() &&
        value.abs() < 9223372036854775808.0) {
      return value.toInt();
    }
    final v = double.parse(_format15g(value));
    if (v == v.truncateToDouble() && v.abs() < 9223372036854775808.0) {
      return v.toInt();
    }
    return v;
  }
  if (value is Map) {
    final keys = value.keys.map((k) => _normStr(k.toString())).toList()
      ..sort(codePointCompare);
    final byNorm = <String, dynamic>{};
    for (final k in value.keys) {
      byNorm[_normStr(k.toString())] = value[k];
    }
    final out = <String, dynamic>{};
    for (final k in keys) {
      out[k] = _stable(byNorm[k], depth + 1);
    }
    return out;
  }
  if (value is List) {
    final items = value.map((v) => _stable(v, depth + 1)).toList();
    items.sort((a, b) => codePointCompare(_compactJson(a), _compactJson(b)));
    return items;
  }
  return _normStr(value.toString());
}

/// `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":"))`.
String _compactJson(dynamic value) {
  if (value is Map) {
    final keys = value.keys.map((k) => k.toString()).toList()
      ..sort(codePointCompare);
    final parts = <String>[];
    for (final k in keys) {
      parts.add('${jsonEncode(k)}:${_compactJson(value[k])}');
    }
    return '{${parts.join(',')}}';
  }
  if (value is List) {
    return '[${value.map(_compactJson).join(',')}]';
  }
  if (value is double) {
    // Python repr float form (json.dumps uses repr for floats).
    return pyFloatRepr(value);
  }
  return jsonEncode(value);
}

/// Port of `dumps_deterministic(value)`.
String dumpsDeterministic(dynamic value) => _compactJson(_stable(value));

/// Python `format(x, ".15g")`.
String _format15g(double x) {
  if (x == x.truncateToDouble() && x.abs() < 1e16) {
    return x.toInt().toString();
  }
  var s = x.toStringAsPrecision(15);
  if (s.contains('.') && !s.contains('e') && !s.contains('E')) {
    s = s.replaceFirst(RegExp(r'0+$'), '');
    s = s.replaceFirst(RegExp(r'\.$'), '');
  }
  return s;
}
