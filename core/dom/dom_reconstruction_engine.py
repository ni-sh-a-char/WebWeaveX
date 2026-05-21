from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_DOM_NODES = 100000


def reconstruct_dom(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    nodes: List[Dict[str, Any]] = []

    count = 0

    for tag in soup.find_all():
        if count >= MAX_DOM_NODES:
            break

        nodes.append({
            "tag": tag.name,
            "text": tag.get_text(strip=True)[:500],
        })

        count += 1

    return {
        "nodes": nodes,
        "node_count": len(nodes),
        "bounded": True,
    }
