from __future__ import annotations

from typing import Dict, List


_FRAMEWORK_HINTS = {
    "python": {"django", "flask", "fastapi", "uvicorn", "celery"},
    "node": {"react", "next", "express", "nestjs", "@angular/core"},
    "jvm": {"spring-boot", "spring", "kotlin"},
    "rust": {"tokio", "actix-web"},
    "go": {"gin", "echo"},
    "dart": {"flutter"},
}


def resolve_runtime(dependencies: List[str], imports: List[str]) -> Dict[str, object]:
    deps = {d.lower() for d in dependencies or []}
    imps = {i.lower() for i in imports or []}
    runtimes: set[str] = set()
    frameworks: set[str] = set()
    api_indicators: set[str] = set()

    for runtime, hints in _FRAMEWORK_HINTS.items():
        if deps & hints or any(any(h in i for h in hints) for i in imps):
            runtimes.add(runtime)
            frameworks.update(sorted(deps & hints))

    if any(i.startswith("python") or i.endswith(".py") for i in imps):
        runtimes.add("python")
    if "fastapi" in deps or "flask" in deps or "django" in deps:
        api_indicators.add("http_api")
    if "graphql" in deps:
        api_indicators.add("graphql")

    return {
        "runtimes": sorted(runtimes),
        "frameworks": sorted(frameworks),
        "api_indicators": sorted(api_indicators),
    }
