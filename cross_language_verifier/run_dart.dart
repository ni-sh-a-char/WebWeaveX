// Cross-language verifier — Dart runner.
// Run from the dart repo root:
//   dart run cross_language_verifier/run_dart.dart cross_language_verifier/vectors.json out_dart.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/crypto/kaalka_runtime.dart' show encryptValue;
import 'package:webweavex/src/crypto/kaalka_v5_proc.dart';
import 'package:webweavex/src/crypto/time_key.dart';
import 'package:webweavex/src/determinism/stable_serialize.dart';
import 'package:webweavex/src/persistence/fingerprint_hex.dart';

void main(List<String> argv) {
  final spec =
      jsonDecode(File(argv[0]).readAsStringSync()) as Map<String, dynamic>;
  final key = spec['key'] as String;
  final timeKey = deriveKaalkaTimeKey(key);
  final out = <String, dynamic>{
    'time_key': timeKey,
    'vectors': <String, dynamic>{},
  };
  final vectors = spec['vectors'] as Map<String, dynamic>;
  final ids = vectors.keys.toList()..sort();
  for (final vid in ids) {
    final v = vectors[vid];
    final enc = encryptValue(v, key);
    final decStr =
        utf8.decode(kaalkaV5DecryptBytes(base64Decode(enc), timeKey));
    (out['vectors'] as Map)[vid] = {
      'stable': stableSerialize(v),
      'canonical': dumpsDeterministic(v),
      'hash': computeDeterministicHash(v),
      'encrypted_b64': enc,
      'roundtrip_ok': decStr == stableSerialize(v),
      'fingerprint_hex': hexFingerprint(v),
    };
  }
  File(argv[1])
      .writeAsStringSync(const JsonEncoder.withIndent(' ').convert(out));
}
