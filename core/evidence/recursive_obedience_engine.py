from __future__ import annotations

from typing import Any, Dict


def detect_recursive_obedience(high_confidence: bool, low_evidence: bool, depth: int) -> Dict[str, Any]:
    obedience = high_confidence and low_evidence and depth >= 2
    return {"obedience": obedience, "suppress": obedience}
