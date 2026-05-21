from __future__ import annotations

from typing import Any, Dict


def detect_runtime_drift(
    current: Dict[str, Any],
    baseline: Dict[str, Any],
) -> Dict[str, Any]:

    drift = sorted(
        set(current.keys())
        ^ set(baseline.keys())
    )

    return {
        "drift": drift,
        "drift_detected": bool(
            drift
        ),
    }
