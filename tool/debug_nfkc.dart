import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  const value = 'café\r\n日本語 🚀';
  final b64 = base64Encode(utf8.encode(value));
  final result = Process.runSync(
    'node',
    [
      '-e',
      "const v=Buffer.from(process.argv[1],'base64').toString('utf8');process.stdout.write(v.normalize('NFKC'))",
      b64,
    ],
  );
  print('exit: ${result.exitCode}');
  print('stdout bytes: ${(result.stdout as String).codeUnits}');
  print('serialized: ${stableSerialize(value)}');
  print('hash: ${computeDeterministicHash(value)}');
  print(
      'expected: 39fac4850cbcebff76e96768a3164632f127101f3c328ad26f7cf4c2a672a229');
}
