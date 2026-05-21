from __future__ import annotations

from typing import Any, Dict

from core.documents.section_engine import extract_sections
from core.evidence import structure_cognition


def reconstruct_discourse(text: str) -> Dict[str, Any]:
    sections = extract_sections(text or "")
    hierarchy = sections.get("hierarchy", [])
    lexical = {"sections": sections.get("sections", []), "heading_count": len(hierarchy)}
    syntactic = {"hierarchy_depth": max((h.get("level", 1) for h in hierarchy), default=0)}
    discourse = {
        "introduces": [h.get("title", "") for h in hierarchy if h.get("level", 1) <= 2],
        "extends": [
            {"from": hierarchy[i].get("title", ""), "to": hierarchy[i + 1].get("title", "")}
            for i in range(max(0, len(hierarchy) - 1))
            if hierarchy[i].get("title") and hierarchy[i + 1].get("title")
        ],
    }
    observed = {"lexical": lexical, "syntactic": syntactic}
    inferred = {"discourse": discourse}
    reconciled = {"structure": discourse, "sections": hierarchy}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
