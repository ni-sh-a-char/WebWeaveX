from __future__ import annotations

from typing import Any, Dict, List

REFERENCE_SECTIONS = {
    "references",
    "bibliography",
}


def extract_references(
    structure: Dict[str, Any],
) -> Dict[str, Any]:
    references = []

    for section in structure.get(
        "sections",
        [],
    ):
        title = (
            section.get("title", "")
            .strip()
            .lower()
        )

        if title in REFERENCE_SECTIONS:
            references.extend(
                section.get("content", [])
            )

    return {
        "references": references,
        "bounded": True,
    }
