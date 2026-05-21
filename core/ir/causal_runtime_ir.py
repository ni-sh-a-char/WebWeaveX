from __future__ import annotations

from typing import Any, Dict


def compile_causal_runtime_ir(
    cognition: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "causal_runtime",
        "causal_graphs": cognition.get("causal_graph", {}),
        "timelines": cognition.get("timeline", {}),
        "event_chains": cognition.get("event_chain", {}),
        "propagation_maps": cognition.get("propagation", {}),
        "distributed_synchronization": cognition.get("distributed", {}),
        "runtime_dependencies": cognition.get("dependencies", {}),
        "alignment": cognition.get("alignment", {}),
        "bridges": {
            "browser_native": cognition.get("browser_bridge", {}),
            "electron_terminal": cognition.get("electron_bridge", {}),
        },
        "recovery_state": cognition.get("recovery", {}),
        "bounded": True,
    }


def causal_runtime_ir_to_graph(
    causal_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = causal_ir.get("causal_graphs", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "causality:root", "type": "causality"}]

    timeline = causal_ir.get("timelines", {})
    for entry in timeline.get("timeline", [])[:5000]:
        nodes.append({
            "id": str(entry.get("event_id", "")),
            "type": "timeline_event",
            "runtime": str(entry.get("runtime", "")),
        })

    return {
        "ir": "causal_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
