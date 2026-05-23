import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  final graph = buildRuntimeGraph({
    'session': {'ok': true}
  });
  final mem = buildRuntimeMemory(graph, [
    {'step': 1, 'kind': 'workflow'},
  ]);
  final queried = queryRuntimeMemory(mem, 'graph');
  final merged = mergeRuntimeMemories(mem, mem);

  final results = {
    'memory_match': mem['stable_hash'] ==
        stableMemoryHash(graph, [
          {'step': 1, 'kind': 'workflow'},
        ]),
    'query_match': queried != null,
    'merge_match': merged['stable_hash'] != null && merged['bounded'] == true,
    'deterministic': mem['stable_hash'] ==
        buildRuntimeMemory(graph, [
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
