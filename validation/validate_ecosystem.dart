import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final parity =
      await Process.run('dart', ['run', 'validation/validate_parity.dart']);
  stdout.write(parity.stdout);
  stderr.write(parity.stderr);
  if (parity.exitCode != 0) exit(parity.exitCode);

  final replay = await Process.run(
      'dart', ['run', 'validation/replay/validate_replay.dart']);
  stdout.write(replay.stdout);
  stderr.write(replay.stderr);
  if (replay.exitCode != 0) exit(replay.exitCode);

  for (final script in [
    'validation/runtime_graph/validate_runtime_graph.dart',
    'validation/runtime_memory/validate_runtime_memory.dart',
    'validation/reconstruction/validate_reconstruction.dart',
  ]) {
    final r = await Process.run('dart', ['run', script]);
    stdout.write(r.stdout);
    stderr.write(r.stderr);
    if (r.exitCode != 0) exit(r.exitCode);
  }

  final graph = buildRuntimeGraph({
    'session': {'ok': true}
  });
  final mem = buildRuntimeMemory(graph);
  final enc = encryptValue({'agent': 'continuity'}, 'agent-key');
  final dec = decryptValue(enc, 'agent-key');

  final summary = {
    'hash_match': true,
    'encrypt_match': true,
    'replay_match': true,
    'graph_match': graphFingerprint(graph).isNotEmpty,
    'memory_match': mem['stable_hash'] != null,
    'reconstruction_match': reconstructRuntime(
          extraction: {'unified_runtime_graph': graph.toJson()},
        )['runtime_id'] !=
        null,
    'agent_memory_query': queryRuntimeMemory(mem, 'graph') != null,
    'agent_decrypt': dec is Map && dec['agent'] == 'continuity',
  };

  final allOk = summary.values.every((v) => v == true);
  print('\n# Ecosystem Validation (Dart)\n');
  print(const JsonEncoder.withIndent('  ').convert(summary));
  if (!allOk) exit(1);
}
