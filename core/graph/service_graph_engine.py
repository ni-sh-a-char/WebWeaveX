from __future__ import annotations

from typing import Dict, List


def build_service_graph(services: List[object]) -> Dict[str, object]:
    names = sorted({str(s.get("name") if isinstance(s, dict) else s) for s in (services or []) if s})
    nodes = [{"id": n, "kind": "service", "metadata": {}} for n in names]
    edges = [{"from": names[i], "to": names[i + 1]} for i in range(len(names) - 1)]
    return {"nodes": nodes, "edges": edges, "max_edges": len(edges)}
