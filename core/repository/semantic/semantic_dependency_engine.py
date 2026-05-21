from __future__ import annotations

import json
import re
from typing import Dict, List


def extract_semantic_dependencies(text: str) -> Dict[str, List[str]]:
    source = text or ""
    deps = set()
    deps.update(re.findall(r"^\s*([A-Za-z0-9_.-]+)==[A-Za-z0-9_.-]+\s*$", source, flags=re.MULTILINE))
    deps.update(re.findall(r"\"([@A-Za-z0-9_.-]+)\"\s*:\s*\"[~^]?[0-9*]", source))
    deps.update(re.findall(r"implementation\s+[\"']([A-Za-z0-9_.:-]+)[\"']", source))
    deps.update(re.findall(r"<artifactId>([^<]+)</artifactId>", source))
    deps.update(re.findall(r"^\s*([A-Za-z0-9_-]+)\s*=\s*\"[0-9][^\"]*\"", source, flags=re.MULTILINE))

    managers = []
    if "requirements.txt" in source or "pip" in source:
        managers.append("pip")
    if "package.json" in source or "node_modules" in source:
        managers.append("npm")
    if "build.gradle" in source:
        managers.append("gradle")
    if "pom.xml" in source:
        managers.append("maven")
    if "Cargo.toml" in source:
        managers.append("cargo")
    if "pubspec.yaml" in source:
        managers.append("pub")

    return {"dependencies": sorted(deps), "package_managers": sorted(set(managers))}
