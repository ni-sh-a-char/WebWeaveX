from __future__ import annotations

from typing import Any, Dict


def apply_semantic_antigravity(gravity_suppressed: bool) -> Dict[str, Any]:
    return {"active": True, "gravity_well_suppressed": gravity_suppressed, "basin_escape": True}
