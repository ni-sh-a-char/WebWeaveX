/// Port of core/evolution_runtime/runtime_policy_engine.py
const int policyMaxMutations = 10000;
const int policyMaxRepairs = 1000;
const int policyMaxSyncThreshold = 1000;
const int policyMaxOptimizationDepth = 100;

Map<String, dynamic> buildRuntimePolicy() {
  return <String, dynamic>{
    'evolution_bounds': policyMaxMutations,
    'repair_limits': policyMaxRepairs,
    'synchronization_threshold': policyMaxSyncThreshold,
    'optimization_ceiling': policyMaxOptimizationDepth,
    'mutation_constraints': <String, dynamic>{
      'allow_selector': true,
      'allow_workflow': true,
      'allow_semantic': true,
      'allow_sync': true,
      'allow_code_synthesis': false,
    },
    'bounded': true,
  };
}

Map<String, dynamic> enforceRuntimePolicy(
  Map<String, dynamic> policy,
  List<dynamic> mutations,
  List<dynamic> repairs,
  int depth,
) {
  final withinBounds =
      mutations.length <= (policy['evolution_bounds'] as int) &&
          repairs.length <= (policy['repair_limits'] as int) &&
          depth <= (policy['optimization_ceiling'] as int);

  return <String, dynamic>{
    'within_bounds': withinBounds,
    'mutation_count': mutations.length,
    'repair_count': repairs.length,
    'depth': depth,
    'bounded': true,
  };
}
