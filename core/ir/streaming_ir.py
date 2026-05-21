from __future__ import annotations

from typing import Any, Dict, List


def compile_streaming_ir(
    websocket_connections: Dict[str, Any],
    websocket_events: Dict[str, Any],
    dom_mutations: Dict[str, Any],
    live_updates: Dict[str, Any],
    sse_events: Dict[str, Any],
    timeline: Dict[str, Any],
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "streaming_runtime",
        "websocket_connections": websocket_connections,
        "stream_events": list(timeline.get("events", [])),
        "dom_mutations": dom_mutations,
        "live_update_graph": live_updates,
        "sse_events": sse_events,
        "replay_snapshots": {
            "checkpoint": checkpoint,
        },
        "runtime_timelines": timeline,
        "bounded": True,
    }


def streaming_ir_to_runtime_graph(
    streaming_ir: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for event in streaming_ir.get("stream_events", []):
        node_id = str(event.get("id", ""))
        if not node_id:
            continue
        nodes.append({
            "id": node_id,
            "type": "stream_event",
            "source": event.get("source"),
        })

    for edge in streaming_ir.get("runtime_timelines", {}).get("edges", []):
        edges.append(dict(edge))

    return {
        "ir": "streaming_runtime_graph",
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
