from __future__ import annotations

from typing import Any, Dict, List


def replay_semantic_history(checkpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(checkpoints, key=lambda c: str(c.get("fingerprint", "")))
    states = [c.get("state", {}) for c in ordered]
    return {"states": states, "count": len(states), "deterministic": True}
