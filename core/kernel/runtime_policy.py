from __future__ import annotations

from typing import Any, Dict


def build_kernel_policy(
    max_phases: int = 20,
    max_graph_nodes: int = 1_000_000,
    require_kaalka_persistence: bool = True,
    allow_simulation: bool = True,
) -> Dict[str, Any]:
    return {
        "max_phases": max_phases,
        "max_graph_nodes": max_graph_nodes,
        "require_kaalka_persistence": require_kaalka_persistence,
        "allow_simulation": allow_simulation,
        "deterministic": True,
        "bounded": True,
    }


def enforce_kernel_policy(
    policy: Dict[str, Any],
    phase_count: int,
    node_count: int,
) -> Dict[str, Any]:
    within_phases = phase_count <= int(policy.get("max_phases", 20))
    within_graph = node_count <= int(policy.get("max_graph_nodes", 1_000_000))
    return {
        "allowed": within_phases and within_graph,
        "within_bounds": within_phases and within_graph,
        "bounded": True,
    }
