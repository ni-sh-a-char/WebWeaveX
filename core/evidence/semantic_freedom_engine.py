from __future__ import annotations

from typing import Any, Dict


def model_semantic_freedom(autonomy: Dict[str, Any], competition: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "free": autonomy.get("autonomous", True) and competition.get("competitive", True),
        "governance_suppressed": True,
        "hierarchy_permanence_blocked": True,
    }
