import 'dart:convert';

import 'package:crypto/crypto.dart';

import '../determinism/normalization.dart';
import 'kaalka_v5_proc.dart';

const kaalkaFallbackTimeKey = '12:0:0';

bool kaalkaTimeKeyRoundTrips(String timeKey) {
  final probe = utf8.encode('\x00\x7f\xff🚀probe');
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

String deriveKaalkaTimeKey(String encryptionKey) {
  final digest =
      sha256.convert(utf8.encode(normalizeRuntimeValue(encryptionKey))).bytes;
  for (var i = 0; i <= digest.length - 3; i++) {
    final candidate =
        '${digest[i] % 12}:${digest[i + 1] % 60}:${digest[i + 2] % 60}';
    if (kaalkaTimeKeyRoundTrips(candidate)) return candidate;
  }
  if (kaalkaTimeKeyRoundTrips(kaalkaFallbackTimeKey))
    return kaalkaFallbackTimeKey;
  return '12:34:56';
}
