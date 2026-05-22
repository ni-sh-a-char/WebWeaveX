"""IR package — lazy exports to avoid import cycles with parsers/repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

_LAZY = {
    "RepositoryIR": (".repository_ir", "RepositoryIR"),
    "compile_repository_ir": (".repository_ir", "compile_repository_ir"),
    "DocumentIR": (".document_ir", "DocumentIR"),
    "compile_document_ir": (".document_ir", "compile_document_ir"),
    "KnowledgeIR": (".knowledge_ir", "KnowledgeIR"),
    "compile_knowledge_ir": (".knowledge_ir", "compile_knowledge_ir"),
    "InternetIR": (".internet_ir", "InternetIR"),
    "compile_internet_ir": (".internet_ir", "compile_internet_ir"),
    "SemanticGraphIR": (".semantic_graph_ir", "SemanticGraphIR"),
    "compile_semantic_graph_ir": (".semantic_graph_ir", "compile_semantic_graph_ir"),
    "ExecutionIR": (".execution_ir", "ExecutionIR"),
    "compile_execution_ir": (".execution_ir", "compile_execution_ir"),
    "TopologyIR": (".topology_ir", "TopologyIR"),
    "compile_topology_ir": (".topology_ir", "compile_topology_ir"),
    "OntologyIR": (".ontology_ir", "OntologyIR"),
    "compile_ontology_ir": (".ontology_ir", "compile_ontology_ir"),
    "ApiIR": (".api_ir", "ApiIR"),
    "compile_api_ir": (".api_ir", "compile_api_ir"),
    "RuntimeIR": (".runtime_ir", "RuntimeIR"),
    "compile_runtime_ir": (".runtime_ir", "compile_runtime_ir"),
    "SemanticQueryIR": (".semantic_query_ir", "SemanticQueryIR"),
    "compile_semantic_query_ir": (".semantic_query_ir", "compile_semantic_query_ir"),
}

__all__ = list(_LAZY.keys())


def __getattr__(name: str) -> Any:
    if name not in _LAZY:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr = _LAZY[name]
    import importlib

    mod = importlib.import_module(module_name, __name__)
    return getattr(mod, attr)


def __dir__() -> list[str]:
    return sorted(__all__)
