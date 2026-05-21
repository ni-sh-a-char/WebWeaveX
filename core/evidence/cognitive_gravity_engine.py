from __future__ import annotations

from typing import Any, Dict


def detect_cognitive_gravity_well(high_confidence: bool, low_diversity: bool, depth: int) -> Dict[str, Any]:
    gravity = high_confidence and low_diversity and depth >= 2
    return {"gravity_well": gravity, "suppress": gravity, "sink_state_blocked": gravity}
