from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_alternatives(observed: Dict[str, Any], inferred: Dict[str, Any]) -> Dict[str, Any]:
    alts = [{"key": k, "source": "observed" if k in observed else "inferred"} for k in sorted(set(observed) | set(inferred))]
    return {"alternatives": alts[:15], "preserved": len(alts) > 1 or not alts}
