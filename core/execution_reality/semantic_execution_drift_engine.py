from __future__ import annotations

from typing import Any, Dict


def detect_execution_drift(
    current: Dict[str, Any],
    baseline: Dict[str, Any],
) -> Dict[str, Any]:
    drift = sorted(
        set(current.keys()) ^ set(baseline.keys())
    )
    return {
        "drift_keys": drift,
        "drift_detected": bool(drift),
    }
