from __future__ import annotations

from typing import Any, Dict, List


def empty_confidence() -> Dict[str, Any]:
    return {"score": 0.0, "basis": [], "deterministic": True}


def empty_lineage(stage: str = "ir") -> Dict[str, Any]:
    return {"stages": [{"stage": stage}], "depth": 1}


def merge_evidence(*parts: List[str]) -> Dict[str, Any]:
    items = sorted({str(e) for part in parts for e in (part or []) if e})
    return {"items": items, "count": len(items)}
