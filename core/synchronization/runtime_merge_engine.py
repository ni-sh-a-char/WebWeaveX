from __future__ import annotations

from typing import Any, Dict, List


def merge_runtime_realities(
    realities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged_semantic: Dict[str, Any] = {}
    merged_workflow: Dict[str, Any] = {}
    merged_application: Dict[str, Any] = {}
    timelines: List[Dict[str, Any]] = []

    for reality in realities[:1000]:
        timelines.append({
            "reality_id": str(reality.get("reality_id", "")),
            "tick": int(reality.get("tick", 0)),
        })
        merged_semantic.update(reality.get("semantic", {}))
        merged_workflow.update(reality.get("workflow", {}))
        merged_application.update(reality.get("application", {}))

    return {
        "semantic": merged_semantic,
        "workflow": merged_workflow,
        "application": merged_application,
        "timelines": sorted(timelines, key=lambda item: item["tick"]),
        "reality_count": len(realities),
        "bounded": True,
    }
