from __future__ import annotations

from typing import Any, Dict, List

from core.documents.discourse_dependency_engine import reconstruct_discourse_dependencies


def build_explanation_graph(text: str) -> Dict[str, Any]:
    deps = reconstruct_discourse_dependencies(text)
    flow = deps.get("reconciled", {}).get("discourse_flow", []) or []
    return {
        "explains": [{"from": e.get("from"), "to": e.get("to")} for e in flow if isinstance(e, dict)],
        "edge_count": len(flow),
        "deterministic_inputs": [f"edges={len(flow)}"],
    }
