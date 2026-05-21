from __future__ import annotations

from typing import Any, Dict, List


_PHASES = (
    "browser",
    "semantic",
    "workflow",
    "synchronization",
    "evolution",
    "connectors",
    "memory",
    "execution",
    "reconstruction",
)


def register_runtime_phase(
    registry: Dict[str, Any],
    phase: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    phases = dict(registry.get("phases", {}))
    phases[phase] = payload
    return {
        "phases": phases,
        "registered": sorted(phases.keys()),
        "bounded": True,
    }


def list_runtime_phases() -> List[str]:
    return list(_PHASES)
