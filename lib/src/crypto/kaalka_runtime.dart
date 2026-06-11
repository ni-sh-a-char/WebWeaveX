import 'dart:convert';

import 'package:kaalka/kaalka.dart';

import '../determinism/stable_serialize.dart';
import 'hashing.dart';
import 'kaalka_v5_proc.dart';
import 'time_key.dart';
import 'utf8_parity.dart';

export '../determinism/normalization.dart'
    show normalizeRuntimeValue, volatileRuntimeKeys;
export '../determinism/stable_serialize.dart' show stableSerialize;
export 'hashing.dart' show computeDeterministicHash;
export 'time_key.dart' show deriveKaalkaTimeKey;

const kaalkaAlgorithm = 'webweavex-formula+kaalka@5.0.0';
const kaalkaPackageVersion = '5.0.0';

String encodeKaalkaCiphertext(List<int> raw) => base64Encode(raw);

List<int> decodeKaalkaCiphertext(String encoded) => base64Decode(encoded);

/// Encrypt canonical runtime value → base64 ciphertext (Kaalka v5 byte path).
String encryptValue(dynamic value, String key) {
  // Registry dependency (parity substrate) — byte path uses kaalka_v5_proc.
  // ignore: unused_local_variable
  final _ = Kaalka();
  final payload = stableSerialize(value);
  final timeKey = deriveKaalkaTimeKey(key);
  final raw = kaalkaV5EncryptBytes(utf8.encode(payload), timeKey);
  return encodeKaalkaCiphertext(raw);
}

/// Decrypt base64 ciphertext → deserialized JSON when possible, else string.
dynamic decryptValue(String encrypted, String key) {
  final timeKey = deriveKaalkaTimeKey(key);
  final raw = decodeKaalkaCiphertext(encrypted);
  final decrypted = utf8DecodeParity(kaalkaV5DecryptBytes(raw, timeKey));
  try {
    return jsonDecode(decrypted);
  } catch (_) {
    return decrypted;
  }
}

Map<String, dynamic> encryptValueEnvelope(dynamic value, String key) => {
      'encrypted': encryptValue(value, key),
      'algorithm': kaalkaAlgorithm,
      'deterministic': true,
      'bounded': true,
    };

Map<String, dynamic> decryptValueEnvelope(String encrypted, String key) => {
      'decrypted': decryptValue(encrypted, key),
      'algorithm': kaalkaAlgorithm,
      'deterministic': true,
      'bounded': true,
    };

String computeKaalkaHash(dynamic value) => computeDeterministicHash(value);
