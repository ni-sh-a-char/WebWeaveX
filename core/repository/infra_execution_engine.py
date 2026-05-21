from __future__ import annotations

from typing import Any, Dict, List

INFRA_KEYWORDS = frozenset({"docker", "kubernetes", "terraform", "helm", "compose"})


def infer_infra_execution(
    dependencies: List[str],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    observed = sorted(dep for dep in dependencies if dep.lower() in INFRA_KEYWORDS)
    return {
        "infra": observed,
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
