from __future__ import annotations

from typing import Any, Dict


def measure_semantic_momentum(inferred_count: int, evidence_count: int) -> Dict[str, Any]:
    ratio = inferred_count / max(1, evidence_count)
    pressure = round(min(1.0, max(0.0, ratio - 1.0) * 0.3), 3)
    return {
        "momentum": pressure,
        "halt_expansion": pressure >= 0.25,
        "inferred_count": inferred_count,
        "evidence_count": evidence_count,
    }
