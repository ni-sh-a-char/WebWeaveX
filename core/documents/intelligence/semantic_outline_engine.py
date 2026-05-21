from __future__ import annotations
from core.documents.section_engine import extract_sections

def extract_semantic_outline(text: str):
    s=extract_sections(text)
    return {"sections": s.get("sections", []), "hierarchy": s.get("hierarchy", [])}
