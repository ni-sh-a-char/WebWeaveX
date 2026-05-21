from __future__ import annotations

from typing import Any, Dict, List


def model_ontology_entropy(entities: List[str], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    n_ent = len(set(entities or []))
    n_edge = len(edges or [])
    entropy = round(min(1.0, n_ent * 0.05 + n_edge * 0.03), 3)
    return {"entropy": entropy, "entities": n_ent, "edges": n_edge, "deterministic_inputs": [f"H={entropy}"]}
