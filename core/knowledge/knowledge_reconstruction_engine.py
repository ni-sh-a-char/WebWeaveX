from __future__ import annotations

from typing import Any, Dict, List

from .reconstruction import (
    build_architecture_knowledge,
    build_concept_graph,
    build_dependency_knowledge,
    build_documentation_knowledge,
    build_repository_knowledge,
    build_semantic_identity,
    resolve_entities,
)


def reconstruct_knowledge(
    symbols: List[str] | None = None,
    dependencies: List[str] | None = None,
    documents: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    sym = sorted(set(symbols or []))
    deps = sorted(set(dependencies or []))
    entities = resolve_entities(sym)
    concept_graph = build_concept_graph(sym)
    return {
        "entities": entities,
        "identity": build_semantic_identity(sym),
        "concept_graph": concept_graph,
        "repository": build_repository_knowledge({"symbols": sym, "dependencies": deps}),
        "documentation": build_documentation_knowledge(documents or {}),
        "architecture": build_architecture_knowledge({}),
        "dependencies": build_dependency_knowledge(deps),
        "evidence_only": True,
    }
