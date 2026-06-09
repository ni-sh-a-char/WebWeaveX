import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_lineage_engine.py
List<Map<String, dynamic>> buildRuntimeLineage(
  String evolutionId,
  List<Map<String, dynamic>> mutations, [
  String parentId = '',
]) {
  final lineage = <Map<String, dynamic>>[];

  if (parentId.isNotEmpty) {
    lineage.add(<String, dynamic>{
      'id': parentId,
      'relation': 'parent',
    });
  }

  lineage.add(<String, dynamic>{
    'id': evolutionId,
    'relation': 'current',
  });

  for (final mutation in mutations.take(1000)) {
    lineage.add(<String, dynamic>{
      'id': "${mutation['kind'] ?? ''}:${mutation['target'] ?? ''}",
      'relation': 'mutation',
      'ancestor': evolutionId,
    });
  }

  return stableSorted<Map<String, dynamic>>(
    lineage,
    (a, b) => pyStrCompare('${a['id'] ?? ''}', '${b['id'] ?? ''}'),
  );
}
