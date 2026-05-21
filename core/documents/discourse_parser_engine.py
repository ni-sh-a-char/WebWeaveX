from __future__ import annotations

from typing import Any, Dict

from core.documents.section_engine import extract_sections


def parse_discourse_structure(text: str) -> Dict[str, Any]:
    sections = extract_sections(text or "")
    hierarchy = sections.get("hierarchy", [])
    return {
        "lexical": {"section_count": len(sections.get("sections", []))},
        "syntactic": {"max_depth": max((h.get("level", 1) for h in hierarchy), default=0)},
        "discourse": {"headings": [h.get("title", "") for h in hierarchy[:50]]},
        "conceptual": {"nodes": len(hierarchy)},
    }
