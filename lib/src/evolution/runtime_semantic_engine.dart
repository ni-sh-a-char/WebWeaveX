import '_sort_util.dart';

/// Port of core/evolution_runtime/semantic_evolution_engine.py
Map<String, dynamic> evolveSemanticRuntime([
  Map<String, dynamic>? semantic,
  List<dynamic>? history,
]) {
  final sem = semantic ?? <String, dynamic>{};
  final hist = history ?? <dynamic>[];
  final inner = (sem['semantic'] is Map)
      ? Map<String, dynamic>.from(sem['semantic'] as Map)
      : sem;

  final entitiesOuter = (inner['entities'] is Map)
      ? Map<String, dynamic>.from(inner['entities'] as Map)
      : <String, dynamic>{};
  final entities = (entitiesOuter['entities'] as List?) ?? <dynamic>[];

  final recurring = <String, int>{};
  for (final entity in entities) {
    final m = entity as Map;
    final label = '${m['label'] ?? m['type'] ?? ''}';
    recurring[label] = (recurring[label] ?? 0) + 1;
  }

  final stable = stableSorted<String>(
    recurring.entries.where((e) => e.value >= 1).map((e) => e.key),
    pyStrCompare,
  );

  final domainOuter = (inner['domain'] is Map)
      ? Map<String, dynamic>.from(inner['domain'] as Map)
      : <String, dynamic>{};

  final domainRaw = inner['domain'];
  final domainStabilized = domainRaw is Map
      ? domainRaw.isNotEmpty
      : (domainRaw != null && domainRaw != '' && domainRaw != false);

  return <String, dynamic>{
    'recurring_entities': stable,
    'stable_ontology':
        (inner['ontology'] is Map) ? inner['ontology'] : <String, dynamic>{},
    'domain': (inner['domain'] is Map) ? (domainOuter['domain'] ?? '') : '',
    'semantic_convergence': stable.length,
    'domain_stabilized': domainStabilized,
    'history_length': hist.length,
    'bounded': true,
  };
}
