from __future__ import annotations

from typing import Any, Dict

from core.internet.citation_verification_engine import verify_citations


def build_citation_network(text: str) -> Dict[str, Any]:
    v = verify_citations(text)
    urls = v.get("url_count", 0)
    nodes = [f"url_{i}" for i in range(min(urls, 50))]
    edges = [{"from": nodes[i], "to": nodes[i + 1]} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges, "verification": v}
