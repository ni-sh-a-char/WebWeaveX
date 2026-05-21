from __future__ import annotations

import re

from typing import Any, Dict


ASSIGNMENT_PATTERNS = {
    "python": r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=",
    "javascript": r"(?:let|const|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
    "typescript": r"(?:let|const|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
}


def build_multilang_ssa(
    source: str,
    language: str,
) -> Dict[str, Any]:

    pattern = ASSIGNMENT_PATTERNS.get(language)

    if pattern is None:

        return {
            "language": language,
            "variables": [],
            "supported": False,
        }

    matches = re.findall(
        pattern,
        source,
    )

    counters: Dict[str, int] = {}

    variables = []

    for name in matches:

        counters[name] = (
            counters.get(name, 0) + 1
        )

        variables.append({
            "name": name,
            "ssa": f"{name}_{counters[name]}",
        })

    return {
        "language": language,
        "variables": variables,
        "supported": True,
    }
