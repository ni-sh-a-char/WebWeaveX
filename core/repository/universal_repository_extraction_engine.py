from __future__ import annotations

from typing import Any, Dict

from core.repository.repository_ingestion_engine import (
    ingest_repository,
)
from core.repository.repository_language_detection_engine import (
    detect_repository_languages,
)
from core.repository.repository_file_graph_engine import (
    build_repository_file_graph,
)
from core.repository.repository_dependency_engine import (
    extract_repository_dependencies,
)
from core.repository.repository_service_detection_engine import (
    detect_repository_services,
)
from core.repository.repository_api_extraction_engine import (
    extract_repository_api_index,
)
from core.repository.repository_infra_detection_engine import (
    detect_repository_infra,
)
from core.repository.repository_execution_flow_engine import (
    reconstruct_execution_flows,
)
from core.repository.repository_runtime_topology_engine import (
    build_runtime_topology,
)
from core.repository.repository_build_system_engine import (
    detect_build_systems,
)
from core.ir.repository_runtime_ir import (
    compile_repository_runtime_ir,
)


def extract_repository(
    path: str,
) -> Dict[str, Any]:
    ingestion = ingest_repository(path)

    if not ingestion.get("available", True):
        return {
            "repository_ir": {
                "ir": "repository_runtime",
                "available": False,
                "reason": ingestion.get("reason"),
            },
            "bounded": True,
        }

    files = ingestion["files"]

    languages = detect_repository_languages(files)

    dependencies = extract_repository_dependencies(files)

    graph = build_repository_file_graph(
        files,
        edges=dependencies.get("edges", []),
    )

    services = detect_repository_services(files)

    apis = extract_repository_api_index(files)

    infra = detect_repository_infra(files)

    build_systems = detect_build_systems(files)

    execution_flows = reconstruct_execution_flows(
        dependencies
    )

    topology = build_runtime_topology(
        services,
        infra,
    )

    repository_ir = compile_repository_runtime_ir(
        ingestion=ingestion,
        languages=languages,
        graph=graph,
        services=services,
        infra=infra,
        topology=topology,
        dependencies=dependencies,
        apis=apis,
        execution_flows=execution_flows,
        build_systems=build_systems,
    )

    return {
        "ingestion": ingestion,
        "languages": languages,
        "dependencies": dependencies,
        "graph": graph,
        "services": services,
        "apis": apis,
        "infra": infra,
        "build_systems": build_systems,
        "execution_flows": execution_flows,
        "runtime_topology": topology,
        "repository_ir": repository_ir,
        "bounded": True,
    }
