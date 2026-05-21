from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_stability(
    evidence: List[str],
    drift_pressure: float,
    unsupported_continuity: List[Dict[str, Any]],
    parser_grounded: bool,
) -> Dict[str, Any]:
    unstable: List[str] = []
    if drift_pressure >= 0.2:
        unstable.append("semantic:drift")
    if unsupported_continuity:
        unstable.append("semantic:continuity")
    if not parser_grounded:
        unstable.append("semantic:parser_gap")
    if len(evidence) < 2:
        unstable.append("semantic:insufficient_evidence")
    stable = not unstable
    return {
        "stable": stable,
        "level": "high" if stable else ("low" if len(unstable) >= 2 else "medium"),
        "unstable_regions": sorted(set(unstable)),
        "boundary_pressure": round(min(1.0, len(unstable) * 0.25), 3),
        "stability_limits": {"max_confidence": 0.5 if not stable else 0.85},
    }
