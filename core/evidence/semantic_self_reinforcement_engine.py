from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_self_reinforcement(
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
    evidence: List[str],
) -> Dict[str, Any]:
    echo = reconciled == inferred and len(inferred) > 1 and len(evidence) < 2
    return {"reinforcement_detected": echo, "suppress": echo, "pressure": 0.8 if echo else 0.0}
