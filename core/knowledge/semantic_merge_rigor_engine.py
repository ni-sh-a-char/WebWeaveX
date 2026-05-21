from __future__ import annotations

from typing import Any, Dict, List


def merge_with_evidence(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """No silent merge: require evidence on every source."""
    merged_evidence: List[str] = []
    for s in sources or []:
        ev = s.get("evidence", []) or []
        if isinstance(ev, str):
            ev = [ev]
        if not ev:
            return {"merged": False, "reason": "silent_merge_forbidden", "sources": len(sources or [])}
        merged_evidence.extend(str(e) for e in ev)
    return {
        "merged": True,
        "evidence": sorted(set(merged_evidence)),
        "source_count": len(sources or []),
        "deterministic_inputs": [f"sources={len(sources or [])}"],
    }
