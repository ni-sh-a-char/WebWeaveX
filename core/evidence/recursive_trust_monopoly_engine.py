from __future__ import annotations

from typing import Any, Dict


def detect_recursive_trust_monopoly(trust_score: float, depth: int, evidence_count: int) -> Dict[str, Any]:
    monopoly = trust_score > 0.85 and depth >= 2 and evidence_count < 2
    return {"monopoly": monopoly, "suppress": monopoly, "absolutism_blocked": True}
