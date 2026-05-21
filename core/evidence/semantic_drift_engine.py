from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_drift(
    observed: Dict[str, Any],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
    evidence: List[str],
) -> Dict[str, Any]:
    drift_keys = []
    if inferred and not observed:
        drift_keys.append("inferred_without_observation")
    if reconciled != observed and len(evidence) < 2:
        drift_keys.append("reconcile_drift")
    for k in inferred:
        if k not in observed and k not in reconciled:
            drift_keys.append(f"drift:{k}")
    pressure = round(min(1.0, len(drift_keys) * 0.2), 3)
    return {
        "drift_detected": bool(drift_keys),
        "drift_keys": sorted(set(drift_keys)),
        "drift_pressure": pressure,
        "suppress_continuation": pressure >= 0.2,
    }
