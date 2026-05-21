from __future__ import annotations

from typing import Any, Dict


def recursive_topology_limits(depth: int) -> Dict[str, Any]:
    return {"normalization_allowed": False, "max_recursive_depth": 3, "depth": depth}
