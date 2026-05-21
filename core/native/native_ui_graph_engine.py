from __future__ import annotations

from typing import Any, Dict, List


def build_native_ui_graph(
    windows: Dict[str, Any],
    accessibility: Dict[str, Any],
    interactions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for index, window in enumerate(windows.get("windows", [])[:5000]):
        window_id = str(window.get("id", f"window_{index}"))
        nodes.append({
            "id": window_id,
            "type": "window",
            "title": str(window.get("title", "")),
        })

    for role, bucket in (
        ("button", "buttons"),
        ("form", "text_inputs"),
        ("tab", "tabs"),
        ("menu", "menus"),
        ("dialog", "dialogs"),
    ):
        for index, element in enumerate(accessibility.get(bucket, [])[:5000]):
            element_id = str(element.get("id", f"{role}_{index}"))
            nodes.append({
                "id": element_id,
                "type": role,
                "name": str(element.get("name", "")),
            })

    focused = str(windows.get("focused_window", ""))
    if focused:
        edges.append({
            "from": "native:root",
            "to": focused,
            "relation": "focuses",
        })

    for index, interaction in enumerate(interactions[:10000]):
        action = str(interaction.get("action", "activate"))
        src = str(interaction.get("from", f"step_{index}"))
        dst = str(interaction.get("to", f"step_{index + 1}"))
        relation = "activates"
        if action == "click":
            relation = "opens"
        elif action == "focus":
            relation = "focuses"
        elif action in ("navigate", "transition"):
            relation = "transitions"

        edges.append({
            "from": src,
            "to": dst,
            "relation": relation,
        })

    if not nodes:
        nodes.append({"id": "native:root", "type": "native"})

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (
                item.get("from", ""),
                item.get("to", ""),
                item.get("relation", ""),
            ),
        ),
        "bounded": True,
    }
