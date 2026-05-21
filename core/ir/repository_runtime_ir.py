from __future__ import annotations

from typing import Any, Dict, Optional


def compile_repository_runtime_ir(
    ingestion: Dict[str, Any],
    languages: Dict[str, Any],
    graph: Dict[str, Any],
    services: Dict[str, Any],
    infra: Dict[str, Any],
    topology: Dict[str, Any],
    dependencies: Optional[Dict[str, Any]] = None,
    apis: Optional[Dict[str, Any]] = None,
    execution_flows: Optional[Dict[str, Any]] = None,
    build_systems: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    deps = dependencies or {}
    api_index = apis or {}
    flows = execution_flows or {}
    builds = build_systems or {}

    return {
        "ir": "repository_runtime",
        "ingestion": ingestion,
        "languages": languages,
        "graph": graph,
        "services": services.get("services", []),
        "dependencies": deps.get("imports", []),
        "dependency_edges": deps.get("edges", []),
        "apis": api_index.get("routes", []),
        "api_index": api_index.get("per_file", []),
        "execution_flows": flows.get("flows", []),
        "infra": infra.get("infra", []),
        "deployments": [
            item for item in infra.get("infra", [])
            if item.get("type") in {"kubernetes", "docker-compose", "docker"}
        ],
        "runtime_topology": topology,
        "build_systems": builds.get("build_systems", []),
        "bounded": True,
    }
