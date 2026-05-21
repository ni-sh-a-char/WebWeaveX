from __future__ import annotations

import re
from typing import Any, Dict, List


_ROLE_PATTERNS = (
    (re.compile(r"\b(example|for instance)\b", re.I), "example"),
    (re.compile(r"\b(therefore|thus|hence)\b", re.I), "conclusion"),
    (re.compile(r"\b(because|since|due to)\b", re.I), "reason"),
    (re.compile(r"\b(note|warning|caution)\b", re.I), "notice"),
)


def assign_semantic_roles(text: str) -> Dict[str, Any]:
    roles: List[Dict[str, str]] = []
    for i, ln in enumerate((text or "").splitlines()):
        for pat, role in _ROLE_PATTERNS:
            if pat.search(ln):
                roles.append({"line": i, "role": role, "text": ln[:120]})
                break
    return {"roles": roles, "count": len(roles)}
