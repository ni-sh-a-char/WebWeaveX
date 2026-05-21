from __future__ import annotations

from typing import Any, Dict, Optional


def build_workflow_runtime_context(
    url: str = "",
    runtime: str = "browser",
    sources: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    sources = sources or {}

    return {
        "url": url,
        "primary_runtime": runtime,
        "sources": sorted(sources.keys()),
        "bounded": True,
    }
