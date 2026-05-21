from __future__ import annotations

from typing import Any, Dict

from .repository_reconstruction_engine import reconstruct_repository


def reason_architecture(text: str, source_url: str = "") -> Dict[str, Any]:
    repo = reconstruct_repository(text, source_url=source_url)
    arch = repo.get("architecture", {})
    return {
        "classification": arch,
        "topology": repo.get("topology", {}),
        "runtime_graph": repo.get("runtime_graph", {}),
        "deployment": repo.get("deployment", {}),
        "evidence": "parser_backed_reconstruction",
    }
