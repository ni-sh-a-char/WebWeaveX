from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

BUILD_FILES = {
    "Makefile": "make",
    "package.json": "npm",
    "pyproject.toml": "python",
    "setup.py": "python",
    "Cargo.toml": "cargo",
    "go.mod": "go",
    "build.gradle": "gradle",
    "pom.xml": "maven",
}


def detect_build_systems(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    systems: List[Dict[str, Any]] = []

    for file in files:
        name = Path(file["path"]).name
        system = BUILD_FILES.get(name)
        if system:
            systems.append({
                "file": file["path"],
                "system": system,
            })

    return {
        "build_systems": sorted(
            systems,
            key=lambda x: x["file"],
        ),
        "bounded": True,
    }
