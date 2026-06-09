import 'runtime_execution_engine.dart';
import 'runtime_mutation_engine.dart';
import 'runtime_sandbox_engine.dart';

/// Port of core/execution/runtime_simulation_engine.simulate_runtime_execution.
Map<String, dynamic> simulateRuntimeExecution(
  List<Map<String, dynamic>> actions, {
  Map<String, dynamic>? sandbox,
  int tick = 0,
}) {
  final Map<String, dynamic> sb = sandbox ?? buildRuntimeSandbox();
  final List<Map<String, dynamic>> predicted = <Map<String, dynamic>>[];
  bool rollbackRequired = false;

  final List<Map<String, dynamic>> bounded =
      actions.length > 1000 ? actions.sublist(0, 1000) : actions;

  for (int index = 0; index < bounded.length; index++) {
    final Map<String, dynamic> raw = bounded[index];
    final Map<String, dynamic> result =
        executeRuntimeAction(raw, sandbox: sb, tick: tick + index);
    if (result['executed'] == true) {
      // Python: raw.get("selector", raw.get("window", raw.get("command", "")))
      final dynamic target = raw.containsKey('selector')
          ? raw['selector']
          : raw.containsKey('window')
              ? raw['window']
              : raw.containsKey('command')
                  ? raw['command']
                  : '';
      predicted.add(<String, dynamic>{
        'kind': '${raw['type'] ?? 'action'}',
        'target': '$target',
        'tick': tick + index,
      });
    } else {
      rollbackRequired = true;
    }
  }

  final Map<String, dynamic> mutationView = trackRuntimeMutations(
    mutation: <String, dynamic>{
      'kind': 'simulated',
      'target': 'dry_run',
      'tick': tick,
    },
  );

  return <String, dynamic>{
    'simulated': true,
    'predicted_mutations': predicted,
    'rollback_required': rollbackRequired,
    'mutation_preview': mutationView['mutations'],
    'runtime_mutated': false,
    'bounded': true,
  };
}
