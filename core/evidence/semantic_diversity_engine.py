from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_diversity(observed: Dict[str, Any], inferred: Dict[str, Any], ambiguities: List[str]) -> Dict[str, Any]:
    score = round(min(1.0, (len(observed) + len(inferred) + len(ambiguities)) * 0.1), 3)
    return {"diversity_score": score, "preserved": score > 0 or bool(ambiguities)}
