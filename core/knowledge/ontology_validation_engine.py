from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_consistency_engine import check_ontology_consistency


def validate_ontology_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    if isinstance(ev, str):
        ev = [ev]
    valid = bool(edge.get("from")) and bool(edge.get("to")) and bool(ev) and "type" not in edge
    return {
        **edge,
        "valid": valid,
        "grounding": edge.get("grounding", {"method": "evidence_required" if ev else "invalid"}),
        "validation": check_ontology_consistency([edge]),
    }
