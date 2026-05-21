from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


DOMAIN_RULES: List[Tuple[str, re.Pattern[str]]] = [
    ("saas", re.compile(r"\b(saas|subscription|tenant|workspace)\b", re.I)),
    ("finance", re.compile(r"\b(invoice|ledger|payment|billing|revenue)\b", re.I)),
    ("analytics", re.compile(r"\b(analytics|dashboard|kpi|metrics|report)\b", re.I)),
    ("infrastructure", re.compile(r"\b(kubernetes|terraform|infra|cluster|deploy)\b", re.I)),
    ("devops", re.compile(r"\b(ci/cd|pipeline|build|release|deploy)\b", re.I)),
    ("crm", re.compile(r"\b(crm|customer|lead|opportunity|contact)\b", re.I)),
    ("ecommerce", re.compile(r"\b(cart|checkout|product|order|sku)\b", re.I)),
    ("support", re.compile(r"\b(ticket|support|helpdesk|incident)\b", re.I)),
    ("security", re.compile(r"\b(security|auth|oauth|permission|role)\b", re.I)),
    ("developer_tooling", re.compile(r"\b(ide|repository|api|sdk|debug)\b", re.I)),
]


def classify_semantic_domain(
    text: str = "",
    signals: Optional[List[str]] = None,
) -> Dict[str, Any]:
    signals = signals or []
    combined = f"{text} {' '.join(signals)}"
    scores: Dict[str, int] = {}

    for domain, pattern in DOMAIN_RULES:
        matches = len(pattern.findall(combined))
        if matches:
            scores[domain] = matches

    if not scores:
        primary = "saas"
    else:
        primary = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[0][0]

    return {
        "domain": primary,
        "scores": scores,
        "signals": signals,
        "bounded": True,
    }
