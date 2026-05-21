from __future__ import annotations

from typing import Any, Dict, List

from core.internet.source_corroboration_engine import corroborate_sources


def build_corroboration_graph(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    corr = corroborate_sources(sources)
    nodes = sorted({str(s.get("url", s.get("id", ""))) for s in sources or [] if s})
    edges = [{"from": nodes[i], "to": nodes[i + 1], "relation": "corroborates"} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges, "corroboration": corr, "evidence": ["internet:corroboration"]}
