from __future__ import annotations

from typing import Any, Dict


def suppress_semantic_governance(governance_detected: bool, depth: int) -> Dict[str, Any]:
    return {"governance": governance_detected and depth >= 2, "suppress": True, "centralized_governance_blocked": True}
