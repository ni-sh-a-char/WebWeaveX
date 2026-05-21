from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_timeline(
    events: List[Dict[str, Any]],
    propagation: Dict[str, Any],
) -> Dict[str, Any]:
    ordered = sorted(events, key=lambda item: int(item.get("step", 0)))
    timeline: List[Dict[str, Any]] = []

    for index, event in enumerate(ordered[:10000]):
        timeline.append({
            "step": index,
            "event_id": str(event.get("id", f"evt:{index}")),
            "runtime": str(event.get("runtime", "")),
            "type": str(event.get("type", "mutation")),
            "propagation_map": [
                handoff.get("workflow_id", "")
                for handoff in propagation.get("handoffs", [])
                if handoff.get("step") == index
            ],
        })

    return {
        "timeline": timeline,
        "evolution_history": [
            entry["event_id"] for entry in timeline
        ],
        "propagation_maps": list(propagation.get("handoffs", [])),
        "bounded": True,
    }
