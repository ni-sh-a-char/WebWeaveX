from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_causality(
    events: List[Dict[str, Any]],
    origins: Dict[str, Any],
) -> Dict[str, Any]:
    ordered = sorted(events, key=lambda item: int(item.get("step", 0)))
    causal_edges: List[Dict[str, Any]] = []

    for index in range(1, len(ordered)):
        prev_id = str(ordered[index - 1].get("id", f"evt:{index - 1}"))
        curr_id = str(ordered[index].get("id", f"evt:{index}"))
        causal_edges.append({
            "from": prev_id,
            "to": curr_id,
            "relation": "propagates",
        })

    propagation_order = [str(event.get("id", "")) for event in ordered]

    return {
        "events": ordered,
        "causal_edges": causal_edges,
        "runtime_origins": dict(origins),
        "propagation_order": propagation_order,
        "bounded": True,
    }
