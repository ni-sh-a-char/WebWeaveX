from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_index(
    entities: List[Dict[str, Any]],
    workflows: List[Dict[str, Any]],
    graphs: List[Dict[str, Any]],
    streams: List[Dict[str, Any]],
    connectors: List[Dict[str, Any]],
) -> Dict[str, Any]:
    entity_index = {
        str(item.get("id", item.get("label", ""))): item
        for item in entities
        if item.get("id") or item.get("label")
    }
    workflow_index = {
        str(item.get("id", item.get("objective", ""))): item
        for item in workflows
    }
    graph_index = {
        str(index): graph for index, graph in enumerate(graphs)
    }

    return {
        "entity_index": dict(sorted(entity_index.items())),
        "workflow_index": dict(sorted(workflow_index.items())),
        "graph_index": graph_index,
        "stream_index": {
            str(index): stream for index, stream in enumerate(streams)
        },
        "connector_index": {
            str(index): connector for index, connector in enumerate(connectors)
        },
        "bounded": True,
    }
