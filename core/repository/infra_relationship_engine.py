from __future__ import annotations

from typing import Any, Dict, List

from core.repository.infra_semantic_engine import detect_infra_signals


def model_infra_relationships(files: List[str]) -> Dict[str, Any]:
    signals = detect_infra_signals(files)
    edges = []
    names = [s["file"] for s in signals.get("signals", [])]
    for i in range(len(names) - 1):
        edges.append({"from": names[i], "to": names[i + 1], "relation": "co_deployed", "evidence": ["infra:signal"]})
    return {"signals": signals.get("signals", []), "edges": edges, "evidence": signals.get("evidence", [])}
