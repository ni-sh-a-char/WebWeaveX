from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_LINKS = 10000


def extract_semantic_html(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    title = ""

    if soup.title:
        title = soup.title.text.strip()

    links: List[str] = []

    for link in soup.find_all("a")[:MAX_LINKS]:
        href = link.get("href")

        if href:
            links.append(href[:2000])

    headings = []

    for tag in ["h1", "h2", "h3"]:
        for node in soup.find_all(tag):
            headings.append({
                "tag": tag,
                "text": node.get_text(strip=True)[:5000],
            })

    return {
        "title": title,
        "links": sorted(set(links)),
        "headings": headings,
        "text": soup.get_text("\n")[:5_000_000],
        "bounded": True,
    }
