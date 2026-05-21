from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional


def build_runtime_delta(
    previous: Optional[Dict[str, Any]] = None,
    current: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    previous = previous or {}
    current = current or {}
    changes: List[Dict[str, Any]] = []

    for key in sorted(set(previous.keys()) | set(current.keys())):
        if previous.get(key) != current.get(key):
            changes.append({
                "field": key,
                "from": previous.get(key),
                "to": current.get(key),
                "kind": _classify_change(key),
            })

    payload = json_key(changes)
    delta_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]

    return {
        "delta_id": delta_id,
        "changes": changes,
        "timestamp": tick,
        "bounded": True,
    }


def _classify_change(field: str) -> str:
    if "semantic" in field:
        return "semantic_change"
    if "workflow" in field:
        return "workflow_change"
    if "dom" in field or "ui" in field:
        return "ui_mutation"
    if "state" in field:
        return "application_state_mutation"
    return "runtime_transition"


def json_key(changes: List[Dict[str, Any]]) -> str:
    parts = [
        f"{c['field']}:{c['kind']}"
        for c in sorted(changes, key=lambda item: item["field"])
    ]
    return "|".join(parts)
