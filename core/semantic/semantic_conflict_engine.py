from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_conflicts(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    keys: Dict[str, set] = {}
    for claim in claims or []:
        if not isinstance(claim, dict):
            continue
        k = str(claim.get("key", ""))
        v = str(claim.get("value", ""))
        keys.setdefault(k, set()).add(v)
    conflicts = [{"key": k, "values": sorted(v)} for k, v in sorted(keys.items()) if len(v) > 1]
    return {
        "conflicts": conflicts,
        "evidence": ["semantic_conflict_scan"],
        "sources": sorted({str(c.get("source", "")) for c in claims or [] if isinstance(c, dict)}),
        "grounding": {"method": "value_multiplicity"},
        "lineage": {"stage": "semantic_conflict"},
    }
