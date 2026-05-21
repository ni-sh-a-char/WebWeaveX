from __future__ import annotations

from typing import Any, Dict


def build_runtime_drift_topology(
    current: Dict[str, Any],
    baseline: Dict[str, Any],
) -> Dict[str, Any]:

    drift = sorted(
        set(current.keys())
        ^ set(baseline.keys())
    )

    return {
        "drift_nodes": drift,
        "drift_count": len(
            drift
        ),
    }
