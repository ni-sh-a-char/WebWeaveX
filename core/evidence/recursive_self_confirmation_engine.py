from __future__ import annotations

from typing import Any, Dict


def detect_recursive_self_confirmation(depth: int, reconciled_eq_inferred: bool, evidence_count: int) -> Dict[str, Any]:
    confirm = depth >= 2 and reconciled_eq_inferred and evidence_count < 2
    return {"detected": confirm, "suppress": confirm, "recursive_pressure": round(depth * 0.1, 3) if confirm else 0.0}
