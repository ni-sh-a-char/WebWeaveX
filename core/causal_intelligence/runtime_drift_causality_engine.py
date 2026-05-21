from __future__ import annotations

from typing import Any, Dict


def analyze_drift_causality(
    current: Dict[str, Any],
    baseline: Dict[str, Any],
) -> Dict[str, Any]:
    drift_keys = sorted(
        set(current.keys()) ^ set(baseline.keys())
    )
    return {
        "drift_causes": drift_keys,
        "drift_count": len(drift_keys),
        "causal_origin": "key_mutation",
    }
