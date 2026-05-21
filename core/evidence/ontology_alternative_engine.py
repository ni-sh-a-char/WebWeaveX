from __future__ import annotations

from typing import Any, Dict, List


def model_ontology_alternatives(entities: List[str]) -> Dict[str, Any]:
    return {"mappings": [{"entity": e, "alternative": True} for e in entities[:10]], "preserved": True}
