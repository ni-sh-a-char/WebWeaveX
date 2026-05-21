from __future__ import annotations

from typing import Any, Dict, List


def model_ontology_competition(entities: List[str], depth: int) -> Dict[str, Any]:
    return {
        "competitive": len(entities) > 1 or depth < 3,
        "monopoly_suppressed": True,
        "dominance_allowed": False,
        "alternatives_required": len(entities) > 0,
    }
