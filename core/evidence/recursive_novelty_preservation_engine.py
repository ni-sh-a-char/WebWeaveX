from __future__ import annotations

from typing import Any, Dict


def preserve_recursive_novelty(novelty: Dict[str, Any], depth: int) -> Dict[str, Any]:
    decay_risk = depth >= 5 and novelty.get("novelty", 0) < 0.15
    return {"preserved": True, "decay_risk": decay_risk, "decay_suppressed": decay_risk}
