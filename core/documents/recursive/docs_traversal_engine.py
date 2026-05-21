from __future__ import annotations

from core.crawling.traversal_engine import discover_links


def traverse_docs(base_url: str, text: str):
    return {"links": discover_links(base_url, text)}

