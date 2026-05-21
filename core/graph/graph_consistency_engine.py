from __future__ import annotations

from typing import Any, Dict

from core.graph.graph_invariant_engine import check_graph_invariants


def assess_graph_consistency(graph: Dict[str, Any]) -> Dict[str, Any]:
    inv = check_graph_invariants(graph)
    return {"consistent": inv["valid"], "invariants": inv, "deterministic_inputs": inv["deterministic_inputs"]}
