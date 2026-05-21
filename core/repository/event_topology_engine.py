from __future__ import annotations

from typing import Any, Dict

from core.parsers import parse_source
from core.repository.topology_cognition_engine import build_topology_cognition

_EVENT_KEYS = ("kafka", "rabbitmq", "sns", "sqs", "nats", "celery", "rq", "bullmq")


def infer_event_topology(text: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(text or "", path=path)
    imports = [str(i).lower() for i in parsed.get("symbols", {}).get("imports", [])]
    deps = [str(d).lower() for d in parsed.get("dependencies", {}).get("dependencies", [])]
    frameworks = [str(f).lower() for f in parsed.get("frameworks", {}).get("frameworks", [])]
    evidence = imports + deps + frameworks
    buses = sorted({k for k in ("kafka", "rabbitmq", "sns", "sqs", "nats") if any(k in e for e in evidence)})
    queues = sorted({k for k in ("celery", "rq", "bullmq") if any(k in e for e in evidence)})
    if not buses and not queues:
        src = (text or "").lower()
        buses = [k for k in ("kafka", "rabbitmq", "sns", "sqs", "nats") if k in src]
        queues = [k for k in ("celery", "rq", "bullmq") if k in src]
    nodes = sorted(set(buses + queues))
    parser_backed = bool(imports or deps or frameworks)
    evidence_kind = "parser_imports" if parser_backed else "text_fallback"
    cognition = build_topology_cognition(text, path=path, observed_nodes=nodes, inferred_nodes=nodes)
    cognition["evidence_trace"] = cognition.get("evidence", [])
    cognition["evidence"] = evidence_kind
    cognition["event_buses"] = buses
    cognition["queue_systems"] = queues
    return cognition
