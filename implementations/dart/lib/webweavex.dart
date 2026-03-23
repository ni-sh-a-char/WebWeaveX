import 'dart:convert';
import 'pipeline.dart';
import 'chunker.dart';
import 'entities.dart';

class WebWeaveX {
  final Pipeline _pipeline = Pipeline();

  Map<String, dynamic> extract(dynamic textOrHtml) {
    try {
      if (textOrHtml is! String || textOrHtml.isEmpty) {
        return _pipeline.extractFromText('');
      }
      return _pipeline.extractFromText(textOrHtml);
    } catch (e) {
      return _createErrorResult();
    }
  }

  String clean(String text) {
    final result = _pipeline.extractFromText(text);
    return (result['content'] as Map<String, dynamic>)['text'] as String? ?? '';
  }

  List<Chunk> chunk(String text) {
    final result = _pipeline.extractFromText(text);
    return (result['chunks'] as List<dynamic>)
        .map(
          (c) => Chunk(
            text: c['text'] as String,
            index: c['index'] as int,
            start: c['start'] as int,
            end: c['end'] as int,
          ),
        )
        .toList();
  }

  List<Entity> entities(String text) {
    final result = _pipeline.extractFromText(text);
    return (result['entities'] as List<dynamic>)
        .map(
          (e) => Entity(type: e['type'] as String, value: e['value'] as String),
        )
        .toList();
  }

  Map<String, dynamic> extractAgent(String text) {
    try {
      final result = extract(text);
      return _extractAgentFromResult(result);
    } catch (e) {
      return LinkedHashMap<String, dynamic>.from({
        'task': 'web_analysis',
        'input': text.length > 500 ? text.substring(0, 500) : text,
        'output': <String, dynamic>{},
        'summary': 'Error: $e',
        'actions': <String>[],
        'confidence': 0.0,
      });
    }
  }

  Map<String, dynamic> _extractAgentFromResult(Map<String, dynamic> result) {
    final content = result['content'] as Map<String, dynamic>? ?? {};
    final text = content['text'] as String? ?? '';
    final entities = (result['entities'] as List<dynamic>?)
            ?.map((e) => Map<String, String>.from(e as Map))
            .toList() ??
        [];
    final relations = (result['relations'] as List<dynamic>?)
            ?.map((r) => Map<String, String>.from(r as Map))
            .toList() ??
        [];

    final summary = entities.isEmpty
        ? 'No entities extracted from input text.'
        : 'Extracted ${entities.length} entities from text.';

    final actions = <String>[];
    final types = entities.map((e) => e['type'] ?? '').toSet();
    if (types.contains('url')) actions.add('crawl');
    if (types.contains('email')) actions.add('contact');
    if (types.contains('phone')) actions.add('call');
    if (entities.length > 5) actions.add('extract_more');
    if (actions.isEmpty) actions.add('analyze');

    final confidence = text.isNotEmpty
        ? (entities.length + relations.length * 0.5) / text.length * 10
        : 0.0;

    return LinkedHashMap<String, dynamic>.from({
      'task': 'web_analysis',
      'input': text.length > 500 ? text.substring(0, 500) : text,
      'output': result,
      'summary': summary,
      'actions': actions,
      'confidence': (confidence * 100).round() / 100,
    });
  }

  Map<String, dynamic> toMemoryBlock(Map<String, dynamic> result) {
    try {
      return LinkedHashMap<String, dynamic>.from({
        'type': 'webweavex_memory',
        'entities': result['entities'] ?? [],
        'relations': result['relations'] ?? [],
        'graph': result['graph'] ?? _createEmptyGraph(),
        'timestamp': DateTime.now().toUtc().toIso8601String(),
        'source': 'webweavex',
      });
    } catch (e) {
      return LinkedHashMap<String, dynamic>.from({
        'type': 'webweavex_memory',
        'entities': [],
        'relations': [],
        'graph': _createEmptyGraph(),
        'timestamp': DateTime.now().toUtc().toIso8601String(),
        'source': 'webweavex',
      });
    }
  }

  List<Map<String, dynamic>> toRagChunks(Map<String, dynamic> result) {
    try {
      final chunks = (result['chunks'] as List<dynamic>?)
              ?.map((c) => Map<String, dynamic>.from(c as Map))
              .toList() ??
          [];
      final entities = (result['entities'] as List<dynamic>?)
              ?.map((e) => Map<String, String>.from(e as Map))
              .toList() ??
          [];
      final relations = (result['relations'] as List<dynamic>?)
              ?.map((r) => Map<String, String>.from(r as Map))
              .toList() ??
          [];

      return chunks.map((chunk) {
        return LinkedHashMap<String, dynamic>.from({
          'text': chunk['text'] ?? '',
          'metadata': LinkedHashMap<String, dynamic>.from({
            'entities': entities,
            'relations': relations.take(5).toList(),
            'source': 'webweavex',
          }),
        });
      }).toList();
    } catch (e) {
      return [];
    }
  }

  Iterable<String> extractStream(String text) {
    return [
      'cleaning',
      'chunking',
      'entities',
      'relations',
      'graph',
      'insights'
    ];
  }

  String prettyPrint(Map<String, dynamic> result) {
    final buffer = StringBuffer();
    buffer.writeln('==================================================');
    buffer.writeln('WebWeaveX Analysis');
    buffer.writeln('==================================================');
    buffer.writeln();
    buffer.writeln('ENTITY SUMMARY:');
    buffer.writeln('------------------------------');

    final insights = result['insights'] as Map<String, dynamic>?;
    final entityCounts = insights?['entity_counts'] as Map<String, int>?;
    entityCounts?.forEach((key, count) {
      buffer.writeln('  $key: $count');
    });

    final stats = insights?['stats'] as Map<String, dynamic>?;
    if (stats != null) {
      buffer.writeln();
      buffer.writeln('STATISTICS:');
      buffer.writeln('------------------------------');
      buffer.writeln('  Total Entities: ${stats['total_entities'] ?? 0}');
      buffer.writeln('  Unique Entities: ${stats['unique_entities'] ?? 0}');
      buffer.writeln('  Entity Types: ${stats['entity_types'] ?? 0}');
      buffer.writeln('  Total Relations: ${stats['total_relations'] ?? 0}');
      buffer.writeln('  Total Chunks: ${stats['total_chunks'] ?? 0}');
      buffer.writeln('  Text Length: ${stats['text_length'] ?? 0}');
      buffer.writeln('  Word Count: ${stats['word_count'] ?? 0}');
    }

    buffer.writeln();
    buffer.writeln('==================================================');
    return buffer.toString();
  }

  static Map<String, dynamic> getToolSchema() {
    return LinkedHashMap<String, dynamic>.from({
      'name': 'webweavex_extract',
      'description': 'Extract structured intelligence from text',
      'parameters': LinkedHashMap<String, dynamic>.from({
        'type': 'object',
        'properties': LinkedHashMap<String, dynamic>.from({
          'input': LinkedHashMap<String, dynamic>.from({'type': 'string'}),
        }),
        'required': ['input'],
      }),
    });
  }

  static List<Map<String, dynamic>> getAllTools() {
    return [
      getToolSchema(),
      LinkedHashMap<String, dynamic>.from({
        'name': 'webweavex_entities',
        'description': 'Extract only entities from text',
        'parameters': LinkedHashMap<String, dynamic>.from({
          'type': 'object',
          'properties': LinkedHashMap<String, dynamic>.from({
            'input': LinkedHashMap<String, dynamic>.from({'type': 'string'}),
          }),
          'required': ['input'],
        }),
      }),
    ];
  }

  static List<String> getCapabilities() {
    return [
      'extract',
      'entities',
      'graph',
      'rag',
      'agent_mode',
      'memory_export',
      'streaming',
    ];
  }

  Map<String, dynamic> _createEmptyGraph() {
    return LinkedHashMap<String, dynamic>.from({
      'nodes': [],
      'edges': [],
    });
  }

  Map<String, dynamic> _createErrorResult() {
    return LinkedHashMap<String, dynamic>.from({
      'meta': LinkedHashMap<String, dynamic>.from({'title': '', 'url': ''}),
      'content': LinkedHashMap<String, dynamic>.from({'text': ''}),
      'chunks': [],
      'entities': [],
      'relations': [],
      'graph': _createEmptyGraph(),
      'insights': LinkedHashMap<String, dynamic>.from({
        'entity_counts': <String, int>{},
        'stats': <String, dynamic>{},
        'top_entities': [],
      }),
    });
  }
}
