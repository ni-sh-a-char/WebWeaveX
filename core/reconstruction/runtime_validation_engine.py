from __future__ import annotations

from typing import Any, Dict, Optional


def validate_reconstructed_runtime(
    runtime: Optional[Dict[str, Any]] = None,
    replay: Optional[Dict[str, Any]] = None,
    topology: Optional[Dict[str, Any]] = None,
    execution: Optional[Dict[str, Any]] = None,
    mutations: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    runtime = runtime or {}
    replay = replay or {}
    topology = topology or {}
    execution = execution or {}

    replay_ok = bool(replay.get("replay_chains") or replay.get("replay_package") or replay.get("replayed"))
    if topology:
        sync_ok = bool(topology.get("synchronization_topology") or topology.get("reconstructed"))
        topology_ok = bool(topology.get("runtime_graph") or topology.get("reconstructed"))
    else:
        sync_ok = True
        topology_ok = True
    execution_ok = bool(
        execution.get("executed")
        or execution.get("actions")
        or runtime.get("reconstructed")
        or runtime.get("fabricated")
    )
    mutation_list = mutations.get("mutations", []) if isinstance(mutations, dict) else (mutations or [])
    mutation_ok = all("kind" in m or "target" in m for m in mutation_list) if mutation_list else True

    checks = [replay_ok or runtime.get("replay_safe"), sync_ok or topology_ok, topology_ok, execution_ok, mutation_ok]
    valid = all(checks) if runtime.get("reconstructed") or runtime.get("fabricated") else bool(runtime and replay_ok)

    return {
        "valid": valid,
        "integrity_score": 1.0 if valid else 0.0,
        "replay_integrity": replay_ok,
        "synchronization_integrity": sync_ok,
        "topology_integrity": topology_ok,
        "execution_integrity": execution_ok,
        "mutation_consistency": mutation_ok,
        "bounded": True,
    }
