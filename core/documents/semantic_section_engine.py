from __future__ import annotations

from core.documents.section_engine import extract_sections


def extract_semantic_sections(text: str):
    sections = extract_sections(text or "")
    return {
        "sections": sections.get("sections", []),
        "hierarchy": sections.get("hierarchy", []),
        "count": len(sections.get("sections", [])),
        "evidence": "section_structure",
    }
