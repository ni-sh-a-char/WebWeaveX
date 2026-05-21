from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.internet.trust_calibration_engine import calibrate_trust


def compute_probabilistic_trust(
    url: str,
    corroboration_count: int = 0,
    html_text: str = "",
    claims: Optional[List[Dict[str, object]]] = None,
) -> Dict[str, Any]:
    base = calibrate_trust(url, corroboration_count, html_text, claims)
    density = base.get("evidence_density", 0)
    score = base.get("trust_score", 0)
    # Deterministic posterior: blend calibrated score with evidence density
    posterior = round(min(1.0, score * 0.7 + density * 0.3), 3)
    return {
        **base,
        "trust_score": posterior,
        "score": posterior,
        "posterior": posterior,
        "prior": score,
        "calibrated": True,
        "deterministic_inputs": sorted(
            set(list(base.get("deterministic_inputs", [])) + [f"posterior={posterior}"])
        ),
    }
