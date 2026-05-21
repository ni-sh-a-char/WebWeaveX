from __future__ import annotations

from typing import Dict, List

_FRAMEWORK_DEPS = {
    "django",
    "flask",
    "fastapi",
    "react",
    "next",
    "express",
    "spring-boot",
    "spring",
    "flutter",
    "gin",
    "actix",
    "tokio",
}


def resolve_frameworks(dependencies: List[str], imports: List[str], decorators: List[str] | None = None) -> Dict[str, object]:
    deps = {d.lower() for d in dependencies or []}
    imps = " ".join(imports or []).lower()
    decs = {d.lower() for d in (decorators or [])}
    detected = sorted(
        fw
        for fw in _FRAMEWORK_DEPS
        if fw in deps or fw in imps or fw in decs or any(fw in i for i in imps.split())
    )
    return {"frameworks": detected, "indicators": sorted(deps & _FRAMEWORK_DEPS)}
