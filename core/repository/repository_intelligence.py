from __future__ import annotations

from typing import Dict, Any
from core.repository.topology_engine import build_topology
from core.repository.dependency_graph_engine import build_dependency_graph
from core.repository.api_surface_engine import extract_api_surface
from core.repository.import_graph_engine import build_import_graph
from core.repository.package_engine import detect_package_managers
from core.repository.architecture_engine import infer_architecture
from core.repository.repo_classifier import classify_repo


def analyze_repository(text: str, source_url: str = "") -> Dict[str, Any]:
    topology = build_topology(text)
    dependency_graph = build_dependency_graph(text)
    api_surface = extract_api_surface(text)
    import_graph = build_import_graph(text)
    packages = detect_package_managers(text)
    architecture = infer_architecture(topology, import_graph)
    classifier = classify_repo(source_url)
    return {
        "topology": topology,
        "dependency_graph": dependency_graph,
        "api_surface": api_surface,
        "import_graph": import_graph,
        "packages": packages,
        "architecture": architecture,
        "classifier": classifier,
    }
