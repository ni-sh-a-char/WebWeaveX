import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_pattern_engine.py
Map<String, dynamic> buildRuntimePatterns({
  Map<String, dynamic>? ui,
  List<dynamic>? workflows,
  Map<String, dynamic>? semantic,
  List<dynamic>? syncHistory,
}) {
  final u = ui ?? <String, dynamic>{};
  final wf = workflows ?? <dynamic>[];
  final sh = syncHistory ?? <dynamic>[];

  final uiStructures = u.keys.toList()..sort(pyStrCompare);

  final workflowPatterns = <String>[
    for (final raw in wf.take(1000))
      '${(raw as Map)['objective'] ?? raw['action'] ?? ''}',
  ];

  // Python preserves dict insertion order for semantic.keys()[:100].
  final semanticLayouts =
      (semantic ?? <String, dynamic>{}).keys.take(100).toList();

  return <String, dynamic>{
    'ui_structures': uiStructures,
    'workflow_patterns': workflowPatterns,
    'semantic_layouts': semanticLayouts,
    'sync_histories': sh.length,
    'bounded': true,
  };
}
