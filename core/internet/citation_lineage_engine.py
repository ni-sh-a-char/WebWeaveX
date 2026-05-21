from __future__ import annotations

import re
from typing import Any, Dict, List

from core.evidence.lineage_engine import build_lineage


_CITATION_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|https?://[^\s\)>]+")


def reconstruct_citation_lineage(text: str) -> Dict[str, Any]:
    citations: List[Dict[str, str]] = []
    for m in _CITATION_RE.finditer(text or ""):
        if m.lastindex == 2:
            citations.append({"label": m.group(1), "target": m.group(2)})
        else:
            citations.append({"label": "", "target": m.group(0)})
    citations = sorted(citations, key=lambda c: c["target"])[:100]
    lineage = build_lineage(
        [{"stage": "citation_scan", "inputs": [], "outputs": [c["target"] for c in citations]}]
    )
    return {
        "citations": citations,
        "citation_count": len(citations),
        "evidence": ["citation_lineage"],
        "lineage": lineage,
    }
