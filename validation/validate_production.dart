import 'dart:io';

/// Production validation gate (Dart) — parity, replay, graph, memory, reconstruction.
Future<void> main() async {
  final steps = <String, List<String>>{
    'parity': ['run', 'validation/validate_parity.dart'],
    'replay': ['run', 'validation/replay/validate_replay.dart'],
    'runtime_graph': [
      'run',
      'validation/runtime_graph/validate_runtime_graph.dart'
    ],
    'runtime_memory': [
      'run',
      'validation/runtime_memory/validate_runtime_memory.dart'
    ],
    'reconstruction': [
      'run',
      'validation/reconstruction/validate_reconstruction.dart'
    ],
  };

  for (final entry in steps.entries) {
    final result = await Process.run('dart', entry.value);
    stdout.write(result.stdout);
    stderr.write(result.stderr);
    if (result.exitCode != 0) {
      stderr.writeln('FAILED: ${entry.key}');
      exit(result.exitCode);
    }
    stdout.writeln('OK: ${entry.key}');
  }

  await Process.run('dart', ['run', 'validation/validate_ecosystem.dart']);
}
