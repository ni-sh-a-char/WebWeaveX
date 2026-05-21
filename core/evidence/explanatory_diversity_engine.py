from __future__ import annotations

from typing import Any, Dict, List


def model_explanatory_diversity(inferred: Dict[str, Any], evidence: List[str]) -> Dict[str, Any]:
    alternatives = [{"explanation": k, "grounded": k in str(evidence)} for k in list(inferred.keys())[:8]]
    return {
        "preserved": True,
        "alternatives": alternatives,
        "collapse_suppressed": True,
        "narrative_monopoly": len(alternatives) <= 1 and len(evidence) < 2,
    }
