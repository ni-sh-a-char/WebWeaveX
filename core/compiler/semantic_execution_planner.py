from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_execution_plan(ir: Dict[str, Any]) -> Dict[str, Any]:
    edges = list(ir.get("optimized_edges", []))

    ordered = sorted(
        edges,
        key=lambda x: (
            str(x.get("source")),
            str(x.get("target")),
        ),
    )

    plan: List[Dict[str, Any]] = []

    for idx, edge in enumerate(ordered):
        plan.append({
            "step": idx,
            "action": "LINK",
            "source": edge.get("source"),
            "target": edge.get("target"),
        })

    return {
        "plan": plan,
        "steps": len(plan),
        "deterministic": True,
    }
