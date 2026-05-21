from __future__ import annotations

from typing import Any, Dict, List


def preserve_recursive_provenance(sources: List[str], lineage: Dict[str, Any]) -> Dict[str, Any]:
    return {"sources": list(sources), "lineage_depth": lineage.get("depth", 0), "complete": bool(sources)}
