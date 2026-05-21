from __future__ import annotations

from typing import Any, Dict


def version_semantic_state(state: Dict[str, Any]) -> Dict[str, Any]:
    v = int(state.get("version", 0)) + 1
    return {**state, "version": v, "version_id": f"v{v}"}
