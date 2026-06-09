/// Port of core/evolution_runtime/runtime_optimization_engine.py
Map<String, dynamic> optimizeRuntimeExecution({
  int depth = 0,
  int replayCost = 0,
  int syncOverhead = 0,
}) {
  final optimizedDepth = _max(1, _min(depth, 100));
  final optimizedReplay = replayCost > 0 ? _max(0, replayCost - 1) : 0;
  final optimizedSync =
      syncOverhead > 1 ? _max(0, syncOverhead - 1) : syncOverhead;

  return <String, dynamic>{
    'execution_depth': optimizedDepth,
    'replay_cost': optimizedReplay,
    'synchronization_overhead': optimizedSync,
    'runtime_pressure': _max(0, depth - optimizedDepth),
    'convergence_gain': optimizedSync == 0,
    'bounded': true,
  };
}

int _max(int a, int b) => a > b ? a : b;
int _min(int a, int b) => a < b ? a : b;
