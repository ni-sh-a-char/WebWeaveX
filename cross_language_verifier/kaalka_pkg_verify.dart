// Phase 6: verify repo's kaalka_v5_proc.dart matches the PUBLISHED pub.dev
// kaalka 5.0.0 package, executable. The published byte API routes through
// utf8.decode, so vectors are designed to keep ciphertext in ASCII range.
import 'dart:convert';
import 'dart:io';

import 'package:kaalka/kaalka.dart';
import 'package:webweavex/src/crypto/kaalka_v5_proc.dart';

Future<void> main() async {
  const timeKeys = ['0:0:0', '3:0:0', '12:34:56', '11:59:59', '23:45:1'];
  var trials = 0, mismatches = 0;
  final detail = <Map<String, dynamic>>[];
  for (final tk in timeKeys) {
    final (h, m, s) = parseKaalkaTimeKey(tk);
    final key = (h * 3600 + m * 60 + s) == 0 ? 1 : (h * 3600 + m * 60 + s);
    for (final len in [0, 1, 7, 64, 255, 300]) {
      // Designed so (b + offset) % 256 == 64 ('@') — ASCII-safe ciphertext.
      final data = List<int>.generate(
          len, (i) => ((64 - (key + i)) % 256 + 256) % 256);
      final pkg = Kaalka();
      final String encStr = await pkg.encrypt(data, timeKey: tk);
      final pubEnc = encStr.codeUnits;
      final repoEnc = kaalkaV5EncryptBytes(data, tk);
      final repoDec = kaalkaV5DecryptBytes(repoEnc, tk);
      trials++;
      final encEqual = pubEnc.length == repoEnc.length &&
          List.generate(pubEnc.length, (i) => pubEnc[i] == repoEnc[i])
              .every((x) => x);
      final decEqual = repoDec.length == data.length &&
          List.generate(data.length, (i) => repoDec[i] == data[i])
              .every((x) => x);
      if (!encEqual || !decEqual) {
        mismatches++;
        if (detail.length < 5) {
          detail.add({'time_key': tk, 'len': len, 'encEqual': encEqual});
        }
      }
    }
  }
  final result = {
    'published_package': 'kaalka 5.0.0 (pub.dev, from pubspec dependency)',
    'trials': trials,
    'time_keys': timeKeys,
    'mismatches': mismatches,
    'detail': detail,
    'verdict': mismatches == 0 ? 'PASS' : 'FAIL',
  };
  File('cross_language_verifier/kaalka_pkg_dart.json')
      .writeAsStringSync(const JsonEncoder.withIndent(' ').convert(result));
  stdout.write(jsonEncode(result));
}
