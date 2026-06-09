import 'dart:convert';

import 'package:crypto/crypto.dart';

import '_sort_util.dart';

/// Port of core/evolution_runtime/runtime_evolution_engine.py
Map<String, dynamic> buildRuntimeEvolution(
  List<Map<String, dynamic>> mutations,
  List<Map<String, dynamic>> lineage,
) {
  final parts = stableSorted<String>(
    mutations.map((m) => "${m['kind'] ?? ''}:${m['target'] ?? ''}"),
    pyStrCompare,
  );
  final payload = parts.join('|');
  final digest = sha256.convert(utf8.encode(payload)).toString();
  final evolutionId = digest.substring(0, 32);

  final sortedMutations = stableSorted<Map<String, dynamic>>(
    mutations,
    (a, b) => pyStrCompare('${a['target'] ?? ''}', '${b['target'] ?? ''}'),
  );
  final sortedLineage = stableSorted<Map<String, dynamic>>(
    lineage,
    (a, b) => pyStrCompare('${a['id'] ?? ''}', '${b['id'] ?? ''}'),
  );

  int countKind(String kind) =>
      mutations.where((m) => m['kind'] == kind).length;

  return <String, dynamic>{
    'evolution_id': evolutionId,
    'mutations': sortedMutations,
    'lineage': sortedLineage,
    'improvements': <String, dynamic>{
      'selector_repairs': countKind('selector'),
      'workflow_optimizations': countKind('workflow'),
      'semantic_convergence': countKind('semantic'),
      'sync_improvements': countKind('sync'),
    },
    'bounded': true,
  };
}
