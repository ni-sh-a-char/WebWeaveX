from __future__ import annotations

from typing import Any, Dict

from core.parsers import parse_source

from .reconstruction import (
    build_dependency_lineage,
    build_deployment_graph,
    build_event_graph,
    build_runtime_graph,
    classify_architecture,
    infer_ownership_domains,
    reconstruct_monorepo,
    reconstruct_topology,
)


def reconstruct_repository(text: str, source_url: str = "", paths: list | None = None) -> Dict[str, Any]:
    parsed = parse_source(text, path=source_url or "repository")
    path_list = paths if isinstance(paths, list) else []
    topology = reconstruct_topology(path_list)
    events = build_event_graph(text)
    runtime = build_runtime_graph(
        parsed.get("runtime", {}).get("runtimes", []),
        topology.get("services", []),
    )
    deployment = build_deployment_graph(text)
    return {
        "parser": parsed,
        "topology": topology,
        "events": events,
        "runtime_graph": runtime,
        "deployment": deployment,
        "architecture": classify_architecture(topology, events, deployment),
        "monorepo": reconstruct_monorepo(path_list),
        "ownership": infer_ownership_domains(path_list),
        "dependency_lineage": build_dependency_lineage(
            parsed.get("dependencies", {}).get("dependencies", [])
        ),
    }
