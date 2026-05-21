from __future__ import annotations

from typing import Any, Dict

from core.internet.semantic_provenance_engine import build_semantic_provenance


def build_source_lineage_graph(text: str, url: str = "") -> Dict[str, Any]:
    prov = build_semantic_provenance(text, url)
    citations = prov.get("citations", []) if isinstance(prov.get("citations"), list) else []
    nodes = [url] + [str(c)[:40] for c in citations[:30]]
    edges = [{"from": nodes[i], "to": nodes[i + 1], "relation": "cites"} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges, "lineage": prov.get("lineage", {})}
