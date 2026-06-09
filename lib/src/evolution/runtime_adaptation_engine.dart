/// Port of core/evolution_runtime/runtime_adaptation_engine.py
Map<String, dynamic> adaptRuntimeStrategy(
  Map<String, dynamic> strategy,
  Map<String, dynamic> optimization,
) {
  final adapted = Map<String, dynamic>.from(strategy);
  if (_truthy(optimization['convergence_gain'])) {
    adapted['synchronization_path'] = 'continuous';
  }
  if (_asNum(optimization['runtime_pressure']) > 0) {
    adapted['extraction_path'] = 'repair_then_extract';
  }
  adapted['adapted'] = true;
  adapted['bounded'] = true;
  return adapted;
}

bool _truthy(dynamic v) {
  if (v == null) return false;
  if (v is bool) return v;
  if (v is num) return v != 0;
  return true;
}

num _asNum(dynamic v) => v is num ? v : 0;
