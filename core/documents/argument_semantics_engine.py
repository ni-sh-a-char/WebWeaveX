from __future__ import annotations

from typing import Any, Dict

from core.documents.argument_dependency_engine import build_argument_dependencies
from core.documents.semantic_role_engine import assign_semantic_roles


def analyze_argument_semantics(text: str) -> Dict[str, Any]:
    deps = build_argument_dependencies(text)
    roles = assign_semantic_roles(text)
    return {
        "dependencies": deps.get("dependencies", []),
        "nodes": deps.get("nodes", []),
        "roles": roles.get("roles", []),
        "evidence": deps.get("evidence", []),
        "structures": ["argumentative", "rhetorical"],
    }
