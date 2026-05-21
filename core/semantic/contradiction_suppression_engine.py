from __future__ import annotations

from typing import Any, Dict, List


def suppress_under_contradiction(
    expansions: List[str],
    contradiction_pressure: Dict[str, Any],
) -> Dict[str, Any]:
    if not contradiction_pressure.get("suppress_propagation"):
        return {"suppressed": [], "allowed": expansions}
    return {
        "suppressed": sorted(expansions),
        "allowed": [],
        "reason": "contradiction_pressure",
    }
