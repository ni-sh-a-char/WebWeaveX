from __future__ import annotations

import re
from typing import Any, Dict

MAX_REFERENCES = 5000

CITATION_PATTERN = re.compile(
    r"\[(\d+)\]"
)


def extract_citations(
    text: str,
) -> Dict[str, Any]:
    citations = []

    matches = CITATION_PATTERN.findall(text)

    for match in matches[:MAX_REFERENCES]:
        citations.append({
            "citation": match,
        })

    return {
        "citations": citations,
        "bounded": True,
    }
