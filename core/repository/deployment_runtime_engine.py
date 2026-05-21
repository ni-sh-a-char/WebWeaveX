from __future__ import annotations

from typing import Any, Dict, List

DEPLOY_KEYWORDS = frozenset({"dockerfile", "docker-compose", "helm", "k8s", "kubernetes"})


def infer_deployment_runtime(
    artifacts: List[str],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    found = sorted(a for a in artifacts if any(k in a.lower() for k in DEPLOY_KEYWORDS))
    return {
        "artifacts": found,
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
