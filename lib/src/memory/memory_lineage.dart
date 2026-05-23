import '../crypto/kaalka_runtime.dart';

Map<String, dynamic> buildMemoryLineage(List<Map<String, dynamic>> history) {
  final lineage = <Map<String, dynamic>>[];
  String? parent;
  for (var i = 0; i < history.length; i++) {
    final item = history[i];
    final tick = item['tick'] ?? item['step'] ?? i;
    final id = computeDeterministicHash({'tick': tick, 'parent': parent});
    lineage.add({
      'id': id,
      'tick': tick,
      'parent_id': parent,
      'stable_hash': computeDeterministicHash(item),
    });
    parent = id;
  }
  return {'lineage': lineage, 'bounded': true};
}

bool verifyMemoryLineage(List<Map<String, dynamic>> lineage) {
  for (var i = 1; i < lineage.length; i++) {
    if (lineage[i]['parent_id'] != lineage[i - 1]['id']) return false;
  }
  return true;
}
