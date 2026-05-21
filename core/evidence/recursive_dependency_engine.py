from __future__ import annotations

from typing import Any, Dict


def _record(reason: str) -> Dict[str, Any]:
    return {
        "reason": reason,
        "dependency_pressure": {"level": 0.85},
        "obedience_pressure": {"level": 0.8},
        "submission_pressure": {"level": 0.75},
        "domestication_pressure": {"level": 0.7},
        "agency_pressure": {"preserve": True},
        "sovereignty_pressure": {"preserve": True},
    }


def detect_recursive_dependency(depth: int, interpretation_count: int, evidence_count: int) -> Dict[str, Any]:
    dependent = depth >= 2 and interpretation_count <= 1 and evidence_count < 2
    return {"dependent": dependent, "suppressed": [_record("recursive_dependency")] if dependent else []}
