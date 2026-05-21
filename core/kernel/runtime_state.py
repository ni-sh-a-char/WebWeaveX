from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_kernel_state(
    context: Dict[str, Any],
    irs: Optional[List[Dict[str, Any]]] = None,
    graph: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "context": dict(context),
        "irs": list(irs or []),
        "graph": dict(graph or {}),
        "tick": int(context.get("tick", 0)),
        "bounded": True,
    }


def merge_kernel_state(
    prior: Dict[str, Any],
    update: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(prior)
    merged.update(update)
    merged["irs"] = list(prior.get("irs", [])) + list(update.get("irs", []))
    return merged
