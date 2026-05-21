from __future__ import annotations

from typing import Any, Dict

from core.evidence.incompleteness_engine import preserve_incompleteness


def preserve_semantic_incompleteness(bundle: Dict[str, Any]) -> Dict[str, Any]:
    inc = preserve_incompleteness(bundle)
    bundle["incompleteness"] = inc
    return bundle
