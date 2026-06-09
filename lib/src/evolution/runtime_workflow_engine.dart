import '_sort_util.dart';

/// Port of core/evolution_runtime/workflow_evolution_engine.py
Map<String, dynamic> evolveWorkflowRuntime([
  Map<String, dynamic>? plan,
  Map<String, dynamic>? execution,
  List<dynamic>? history,
]) {
  final p = plan ?? <String, dynamic>{};
  final e = execution ?? <String, dynamic>{};
  final hist = history ?? <dynamic>[];
  final steps = List<dynamic>.from((p['steps'] as List?) ?? <dynamic>[]);

  final executed = (e['executed'] as List?) ?? <dynamic>[];
  final score = executed.length;

  final optimizedSteps = stableSorted<dynamic>(steps, (a, b) {
    final am = a as Map;
    final bm = b as Map;
    final pa = -(_asInt(am['priority']));
    final pb = -(_asInt(bm['priority']));
    if (pa != pb) return pa.compareTo(pb);
    return pyStrCompare('${am['id'] ?? ''}', '${bm['id'] ?? ''}');
  });

  return <String, dynamic>{
    'execution_ordering': [
      for (final s in optimizedSteps) (s as Map)['id'] ?? ''
    ],
    'retries': hist.length < 3 ? hist.length : 3,
    'pacing': (steps.length - score) > 0 ? steps.length - score : 0,
    'sync_timing': steps.length,
    'recovery_ordering': <String>[
      'retry_step',
      'realign_runtime',
      'checkpoint'
    ],
    'score': score,
    'bounded': true,
  };
}

int _asInt(dynamic v) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  return 0;
}
