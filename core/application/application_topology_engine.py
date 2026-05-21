from __future__ import annotations

from typing import Any, Dict, List


def build_application_topology(
    workflow: Dict[str, Any],
    navigation: Dict[str, Any],
    dashboard: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = list(workflow.get("nodes", []))

    for menu in navigation.get("menus", [])[:1000]:
        nodes.append({
            "id": str(menu.get("href", "")),
            "type": "nav_link",
        })

    return {
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "dashboard_widgets": len(dashboard.get("widgets", [])),
        "bounded": True,
    }
