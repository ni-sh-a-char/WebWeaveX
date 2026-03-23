"""WebWeaveX Insights - Analytics engine."""

from typing import List, Dict, Any, Optional

from .config import DEFAULT_CONFIG, get_config
from .schema import Entity, Insights


class InsightsEngine:
    """Compute insights from extracted data."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.insights_config = cfg.get("insights", DEFAULT_CONFIG["insights"])
        self.top_n = self.insights_config.get("top_entities_count", 10)
        self.include_stats = self.insights_config.get("include_stats", True)

    def compute(self, entities: List[Entity], chunks: List[Any] = None, text: str = "") -> Insights:
        """Compute insights from entities."""
        entity_counts: Dict[str, int] = {}
        for e in entities:
            key = f"{e.type}:{e.value}"
            entity_counts[key] = entity_counts.get(key, 0) + 1

        sorted_counts = sorted(entity_counts.items(), key=lambda x: (-x[1], x[0]))

        top_entities = [
            {"type": k.split(":")[0], "value": k.split(":", 1)[1], "count": c}
            for k, c in sorted_counts[:self.top_n]
        ]

        stats: Dict[str, Any] = {}
        if self.include_stats:
            stats = {
                "total_entities": len(entities),
                "unique_entities": len(entity_counts),
                "entity_types": len(set(e.type for e in entities)),
                "total_relations": len(set()),
            }
            if chunks:
                stats["total_chunks"] = len(chunks)
            if text:
                stats["text_length"] = len(text)
                stats["word_count"] = len(text.split())

        return Insights(
            top_entities=top_entities,
            stats=stats,
            entity_counts=entity_counts
        )
