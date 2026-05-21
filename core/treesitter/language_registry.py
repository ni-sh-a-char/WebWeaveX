from __future__ import annotations

from typing import Optional


EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".tf": "terraform",
    ".yaml": "yaml",
    ".yml": "yaml",
}


def detect_language(
    path: str,
) -> Optional[str]:

    for ext, lang in EXTENSION_MAP.items():

        if path.endswith(ext):
            return lang

    return None
