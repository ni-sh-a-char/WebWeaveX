"""WebWeaveX Insights - Analytics and statistics."""

from typing import List, Dict, Any, Optional

from .config import DEFAULT_CONFIG
from .schema import Entity, Chunk, Insights


class InsightsEngine:
    """Compute insights and statistics from extracted data."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.insights_config = cfg.get("insights", DEFAULT_CONFIG["insights"])
        self.top_entities_count = self.insights_config.get("top_entities_count", 10)
        self.include_stats = self.insights_config.get("include_stats", True)

    def compute(
        self,
        entities: List[Entity],
        chunks: List[Chunk],
        text: str = ""
    ) -> Insights:
        """Compute insights deterministically."""
        entity_counts = self._count_entities(entities)
        top_entities = self._get_top_entities(entity_counts)
        stats = self._compute_stats(entities, chunks, text) if self.include_stats else {}

        return Insights(
            top_entities=top_entities,
            stats=stats,
            entity_counts=entity_counts
        )

    def _count_entities(self, entities: List[Entity]) -> Dict[str, int]:
        """Count entities by type."""
        counts: Dict[str, int] = {}
        for entity in sorted(entities, key=lambda e: (e.type, e.value)):
            counts[entity.type] = counts.get(entity.type, 0) + 1
        return counts

    def _get_top_entities(self, entity_counts: Dict[str, int]) -> List[Dict[str, Any]]:
        """Get top entities by frequency."""
        type_totals: Dict[str, Dict[str, int]] = {}
        for entity_type, count in entity_counts.items():
            if entity_type not in type_totals:
                type_totals[entity_type] = {"total": 0}
            type_totals[entity_type]["total"] = count

        result = []
        for entity_type in sorted(entity_counts.keys()):
            result.append({
                "type": entity_type,
                "count": entity_counts[entity_type]
            })

        return sorted(result, key=lambda x: (-x["count"], x["type"]))[:self.top_entities_count]

    def _compute_stats(
        self,
        entities: List[Entity],
        chunks: List[Chunk],
        text: str
    ) -> Dict[str, Any]:
        """Compute statistical insights."""
        stats: Dict[str, Any] = {}

        stats["total_entities"] = len(entities)
        stats["total_chunks"] = len(chunks)
        stats["total_characters"] = len(text) if text else 0
        stats["entity_types"] = len(set(e.type for e in entities))

        if chunks:
            total_chunk_chars = sum(len(c.text) for c in chunks)
            stats["avg_chunk_size"] = round(total_chunk_chars / len(chunks), 2)
        else:
            stats["avg_chunk_size"] = 0

        if text:
            stats["text_length"] = len(text)
            stats["word_count"] = len(text.split())
        else:
            stats["text_length"] = 0
            stats["word_count"] = 0

        for entity_type in sorted(set(e.type for e in entities)):
            type_entities = [e for e in entities if e.type == entity_type]
            stats[f"{entity_type}_count"] = len(type_entities)

        return stats
