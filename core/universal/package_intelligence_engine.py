from __future__ import annotations

import re


def extract_package_intelligence(text: str):
    source = text or ""
    managers = []
    if "requirements.txt" in source or re.search(r"^[A-Za-z0-9_.-]+==", source, flags=re.MULTILINE):
        managers.append("pip")
    if "package.json" in source or '"dependencies"' in source:
        managers.append("npm")
    if "pubspec.yaml" in source:
        managers.append("pub")
    if "Cargo.toml" in source:
        managers.append("cargo")
    if "pom.xml" in source:
        managers.append("maven")
    return {"package_managers": sorted(set(managers))}
