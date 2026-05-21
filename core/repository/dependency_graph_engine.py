from __future__ import annotations

from typing import Any, Dict
import re


def build_dependency_graph(text: str) -> Dict[str, Any]:
    src = text or ""
    lines = [ln.strip() for ln in src.splitlines() if ln.strip()]
    req_nodes = []
    for ln in lines:
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*(?:==|>=|~=|<=|>|<)", ln)
        if m:
            req_nodes.append(m.group(1))
    pkg_nodes = re.findall(r'"([@A-Za-z0-9_.\-/]+)"\s*:\s*"[~^<>=0-9.*]+"', src)
    nodes = sorted(set(req_nodes + pkg_nodes))
    edges = [{"from": nodes[i], "to": nodes[i + 1]} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges}

