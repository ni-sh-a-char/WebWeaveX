from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_electron_routes(
    routes: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    route_list = sorted(
        routes or [{"path": "/", "order": 0}],
        key=lambda r: (int(r.get("order", 0)), str(r.get("path", ""))),
    )
    nodes = [{"id": f"route:{r['path']}", "type": "route", "path": r["path"]} for r in route_list]
    edges = []
    for i in range(len(route_list) - 1):
        edges.append(
            {
                "source": f"route:{route_list[i]['path']}",
                "target": f"route:{route_list[i + 1]['path']}",
                "type": "navigate",
            }
        )
    return {
        "routes": route_list,
        "graph": {"nodes": nodes, "edges": edges, "bounded": True},
        "bounded": True,
    }
