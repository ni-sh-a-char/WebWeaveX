from __future__ import annotations

from typing import Any, Dict


def detect_recursive_stabilization(reconciled_eq_inferred: bool, depth: int) -> Dict[str, Any]:
    stabilized = reconciled_eq_inferred and depth >= 2
    return {"stabilized": stabilized, "suppress": stabilized, "basin_blocked": stabilized}
