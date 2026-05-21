from __future__ import annotations

from typing import Dict, List


def build_semantic_import_graph(ast_data: Dict[str, List[str]], source: str = "module") -> Dict[str, List[dict]]:
    imports = sorted(set((ast_data or {}).get("imports", [])))
    nodes = sorted(set([source] + imports))
    edges = [{"from": source, "to": imp} for imp in imports]
    return {"nodes": nodes, "edges": edges}
