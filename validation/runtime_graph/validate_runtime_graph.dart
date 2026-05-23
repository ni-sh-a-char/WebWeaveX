import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  final graph = buildRuntimeGraph({
    'nodes': [
      {'id': 'b'},
      {'id': 'a'},
    ],
    'edges': <dynamic>[],
  });
  final v = validateRuntimeGraph(graph);
  final fp1 = computeRuntimeFingerprint(graph);
  final fp2 = graphFingerprint(graph);

  final results = {
    'graph_match': v['valid'] == true,
    'fingerprint_match': fp1 == fp2,
    'deterministic':
        computeRuntimeFingerprint(graph) == computeRuntimeFingerprint(graph),
  };

  final allOk = results.values.every((x) => x == true);
  final body = {
    'algorithm': 'webweavex-runtime-graph-v2.0.0',
    'vectors': [results],
  };

  Directory('validation/runtime_graph').createSync(recursive: true);
  File('validation/runtime_graph/runtime_graph_vectors.json')
      .writeAsStringSync(const JsonEncoder.withIndent('  ').convert(body));
  File('validation/runtime_graph/runtime_graph_report.md').writeAsStringSync(
    '# Runtime Graph Validation (Dart)\n\n${allOk ? "✅ PASS" : "❌ FAIL"}\n\n```json\n${const JsonEncoder.withIndent("  ").convert(results)}\n```\n',
  );

  stdout.writeln(allOk ? 'PASS' : 'FAIL');
  if (!allOk) exit(1);
}
