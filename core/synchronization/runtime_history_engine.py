from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_history(
    deltas: List[Dict[str, Any]],
    transitions: Optional[List[Dict[str, Any]]] = None,
    workflows: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    transitions = transitions or []
    workflows = workflows or []

    return {
        "deltas": sorted(deltas, key=lambda item: int(item.get("timestamp", 0))),
        "transitions": transitions,
        "mutations": [
            change
            for delta in deltas
            for change in delta.get("changes", [])
        ],
        "workflows": workflows,
        "semantic_evolution": [
            change for change in (
                change
                for delta in deltas
                for change in delta.get("changes", [])
            )
            if change.get("kind") == "semantic_change"
        ],
        "length": len(deltas),
        "bounded": True,
    }
