import 'dart:collection';
import 'entities.dart';

class Relation {
  final String source;
  final String target;
  final String type;

  Relation({
    required this.source,
    required this.target,
    this.type = 'cooccurrence',
  });

  Map<String, String> toMap() {
    return LinkedHashMap<String, String>.from({
      'source': source,
      'target': target,
      'type': type,
    });
  }
}

class Relations {
  List<Relation> extract(List<Entity> entities) {
    if (entities.isEmpty) return [];

    final uniqueEntities = entities.toSet().toList();
    uniqueEntities.sort((a, b) {
      final typeCmp = a.type.compareTo(b.type);
      if (typeCmp != 0) return typeCmp;
      return a.value.compareTo(b.value);
    });

    final relations = <Relation>[];
    for (var i = 0; i < uniqueEntities.length; i++) {
      for (var j = i + 1; j < uniqueEntities.length; j++) {
        final source = '${uniqueEntities[i].type}:${uniqueEntities[i].value}';
        final target = '${uniqueEntities[j].type}:${uniqueEntities[j].value}';
        relations.add(
          Relation(source: source, target: target, type: 'cooccurrence'),
        );
      }
    }

    relations.sort((a, b) {
      final sourceCmp = a.source.compareTo(b.source);
      if (sourceCmp != 0) return sourceCmp;
      return a.target.compareTo(b.target);
    });

    return relations;
  }
}
