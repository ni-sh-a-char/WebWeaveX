from __future__ import annotations

from typing import Any, Dict, List


def predict_semantic_execution(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        transitions,
        key=lambda x: (
            str(x.get("from")),
            str(x.get("to")),
        ),
    )

    return {
        "predicted_execution": ordered,
        "prediction_count": len(ordered),
    }
