from __future__ import annotations

from bs4 import BeautifulSoup


def safe_html_text(text: str) -> str:
    try:
        soup = BeautifulSoup(text or "", "lxml")
        for t in soup(["script", "style"]):
            t.decompose()
        return soup.get_text(" ", strip=True)
    except Exception:
        return ""
