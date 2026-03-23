"""WebWeaveX Graph - Entity graph building."""

from typing import List, Dict, Any, Optional, Set

from .config import DEFAULT_CONFIG
from .schema import Entity, GraphNode, GraphEdge, Graph


class GraphEngine:
    """Build entity co-occurrence graphs."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.graph_config = cfg.get("graph", DEFAULT_CONFIG["graph"])
        self.directed = self.graph_config.get("directed", False)
        self.min_occurrence = self.graph_config.get("min_occurrence", 1)

    def build(self, entities: List[Entity]) -> Graph:
        """Build graph from entities deterministically."""
        if not entities:
            return Graph(nodes=[], edges=[])

        unique_entities = self._deduplicate_entities(entities)
        sorted_entities = sorted(unique_entities, key=lambda e: (e.type, e.value))

        nodes = self._create_nodes(sorted_entities)
        edges = self._create_edges(sorted_entities)

        return Graph(nodes=nodes, edges=edges)

    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """Remove duplicate entities."""
        seen: Set[tuple] = set()
        unique: List[Entity] = []
        
        for entity in entities:
            key = (entity.type, entity.value)
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return unique

    def _create_nodes(self, entities: List[Entity]) -> List[GraphNode]:
        """Create graph nodes from entities."""
        nodes = []
        for entity in entities:
            node_id = f"{entity.type}:{entity.value}"
            nodes.append(GraphNode(id=node_id, type=entity.type, value=entity.value))
        return sorted(nodes, key=lambda n: n.id)

    def _create_edges(self, entities: List[Entity]) -> List[GraphEdge]:
        """Create edges between co-occurring entities."""
        edges: List[GraphEdge] = []
        
        for i, e1 in enumerate(entities):
            for e2 in entities[i + 1:]:
                source = f"{e1.type}:{e1.value}"
                target = f"{e2.type}:{e2.value}"
                edges.append(GraphEdge(
                    source=source,
                    target=target,
                    weight=1,
                    directed=self.directed
                ))

        return sorted(edges, key=lambda e: (e.source, e.target))
