from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_timeline(
    events: Optional[List[Dict[str, Any]]] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    mutations: Optional[List[Dict[str, Any]]] = None,
    synchronization: Optional[List[Dict[str, Any]]] = None,
    execution: Optional[List[Dict[str, Any]]] = None,
    recovery: Optional[List[Dict[str, Any]]] = None,
    replay: Optional[List[Dict[str, Any]]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    timeline: List[Dict[str, Any]] = []

    for kind, items in (
        ("event", events or []),
        ("action", actions or []),
        ("mutation", mutations or []),
        ("sync", synchronization or []),
        ("execution", execution or []),
        ("recovery", recovery or []),
        ("replay", replay or []),
    ):
        for index, item in enumerate(items):
            timeline.append({
                "kind": kind,
                "tick": int(item.get("tick", tick + index)),
                "id": str(item.get("id", f"{kind}:{index}")),
                "payload": dict(item),
            })

    ordered = sorted(timeline, key=lambda item: (item["tick"], item["kind"], item["id"]))

    return {
        "timeline": ordered,
        "count": len(ordered),
        "replay_deterministic": True,
        "bounded": True,
    }
