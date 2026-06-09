/// Port of core/evolution_runtime/runtime_strategy_engine.py
Map<String, dynamic> buildRuntimeStrategy([Map<String, dynamic>? evidence]) {
  final e = evidence ?? <String, dynamic>{};
  final driftCount = _asInt(e['drift_count']);
  final failedSteps = _asInt(e['failed_steps']);

  return <String, dynamic>{
    'extraction_path':
        driftCount == 0 ? 'browser_first' : 'repair_then_extract',
    'synchronization_path':
        failedSteps == 0 ? 'continuous' : 'converge_then_sync',
    'workflow_order': 'priority_asc',
    'selector_hierarchy': <String>['healed', 'structural', 'fallback'],
    'recovery_order': <String>[
      'heal_selector',
      'recover_workflow',
      'resync_runtime',
    ],
    'bounded': true,
  };
}

int _asInt(dynamic v) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  return 0;
}
