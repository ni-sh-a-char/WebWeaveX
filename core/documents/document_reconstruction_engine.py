from __future__ import annotations

from typing import Any, Dict

from core.parsers import parse_source

from .reconstruction import (
    build_concept_graph,
    build_semantic_flow,
    chunk_semantic,
    extract_api_contracts,
    extract_architecture_sections,
    reconstruct_tutorial,
)


def reconstruct_document(text: str, source_url: str = "") -> Dict[str, Any]:
    parsed = parse_source(text, path=source_url or "document.md")
    return {
        "parser": parsed,
        "semantic_flow": build_semantic_flow(text),
        "tutorial": reconstruct_tutorial(text),
        "concept_graph": build_concept_graph(text),
        "chunks": chunk_semantic(text),
        "api_contracts": extract_api_contracts(text),
        "architecture_docs": extract_architecture_sections(text),
    }
