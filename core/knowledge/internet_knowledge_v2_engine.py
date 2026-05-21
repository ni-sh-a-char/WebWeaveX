from __future__ import annotations

from typing import Any, Dict, List


def build_internet_knowledge_v2(sources: List[Any]) -> Dict[str, Any]:
    urls = sorted(set(str(u).strip() for u in sources or [] if u))
    return {"source_count": len(urls), "sources": urls[:100], "evidence": "canonical_urls"}
