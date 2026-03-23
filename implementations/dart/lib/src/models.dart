class Entity {
  final String type;
  final String value;

  Entity(this.type, this.value);

  Map<String, String> toMap() => {'type': type, 'value': value};

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Entity && type == other.type && value == other.value;

  @override
  int get hashCode => type.hashCode ^ value.hashCode;
}

class Chunk {
  final String text;
  final int index;
  final int start;
  final int end;

  Chunk(this.text, this.index, this.start, this.end);

  Map<String, dynamic> toMap() => {
    'text': text,
    'index': index,
    'start': start,
    'end': end,
  };
}

class GraphEdge {
  final String source;
  final String target;
  final int weight;
  final bool directed;

  GraphEdge(this.source, this.target, this.weight, {this.directed = false});

  Map<String, dynamic> toMap() {
    final map = <String, dynamic>{
      'source': source,
      'target': target,
      'weight': weight,
    };
    if (directed) map['directed'] = true;
    return map;
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is GraphEdge && source == other.source && target == other.target;

  @override
  int get hashCode => source.hashCode ^ target.hashCode;
}

class GraphResult {
  final List<Entity> nodes;
  final List<GraphEdge> edges;

  GraphResult(this.nodes, this.edges);

  Map<String, dynamic> toMap() => {
    'nodes': nodes.map((e) => e.toMap()).toList(),
    'edges': edges.map((e) => e.toMap()).toList(),
  };
}

class CrawlResult {
  final String url;
  final String text;
  final List<Chunk> chunks;
  final List<Entity> entities;
  final GraphResult? graph;
  final Map<String, String>? metadata;

  CrawlResult({
    required this.url,
    required this.text,
    this.chunks = const [],
    this.entities = const [],
    this.graph,
    this.metadata,
  });

  Map<String, dynamic> toMap() {
    final map = <String, dynamic>{'url': url, 'text': text};
    if (chunks.isNotEmpty)
      map['chunks'] = chunks.map((c) => c.toMap()).toList();
    if (entities.isNotEmpty)
      map['entities'] = entities.map((e) => e.toMap()).toList();
    if (graph != null) map['graph'] = graph!.toMap();
    if (metadata != null) map['metadata'] = metadata;
    return map;
  }
}
