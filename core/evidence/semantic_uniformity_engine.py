from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_uniformity(keys: List[str], depth: int) -> Dict[str, Any]:
    uniform = len(set(keys)) <= 1 and depth >= 2
    return {"uniformity_detected": uniform, "suppress": uniform}
