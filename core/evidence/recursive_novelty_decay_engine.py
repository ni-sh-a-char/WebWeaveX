from __future__ import annotations

from typing import Any, Dict


def resist_novelty_decay(novelty: float, depth: int) -> Dict[str, Any]:
    decay = depth >= 4 and novelty < 0.2
    return {"decay_risk": decay, "resist": True, "exhaustion_blocked": decay}
