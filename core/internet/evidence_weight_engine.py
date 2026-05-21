from __future__ import annotations

from typing import Dict, List

from .authority_engine import score_authority
from .trust_engine import compute_trust


def weight_evidence(sources: List[Dict[str, object]]) -> List[Dict[str, object]]:
    weighted = []
    for src in sources or []:
        if not isinstance(src, dict):
            continue
        url = str(src.get("url", ""))
        authority = score_authority(url)["authority_score"]
        trust = compute_trust(url)["score"]
        weight = round((authority * 0.6) + (trust * 0.4), 3)
        weighted.append({**src, "evidence_weight": weight})
    return sorted(weighted, key=lambda x: (-x["evidence_weight"], str(x.get("url", ""))))
