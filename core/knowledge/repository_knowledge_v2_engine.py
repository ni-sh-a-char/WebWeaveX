from __future__ import annotations

from typing import Any, Dict


def build_repository_knowledge_v2(repo: Dict[str, Any]) -> Dict[str, Any]:
    symbols = repo.get("symbols", []) if isinstance(repo, dict) else []
    deps = repo.get("dependencies", []) if isinstance(repo, dict) else []
    frameworks = repo.get("frameworks", []) if isinstance(repo, dict) else []
    return {
        "symbol_count": len(symbols) if isinstance(symbols, list) else 0,
        "dependency_count": len(deps) if isinstance(deps, list) else 0,
        "frameworks": sorted(frameworks) if isinstance(frameworks, list) else [],
        "evidence": "repository_payload",
    }
