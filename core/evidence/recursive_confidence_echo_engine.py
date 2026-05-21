from __future__ import annotations

from typing import Any, Dict, List


def detect_recursive_confidence_echo(score: float, depth: int, prior_scores: List[float]) -> Dict[str, Any]:
    if depth < 2 or not prior_scores:
        return {"echo_detected": False, "suppress": False}
    avg = sum(prior_scores) / len(prior_scores)
    echo = score > avg + 0.1 * depth
    return {"echo_detected": echo, "suppress": echo, "decay_to": round(min(score, avg), 3) if echo else score}
