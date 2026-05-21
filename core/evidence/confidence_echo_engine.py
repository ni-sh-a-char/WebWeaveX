from __future__ import annotations

from typing import Any, Dict


def detect_confidence_echo(score: float, prior_scores: list[float]) -> Dict[str, Any]:
    if not prior_scores:
        return {"echo_detected": False, "suppress": False}
    avg_prior = sum(prior_scores) / len(prior_scores)
    echo = score > avg_prior + 0.15 and score > 0.6
    return {"echo_detected": echo, "suppress": echo, "collapse_to": round(min(score, avg_prior), 3) if echo else score}
