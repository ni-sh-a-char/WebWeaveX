from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_tasks(specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "id": s.get("id"),
            "kind": s.get("kind", "semantic"),
            "priority": int(s.get("priority", 0)),
            "evidence": sorted(set(s.get("evidence", []) or [])),
        }
        for s in sorted(specs, key=lambda x: str(x.get("id", "")))
    ]
