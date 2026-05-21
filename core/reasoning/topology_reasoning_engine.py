from __future__ import annotations

from typing import Any, Dict

from core.graph.topology_reasoning_engine import reason_topology
from core.graph.semantic_cycle_analysis_engine import detect_cycles


def reason_topology_semantic(graph: Dict[str, Any]) -> Dict[str, Any]:
    topo = reason_topology(graph)
    cycles = detect_cycles(graph)
    return {**topo, "cycles": cycles, "contradiction_pressure": cycles.get("contradiction_pressure", 0), "explainable": True}
