from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.internet.trust_engine import compute_trust


def calibrate_trust(
    url: str,
    corroboration_count: int = 0,
    html_text: str = "",
    claims: Optional[List[Dict[str, object]]] = None,
) -> Dict[str, Any]:
    """Trust derived only from evidence density, corroboration, citations, consistency."""
    base = compute_trust(url, corroboration_count, html_text, claims)
    evidence = base.get("evidence", []) or []
    density = round(min(1.0, len(evidence) * 0.1), 3)
    calibration_error = round(abs(base.get("trust_score", 0) - density), 3)
    return {
        **base,
        "calibrated": True,
        "evidence_density": density,
        "calibration_error": calibration_error,
        "opaque_heuristic": False,
        "deterministic_inputs": sorted(
            set(list(base.get("deterministic_inputs", [])) + [f"density={density}", f"cal_err={calibration_error}"])
        ),
    }
