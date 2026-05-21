from __future__ import annotations

from typing import Any, Dict


def resist_plurality_decay(plurality_count: int, depth: int) -> Dict[str, Any]:
    decay_risk = depth >= 3 and plurality_count < 2
    return {"decay_risk": decay_risk, "resist": True, "boost_plurality": decay_risk}
