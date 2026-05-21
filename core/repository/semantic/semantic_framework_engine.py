from __future__ import annotations

from typing import List


_FRAMEWORK_SIGNATURES = {
    "django": {"django"},
    "flask": {"flask"},
    "fastapi": {"fastapi"},
    "react": {"react"},
    "next.js": {"next"},
    "nestjs": {"nestjs"},
    "spring": {"spring-boot", "springframework"},
    "flutter": {"flutter"},
    "express": {"express"},
    "kubernetes": {"kubernetes", "k8s"},
    "docker": {"docker"},
    "terraform": {"terraform"},
}


def detect_semantic_frameworks(imports: List[str], dependencies: List[str], configs: List[str] | None = None) -> List[str]:
    haystack = {x.lower() for x in (imports or []) + (dependencies or []) + (configs or [])}
    found = []
    for framework, signatures in sorted(_FRAMEWORK_SIGNATURES.items()):
        if any(sig in item for sig in signatures for item in haystack):
            found.append(framework)
    return sorted(found)
