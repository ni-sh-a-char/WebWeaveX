from __future__ import annotations

from typing import Any, Dict, List

MAX_SECTIONS = 5000

HEADING_PREFIXES = (
    "#",
    "##",
    "###",
)


def build_document_structure(
    text: str,
) -> Dict[str, Any]:
    sections = []

    current = {
        "title": "root",
        "content": [],
    }

    lines = text.splitlines()

    for line in lines[:MAX_SECTIONS]:
        stripped = line.strip()

        if stripped.startswith(HEADING_PREFIXES):
            if current["content"]:
                sections.append(current)

            current = {
                "title": stripped.lstrip("#").strip(),
                "content": [],
            }
        else:
            current["content"].append(stripped)

    if current["content"]:
        sections.append(current)

    return {
        "sections": sections,
        "bounded": True,
    }
