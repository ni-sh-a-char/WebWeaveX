import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_recovery_evolution_engine.py
Map<String, dynamic> evolveRecoveryOrder(List<Map<String, dynamic>> repairs) {
  final ordering = stableSorted<Map<String, dynamic>>(
    repairs,
    (a, b) => pyStrCompare('${a['action'] ?? ''}', '${b['action'] ?? ''}'),
  );

  return <String, dynamic>{
    'recovery_order': [for (final item in ordering) item['action'] ?? ''],
    'evolved': true,
    'bounded': true,
  };
}
