// Million-vector certification — Dart runner (mirror of mv_python.py).
//   dart run validation/zero_trust_v2/mv_dart.dart [count] > mv_dart.json
import 'dart:convert';
import 'dart:io';

import 'package:convert/convert.dart' show AccumulatorSink;
import 'package:crypto/crypto.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/extraction/html_semantic_extraction.dart'
    show extractSemanticHtml;
import 'package:webweavex/src/semantic_ir/composites_c.dart'
    show analyzeDeploymentSemantics;
import 'package:webweavex/src/semantic_ir/evidence_leaves_4.dart'
    show modelUncertainty;
import 'package:webweavex/src/semantic_ir/graph_engines.dart'
    show proveTopology;
import 'package:webweavex/src/semantic_ir/pressure_engines.dart'
    show computeAmbiguityPressure;
import 'package:webweavex/src/semantic_ir/repository_engines.dart'
    show detectInfraSignals, reasonApiSurface;

const List<String> w = [
  'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta'
];
const List<String> f = [
  'Dockerfile', 'k8s/deploy.yaml', 'src/main.py', 'README.md',
  'helm/chart.yaml', '.github/workflows/ci.yml', 'infra/main.tf',
  'docs/guide.md'
];
const List<String> methods = ['get', 'post', 'delete'];
const int lcgA = 6364136223846793005;
const int lcgC = 1442695040888963407;

void main(List<String> argv) {
  final n = argv.isNotEmpty ? int.parse(argv[0]) : 1000000;
  var state = 20260612;
  int rnd() {
    state = state * lcgA + lcgC; // 64-bit wrapping == mod 2^64
    return (state >>> 33) & 0x7FFFFFFF;
  }

  final acc = AccumulatorSink<Digest>();
  final accIn = sha256.startChunkedConversion(acc);
  final famNames = [
    'application', 'extraction', 'repository', 'runtime', 'semantic'
  ];
  final famIn = <String, ByteConversionSink>{};
  final famOut = <String, AccumulatorSink<Digest>>{};
  for (final k in famNames) {
    final s = AccumulatorSink<Digest>();
    famOut[k] = s;
    famIn[k] = sha256.startChunkedConversion(s);
  }
  final famCounts = <String, int>{for (final k in famNames) k: 0};

  for (var i = 0; i < n; i++) {
    String fam;
    dynamic out;
    if (i % 20 == 0) {
      fam = 'extraction';
      final t = w[rnd() % 8];
      final h1 = w[rnd() % 8];
      final p1 = w[rnd() % 8];
      final p2 = w[rnd() % 8];
      final extra = rnd() % 2;
      final html = '<html><head><title>$t</title></head><body>'
          '<h1>$h1</h1><p>$p1 $p2</p>'
          '${extra == 1 ? '<ul><li>${w[rnd() % 8]}</li></ul>' : ''}'
          '</body></html>';
      out = extractSemanticHtml(html);
    } else {
      final k = i % 6;
      if (k == 0) {
        fam = 'semantic';
        out = modelUncertainty(rnd() % 8, rnd() % 8, rnd() % 8);
      } else if (k == 1) {
        fam = 'semantic';
        final cnt = rnd() % 5;
        out = computeAmbiguityPressure(
            <dynamic>[for (var j = 0; j < cnt; j++) w[rnd() % 8]]);
      } else if (k == 2) {
        fam = 'repository';
        final cnt = rnd() % 4;
        final paths = <String, dynamic>{};
        for (var j = 0; j < cnt; j++) {
          paths['/p${j}_${rnd() % 50}'] = <String, dynamic>{
            methods[rnd() % 3]: <String, dynamic>{}
          };
        }
        out = reasonApiSurface(<String, dynamic>{'paths': paths});
      } else if (k == 3) {
        fam = 'repository';
        final cnt = rnd() % 6;
        out = detectInfraSignals(
            <dynamic>[for (var j = 0; j < cnt; j++) f[rnd() % 8]]);
      } else if (k == 4) {
        fam = 'runtime';
        final cnt = rnd() % 6;
        out = proveTopology(<String, dynamic>{
          'edges': <dynamic>[
            for (var j = 0; j < cnt; j++)
              <String, dynamic>{'from': w[rnd() % 8], 'to': w[rnd() % 8]}
          ]
        });
      } else {
        fam = 'application';
        final cnt = rnd() % 6;
        out = analyzeDeploymentSemantics(
            <dynamic>[for (var j = 0; j < cnt; j++) f[rnd() % 8]]);
      }
    }
    final b = ascii.encode('${computeDeterministicHash(out)}\n');
    accIn.add(b);
    famIn[fam]!.add(b);
    famCounts[fam] = famCounts[fam]! + 1;
    if ((i + 1) % 100000 == 0) stderr.writeln('  dart ${i + 1}');
  }
  accIn.close();
  for (final k in famNames) {
    famIn[k]!.close();
  }
  stdout.write(jsonEncode(<String, dynamic>{
    'count': n,
    'family_counts': famCounts,
    'family_digests': <String, String>{
      for (final k in famNames) k: famOut[k]!.events.single.toString()
    },
    'final_digest': acc.events.single.toString(),
  }));
}
