from __future__ import annotations

from typing import Any, Dict


def detect_semantic_hierarchy_permanence(depth: int, hierarchy_locked: bool) -> Dict[str, Any]:
    permanent = hierarchy_locked and depth >= 3
    return {"permanent": permanent, "suppress": permanent, "aristocracy_blocked": True}
