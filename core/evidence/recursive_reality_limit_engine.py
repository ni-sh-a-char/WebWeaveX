from __future__ import annotations

from typing import Any, Dict


def recursive_reality_limits(depth: int, entropy: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "max_depth_without_evidence": 2,
        "closure_allowed": False,
        "stabilization_allowed": not entropy.get("suppress_recursive_stabilization", False),
        "current_depth": depth,
    }
