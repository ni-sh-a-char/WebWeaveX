from __future__ import annotations

from typing import Dict, Any


def detect_package_managers(text: str) -> Dict[str, Any]:
    src = text or ""
    managers = []
    mapping = {
        "requirements.txt": "pip", "pyproject.toml": "poetry_or_pep621", "package.json": "npm",
        "pubspec.yaml": "pub", "pom.xml": "maven", "build.gradle": "gradle", "Cargo.toml": "cargo"
    }
    for k, v in mapping.items():
        if k in src:
            managers.append(v)
    return {"package_managers": sorted(set(managers))}
