from __future__ import annotations

from typing import Any, Dict

from core.graph.topology_reasoning_engine import reason_topology
from core.graph.semantic_cycle_analysis_engine import detect_cycles
from core.ir._base import empty_lineage

TopologyIR = Dict[str, Any]


def compile_topology_ir(graph: Dict[str, Any]) -> TopologyIR:
    topo = reason_topology(graph)
    cycles = detect_cycles(graph)
    return {
        "topology": topo,
        "cycles": cycles,
        "edges": graph.get("edges", []),
        "lineage": empty_lineage("topology_ir"),
        "confidence": {"score": 0.9 if topo.get("proved") else 0.4, "deterministic": True},
    }
