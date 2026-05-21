from __future__ import annotations

from typing import Any, Dict, Optional

from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime


def fabricate_runtime_reality(
    runtime: Optional[Dict[str, Any]] = None,
    environment: Optional[Dict[str, Any]] = None,
    browser: Optional[Dict[str, Any]] = None,
    application: Optional[Dict[str, Any]] = None,
    portable: bool = True,
) -> Dict[str, Any]:
    base = runtime or reconstruct_runtime(runtime_type=str(environment.get("runtime", "browser") if environment else "browser"))
    fabricated_runtime = {
        **base,
        "environment": dict(environment or {}),
        "browser": dict(browser or {}),
        "application": dict(application or {}),
    }

    return {
        "fabricated": True,
        "runtime": fabricated_runtime,
        "portable": portable,
        "replay_safe": True,
        "operational_twin": True,
        "bounded": True,
    }
