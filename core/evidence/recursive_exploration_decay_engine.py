from __future__ import annotations

from typing import Any, Dict


def resist_exploration_decay(exploratory: bool, depth: int) -> Dict[str, Any]:
    decay = depth >= 5 and not exploratory
    return {"decay_risk": decay, "resist": True}
