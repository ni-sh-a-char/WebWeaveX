from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_orthodoxy(interpretations: List[Dict[str, Any]], depth: int) -> Dict[str, Any]:
    orthodox = len(interpretations) <= 1 and depth >= 3
    return {"orthodoxy_detected": orthodox, "suppress": orthodox, "orthodoxy_pressure": {"level": 0.85 if orthodox else 0.0}}
