from __future__ import annotations

from typing import Any, Dict

from .semantic_ast_engine import extract_semantic_ast
from .semantic_symbol_engine import resolve_semantic_symbols
from .semantic_import_engine import build_semantic_import_graph
from .semantic_call_graph_engine import build_semantic_call_graph
from .semantic_dependency_engine import extract_semantic_dependencies
from .semantic_service_engine import infer_semantic_services
from .semantic_runtime_engine import detect_semantic_runtime
from .semantic_api_engine import reconstruct_semantic_api
from .semantic_build_engine import infer_semantic_build_graph
from .semantic_framework_engine import detect_semantic_frameworks
from .semantic_architecture_engine import reconstruct_semantic_architecture
from .semantic_repository_graph_engine import build_semantic_repository_graph


def extract_semantic_repository(text: str, source_url: str = "") -> Dict[str, Any]:
    src = text or ""
    ast_data = extract_semantic_ast(src)
    symbols = resolve_semantic_symbols(ast_data)
    deps = extract_semantic_dependencies(src)
    api = reconstruct_semantic_api(src)
    services = infer_semantic_services(
        {"modules": []}, ast_data.get("imports", []), api.get("routes", []), deps.get("dependencies", [])
    )
    runtime = detect_semantic_runtime(deps.get("dependencies", []), deps.get("package_managers", []), [source_url])
    frameworks = detect_semantic_frameworks(ast_data.get("imports", []), deps.get("dependencies", []), [source_url])
    architecture = reconstruct_semantic_architecture(
        services, deps.get("dependencies", []), ast_data.get("imports", []), api.get("routes", [])
    )
    import_graph = build_semantic_import_graph(ast_data, source="repository")
    call_graph = build_semantic_call_graph(src)
    build_graph = infer_semantic_build_graph(deps.get("package_managers", []))
    repository_graph = build_semantic_repository_graph(
        {
            "symbols": symbols.get("symbols", []),
            "frameworks": frameworks,
            "dependencies": deps.get("dependencies", []),
            "services": services.get("services", []),
            "routes": api.get("routes", []),
        }
    )
    return {
        "ast": ast_data,
        "symbols": symbols,
        "imports": import_graph,
        "calls": call_graph,
        "dependencies": deps,
        "services": services,
        "runtime": runtime,
        "api": api,
        "build": build_graph,
        "frameworks": frameworks,
        "architecture": architecture,
        "repository_graph": repository_graph,
    }
