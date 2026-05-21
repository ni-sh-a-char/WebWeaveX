from __future__ import annotations

from typing import Any, Dict


def detect_recursive_consensus(reconciled_eq_inferred: bool, depth: int, evidence_count: int) -> Dict[str, Any]:
    inflated = reconciled_eq_inferred and depth >= 2 and evidence_count < 2
    return {"consensus_inflated": inflated, "suppress": inflated, "plurality_pressure": {"level": 0.8 if inflated else 0.0}}
