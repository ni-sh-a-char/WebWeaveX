from __future__ import annotations

from typing import Any, Dict

from core.knowledge.speculative_ontology_engine import suppress_speculative_ontology_edge


def restrain_ontology_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    humbled = suppress_speculative_ontology_edge(edge)
    return {
        **humbled,
        "restraint": {"expansion_allowed": not humbled.get("unsupported", {}).get("edge", True)},
        "lineage": edge.get("lineage", {}),
    }
