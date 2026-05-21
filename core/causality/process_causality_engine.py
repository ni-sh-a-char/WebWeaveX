from __future__ import annotations

from typing import Any, Dict, List


def track_process_causality(
    processes: List[Dict[str, Any]],
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    chains: List[Dict[str, Any]] = []

    for index, process in enumerate(processes[:5000]):
        parent = str(process.get("parent", ""))
        chains.append({
            "process": str(process.get("name", process.get("pid", f"proc:{index}"))),
            "parent": parent,
            "launched_at_step": index,
            "mutation_event": str(
                events[index].get("id", "") if index < len(events) else ""
            ),
        })

    return {
        "process_chains": chains,
        "subprocess_depth": max((c.get("launched_at_step", 0) for c in chains), default=0),
        "bounded": True,
    }
