// Phase 13: Dart micro-benchmark.
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/crypto/kaalka_runtime.dart' show encryptValue;
import 'package:webweavex/src/determinism/stable_serialize.dart';

void main() {
  final payload = <String, dynamic>{
    'title': 'Benchmark payload — café 中文 🚀',
    'items': [
      for (var i = 0; i < 50; i++)
        {
          'id': i,
          'score': i / 7.0,
          'tags': ['a', 'b', 'c']
        }
    ],
    'nested': {
      'depth': {
        'x': [1, 2.5, null, true]
      }
    },
  };
  const n = 2000;
  final sw = Stopwatch()..start();
  for (var i = 0; i < n; i++) {
    stableSerialize({...payload, 'i': i});
  }
  final tSer = sw.elapsedMicroseconds;
  sw.reset();
  for (var i = 0; i < n; i++) {
    computeDeterministicHash({...payload, 'i': i});
  }
  final tHash = sw.elapsedMicroseconds;
  sw.reset();
  for (var i = 0; i < n ~/ 10; i++) {
    encryptValue({...payload, 'i': i}, 'bench-key');
  }
  final tEnc = sw.elapsedMicroseconds;
  stdout.write(jsonEncode({
    'language': 'dart',
    'serialize_ops_per_s': (n / (tSer / 1e6)).round(),
    'hash_ops_per_s': (n / (tHash / 1e6)).round(),
    'encrypt_ops_per_s': ((n ~/ 10) / (tEnc / 1e6)).round(),
  }));
}
