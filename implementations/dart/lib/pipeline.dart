import 'dart:convert';
import 'dart:collection';
import 'cleaner.dart';
import 'chunker.dart';
import 'entities.dart';
import 'relations.dart';
import 'graph.dart';
import 'insights.dart';

class Pipeline {
  final Cleaner _cleaner = Cleaner();
  final Chunker _chunker = Chunker();
  final Entities _entities = Entities();
  final Relations _relations = Relations();
  final Graph _graph = Graph();
  final Insights _insights = Insights();

  Map<String, dynamic> extractFromText(String text) {
    final cleanedText = _cleaner.clean(text);
    final chunkList = _chunker.chunk(cleanedText);
    final entityList = _entities.extract(cleanedText);
    final relationList = _relations.extract(entityList);
    final graphData = _graph.build(entityList);
    final insightsData = _insights.compute(entityList, chunkList, cleanedText);

    return buildResult(
      cleanedText,
      chunkList,
      entityList,
      relationList,
      graphData,
      insightsData,
    );
  }

  Map<String, dynamic> buildResult(
    String text,
    List<Chunk> chunks,
    List<Entity> entities,
    List<Relation> relations,
    GraphData graphData,
    Map<String, dynamic> insightsData,
  ) {
    final sortedEntities = List<Entity>.from(entities)
      ..sort((a, b) {
        final typeCmp = a.type.compareTo(b.type);
        if (typeCmp != 0) return typeCmp;
        return a.value.compareTo(b.value);
      });

    final chunksList = chunks.map((c) => c.toMap()).toList();
    final entitiesList = sortedEntities.map((e) => e.toMap()).toList();
    final relationsList = relations.map((r) => r.toMap()).toList();

    return LinkedHashMap<String, dynamic>.from({
      'meta': LinkedHashMap<String, dynamic>.from({'title': '', 'url': ''}),
      'content': LinkedHashMap<String, dynamic>.from({'text': text}),
      'chunks': chunksList,
      'entities': entitiesList,
      'relations': relationsList,
      'graph': graphData.toMap(),
      'insights': insightsData,
    });
  }

  String toJson(Map<String, dynamic> map) {
    return const JsonEncoder.withIndent('  ').convert(map);
  }
}
