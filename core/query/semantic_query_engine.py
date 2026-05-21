from __future__ import annotations

from typing import Any, Dict

from core.ir.semantic_query_ir import compile_semantic_query_ir


def query_semantics(query_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    from core.query.repository_query_engine import query_repository
    from core.query.document_query_engine import query_documents
    from core.query.graph_query_engine import query_graph
    from core.query.ontology_query_engine import query_knowledge

    dispatch = {
        "repository": lambda: query_repository(payload.get("source", ""), payload.get("path", "")),
        "document": lambda: query_documents(payload.get("text", "")),
        "graph": lambda: query_graph(payload.get("graph", {})),
        "knowledge": lambda: query_knowledge(payload.get("entities", []), payload.get("edges", [])),
    }
    fn = dispatch.get(query_type)
    if not fn:
        return compile_semantic_query_ir(query_type, "", {"error": "unknown_query_type"})
    result = fn()
    return compile_semantic_query_ir(query_type, str(payload)[:80], result)
