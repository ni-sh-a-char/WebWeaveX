from __future__ import annotations

from typing import Any, Dict, List


def build_causal_graph(
    events: List[Dict[str, Any]],
    causality: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen_runtimes = set()

    for event in events[:10000]:
        event_id = str(event.get("id", ""))
        nodes.append({
            "id": event_id,
            "type": "event",
            "runtime": str(event.get("runtime", "")),
        })

        runtime = str(event.get("runtime", ""))
        if runtime and runtime not in seen_runtimes:
            seen_runtimes.add(runtime)
            nodes.append({
                "id": f"runtime:{runtime}",
                "type": "runtime",
            })
            edges.append({
                "from": f"runtime:{runtime}",
                "to": event_id,
                "relation": "triggers",
            })

    for edge in causality.get("causal_edges", [])[:10000]:
        edges.append({
            "from": str(edge.get("from", "")),
            "to": str(edge.get("to", "")),
            "relation": "propagates",
        })

    for index, event in enumerate(events[:10000]):
        if event.get("type") == "notification":
            event_id = str(event.get("id", f"evt:{index}"))
            edges.append({
                "from": event_id,
                "to": f"workflow:{index}",
                "relation": "mutates",
            })

    if not nodes:
        nodes.append({"id": "causality:root", "type": "causality"})

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (
                item.get("from", ""),
                item.get("to", ""),
                item.get("relation", ""),
            ),
        ),
        "bounded": True,
    }
