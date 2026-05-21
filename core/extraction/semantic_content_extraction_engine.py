from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_LINKS = 10000


def extract_semantic_content(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    headings: List[Dict[str, Any]] = []

    for level in ["h1", "h2", "h3"]:
        for node in soup.find_all(level):
            headings.append({
                "level": level,
                "text": node.get_text(strip=True)[:5000],
            })

    paragraphs: List[str] = []

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        if text:
            paragraphs.append(text[:10000])

    links: List[str] = []

    for a in soup.find_all("a")[:MAX_LINKS]:
        href = a.get("href")

        if href:
            links.append(href[:2000])

    return {
        "headings": headings,
        "paragraphs": paragraphs,
        "links": sorted(set(links)),
        "bounded": True,
    }
