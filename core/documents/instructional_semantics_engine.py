from __future__ import annotations

from typing import Any, Dict

from core.documents.instructional_flow_engine import extract_instructional_flow
from core.documents.semantic_role_engine import assign_semantic_roles


def analyze_instructional_semantics(text: str) -> Dict[str, Any]:
    flow = extract_instructional_flow(text)
    roles = assign_semantic_roles(text)
    ordering = [{"step": i + 1, "title": s.get("title", "")} for i, s in enumerate(flow.get("steps", []))]
    return {
        "ordering": ordering,
        "prerequisites": flow.get("prerequisites", []),
        "notices": [r for r in roles.get("roles", []) if r.get("role") == "notice"],
        "evidence": ["discourse:instructional_flow"],
        "deterministic_inputs": [f"steps={len(ordering)}"],
    }
