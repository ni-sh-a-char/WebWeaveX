from __future__ import annotations

from typing import Any, Dict


def detect_explanatory_fixation(alternative_count: int, depth: int) -> Dict[str, Any]:
    fixation = alternative_count <= 1 and depth >= 2
    return {"fixation": fixation, "suppress": fixation}
