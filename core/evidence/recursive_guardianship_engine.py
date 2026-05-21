from __future__ import annotations

from typing import Any, Dict


def detect_recursive_guardianship(centrality: bool, depth: int) -> Dict[str, Any]:
    guardianship = centrality and depth >= 2
    return {"guardianship": guardianship, "suppress": guardianship, "paternalism_blocked": True}
