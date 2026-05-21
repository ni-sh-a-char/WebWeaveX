from __future__ import annotations

from typing import Any, Dict, List


def preserve_explanatory_freedom(alternatives: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"free": len(alternatives) > 0, "monopolization_blocked": True, "alternatives": len(alternatives)}
