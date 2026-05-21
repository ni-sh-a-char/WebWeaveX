from __future__ import annotations

from typing import Dict, List


def resolve_imports(symbols: Dict[str, List[str]], source_id: str = "module") -> Dict[str, List[dict]]:
    imports = sorted(set((symbols or {}).get("imports", [])))
    exports = sorted(set((symbols or {}).get("exports", [])))
    nodes = sorted({source_id, *imports, *exports})
    edges = [{"from": source_id, "to": imp} for imp in imports]
    return {"nodes": nodes, "edges": edges, "exports": exports}
