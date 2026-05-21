from __future__ import annotations

from typing import Any, Dict

from core.documents.section_engine import extract_sections
from core.evidence import structure_cognition


def reconstruct_semantic_sections(text: str) -> Dict[str, Any]:
    sections = extract_sections(text or "")
    hierarchy = sections.get("hierarchy", [])
    lexical = {"sections": sections.get("sections", []), "titles": [h.get("title", "") for h in hierarchy]}
    syntactic = {"levels": [h.get("level", 1) for h in hierarchy], "depth": max((h.get("level", 1) for h in hierarchy), default=0)}
    semantic = {
        "introduces": [h["title"] for h in hierarchy if h.get("level", 1) == 1],
        "explains": [
            {"from": hierarchy[i].get("title", ""), "to": hierarchy[i + 1].get("title", "")}
            for i in range(max(0, len(hierarchy) - 1))
            if hierarchy[i].get("title") and hierarchy[i + 1].get("title")
        ],
    }
    discourse = {"flow": semantic["explains"]}
    conceptual = {"dependencies": semantic["explains"]}
    observed = {"lexical": lexical, "syntactic": syntactic}
    inferred = {"semantic": semantic, "discourse": discourse, "conceptual": conceptual}
    reconciled = {"sections": hierarchy, "structure": semantic}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
