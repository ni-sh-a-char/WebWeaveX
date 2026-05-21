from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_continuity_engine import track_continuity
from core.memory.semantic_change_engine import detect_semantic_changes


def evolve_semantic_state(prior: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    continuity = track_continuity(prior, current)
    changes = detect_semantic_changes(prior, current)
    version = int(prior.get("version", 0)) + 1 if prior else 1
    return {
        "version": version,
        "continuity": continuity,
        "changes": changes,
        "evolved": changes["has_changes"],
        "deterministic_inputs": continuity.get("deterministic_inputs", []),
    }
