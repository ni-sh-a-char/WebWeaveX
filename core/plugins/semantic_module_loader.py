from __future__ import annotations

from typing import Any, Dict


def load_semantic_module(
    manifest: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "module": manifest.get("name"),
        "loaded": True,
    }
