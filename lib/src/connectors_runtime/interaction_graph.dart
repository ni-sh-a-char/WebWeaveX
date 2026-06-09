/// Port of core/interaction/interaction_graph_engine.build_interaction_graph.
library;

import '../crypto/hashing.dart';

const int maxGraphNodes = 10000;
const int maxGraphEdges = 50000;

/// Port of core/interaction/interaction_graph_engine.build_interaction_graph.
///
/// `graph_hash` reuses the cross-language deterministic hash engine
/// (compute_kaalka_hash_payload == compute_deterministic_hash).
Map<String, dynamic> buildInteractionGraph(
  List<Map<String, dynamic>> interactions,
) {
  final List<Map<String, dynamic>> nodes = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> edges = <Map<String, dynamic>>[];

  String previousId = 'state_root';
  nodes.add(<String, dynamic>{
    'id': previousId,
    'type': 'state',
    'name': 'root',
  });

  final int limit =
      interactions.length > maxGraphNodes ? maxGraphNodes : interactions.length;

  for (int index = 0; index < limit; index++) {
    final Map<String, dynamic> interaction = interactions[index];
    final String nodeId = '${interaction['id'] ?? 'interaction_$index'}';
    final String action = '${interaction['action'] ?? ''}';
    final String selector = '${interaction['selector'] ?? ''}';

    String nodeType = action == 'fill' ? 'form' : 'page';
    if (selector.toLowerCase().contains('modal')) {
      nodeType = 'modal';
    }
    if (selector.toLowerCase().contains('tab')) {
      nodeType = 'tab';
    }

    nodes.add(<String, dynamic>{
      'id': nodeId,
      'type': nodeType,
      'action': action,
      'selector': selector,
    });

    String relation = action.isNotEmpty ? action : 'transition';
    if (action == 'click') {
      relation = 'click';
    } else if (action == 'fill' || action == 'select') {
      relation = 'submission';
    } else if (action == 'wait') {
      relation = 'navigation';
    }

    edges.add(<String, dynamic>{
      'from': previousId,
      'to': nodeId,
      'relation': relation,
    });

    previousId = nodeId;
  }

  final List<Map<String, dynamic>> boundedNodes =
      nodes.length > maxGraphNodes ? nodes.sublist(0, maxGraphNodes) : nodes;
  final List<Map<String, dynamic>> boundedEdges =
      edges.length > maxGraphEdges ? edges.sublist(0, maxGraphEdges) : edges;

  return <String, dynamic>{
    'ir': 'interaction_graph',
    'nodes': boundedNodes,
    'edges': boundedEdges,
    'graph_hash': computeDeterministicHash(<String, dynamic>{
      'nodes': boundedNodes,
      'edges': boundedEdges,
    }),
    'bounded': true,
  };
}
