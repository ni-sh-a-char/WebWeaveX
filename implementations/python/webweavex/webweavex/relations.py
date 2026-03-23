"""WebWeaveX Relations - Entity relation extraction."""

from typing import List, Dict, Any, Optional

from .config import DEFAULT_CONFIG, get_config
from .schema import Entity, Relation


class RelationEngine:
    """Extract relations between entities."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.relations_config = cfg.get("relations", DEFAULT_CONFIG["relations"])
        self.within_chunks = self.relations_config.get("within_chunks", True)
        self.edge_type = self.relations_config.get("edge_type", "cooccurrence")

    def extract(self, entities: List[Entity], chunks: List[Any] = None) -> List[Relation]:
        """Extract relations from entities."""
        if not entities:
            return []

        unique_entities = list(set(entities))
        sorted_entities = sorted(unique_entities, key=lambda e: (e.type, e.value))

        relations = []
        for i, e1 in enumerate(sorted_entities):
            for e2 in sorted_entities[i + 1:]:
                source = f"{e1.type}:{e1.value}"
                target = f"{e2.type}:{e2.value}"
                relations.append(Relation(
                    source=source,
                    target=target,
                    type=self.edge_type
                ))

        return sorted(relations, key=lambda r: (r.source, r.target))
