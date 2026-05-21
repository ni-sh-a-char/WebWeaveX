from __future__ import annotations

from typing import Any, Dict


def resist_interpretive_decay(interpretation_count: int, depth: int) -> Dict[str, Any]:
    decay = depth >= 4 and interpretation_count < 2
    return {"decay_detected": decay, "resist": True}
