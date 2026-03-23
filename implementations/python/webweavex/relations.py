"""WebWeaveX Relations - Entity relationship extraction."""

from typing import List, Dict, Any, Optional, Set

from .config import DEFAULT_CONFIG
from .schema import Entity, Chunk, Relation


class RelationEngine:
    """Extract entity relations based on co-occurrence."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.relations_config = cfg.get("relations", DEFAULT_CONFIG["relations"])
        self.within_chunks = self.relations_config.get("within_chunks", True)
        self.edge_type = self.relations_config.get("edge_type", "cooccurrence")

    def extract(self, entities: List[Entity], chunks: Optional[List[Chunk]] = None) -> List[Relation]:
        """Extract relations deterministically."""
        if not entities:
            return []

        if self.within_chunks and chunks:
            return self._extract_within_chunks(entities, chunks)
        else:
            return self._extract_all_pairs(entities)

    def _extract_within_chunks(self, entities: List[Entity], chunks: List[Chunk]) -> List[Relation]:
        """Extract relations from entities within the same chunks."""
        seen: Set[tuple] = set()
        relations: List[Relation] = []

        entity_to_chunks: Dict[str, Set[int]] = {}
        for i, chunk in enumerate(chunks):
            for entity in entities:
                if entity.value in chunk.text:
                    key = f"{entity.type}:{entity.value}"
                    if key not in entity_to_chunks:
                        entity_to_chunks[key] = set()
                    entity_to_chunks[key].add(i)

        entity_list = sorted(set(entities), key=lambda e: (e.type, e.value))

        for i, e1 in enumerate(entity_list):
            for e2 in entity_list[i + 1:]:
                key1 = f"{e1.type}:{e1.value}"
                key2 = f"{e2.type}:{e2.value}"
                
                chunks1 = entity_to_chunks.get(key1, set())
                chunks2 = entity_to_chunks.get(key2, set())
                common_chunks = chunks1 & chunks2

                if common_chunks:
                    relation_key = tuple(sorted([f"{e1.type}:{e1.value}", f"{e2.type}:{e2.value}"]))
                    if relation_key not in seen:
                        seen.add(relation_key)
                        relations.append(Relation(
                            source=f"{e1.type}:{e1.value}",
                            target=f"{e2.type}:{e2.value}",
                            type=self.edge_type
                        ))

        return sorted(relations)

    def _extract_all_pairs(self, entities: List[Entity]) -> List[Relation]:
        """Extract relations from all entity pairs."""
        seen: Set[tuple] = set()
        relations: List[Relation] = []

        sorted_entities = sorted(set(entities), key=lambda e: (e.type, e.value))

        for i, e1 in enumerate(sorted_entities):
            for e2 in sorted_entities[i + 1:]:
                key = tuple(sorted([f"{e1.type}:{e1.value}", f"{e2.type}:{e2.value}"]))
                if key not in seen:
                    seen.add(key)
                    relations.append(Relation(
                        source=f"{e1.type}:{e1.value}",
                        target=f"{e2.type}:{e2.value}",
                        type=self.edge_type
                    ))

        return relations
