import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  final graph = buildRuntimeGraph({
    'session': {'ok': true}
  });
  final mem = buildRuntimeMemoryFabric(graph, [
    {'step': 1, 'kind': 'workflow'},
  ]);
  final queried = queryRuntimeMemoryFabric(mem, "graph");
  final merged = mergeRuntimeMemories(mem, mem);

  final results = {
    'memory_match': mem['stable_hash'] ==
        stableMemoryFabricHash(graph, [
          {'step': 1, 'kind': 'workflow'},
        ]),
    'query_match': queried != null,
    'merge_match': merged['stable_hash'] != null && merged['bounded'] == true,
    'deterministic': mem['stable_hash'] ==
        buildRuntimeMemoryFabric(graph, [
          {'step': 1, 'kind': 'workflow'},
        ])['stable_hash'],
  };

  final allOk = results.values.every((x) => x == true);
  Directory('validation/runtime_memory').createSync(recursive: true);
  File('validation/runtime_memory/runtime_memory_vectors.json')
      .writeAsStringSync(
    const JsonEncoder.withIndent('  ').convert({
      'algorithm': 'webweavex-runtime-memory-v2.0.0',
      'vectors': [results],
    }),
  );
  stdout.writeln(allOk ? 'PASS' : 'FAIL');
  if (!allOk) exit(1);
}
