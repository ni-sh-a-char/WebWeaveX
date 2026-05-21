from __future__ import annotations

import json
import re
from typing import Dict, List, Set


def resolve_dependencies(source: str, path: str = "") -> Dict[str, List[str]]:
    src = source or ""
    deps: Set[str] = set()
    managers: Set[str] = set()

    if "package.json" in path or '"dependencies"' in src:
        managers.add("npm")
        try:
            start = src.find("{")
            if start >= 0:
                blob = json.loads(src[start : src.rfind("}") + 1])
                for section in ("dependencies", "devDependencies", "peerDependencies"):
                    block = blob.get(section, {})
                    if isinstance(block, dict):
                        deps.update(block.keys())
        except (json.JSONDecodeError, ValueError):
            pass

    if path.endswith("Cargo.toml") or "[dependencies]" in src:
        managers.add("cargo")
        deps.update(re.findall(r'^([A-Za-z0-9_-]+)\s*=\s*"', src, flags=re.MULTILINE))

    if path.endswith("go.mod") or "module " in src[:200]:
        managers.add("go")
        deps.update(re.findall(r"^\s*([a-zA-Z0-9./_-]+)\s+v", src, flags=re.MULTILINE))

    deps.update(re.findall(r"^\s*([A-Za-z0-9_.-]+)==[A-Za-z0-9_.-]+\s*$", src, flags=re.MULTILINE))
    deps.update(re.findall(r"^\s*([A-Za-z0-9_.-]+)\s*[><=~!]", src, flags=re.MULTILINE))
    deps.update(re.findall(r"^\s*([A-Za-z0-9_.-]+)\s*$", src, flags=re.MULTILINE))
    deps.update(re.findall(r"implementation\s+[\"']([A-Za-z0-9_.:-]+)[\"']", src))
    deps.update(re.findall(r"<artifactId>([^<]+)</artifactId>", src))

    if "requirements.txt" in path or "pip" in src:
        managers.add("pip")
    if "build.gradle" in path:
        managers.add("gradle")
    if "pom.xml" in path:
        managers.add("maven")
    if "pubspec.yaml" in path:
        managers.add("pub")

    return {"dependencies": sorted(deps), "package_managers": sorted(managers)}
