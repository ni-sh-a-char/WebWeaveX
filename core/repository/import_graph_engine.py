from __future__ import annotations

from typing import Any, Dict
import re


def build_import_graph(text: str) -> Dict[str, Any]:
    src = text or ""
    py = re.findall(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)", src, flags=re.MULTILINE)
    js = re.findall(r"""import\s+.*?from\s+['"]([^'"]+)['"]""", src)
    dart = re.findall(r"""import\s+['"]([^'"]+)['"]""", src)
    java = re.findall(r"^\s*import\s+([A-Za-z0-9_.]+);", src, flags=re.MULTILINE)
    nodes = sorted(set(py + js + dart + java))
    edges = [{"from": nodes[i], "to": nodes[i + 1]} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges}

