from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_ontology(
    entities: List[Dict[str, Any]],
    domain: str,
) -> Dict[str, Any]:
    taxonomy = {
        "entity": sorted({str(e.get("type", "")) for e in entities}),
        "runtime": ["browser", "native", "distributed", "application"],
        "workflow": ["transition", "submit", "navigate", "objective"],
        "ui": ["form", "dashboard", "navigation", "authentication"],
        "infrastructure": ["service", "api", "deployment", "monitoring"],
    }

    return {
        "entity_taxonomy": taxonomy["entity"],
        "runtime_ontology": taxonomy["runtime"],
        "workflow_ontology": taxonomy["workflow"],
        "ui_ontology": taxonomy["ui"],
        "infrastructure_ontology": taxonomy["infrastructure"],
        "primary_domain": domain,
        "taxonomy": taxonomy,
        "bounded": True,
    }
