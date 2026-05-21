from __future__ import annotations

from typing import Any, Dict, List


def calibrate_confidence(predicted: float, observed_accuracy: float) -> Dict[str, Any]:
    error = round(abs(predicted - observed_accuracy), 3)
    reliable = error < 0.25
    return {
        "predicted": round(predicted, 3),
        "observed_accuracy": round(observed_accuracy, 3),
        "calibration_error": error,
        "reliable": reliable,
        "deterministic_inputs": [f"error={error}"],
    }
