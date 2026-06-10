import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

void main() {
  final graph = buildRuntimeGraph({
    'nodes': [
      {'id': 'a'},
      {'id': 'b'},
    ],
    'edges': <dynamic>[],
  });
  final memory = buildRuntimeMemoryFabric(graph, [
    {'step': 'login'},
  ]);
  final envelope = {
    'bounded': true,
    'pipeline_hash':
        computeDeterministicHash({'kind': 'web', 'url': 'https://example.com'}),
    'unified_runtime_graph': graph.toJson(),
    'graph': graph.toJson(),
    'browser_ir': {
      'runtime_identity':
          computeDeterministicHash({'url': 'https://example.com'}),
    },
    'global_runtime_fingerprint': computeRuntimePipelineFingerprint(
      {'bounded': true, 'pipeline_hash': 'x'},
      graph,
    ),
    'runtime_memory': memory,
  };

  final clone = jsonDecode(jsonEncode(envelope)) as Map<String, dynamic>;
  final replay = validateReplayEquivalenceExtended(envelope, clone);
  final reconstructed = reconstructRuntimeFromEnvelope(extraction: envelope);
  final reconstructed2 = reconstructRuntimeFromEnvelope(extraction: envelope);

  final results = {
    'replay_match': replay['equivalent'] == true,
    'graph_match': graphFingerprint(graph) == graphFingerprint(graph),
    'memory_match': memory['stable_hash'] ==
        stableMemoryFabricHash(graph, [
          {'step': 'login'},
        ]),
    'reconstruction_match':
        reconstructed['runtime_id'] == reconstructed2['runtime_id'],
    'memory_query': queryRuntimeMemoryFabric(memory, "graph") != null,
  };

  final allOk = results.values.every((v) => v == true);
  final report = StringBuffer()
    ..writeln('# Replay Validation Report (Dart)')
    ..writeln()
    ..writeln(allOk ? '✅ **PASS**' : '❌ **FAIL**')
    ..writeln()
    ..writeln('```json')
    ..writeln(const JsonEncoder.withIndent('  ').convert(results))
    ..writeln('```');

  File('validation/replay/replay_report.md')
      .writeAsStringSync(report.toString());
  File('validation/replay/replay_vectors.json').writeAsStringSync(
    const JsonEncoder.withIndent('  ').convert({
      'algorithm': 'webweavex-replay-v2.0.0',
      'vectors': [results],
    }),
  );

  stdout.writeln(report.toString());
  if (!allOk) exit(1);
}
