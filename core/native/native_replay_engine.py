from __future__ import annotations

from typing import Any, Dict


def replay_native_runtime(
    memory: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "windows": memory.get("windows", {}),
        "dialogs": memory.get("accessibility_trees", {}).get("dialogs", []),
        "interactions": memory.get("interactions", []),
        "terminal_flows": memory.get("terminal_streams", {}),
        "electron_routes": memory.get("electron_state", {}).get("routes", []),
        "ui_graph": memory.get("runtime_graphs", {}),
        "replayed": True,
        "bounded": True,
    }
