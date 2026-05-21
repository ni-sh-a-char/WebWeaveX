from __future__ import annotations

from bs4 import BeautifulSoup


def extract_html(text: str) -> dict:
    soup = BeautifulSoup(text or "", "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    body = soup.get_text(separator=" ", strip=True)
    links = sorted({a.get("href", "") for a in soup.find_all("a") if a.get("href")})
    code_blocks = [c.get_text("\n", strip=True) for c in soup.find_all(["pre", "code"]) if c.get_text(strip=True)]
    return {
        "content": {"text": body, "links": links},
        "code": {"blocks": sorted(code_blocks)},
        "metadata": {"title": (soup.title.string.strip() if soup.title and soup.title.string else "")},
    }

