import 'dart:convert';
import 'dart:io';

import 'normalization_core.dart';

export 'normalization_core.dart';

/// NFKC via Node.js when available (matches `String.normalize('NFKC')` in JavaScript).
/// Falls back to CRLF/trim normalization when Node is not installed.
String normalizeRuntimeValue(String value) {
  try {
    final b64 = base64Encode(utf8.encode(value));
    final result = Process.runSync(
      'node',
      [
        '-e',
        "const v=Buffer.from(process.argv[1],'base64').toString('utf8');process.stdout.write(v.normalize('NFKC'))",
        b64,
      ],
      stdoutEncoding: utf8,
      stderrEncoding: utf8,
    );
    if (result.exitCode == 0) {
      return normalizeRuntimeValueCore(result.stdout as String);
    }
  } catch (_) {
    // Node optional — CRLF normalization still applied.
  }
  return normalizeRuntimeValueCore(value);
}
