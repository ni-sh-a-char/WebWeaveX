from __future__ import annotations

from typing import Any, Dict

from core.evidence.semantic_fragility_engine import model_fragility


def assess_ontology_edge_fragility(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    amb = edge.get("ambiguities", []) or []
    return model_fragility(ev, amb, 0, 0)
