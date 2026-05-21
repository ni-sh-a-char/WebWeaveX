from __future__ import annotations

from typing import Any, Dict, List


def plan_semantic_query(intent: str, targets: List[str]) -> Dict[str, Any]:
    steps = []
    if "graph" in intent:
        steps.append("traverse_graph")
    if "document" in intent:
        steps.append("query_documents")
    if "repository" in intent:
        steps.append("query_repository")
    if not steps:
        steps = ["query_semantics"]
    return {
        "intent": intent,
        "steps": steps,
        "targets": sorted(targets),
        "deterministic": True,
    }
