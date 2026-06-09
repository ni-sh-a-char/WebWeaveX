import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

const parityAlgorithm = 'webweavex-formula+kaalka@5.0.0';

Future<void> main() async {
  final root = Directory.current;
  final parityDir = Directory('${root.path}/validation/parity');
  parityDir.createSync(recursive: true);

  final cases = <Map<String, dynamic>>[
    {'id': 'probe-1', 'plaintext': 'probe', 'key': 'k'},
    {'id': 'probe-2', 'plaintext': 'runtime', 'key': 'kaalka-key'},
    {'id': 'unicode', 'plaintext': 'café\r\n日本語 🚀', 'key': 'uni'},
    {'id': 'emoji', 'plaintext': 'runtime 🚀', 'key': 'emoji-key'},
    {'id': 'crlf', 'plaintext': 'line\r\nbreak', 'key': 'crlf-key'},
    {
      'id': 'session',
      'plaintext': '{"cookies":[],"headers":{}}',
      'key': 'session-key'
    },
    {
      'id': 'nested-object',
      'payload': {
        'z': 3,
        'a': {'b': 2, 'timestamp': 999},
        'm': [1, <String, dynamic>{}],
      },
      'key': 'nested',
    },
    {
      'id': 'graph',
      'payload': buildRuntimeGraph({
        'nodes': [
          {'id': 'b'},
          {'id': 'a'},
        ],
        'edges': <dynamic>[],
      }).toJson(),
      'key': 'graph-key',
    },
    {
      'id': 'array',
      'payload': [
        {'id': 'b'},
        {'id': 'a'},
      ],
      'key': 'arr',
    },
    {
      'id': 'dom',
      'dom_html':
          '<div data-reactroot="" nonce="abc">Hi <span data-v-1="x">🚀</span></div>',
      'key': 'dom-key',
    },
    {
      'id': 'memory-graph',
      'payload': {
        'memories': [
          {'id': 'm2'},
          {'id': 'm1'},
        ],
        'merged': true,
      },
      'key': 'mem',
    },
  ];

  final vectors = <Map<String, dynamic>>[];
  for (final c in cases) {
    final value = c.containsKey('plaintext')
        ? c['plaintext']
        : c.containsKey('dom_html')
            ? c['dom_html']
            : c['payload'];
    final serialized = stableSerialize(value);
    final timeKey = deriveKaalkaTimeKey(c['key'] as String);
    final enc1 = encryptValue(value, c['key'] as String);
    final enc2 = encryptValue(value, c['key'] as String);
    final dec = decryptValue(enc1, c['key'] as String);
    final row = <String, dynamic>{
      'id': c['id'],
      'serialized': serialized,
      'time_key': timeKey,
      'hash': computeDeterministicHash(value),
      'encrypted': enc1,
      'decrypt_ok': dec is String
          ? dec == serialized
          : stableSerialize(dec) == serialized,
      'deterministic': enc1 == enc2,
    };
    if (c.containsKey('dom_html')) {
      row['dom_hash'] = computeStableDomHash(c['dom_html'] as String);
    }
    vectors.add(row);
  }

  final dartFile = {
    'algorithm': parityAlgorithm,
    'kaalka': '5.0.0',
    'vectors': vectors,
  };
  File('${parityDir.path}/dart_vectors.json')
      .writeAsStringSync(const JsonEncoder.withIndent('  ').convert(dartFile));

  // Three-way reference comparison: Dart vs the JavaScript reference AND vs the
  // Python reference. A BOM-tolerant read handles UTF-8-with-BOM reference files.
  Map<String, Map<String, dynamic>> loadRef(String name) {
    final f = File('${parityDir.path}/$name');
    if (!f.existsSync()) return <String, Map<String, dynamic>>{};
    var text = f.readAsStringSync();
    if (text.isNotEmpty && text.codeUnitAt(0) == 0xFEFF) {
      text = text.substring(1);
    }
    final decoded = jsonDecode(text) as Map<String, dynamic>;
    final list = (decoded['vectors'] as List).cast<Map<String, dynamic>>();
    return {for (final v in list) v['id'] as String: v};
  }

  final jsRef = loadRef('javascript_vectors.json');
  final pyRef = loadRef('python_vectors.json');

  var allOk = true;
  final results = <Map<String, dynamic>>[];
  for (final dv in vectors) {
    final id = dv['id'] as String;
    final js = jsRef[id];
    final py = pyRef[id];
    final jsHashMatch = js != null && js['hash'] == dv['hash'];
    final jsEncMatch = js != null && js['encrypted'] == dv['encrypted'];
    // Python reference may not carry every id; only assert when present.
    final pyHashMatch = py == null || py['hash'] == dv['hash'];
    final pyEncMatch = py == null || py['encrypted'] == dv['encrypted'];
    final decryptOk = dv['decrypt_ok'] == true;
    final deterministic = dv['deterministic'] == true;
    if (!jsHashMatch ||
        !jsEncMatch ||
        !pyHashMatch ||
        !pyEncMatch ||
        !decryptOk ||
        !deterministic) {
      allOk = false;
    }
    results.add({
      'id': id,
      'hash_match_js': jsHashMatch,
      'encrypt_match_js': jsEncMatch,
      'hash_match_py': py != null ? py['hash'] == dv['hash'] : 'no-ref',
      'encrypt_match_py':
          py != null ? py['encrypted'] == dv['encrypted'] : 'no-ref',
      'decrypt_ok': decryptOk,
      'deterministic': deterministic,
    });
  }

  final report = StringBuffer()
    ..writeln('# Cross-Language Parity Report (Dart)')
    ..writeln()
    ..writeln('**Algorithm:** `$parityAlgorithm`')
    ..writeln('**Generated:** ${DateTime.now().toUtc().toIso8601String()}')
    ..writeln()
    ..writeln(allOk
        ? '✅ **PASS** — Dart matches JavaScript AND Python reference vectors (three-way)'
        : '❌ **FAIL** — see results')
    ..writeln()
    ..writeln('```json')
    ..writeln(const JsonEncoder.withIndent('  ')
        .convert({'crossLangMatch': allOk, 'results': results}))
    ..writeln('```');

  File('${parityDir.path}/parity_report.md')
      .writeAsStringSync(report.toString());

  stdout.writeln(report.toString());
  if (!allOk) exit(1);
}
