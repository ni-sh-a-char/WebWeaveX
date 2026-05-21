from __future__ import annotations

from typing import Any, Dict, List, Optional


def compile_unified_runtime_ir(
    registry: Optional[Dict[str, Any]] = None,
    graph: Optional[Dict[str, Any]] = None,
    bus: Optional[List[Dict[str, Any]]] = None,
    phase_results: Optional[List[Dict[str, Any]]] = None,
    sources: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    registry = registry or {}
    graph = graph or {}
    bus = bus or []
    phase_results = phase_results or []
    sources = sources or {}

    phases = registry.get("phases", {})

    return {
        "ir": "unified_runtime",
        "browser": _phase_payload(phases, sources, "browser"),
        "interaction": _phase_payload(phases, sources, "interaction"),
        "streaming": _phase_payload(phases, sources, "streaming"),
        "adaptive": _phase_payload(phases, sources, "adaptive"),
        "application": _phase_payload(phases, sources, "application"),
        "native": _phase_payload(phases, sources, "native"),
        "causality": _phase_payload(phases, sources, "causality"),
        "semantic": phases.get("semantic", sources.get("semantic", {})),
        "workflow": phases.get("semantic", sources.get("workflow", {})),
        "synchronization": phases.get("synchronization", sources.get("sync", {})),
        "evolution": _phase_payload(phases, sources, "evolution"),
        "connectors": _phase_payload(phases, sources, "connectors"),
        "memory": phases.get("memory", sources.get("memory", {})),
        "execution": phases.get("execution", sources.get("execution", {})),
        "reconstruction": phases.get("reconstruction", sources.get("reconstruction", {})),
        "runtime_graph": graph,
        "event_bus": sorted(bus, key=lambda item: (item.get("tick", 0), item.get("order", 0))),
        "phase_results": sorted(phase_results, key=lambda item: str(item.get("phase", ""))),
        "bounded": True,
    }


def _phase_payload(
    phases: Dict[str, Any],
    sources: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    if key in phases:
        return dict(phases[key]) if isinstance(phases[key], dict) else {"payload": phases[key]}
    return dict(sources.get(key, {}))


def unified_runtime_ir_to_graph(
    unified_ir: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = [{"id": "unified:root", "type": "unified_runtime"}]
    edges = []

    graph = unified_ir.get("runtime_graph", {})
    for node in graph.get("nodes", [])[:100000]:
        node_id = str(node.get("id", ""))
        if node_id:
            nodes.append(dict(node))
            edges.append({
                "from": "unified:root",
                "to": node_id,
                "relation": "contains",
            })

    for phase in ("semantic", "memory", "execution", "reconstruction", "synchronization"):
        if unified_ir.get(phase):
            pid = f"phase:{phase}"
            nodes.append({"id": pid, "type": phase})
            edges.append({"from": pid, "to": "unified:root", "relation": "grounds"})

    return {
        "ir": "unified_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
