from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_autonomy(interpretations: List[Dict[str, Any]], evidence_count: int) -> Dict[str, Any]:
    return {
        "autonomous": len(interpretations) > 1 or evidence_count >= 2,
        "capture_resistant": True,
        "dominant_cluster": len(interpretations) <= 1 and evidence_count < 2,
    }
