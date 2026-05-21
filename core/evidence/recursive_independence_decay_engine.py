from __future__ import annotations

from typing import Any, Dict


def resist_independence_decay(independent: bool, depth: int) -> Dict[str, Any]:
    decay = depth >= 5 and not independent
    return {"decay_risk": decay, "resist": True}
