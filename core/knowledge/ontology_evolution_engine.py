from __future__ import annotations

from typing import Any, Dict, List

from core.memory.semantic_evolution_engine import evolve_semantic_state


def evolve_ontology(prior_edges: List[Dict[str, Any]], current_edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    prior = {"relations": prior_edges, "version": len(prior_edges)}
    current = {"relations": current_edges, "version": len(current_edges)}
    return evolve_semantic_state(prior, current)
