from __future__ import annotations

from typing import Any, Dict


def detect_semantic_fixation(key_uniformity: bool, depth: int) -> Dict[str, Any]:
    fixation = key_uniformity and depth >= 2
    return {"fixation": fixation, "suppress": fixation, "inevitability_blocked": fixation}
