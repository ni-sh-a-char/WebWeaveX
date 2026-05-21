from __future__ import annotations

from typing import Any, Dict, List


def build_workflow_propagation(
    aligned: Dict[str, Any],
    dependencies: Dict[str, Any],
) -> Dict[str, Any]:
    events = list(aligned.get("aligned_events", []))
    handoffs: List[Dict[str, Any]] = []

    for index in range(1, len(events)):
        prev = events[index - 1]
        curr = events[index]
        if prev.get("runtime") != curr.get("runtime"):
            handoffs.append({
                "from": str(prev.get("runtime", "")),
                "to": str(curr.get("runtime", "")),
                "step": index,
                "workflow_id": f"wf:{index}",
            })

    return {
        "continuations": handoffs,
        "handoffs": handoffs,
        "distributed": list(dependencies.get("synchronization_chains", [])),
        "synchronized_steps": [
            event.get("aligned_step", 0) for event in events
        ],
        "bounded": True,
    }
