from __future__ import annotations

from typing import Any, Dict, List


def _record(reason: str) -> Dict[str, Any]:
    return {
        "reason": reason,
        "capture_pressure": {"level": 0.85},
        "authority_pressure": {"level": 0.8},
        "monopoly_pressure": {"level": 0.9},
        "decentralization_pressure": {"preserve": True},
        "autonomy_pressure": {"preserve": True},
        "plurality_pressure": {"preserve": True},
    }


def detect_semantic_monopoly(interpretation_count: int, depth: int, evidence_count: int) -> Dict[str, Any]:
    monopoly = interpretation_count <= 1 and depth >= 2 and evidence_count < 2
    return {"monopoly": monopoly, "suppressed": [_record("semantic_monopoly")] if monopoly else []}
