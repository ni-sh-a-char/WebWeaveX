from __future__ import annotations

from typing import Any, Dict


def build_document_knowledge_v2(docs: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(docs, dict):
        return {"sections": 0, "evidence": "empty"}
    sections = docs.get("sections", {})
    count = sections.get("count", len(sections.get("sections", []))) if isinstance(sections, dict) else 0
    return {
        "section_count": count,
        "has_tutorial": bool(docs.get("tutorial_flow")),
        "has_chunks": bool(docs.get("chunks")),
        "evidence": "document_payload",
    }
