from __future__ import annotations

from typing import Any, Dict, List


def combine_evidence(evidence: List[str], weights: Dict[str, float] | None = None) -> Dict[str, Any]:
    """Deterministic evidence union with additive weight."""
    w = weights or {}
    items = sorted(set(str(e) for e in evidence if e))
    total = round(sum(w.get(e, 1.0) for e in items), 3)
    return {
        "items": items,
        "count": len(items),
        "weight_sum": total,
        "sufficient": len(items) >= 2,
        "deterministic_inputs": [f"count={len(items)}", f"weight_sum={total}"],
    }
