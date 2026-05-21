from __future__ import annotations

from typing import Dict, List


def build_runtime_graph(runtime_hints: Dict[str, object]) -> Dict[str, object]:
    runtimes = runtime_hints.get("runtimes", []) if isinstance(runtime_hints, dict) else []
    frameworks = runtime_hints.get("frameworks", []) if isinstance(runtime_hints, dict) else []
    nodes = [{"id": r, "kind": "runtime", "metadata": {}} for r in sorted(set(str(r) for r in runtimes))]
    edges: List[dict] = []
    for fw in sorted(set(str(f) for f in frameworks)):
        nodes.append({"id": fw, "kind": "framework", "metadata": {}})
        if runtimes:
            edges.append({"from": str(runtimes[0]), "to": fw})
    return {"nodes": nodes, "edges": edges, "max_edges": len(edges)}
