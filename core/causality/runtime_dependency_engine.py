from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_dependencies(
    events: List[Dict[str, Any]],
    propagation: Dict[str, Any],
) -> Dict[str, Any]:
    dependencies: List[Dict[str, Any]] = []
    consumers: List[Dict[str, Any]] = []
    sync_chains: List[Dict[str, Any]] = []

    runtimes_seen = []
    for event in sorted(events, key=lambda item: int(item.get("step", 0))):
        runtime = str(event.get("runtime", ""))
        if runtime and runtime not in runtimes_seen:
            if runtimes_seen:
                dependencies.append({
                    "from": runtimes_seen[-1],
                    "to": runtime,
                    "relation": "depends_on",
                })
            runtimes_seen.append(runtime)
            consumers.append({
                "runtime": runtime,
                "event_id": str(event.get("id", "")),
            })

    for handoff in propagation.get("handoffs", [])[:5000]:
        sync_chains.append({
            "from": handoff.get("from", ""),
            "to": handoff.get("to", ""),
            "workflow_id": handoff.get("workflow_id", ""),
        })

    return {
        "dependencies": dependencies,
        "consumers": consumers,
        "synchronization_chains": sync_chains,
        "causal_relationships": dependencies,
        "bounded": True,
    }
