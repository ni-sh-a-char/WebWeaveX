from __future__ import annotations

from typing import Any, Dict, List, Optional


_ENV_TYPES = ("browser", "terminal", "electron", "connector", "vm", "distributed")


def build_runtime_environment(
    runtime: str = "browser",
    connectors: Optional[List[Dict[str, Any]]] = None,
    workers: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    runtime = runtime if runtime in _ENV_TYPES else "browser"
    connectors = connectors or []
    workers = workers or []

    return {
        "runtime": runtime,
        "browser": runtime == "browser",
        "terminal": runtime == "terminal",
        "electron": runtime == "electron",
        "connector": runtime == "connector",
        "vm": runtime == "vm",
        "distributed": runtime == "distributed",
        "connectors": sorted(connectors, key=lambda item: str(item.get("id", ""))),
        "workers": sorted(workers, key=lambda item: str(item.get("worker_id", ""))),
        "execution_ready": True,
        "bounded": True,
    }
