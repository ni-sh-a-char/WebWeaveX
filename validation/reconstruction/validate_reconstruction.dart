import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  final graph = buildRuntimeGraph({'a': 1});
  final extraction = {
    'unified_runtime_graph': graph.toJson(),
    'graph': graph.toJson(),
  };
  final r1 = reconstructRuntimeFromEnvelope(extraction: extraction);
  final r2 = reconstructRuntimeFromEnvelope(extraction: extraction);

  final results = {
    'reconstruction_match': r1['runtime_id'] == r2['runtime_id'],
    'reconstructed': r1['reconstructed'] == true,
    'bounded': r1['bounded'] == true,
  };

  final allOk = results.values.every((x) => x == true);
  Directory('validation/reconstruction').createSync(recursive: true);
  File('validation/reconstruction/reconstruction_vectors.json')
      .writeAsStringSync(
    const JsonEncoder.withIndent('  ').convert({
      'algorithm': 'webweavex-reconstruction-v2.0.0',
      'vectors': [results],
    }),
  );
  stdout.writeln(allOk ? 'PASS' : 'FAIL');
  if (!allOk) exit(1);
}
