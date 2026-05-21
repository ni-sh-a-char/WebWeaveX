from __future__ import annotations

from typing import Any, Dict, List


def measure_semantic_consensus(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    texts = [str(c.get("text", c.get("claim", ""))).strip().lower() for c in claims or []]
    unique = set(t for t in texts if t)
    agreement = 1.0 - (len(unique) / max(1, len(texts))) if texts else 0.0
    return {
        "consensus": round(agreement, 3),
        "claim_count": len(texts),
        "unique_count": len(unique),
        "deterministic_inputs": [f"consensus={round(agreement, 3)}"],
    }
