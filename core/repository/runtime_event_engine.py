from __future__ import annotations

from typing import Any, Dict, List


EVENT_KEYWORDS = frozenset(
    {
        "kafka",
        "rabbitmq",
        "sns",
        "sqs",
        "nats",
        "celery",
        "rq",
    }
)


def infer_runtime_events(
    dependencies: List[str],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    observed = sorted(
        dep
        for dep in dependencies
        if dep.lower() in EVENT_KEYWORDS
    )

    return {
        "events": observed,
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
