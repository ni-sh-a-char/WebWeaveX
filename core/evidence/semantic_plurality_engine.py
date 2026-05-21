from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_plurality(
    observed: Dict[str, Any],
    inferred: Dict[str, Any],
    ambiguities: List[str],
    contradicted: Dict[str, Any],
) -> Dict[str, Any]:
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    alt_count = len(set(observed.keys()) | set(inferred.keys())) + len(ambiguities) + len(pairs)
    return {
        "preserved": True,
        "alternative_count": alt_count,
        "unresolved": bool(ambiguities or pairs),
        "monoculture_risk": alt_count < 2 and not pairs,
    }
