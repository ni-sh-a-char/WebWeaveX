import 'dart:collection';
import 'entities.dart';

class GraphNode {
  final String id;
  final String type;
  final String value;

  GraphNode({required this.id, required this.type, required this.value});

  Map<String, String> toMap() {
    return LinkedHashMap<String, String>.from({
      'id': id,
      'type': type,
      'value': value,
    });
  }
}

class GraphEdge {
  final String source;
  final String target;
  final int weight;

  GraphEdge({required this.source, required this.target, this.weight = 1});

  Map<String, dynamic> toMap() {
    return LinkedHashMap<String, dynamic>.from({
      'source': source,
      'target': target,
      'weight': weight,
    });
  }
}

class GraphData {
  final List<GraphNode> nodes;
  final List<GraphEdge> edges;

  GraphData({required this.nodes, required this.edges});

  Map<String, dynamic> toMap() {
    return LinkedHashMap<String, dynamic>.from({
      'nodes': nodes.map((n) => n.toMap()).toList(),
      'edges': edges.map((e) => e.toMap()).toList(),
    });
  }
}

class Graph {
  GraphData build(List<Entity> entities) {
    if (entities.isEmpty) {
      return GraphData(nodes: [], edges: []);
    }

    final uniqueEntities = entities.toSet().toList();
    uniqueEntities.sort((a, b) {
      final typeCmp = a.type.compareTo(b.type);
      if (typeCmp != 0) return typeCmp;
      return a.value.compareTo(b.value);
    });

    final nodes = uniqueEntities.map((e) {
      final id = '${e.type}:${e.value}';
      return GraphNode(id: id, type: e.type, value: e.value);
    }).toList();

    nodes.sort((a, b) => a.id.compareTo(b.id));

    final edges = <GraphEdge>[];
    for (var i = 0; i < uniqueEntities.length; i++) {
      for (var j = i + 1; j < uniqueEntities.length; j++) {
        final source = '${uniqueEntities[i].type}:${uniqueEntities[i].value}';
        final target = '${uniqueEntities[j].type}:${uniqueEntities[j].value}';
        edges.add(GraphEdge(source: source, target: target, weight: 1));
      }
    }

    edges.sort((a, b) {
      final sourceCmp = a.source.compareTo(b.source);
      if (sourceCmp != 0) return sourceCmp;
      return a.target.compareTo(b.target);
    });

    return GraphData(nodes: nodes, edges: edges);
  }
}
