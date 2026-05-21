from __future__ import annotations

from typing import Any, Dict


def detect_recursive_domestication(passive: bool, depth: int) -> Dict[str, Any]:
    domesticated = passive and depth >= 3
    return {"domesticated": domesticated, "suppress": domesticated}
