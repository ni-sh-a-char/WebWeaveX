from __future__ import annotations

from typing import Any, Dict, List


def analyze_trust_error(predictions: List[Dict[str, float]]) -> Dict[str, Any]:
    errors = [abs(p.get("predicted", 0) - p.get("actual", 0)) for p in predictions or []]
    mae = round(sum(errors) / max(1, len(errors)), 3)
    return {
        "mean_absolute_error": mae,
        "samples": len(errors),
        "calibration_error": mae,
        "deterministic_inputs": [f"mae={mae}"],
    }
