from __future__ import annotations

from typing import Any, Dict


def compile_adaptive_runtime_ir(
    adaptation: Dict[str, Any],
    memory: Dict[str, Any],
    schema: Dict[str, Any],
    reconciliation: Dict[str, Any],
    snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "adaptive_runtime",
        "healed_selectors": memory.get("healed_selectors", {}),
        "fallback_chains": adaptation.get("fallback", {}),
        "adaptation_history": {
            "modal_recovery": adaptation.get("modal_recovery", {}),
            "pagination_recovery": adaptation.get("pagination_recovery", {}),
            "interaction_recovery": adaptation.get("interaction_recovery", {}),
        },
        "schema_stabilization": schema,
        "runtime_reconciliation": reconciliation,
        "snapshot": snapshot,
        "bounded": True,
    }


def adaptive_runtime_ir_to_graph(
    adaptive_ir: Dict[str, Any],
) -> Dict[str, Any]:
    chain = adaptive_ir.get("fallback_chains", {}).get("chain", [])
    nodes = []
    edges = []

    for step in chain:
        node_id = f"adaptive:{step.get('step', 0)}"
        nodes.append({
            "id": node_id,
            "type": "adaptive_fallback",
            "name": step.get("strategy", ""),
        })

    for index in range(len(chain) - 1):
        edges.append({
            "from": f"adaptive:{index}",
            "to": f"adaptive:{index + 1}",
            "relation": "fallback_next",
        })

    return {
        "ir": "adaptive_runtime_graph",
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
