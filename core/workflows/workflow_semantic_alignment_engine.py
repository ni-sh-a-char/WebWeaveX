from __future__ import annotations

from typing import Any, Dict, Optional


def align_workflow_semantics(
    plan: Dict[str, Any],
    semantic_runtime: Optional[Dict[str, Any]] = None,
    causality: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    semantic_runtime = semantic_runtime or {}
    inner = semantic_runtime.get("semantic", semantic_runtime)

    return {
        "ontology": inner.get("ontology", {}),
        "domain": inner.get("domain", {}),
        "causality_chains": (
            causality.get("causality", causality).get("propagation", {})
            if causality
            else {}
        ),
        "workflow_objective": plan.get("objective", ""),
        "extraction_semantics": inner.get("semantic_graph", {}),
        "aligned": True,
        "bounded": True,
    }
