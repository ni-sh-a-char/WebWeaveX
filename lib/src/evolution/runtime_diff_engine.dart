/// Port of core/evolution_runtime/runtime_diff_engine.py
Map<String, dynamic> diffEvolutionRuntime(
  Map<String, dynamic> previous,
  Map<String, dynamic> current,
) {
  final prevId = '${previous['evolution_id'] ?? ''}';
  final currId = '${current['evolution_id'] ?? ''}';

  final currMutations = (current['mutations'] as List?) ?? <dynamic>[];
  final prevMutations = (previous['mutations'] as List?) ?? <dynamic>[];

  return <String, dynamic>{
    'evolution_changed': prevId != currId,
    'previous_id': prevId,
    'current_id': currId,
    'mutation_delta': currMutations.length - prevMutations.length,
    'revertible': true,
    'bounded': true,
  };
}
