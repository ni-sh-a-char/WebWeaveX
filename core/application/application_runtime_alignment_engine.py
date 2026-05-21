from __future__ import annotations

from typing import Any, Dict


def align_application_runtime(
    browser_runtime: Dict[str, Any],
    application_state: Dict[str, Any],
    workflow: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "aligned": True,
        "route": application_state.get("route", browser_runtime.get("url", "")),
        "workflow_nodes": len(workflow.get("nodes", [])),
        "bounded": True,
    }
