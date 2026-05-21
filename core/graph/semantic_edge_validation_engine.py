from __future__ import annotations

from typing import Any, Dict


def validate_semantic_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    if "type" in edge:
        return {"valid": False, "reason": "forbidden_type_field"}
    if not edge.get("from") or not edge.get("to"):
        return {"valid": False, "reason": "missing_endpoints"}
    ev = edge.get("evidence", []) or []
    if isinstance(ev, str):
        ev = [ev]
    return {
        "valid": bool(ev),
        "evidence_count": len(ev),
        "grounding": edge.get("grounding", {}),
        "uncertainty": edge.get("uncertainty", {}),
        "justification": edge.get("justification", {}),
    }
