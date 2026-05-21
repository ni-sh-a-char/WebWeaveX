from __future__ import annotations

from typing import Any, Dict, List


def version_semantic_state(state: Dict[str, Any], version: int) -> Dict[str, Any]:
    return {"version": version, "state": state, "deterministic": True}


def list_versions(versions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(versions, key=lambda v: int(v.get("version", 0)))
