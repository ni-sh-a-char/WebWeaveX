from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

MAX_FILES = 100000

SUPPORTED_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
}

SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


def ingest_repository(path: str) -> Dict[str, Any]:
    root = Path(path)

    if not root.exists():
        return {
            "root": str(root),
            "files": [],
            "file_count": 0,
            "available": False,
            "reason": "path_not_found",
            "bounded": True,
        }

    files: List[Dict[str, Any]] = []

    count = 0

    for file in root.rglob("*"):
        if count >= MAX_FILES:
            break

        if not file.is_file():
            continue

        if any(part in SKIP_DIR_NAMES for part in file.parts):
            continue

        ext = file.suffix.lower()

        try:
            size = file.stat().st_size
        except OSError:
            size = 0

        files.append({
            "path": str(file),
            "extension": ext,
            "supported_code": ext in SUPPORTED_CODE_EXTENSIONS,
            "size": size,
        })

        count += 1

    return {
        "root": str(root),
        "files": sorted(files, key=lambda x: x["path"]),
        "file_count": len(files),
        "available": True,
        "bounded": True,
    }
