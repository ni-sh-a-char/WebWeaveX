import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('matches javascript reference vectors', () {
    final raw =
        File('validation/parity/javascript_vectors.json').readAsStringSync();
    final ref = jsonDecode(raw) as Map<String, dynamic>;
    final vectors = (ref['vectors'] as List).cast<Map<String, dynamic>>();

    for (final v in vectors) {
      final id = v['id'] as String;
      final serialized = v['serialized'] as String;
      final key = switch (id) {
        'probe-1' => 'k',
        'probe-2' => 'kaalka-key',
        'unicode' => 'uni',
        'emoji' => 'emoji-key',
        'crlf' => 'crlf-key',
        'session' => 'session-key',
        'nested-object' => 'nested',
        'graph' => 'graph-key',
        'array' => 'arr',
        'dom' => 'dom-key',
        'memory-graph' => 'mem',
        _ => 'k',
      };

      dynamic value;
      if (id == 'dom') {
        value = serialized;
      } else if (id == 'graph') {
        value = jsonDecode(serialized);
      } else if (id == 'nested-object' || id == 'memory-graph') {
        value = jsonDecode(serialized);
      } else if (id == 'array') {
        value = jsonDecode(serialized);
      } else {
        value = serialized;
      }

      expect(computeDeterministicHash(value), v['hash'], reason: id);
      expect(encryptValue(value, key), v['encrypted'], reason: id);
      expect(deriveKaalkaTimeKey(key), v['time_key'], reason: id);
    }
  });
}
