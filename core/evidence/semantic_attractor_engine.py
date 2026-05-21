from __future__ import annotations

from typing import Any, Dict, List


def _record(reason: str) -> Dict[str, Any]:
    return {
        "reason": reason,
        "attractor_pressure": {"level": 0.85},
        "gravity_pressure": {"level": 0.8},
        "stabilization_pressure": {"level": 0.75},
        "fixation_pressure": {"level": 0.7},
        "phase_space_pressure": {"preserve": True},
        "exploration_pressure": {"maintain": True},
    }


def detect_semantic_attractor(depth: int, interpretation_count: int, evidence_count: int) -> Dict[str, Any]:
    attractor = depth >= 2 and interpretation_count <= 1 and evidence_count < 2
    return {"attractor": attractor, "suppressed": [_record("semantic_attractor")] if attractor else []}
