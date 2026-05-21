from __future__ import annotations

from typing import Any, Dict, List

ASYNC_KEYWORDS = frozenset({"asyncio", "aiohttp", "celery", "rq", "dramatiq"})


def infer_async_topology(
    dependencies: List[str],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    async_deps = sorted(dep for dep in dependencies if dep.lower() in ASYNC_KEYWORDS)
    return {
        "async_components": async_deps,
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
