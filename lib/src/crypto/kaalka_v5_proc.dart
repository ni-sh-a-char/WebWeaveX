/// Byte `_proc` bridge aligned with `package:kaalka` v5.0.0 (JavaScript `_proc` path).
library;

import 'package:kaalka/kaalka.dart' show Kaalka;

(int, int, int) parseKaalkaTimeKey(String timeKey) {
  final parts = timeKey.split(':');
  var hh = 0, mm = 0, ss = 0;
  if (parts.length == 3) {
    hh = int.parse(parts[0]);
    mm = int.parse(parts[1]);
    ss = int.parse(parts[2]);
  } else if (parts.length == 2) {
    mm = int.parse(parts[0]);
    ss = int.parse(parts[1]);
  } else if (parts.length == 1 && parts[0].isNotEmpty) {
    ss = int.parse(parts[0]);
  }
  return (hh % 12, mm, ss);
}

List<int> kaalkaV5ProcBytes(List<int> data, bool encrypt, int h, int m, int s) {
  final key = (h * 3600 + m * 60 + s) == 0 ? 1 : (h * 3600 + m * 60 + s);
  final result = <int>[];
  for (var idx = 0; idx < data.length; idx++) {
    final b = data[idx];
    final offset = (key + idx) % 256;
    final val = encrypt ? (b + offset) % 256 : (b - offset) % 256;
    result.add(val);
  }
  return result;
}

List<int> kaalkaV5EncryptBytes(List<int> payloadUtf8, String timeKey) {
  final (h, m, s) = parseKaalkaTimeKey(timeKey);
  return kaalkaV5ProcBytes(payloadUtf8, true, h, m, s);
}

List<int> kaalkaV5DecryptBytes(List<int> ciphertext, String timeKey) {
  final (h, m, s) = parseKaalkaTimeKey(timeKey);
  return kaalkaV5ProcBytes(ciphertext, false, h, m, s);
}

/// Round-trip probe using package [Kaalka] registry class (import requirement).
bool kaalkaPackageRoundTrips(String timeKey) {
  final probe = '\x00\x7f\xff🚀probe'.codeUnits;
  try {
    final enc = kaalkaV5EncryptBytes(probe, timeKey);
    final dec = kaalkaV5DecryptBytes(enc, timeKey);
    if (dec.length != probe.length) return false;
    for (var i = 0; i < probe.length; i++) {
      if (dec[i] != probe[i]) return false;
    }
    return true;
  } catch (_) {
    return false;
  }
}
