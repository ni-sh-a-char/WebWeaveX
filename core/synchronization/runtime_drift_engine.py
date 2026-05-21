from __future__ import annotations

from typing import Any, Dict, Optional


def detect_runtime_drift(
    baseline: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    drifts: List[Dict[str, Any]] = []

    checks = (
        ("selector_drift", "selectors"),
        ("semantic_drift", "semantic"),
        ("workflow_drift", "workflow"),
        ("topology_drift", "topology"),
        ("application_drift", "application"),
        ("runtime_divergence", "runtime"),
    )

    for drift_type, field in checks:
        if baseline.get(field) != current.get(field):
            drifts.append({
                "type": drift_type,
                "field": field,
                "detected": True,
            })

    return {
        "drifts": drifts,
        "drift_count": len(drifts),
        "diverged": len(drifts) > 0,
        "bounded": True,
    }
