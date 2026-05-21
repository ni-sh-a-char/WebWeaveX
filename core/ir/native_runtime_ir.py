from __future__ import annotations

from typing import Any, Dict


def compile_native_runtime_ir(
    cognition: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "native_runtime",
        "windows": cognition.get("windows", {}),
        "accessibility_trees": cognition.get("accessibility", {}),
        "runtime_graphs": cognition.get("ui_graph", {}),
        "electron_state": cognition.get("electron", {}),
        "terminal_streams": cognition.get("terminal", {}),
        "vm_state": cognition.get("vm", {}),
        "remote_sessions": cognition.get("remote", {}),
        "desktop_runtime": cognition.get("desktop", {}),
        "navigation": cognition.get("navigation", {}),
        "streams": cognition.get("streams", {}),
        "native_state": cognition.get("native_state", {}),
        "bounded": True,
    }


def native_runtime_ir_to_graph(
    native_ir: Dict[str, Any],
) -> Dict[str, Any]:
    ui_graph = native_ir.get("runtime_graphs", {})
    nodes = list(ui_graph.get("nodes", []))
    edges = list(ui_graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "native:root", "type": "native"}]

    electron = native_ir.get("electron_state", {})
    if electron.get("application"):
        nodes.append({
            "id": f"electron:{electron['application']}",
            "type": "electron",
        })

    terminal = native_ir.get("terminal_streams", {})
    if terminal.get("stream_id"):
        nodes.append({
            "id": str(terminal["stream_id"]),
            "type": "terminal",
        })

    vm = native_ir.get("vm_state", {})
    if vm.get("backend"):
        nodes.append({
            "id": f"vm:{vm['backend']}",
            "type": "vm",
        })

    remote = native_ir.get("remote_sessions", {})
    if remote.get("protocol"):
        nodes.append({
            "id": f"remote:{remote['protocol']}",
            "type": "remote",
        })

    return {
        "ir": "native_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
