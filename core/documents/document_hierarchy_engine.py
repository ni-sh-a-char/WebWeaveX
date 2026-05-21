from __future__ import annotations

from typing import Any, Dict, List


def build_document_hierarchy(
    structure: Dict[str, Any],
) -> Dict[str, Any]:
    hierarchy = []

    sections = structure.get(
        "sections",
        [],
    )

    for idx, section in enumerate(sections):
        hierarchy.append({
            "id": f"section_{idx}",
            "title": section.get("title"),
            "children": [],
        })

    return {
        "hierarchy": hierarchy,
        "bounded": True,
    }
