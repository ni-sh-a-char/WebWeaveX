from __future__ import annotations

from typing import Any, Dict, List


def prove_dependency(edge: Dict[str, Any], evidence_required: bool = True) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    if isinstance(ev, str):
        ev = [ev]
    proved = bool(edge.get("from")) and bool(edge.get("to")) and (bool(ev) if evidence_required else True)
    return {
        "proved": proved,
        "from": edge.get("from"),
        "to": edge.get("to"),
        "evidence": sorted(set(str(e) for e in ev)),
        "justification": edge.get("justification", {"rule": "dependency_requires_evidence"}),
        "uncertainty": edge.get("uncertainty", {}),
        "deterministic_inputs": [f"evidence={len(ev)}", f"proved={proved}"],
    }
