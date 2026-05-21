from __future__ import annotations

import re
from typing import Any, Dict, List


def resolve_coreferences(text: str) -> Dict[str, Any]:
    """Deterministic pronoun→nearest heading antecedent (bounded)."""
    headings = re.findall(r"^#{1,6}\s+(.+)$", text or "", re.M)
    pronouns = re.findall(r"\b(it|this|that|they|these|those)\b", text or "", re.I)
    antecedent = headings[-1] if headings else ""
    chains = [{"pronoun": p, "antecedent": antecedent} for p in pronouns[:50]]
    return {"chains": chains, "count": len(chains)}
