from __future__ import annotations

from typing import Any, Dict


MAX_FRICTION = 100000


def compute_runtime_friction(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    conflicts = runtime_ir.get("runtime_conflicts", {})
    conflict_count = len(
        conflicts.get("conflicts", [])
        if isinstance(conflicts, dict)
        else []
    )
    friction = min(conflict_count * 10, MAX_FRICTION)
    return {
        "friction": friction,
        "conflict_count": conflict_count,
        "bounded": True,
    }
