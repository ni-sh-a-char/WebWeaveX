import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_repair_engine.py
Map<String, dynamic> repairRuntimeFailures([
  List<String>? failures,
  Map<String, dynamic>? selectors,
]) {
  final f = failures ?? <String>[];
  final s = selectors ?? <String, dynamic>{};
  final repairs = <Map<String, dynamic>>[];

  const repairMap = <String, String>{
    'broken_selector': 'heal_selector',
    'failed_workflow': 'reorder_workflow',
    'sync_divergence': 'resync_runtime',
    'runtime_inconsistency': 'verify_consistency',
    'causality_gap': 'bridge_causality',
  };

  final sortedFailures = stableSorted<String>(f, pyStrCompare);
  for (final failure in sortedFailures) {
    final action = repairMap[failure] ?? 'retry_step';
    repairs.add(<String, dynamic>{
      'failure': failure,
      'action': action,
      'repaired': true,
    });
  }

  final selectorKeys = s.keys.toList()..sort(pyStrCompare);
  for (final selector in selectorKeys) {
    repairs.add(<String, dynamic>{
      'failure': 'broken_selector',
      'action': 'heal_selector',
      'selector': selector,
      'healed': s[selector],
      'repaired': true,
    });
  }

  return <String, dynamic>{
    'repairs': repairs,
    'repair_count': repairs.length,
    'bounded': true,
  };
}
