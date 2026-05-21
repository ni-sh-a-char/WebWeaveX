from __future__ import annotations

from typing import Any, Dict, List


def require_ontology_evidence(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    if isinstance(ev, str):
        ev = [ev]
    grounded = bool(ev) and "type" not in edge
    return {
        **edge,
        "grounded": grounded,
        "evidence": sorted(set(str(e) for e in ev)),
        "grounding": edge.get("grounding", {"method": "evidence_backed" if grounded else "unsupported"}),
        "uncertainty": {"insufficient": not grounded},
    }
