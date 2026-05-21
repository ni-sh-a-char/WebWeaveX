from __future__ import annotations

import re
from typing import Dict, List


def extract_citation_chain(text: str) -> Dict[str, object]:
    urls = sorted(set(re.findall(r"https?://[^\s\)\]>\"']+", text or "")))
    refs = sorted(set(re.findall(r"\[[^\]]+\]\((https?://[^\)]+)\)", text or "")))
    chain = sorted(set(urls + refs))
    edges = [{"from": chain[i], "to": chain[i + 1]} for i in range(len(chain) - 1)]
    return {"citations": chain, "edges": edges, "citation_count": len(chain)}
