from __future__ import annotations

from typing import Any, Dict, List


MAX_BRANCHES = 32


def branch_semantic_state(state: Dict[str, Any], branch_id: str) -> Dict[str, Any]:
    return {"branch_id": branch_id, "state": state, "deterministic": True}


def list_branches(branches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(branches, key=lambda b: str(b.get("branch_id", "")))[:MAX_BRANCHES]
