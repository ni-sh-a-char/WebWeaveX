from __future__ import annotations

from typing import Any, Dict, List


def model_worldview_diversity(interpretations: List[Dict[str, Any]], contradicted: Dict[str, Any]) -> Dict[str, Any]:
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    return {
        "diverse": len(interpretations) > 1 or bool(pairs),
        "convergence_suppressed": True,
        "worldview_lock_in": False,
        "alternative_worldviews": len(interpretations),
    }
