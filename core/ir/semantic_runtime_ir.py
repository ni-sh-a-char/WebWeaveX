from __future__ import annotations

from typing import Any, Dict


def compile_semantic_runtime_ir(
    cognition: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "semantic_runtime",
        "ontology": cognition.get("ontology", {}),
        "entities": cognition.get("entities", {}),
        "semantic_graph": cognition.get("semantic_graph", {}),
        "domain": cognition.get("domain", {}),
        "ui_semantics": cognition.get("ui", {}),
        "table_semantics": cognition.get("tables", {}),
        "document_semantics": cognition.get("document", {}),
        "repository_semantics": cognition.get("repository", {}),
        "application_semantics": cognition.get("application", {}),
        "causality_semantics": cognition.get("causality", {}),
        "workflow_semantics": cognition.get("workflow", {}),
        "alignment": cognition.get("alignment", {}),
        "bounded": True,
    }


def semantic_runtime_ir_to_graph(
    semantic_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = semantic_ir.get("semantic_graph", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    ontology = semantic_ir.get("ontology", {})
    if ontology.get("primary_domain"):
        nodes.append({
            "id": f"domain:{ontology['primary_domain']}",
            "type": "domain",
        })

    if not nodes:
        nodes = [{"id": "semantic:root", "type": "semantic"}]

    return {
        "ir": "semantic_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
