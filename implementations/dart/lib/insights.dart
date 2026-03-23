import 'dart:collection';
import 'entities.dart';
import 'chunker.dart';

class Insights {
  Map<String, dynamic> compute(
    List<Entity> entities,
    List<Chunk> chunks,
    String text,
  ) {
    final entityCounts = <String, int>{};
    final entityTypes = <String>{};

    for (final entity in entities) {
      final key = '${entity.type}:${entity.value}';
      entityCounts[key] = (entityCounts[key] ?? 0) + 1;
      entityTypes.add(entity.type);
    }

    final sortedCounts = entityCounts.entries.toList()
      ..sort((a, b) {
        final countCmp = b.value.compareTo(a.value);
        if (countCmp != 0) return countCmp;
        return a.key.compareTo(b.key);
      });

    final topEntities = sortedCounts.take(10).map((e) {
      final colonIndex = e.key.indexOf(':');
      final type = colonIndex > 0 ? e.key.substring(0, colonIndex) : '';
      final value = colonIndex > 0 && colonIndex < e.key.length - 1
          ? e.key.substring(colonIndex + 1)
          : '';
      return LinkedHashMap<String, dynamic>.from({
        'type': type,
        'value': value,
        'count': e.value,
      });
    }).toList();

    final stats = LinkedHashMap<String, dynamic>.from({
      'total_entities': entities.length,
      'unique_entities': entityCounts.length,
      'entity_types': entityTypes.length,
      'total_relations': 0,
    });

    if (chunks.isNotEmpty) {
      stats['total_chunks'] = chunks.length;
    }

    if (text.isNotEmpty) {
      stats['text_length'] = text.length;
      stats['word_count'] = text.trim().split(RegExp(r'\s+')).length;
    }

    final sortedEntityCounts = entityCounts.entries.toList()
      ..sort((a, b) => a.key.compareTo(b.key));
    final entityCountsMap = LinkedHashMap<String, int>.fromEntries(
      sortedEntityCounts.map((e) => MapEntry(e.key, e.value)),
    );

    return LinkedHashMap<String, dynamic>.from({
      'entity_counts': entityCountsMap,
      'stats': stats,
      'top_entities': topEntities,
    });
  }
}
