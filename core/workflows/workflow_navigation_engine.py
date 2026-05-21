from __future__ import annotations

from typing import Any, Dict, List


RUNTIME_NAVIGATORS = {
    "browser": "browser_navigation",
    "electron": "electron_navigation",
    "desktop": "modal_traversal",
    "terminal": "terminal_progression",
    "native": "vm_runtime_transition",
    "remote": "remote_runtime_traversal",
    "application": "application_navigation",
    "repository": "repository_navigation",
}


def navigate_runtime_workflow(
    plan: Dict[str, Any],
    tick: int = 0,
) -> Dict[str, Any]:
    navigations: List[Dict[str, Any]] = []

    for index, step in enumerate(plan.get("steps", [])[:10000]):
        runtime = str(step.get("runtime", "browser"))
        navigations.append({
            "step_id": str(step.get("id", f"step:{index}")),
            "runtime": runtime,
            "navigator": RUNTIME_NAVIGATORS.get(runtime, "browser_navigation"),
            "action": str(step.get("action", "")),
            "tick": tick + index,
        })

    return {
        "navigations": navigations,
        "count": len(navigations),
        "bounded": True,
    }
