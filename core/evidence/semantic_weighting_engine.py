from __future__ import annotations

from typing import Any, Dict, List


def weight_evidence_items(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    weights = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        ev = item.get("evidence", [])
        count = len(ev) if isinstance(ev, list) else 1
        weights.append({"id": item.get("id", ""), "weight": round(min(1.0, 0.2 + count * 0.15), 3), "evidence": ev})
    return {"weights": sorted(weights, key=lambda x: x["id"]), "evidence": ["semantic_weighting"]}
