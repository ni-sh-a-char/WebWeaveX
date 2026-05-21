from __future__ import annotations

from typing import Any, Dict

from core.documents.section_engine import extract_sections
from core.evidence import structure_cognition
from core.parsers import parse_source


def build_concept_dependencies(text: str, path: str = "") -> Dict[str, Any]:
    sections = extract_sections(text or "")
    hierarchy = sections.get("hierarchy", [])
    lexical = {"sections": sections.get("sections", []), "hierarchy": hierarchy}
    discourse = {
        "headings": [h.get("title", "") for h in hierarchy],
        "flow_edges": [
            {"from": hierarchy[i].get("title", ""), "to": hierarchy[i + 1].get("title", "")}
            for i in range(max(0, len(hierarchy) - 1))
            if hierarchy[i].get("title") and hierarchy[i + 1].get("title")
        ],
    }
    concepts = [h.get("title", "") for h in hierarchy if h.get("title")]
    parsed = None
    if not concepts and path.endswith((".py", ".js", ".ts", ".go", ".rs", ".java", ".kt", ".dart")):
        parsed = parse_source(text or "", path=path)
        sym = parsed.get("symbols", [])
        if isinstance(sym, list):
            concepts = sym[:20]
        else:
            concepts = list(sym.get("classes", [])[:20]) if isinstance(sym, dict) else []
    concepts = sorted(set(c for c in concepts if c))
    conceptual = {
        "concepts": concepts,
        "edges": [{"from": concepts[i], "to": concepts[i + 1]} for i in range(max(0, len(concepts) - 1))],
    }
    semantic = {"concepts": concepts}
    observed = {"lexical": lexical, "syntactic": {"hierarchy": hierarchy}, "discourse": discourse}
    inferred = {"semantic": semantic, "conceptual": conceptual}
    reconciled = {
        "concepts": concepts,
        "edges": conceptual["edges"],
        "discourse": discourse,
    }
    out = structure_cognition(observed, inferred, reconciled, parsed=parsed)
    out["concepts"] = reconciled.get("concepts", [])
    out["edges"] = reconciled.get("edges", [])
    return out
