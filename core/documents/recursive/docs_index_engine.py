from __future__ import annotations

from core.documents.section_engine import extract_sections


def build_docs_index(text: str):
    sec = extract_sections(text)
    return {"index": sec.get("sections", [])}

