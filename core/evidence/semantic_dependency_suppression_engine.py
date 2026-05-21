from __future__ import annotations

from typing import Any, Dict, List


def suppress_semantic_dependency(suppressed: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"suppressed": len(suppressed), "active": bool(suppressed), "loops_blocked": True}
