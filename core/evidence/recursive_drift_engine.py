from __future__ import annotations

from typing import Any, Dict


def detect_recursive_drift(depth: int, evidence_count: int, inferred_count: int) -> Dict[str, Any]:
    drift = round(min(1.0, depth * 0.1 + max(0, inferred_count - evidence_count) * 0.15), 3)
    return {
        "drift_detected": drift >= 0.2,
        "drift_pressure": drift,
        "suppress_normalization": drift >= 0.15,
    }
