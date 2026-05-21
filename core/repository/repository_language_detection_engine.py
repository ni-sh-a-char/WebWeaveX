from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
}


def detect_repository_languages(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    counts = Counter()

    for file in files:
        ext = file.get("extension")

        language = EXTENSION_LANGUAGE_MAP.get(ext)

        if language:
            counts[language] += 1

    return {
        "languages": dict(sorted(counts.items())),
        "primary_language": (
            counts.most_common(1)[0][0]
            if counts
            else None
        ),
        "bounded": True,
    }
