from __future__ import annotations

from typing import Dict, Any
from core.documents.heading_engine import extract_headings


def extract_sections(text: str) -> Dict[str, Any]:
    heads = extract_headings(text).get("headings", [])
    sections = [h.get("title", "") for h in heads]
    hierarchy = [{"title": h.get("title", ""), "level": h.get("level", 1)} for h in heads]
    return {"sections": sorted(set(sections)), "hierarchy": hierarchy}
