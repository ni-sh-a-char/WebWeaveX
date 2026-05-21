from __future__ import annotations

from typing import Any, Dict, List


def model_explanatory_competition(alternatives: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "competitive": len(alternatives) > 1,
        "monopoly_suppressed": True,
        "authoritarianism_blocked": True,
    }
